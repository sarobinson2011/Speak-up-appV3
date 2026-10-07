import io
from v4_ingest.definition import SOURCE_ID, SOURCE_SHA256, definition_hashes
"""Collect exact binding, qualification, semantic and budget failures in ORDER.

Conditional test mode has a concrete finite source/checker implementation.
Actual mode fails closed: no actual independently qualified source provider is
available in this checkpoint. No decision performs E/D/U or publishes anything.
"""
from fractions import Fraction
from v4_ingest.records import (canonical, digest, exact, parse, primitive, require,
                              validate_array, local_joins, SCHEMAS, IDENTITY, TEMPLATES,
                              ingest_security, ValidationError, _source_refs)
from v4_ingest.wire import (FILES, EVIDENCE_HEADER, decode_container, ingest_tables,
                           object_digest, verify_signature)
from .failures import Failures, EXPERIMENT_FAILURE
from .model import Model
from .sources import FiniteLabProvider, MissingMaterial, ROLES, pair

PROFILE_KEYS = ('format', 'profile_id', 'format_source', 'format_source_sha256', 'policy_sources',
                'components', 'public_output', 'declaration_input_sha256', 'procedures_sha256',
                'model', 'evidence_contract', 'appointment', 'security_contract')
STATIC = {'POLICY': lambda s: [s['policy']['record']], 'ALGORITHM': lambda s: s['policy']['algorithms'],
          'ARTIFACT': lambda s: s['policy']['artifacts'], 'OBSERVER': lambda s: s['policy']['observers'],
          'FIELD-LABEL': lambda s: s['policy']['field_labels'], 'EXPERIMENT': lambda s: s['experiments'],
          'ASSUMPTION': lambda s: s['assumptions'], 'QUALIFICATION': lambda s: s['qualification_contracts'],
          'ENVELOPE': lambda s: [s['operating_envelope']], 'LEAKAGE': lambda s: [s['leakage']]}
REQUEST_KEYS = ('format', 'mode', 'outer_hex', 'profile_digest', 'security_records_hex', 'materials',
                'source_objects', 'bundles', 'mapping_digest', 'phase', 'attempt', 'observations_ref',
                'occurrence_bindings')


def appointment(value):
    exact(value, ('authority_id', 'algorithm', 'public_key', 'key_fingerprint_sha256', 'owner_source_id', 'owner_anchor'))
    for k in ('authority_id', 'owner_source_id', 'owner_anchor'): primitive('ID', value[k])
    require(value['algorithm'] == 'ED25519-RFC8032', 'appointed algorithm')
    primitive('BYTES', value['public_key'])
    require(len(value['public_key']) == 64 and digest(bytes.fromhex(value['public_key'])) == value['key_fingerprint_sha256'], 'appointed key fingerprint')
    return value


def external(raw, field_register=None):
    value = parse(raw)
    exact(value, ('format', 'profile_digest', 'phase', 'records'))
    require(value['format'] == 'PE-G4-SECURITY-RECORDS-V4', 'external format')
    primitive('DIGEST', value['profile_digest']); primitive('ENUM-STAGE', value['phase'])
    exact(value['records'], SCHEMAS)
    dirs = {}
    for name in SCHEMAS:
        d = value['records'][name]
        exact(d, ('status', 'justification', 'instances'))
        require(d['status'] in ('PRESENT', 'UNAVAILABLE', 'INAPPLICABLE'), 'external availability')
        if d['justification'] is not None: primitive('SOURCE-REF', d['justification'])
        validate_array(name, d['instances'], field_register=field_register)
        require((d['status'] == 'PRESENT') == bool(d['instances']), 'status/presence join')
        require(d['status'] != 'INAPPLICABLE' or d['justification'] is not None, 'inapplicability needs exact source justification')
        require(name not in ('POLICY', 'ENVELOPE', 'LEAKAGE') or len(d['instances']) <= 1, 'single immutable owner')
        dirs[name] = d['instances'] if d['status'] == 'PRESENT' else None
    return value, dirs


def _collect(request, trusted, f, adapter=None):
    mode = request.get('mode', 'ACTUAL') if isinstance(request, dict) else 'ACTUAL'
    def check(code, condition, detail):
        if not condition: f.add(code, detail)
        return condition
    def attempt(fn, label, code='INVALID-PROFILE-SCHEMA'):
        try:
            return fn()
        except MissingMaterial as e:
            f.add('MISSING-EVIDENCE', label + ': ' + str(e))
        except (ValidationError, ValueError, KeyError, TypeError, IndexError, OverflowError, OSError) as e:
            selected = 'MISSING-EVIDENCE' if isinstance(e,OSError) else getattr(e, 'category', code)
            f.add(selected if selected in ('INVALID-PROFILE-SCHEMA', 'MISSING-EVIDENCE', 'INVALID-EVIDENCE-DIGEST', 'INVALID-EVIDENCE-AUTHORITY', 'INVALID-ACTION-CONTEXT', 'INCOMPLETE-EVIDENCE-UNIVERSE') else code, label + ': ' + str(e))
        return None
    if attempt(lambda: exact(request, REQUEST_KEYS), 'request shape') is not None:
        pass
    if type(request) is not dict: return f.result(mode)
    check('INVALID-PROFILE-SCHEMA', mode in ('ACTUAL', 'CONDITIONAL-LAB'), 'explicit admission mode')
    check('INVALID-PROFILE-SCHEMA', request.get('format') == 'CP3-ADMISSION-REQUEST-V1', 'request carrier format')
    if mode == 'ACTUAL':
        f.add('INVALID-EVIDENCE-AUTHORITY', 'Actual independently qualified source/assessor/evidence provider is unavailable; LAB hypotheses cannot appoint one')
        f.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'Actual source/model/observer/proof/state correspondence remains unestablished')
    def octets(name):
        if adapter is not None: return adapter.octets(name)
        v = request.get(name)
        if v is None:
            f.add('MISSING-EVIDENCE', name); return None
        primitive('BYTES', v)
        return bytes.fromhex(v)
    outer = attempt(lambda: octets('outer_hex'), 'outer bytes')
    if outer is not None:
        check('PROFILE-DIGEST-MISMATCH', digest(outer) == request.get('profile_digest'), 'final outer digest, not PRIVACY subobject')
    members = attempt(lambda: decode_container(outer), 'three-member container') if outer is not None else None
    profile = attempt(lambda: parse(members['PRIVACY']), 'canonical V4 member') if members else None
    if profile is not None:
        attempt(lambda: exact(profile, PROFILE_KEYS), 'exact V4 member fields')
        check('INVALID-PROFILE-SCHEMA', profile.get('format') == 'PE-G4-PRIVACY-PROFILE-V4' and profile.get('public_output') is False and profile.get('format_source') == SOURCE_ID, 'V4 format/public-output/source')
        check('INVALID-PROFILE-SCHEMA', profile.get('format_source_sha256') == SOURCE_SHA256, 'accepted S90 exact identity')
        def component_shapes():
            require(isinstance(profile['components'], list), 'component array')
            for c in profile['components']:
                exact(c, ('id','mode','canonical_type','necessity','privacy'))
                primitive('ID', c['id'])
                require(c['mode'] == 'CANONICAL-VALUE' and c['canonical_type'] == 'PE-TSE-BOOL3' and c['necessity'] == 'PREDICATE-INPUT' and c['privacy'] == 'CONFIDENTIAL', 'accepted two-component type/mode/necessity/privacy')
            require(len({c['id'] for c in profile['components']}) == len(profile['components']), 'unique components')
        attempt(component_shapes, 'component grammar')
    provider = None
    if trusted is None:
        f.add('INVALID-EVIDENCE-AUTHORITY', 'No external conditional contract or actual authority input')
    else:
        def decode_map(name):
            if adapter is not None: return adapter.source_map(name)
            obj = request.get(name)
            require(isinstance(obj, dict), 'digest-indexed exact byte acquisition map')
            for key, value in obj.items(): primitive('DIGEST', key); primitive('BYTES', value)
            return {key: bytes.fromhex(value) for key, value in obj.items()}
        materials = attempt(lambda: decode_map('materials'), 'material acquisition')
        sources = attempt(lambda: decode_map('source_objects'), 'source acquisition')
        if materials is not None and sources is not None:
            provider = attempt(lambda: (adapter.provider(trusted, materials, sources) if adapter is not None else FiniteLabProvider(trusted, materials, sources)), 'external source contract', 'INVALID-EVIDENCE-AUTHORITY')
    trusted_appointment = attempt(lambda: appointment(trusted['appointment']), 'external evidence appointment', 'INVALID-EVIDENCE-AUTHORITY') if trusted else None
    if profile is not None:
        proposed = attempt(lambda: appointment(profile.get('appointment')), 'proposed appointment', 'INVALID-EVIDENCE-AUTHORITY')
        check('INVALID-EVIDENCE-AUTHORITY', proposed is not None and proposed == trusted_appointment, 'exact external evidence appointment binding')
    role_ready = {}
    if provider:
        for role in ROLES:
            role_ready[role] = attempt(lambda r=role: provider.role(r), role, 'INVALID-EVIDENCE-AUTHORITY') is not None
    # Authenticate every available four-file bundle BEFORE dependent record parsing.
    # Detect signature/digest failure even when later security records are malformed.
    parsed_bundles = {}; authentication = {}
    supplied = request.get('bundles', {})
    check('MISSING-EVIDENCE', isinstance(supplied, dict) and set(supplied) == {'ROOT-ELIGIBLE', 'SCOPED-USED', 'NOT-APPLICABLE'}, 'three distinct evidence scopes')
    from scope_auth.auth import authenticate
    for scope in ('ROOT-ELIGIBLE', 'SCOPED-USED', 'NOT-APPLICABLE'):
        item = supplied.get(scope) if isinstance(supplied, dict) else None
        if item is None: f.add('MISSING-EVIDENCE', 'bundle ' + scope); continue
        files, auth = adapter.authenticate(scope, trusted_appointment, f) if adapter is not None else authenticate(item, trusted_appointment, f)
        # Key possession is not appointment. Equality and external role are required.
        auth['complete'] = bool(auth['complete'] and profile is not None and
             profile.get('appointment') == trusted_appointment and role_ready.get('evidence-authority'))
        authentication[scope] = auth
        if files is None: continue
        parsed = attempt(lambda: adapter.tables(scope, files) if adapter is not None else ingest_tables(files, stream_links=True), 'signed tables ' + scope)
        if parsed is not None: parsed_bundles[scope] = (files, parsed)
    security = None
    model = None
    if profile is not None:
        security = attempt(lambda: ingest_security(canonical(profile['security_contract']), field_register={s['node_id'] for s in profile['model']['surfaces']})[0], 'immutable security grammar')
        model = attempt(lambda: Model(profile['model']), 'immutable model adapter')
    if provider and profile is not None and members:
        check('PROFILE-DIGEST-MISMATCH', members['SOURCE-OWNED-BODY'].hex() == trusted['body_hex'] and members['EXPRESSION-PROGRAM'].hex() == trusted['program_hex'], 'independent body/program byte bindings')
        check('INVALID-ACTION-CONTEXT', digest(outer) == trusted['profile_digest'], 'external approved conditional immutable-profile binding')
        check('INVALID-PROFILE-SCHEMA', profile['model'] == trusted['model'], 'external model construction/classifier contract')
        check('INCOMPLETE-EVIDENCE-UNIVERSE', profile.get('declaration_input_sha256') == trusted['declaration_input_sha256'] and profile.get('procedures_sha256') == trusted['procedures_sha256'], 'complete source and procedure identities')
        check('COMPONENT-COUNT-MISMATCH', len(profile.get('components', [])) == len(trusted['components']), 'source-defined component count')
        required_components = {c['id'] for c in trusted['components']}
        supplied_components = {c['id'] for c in profile.get('components', [])}
        check('UNNECESSARY-COMPONENT', supplied_components <= required_components, 'no source-unrequired component')
        check('COMPONENT-FAILURE', profile.get('components') == trusted['components'], 'component type/mode/necessity/source joins')
        check('INVALID-ACTION-CONTEXT', profile.get('evidence_contract') == trusted['evidence_contract'], 'immutable domains/bundles/kinds contract')
    if security and provider:
        check('INVALID-ACTION-CONTEXT', digest(canonical(security)) == trusted['security_digest'], 'independent policy/template immutable binding')
        roots = [r for _, r in _source_refs(security)]
        for label, ref in _source_refs(security): attempt(lambda r=ref: provider.raw(r), label)
        attempt(lambda: provider.construction(roots), 'complete source-parsed static construction DAG')
        for field, expected in definition_hashes().items():
            check('INVALID-PROFILE-SCHEMA', security[field] == expected, 'active amendment exact definition identity ' + field)
        for field, expected in trusted['definition_hashes'].items():
            check('INVALID-PROFILE-SCHEMA', security[field] == expected, 'exact accepted definition/schema/interface ' + field)
        for qualification in security['qualification_contracts']:
            checker = attempt(lambda q=qualification: provider.payload(q['semantic_checker']), 'exact selected semantic checker')
            if checker is not None:
                check('INVALID-EVIDENCE-AUTHORITY', checker == trusted['mechanism'], 'qualification mechanism/code/grammar binding')
            else: f.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'qualification checker exact bytes unavailable')
    raw = attempt(lambda: octets('security_records_hex'), 'external record bytes')
    decoded = attempt(lambda: external(raw, field_register={s['node_id'] for s in model.value['surfaces']} if model else None), 'external directory/record grammar') if raw is not None else None
    if decoded is None:
        f.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'No usable complete external record directory; no inferred bounds or counterexamples')
        return f.result(mode)
    evidence, dirs = decoded
    check('PROFILE-DIGEST-MISMATCH', evidence['profile_digest'] == request.get('profile_digest'), 'external final-profile wrapper binding')
    check('INVALID-ACTION-CONTEXT', evidence['phase'] == request.get('phase'), 'external exact phase')
    indexes = {s: {r[IDENTITY[s]]: r for r in rows or []} for s, rows in dirs.items()}
    for name, rows in dirs.items():
        if rows is None:
            # Inapplicability is interpreted only by an exact qualified source law.
            # This finite selected contract requires every registered directory.
            f.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'Required directory ' + name + ' is ' + evidence['records'][name]['status'])
        for rec in rows or []:
            if 'profile_digest' in rec: check('PROFILE-DIGEST-MISMATCH', rec['profile_digest'] == request.get('profile_digest'), 'record final-profile ' + name)
            if 'model_digest' in rec and model: check('INVALID-ACTION-CONTEXT', rec['model_digest'] == model.digest, 'record canonical model ' + name)
    attempt(lambda: local_joins(dirs, [], phase=request.get('phase')), 'cross-record typed joins', 'INVALID-ACTION-CONTEXT')
    if provider:
        for label, ref in _source_refs(evidence): attempt(lambda r=ref: provider.raw(r), label)
    if security is None or model is None or provider is None:
        f.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'Semantic binding inputs unavailable; later factual errors are not fabricated')
        return f.result(mode)
    for name, get in STATIC.items():
        check('INVALID-ACTION-CONTEXT', dirs[name] == get(security), 'external repeated immutable ' + name)
    policy = security['policy']['record']
    check('INVALID-ACTION-CONTEXT', policy['profile_id'] == profile['profile_id'], 'policy/profile identity')
    check('INCOMPLETE-EVIDENCE-UNIVERSE', policy['target_ids'] == trusted['target_ids'] and policy['coalition_ids'] == trusted['coalition_ids'], 'independently regenerated complete targets/coalitions')
    labels = security['policy']['field_labels']
    check('INCOMPLETE-EVIDENCE-UNIVERSE', {r['surface_id'] for r in labels} == {r['node_id'] for r in model.value['surfaces']}, 'full field-class labels')
    for token in model.tokens:
        check('INVALID-SURFACE-LABELS', token['exposure'] in ('PUBLIC', 'CONFIDENTIAL', 'PRIVATE-ACTOR'), 'UNKNOWN/invalid exposure ' + token['id'])
        owning = next((r for r in labels if r['surface_id'] == token['surface']), None)
        if owning is not None: check('INVALID-SURFACE-LABELS', token['exposure'] == owning['exposure'], 'source-qualified inherited field-class exposure ' + token['id'])
    for label in labels:
        visibility = attempt(lambda r=label: provider.payload(r['visibility_evidence']), 'source-qualified visibility')
        if visibility is None or visibility != {'surface': label['surface_id'], 'coalitions': label['coalition_ids'], 'state': 'ESTABLISHED'}:
            f.add('INVALID-SURFACE-LABELS', 'Unknown/incoherent owning visibility ' + label['surface_id'])
            f.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'Missing full observer view ' + label['surface_id'])
    check('INCOMPLETE-EVIDENCE-UNIVERSE', security['obligations'] == trusted['ledger'], 'complete independently regenerated exact/computational ledger')
    from ledger_kernel.validate import validate as validate_ledger
    ledger = validate_ledger(provider, trusted, security, model, indexes, role_ready, f, mode)
    templates = {o['obligation_id']: o for o in security['obligations']}
    check('INCOMPLETE-EVIDENCE-UNIVERSE', set(indexes['OBLIGATION']) == set(templates), 'external full obligation directory')
    for o in security['obligations']: attempt(lambda o=o: model.obligation(o), 'exact model ledger IDs')
    rules = {c['composition_id']: c for c in security['composition_rules']['records']}
    check('INCOMPLETE-EVIDENCE-UNIVERSE', set(indexes['COMPOSITION']) == set(rules), 'complete external composition directory')
    # Actual value tokens require full independently acquired byte laws.
    values = None
    if request.get('phase') != 'STATIC-ADMISSION':
        def acquire_values():
            if adapter is not None:
                from occurrence_values.acquire import acquire
                return acquire(adapter,provider,trusted,request,model)
            require(False, 'file-backed owning occurrence adapter required; legacy unchecked values are unsupported', category='INCOMPLETE-EVIDENCE-UNIVERSE')
        values = attempt(acquire_values, 'actual canonical typed owning values')
    from scope_auth.scopes import validate as validate_scopes
    scopes = validate_scopes(provider, trusted, request, profile, security, model, ledger, role_ready, parsed_bundles, authentication, values, f, adapter=adapter)
    if model.value['equality_stream'].get('sha256') is None:
        f.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'Unverified full potential stream digest: provisional model cannot be an admitted final member')
    for scope, (files, parsed) in parsed_bundles.items():
        row = parsed['evidence']
        expected_kind = ('ADMISSION-' if request.get('phase') == 'STATIC-ADMISSION' else '') + ('COMPOSITION' if scope == 'NOT-APPLICABLE' else 'COMPONENT')
        check('INVALID-ACTION-CONTEXT', row['evidence_kind'] == expected_kind, 'signed evidence kind binds current phase ' + scope)
        check('PROFILE-DIGEST-MISMATCH', row['profile_sha256'] == request.get('profile_digest'), 'signed final outer binding ' + scope)
        check('INVALID-ACTION-CONTEXT', row['profile_id'] == profile['profile_id'] and row['component_id'] == scope, 'signed owning component/scope ' + scope)
        check('INVALID-EVIDENCE-DIGEST', row['surface_template_sha256'] == model.surface_digest and row['relation_template_sha256'] == model.relation_digest, 'V4 full template array digests ' + scope)
    arguments, assessments, events = indexes['ARGUMENT'], indexes['ASSESSMENT'], indexes['ASSESSOR-EVENT']
    by_arg = {}
    for a in assessments.values(): by_arg.setdefault(a['argument_id'], []).append(a)
    check('INCOMPLETE-EVIDENCE-UNIVERSE', set(by_arg) == set(arguments) and all(len(v) == 1 for v in by_arg.values()), 'one complete owning assessment per argument')
    experiments, artifacts = indexes['EXPERIMENT'], indexes['ARTIFACT']
    bounds, dispositions, result_codes = {}, {}, set()
    for aid, arg in arguments.items():
        exp = experiments.get(arg['experiment_id'])
        if exp is None: continue
        rule = rules.get(arg['composition_id'])
        check('INVALID-ACTION-CONTEXT', rule is not None and rule['experiment_id'] == exp['experiment_id'] and arg['envelope_id'] == policy['envelope_id'], 'argument experiment/envelope/rule')
        required_hypotheses = [h['assumption_id'] for h in security['assumptions'] if exp['experiment_id'] in h['experiment_ids']]
        check('INCOMPLETE-EVIDENCE-UNIVERSE', arg['assumption_ids'] == required_hypotheses, 'all required approved experiment assumptions')
        check('INCOMPLETE-EVIDENCE-UNIVERSE', set(arg['obligation_ids']) <= set(templates) and all(templates[o]['kind'] == 'COMPUTATIONAL' and templates[o]['experiment_id'] == exp['experiment_id'] for o in arg['obligation_ids'] if o in templates), 'argument exact computational obligation scope')
        for hid in arg['assumption_ids']:
            h = indexes['ASSUMPTION'].get(hid)
            check('INCOMPLETE-EVIDENCE-UNIVERSE', h is not None and exp['experiment_id'] in h['experiment_ids'] and h['envelope_id'] == arg['envelope_id'] and h['qualification_id'] == arg['qualification_id'], 'approved scoped primitive hypothesis')
            if h:
                statement = attempt(lambda h=h: provider.payload(h['statement']), 'assumption statement')
                if isinstance(statement, dict) and statement.get('assumes_target') == exp['experiment_id']:
                    f.add('INVALID-EVIDENCE-AUTHORITY', 'Circular target conclusion is not an independent premise')
        nv = attempt(lambda exp=exp: provider.nonvacuity(exp), 'non-vacuity source assessment')
        if nv and nv['status'] == 'INVALID': f.add('INVALID-ACTION-CONTEXT', nv['reason'])
        inp = attempt(lambda arg=arg: provider.invocation(arg, security, model.digest), 'exact mechanism-specific invocation')
        checked = attempt(lambda arg=arg, exp=exp: provider.evaluate(arg, exp, artifacts), 'concrete qualified LAB assessment', 'INCOMPLETE-EVIDENCE-UNIVERSE')
        aset = by_arg.get(aid, [])
        if len(aset) != 1 or inp is None or checked is None: continue
        a = aset[0]
        check('INVALID-ACTION-CONTEXT', a['exact_input_digest'] == digest(inp) and a['qualification_id'] == arg['qualification_id'] and a['artifact_ids'] == arg['certificate_artifact_ids'] and a['assumption_ids'] == arg['assumption_ids'], 'exact assessment invocation/claim/premise/artifact binding')
        invocation = attempt(lambda a=a: provider.payload(a['invocation_source']), 'bound invocation source')
        if invocation is not None:
            check('INVALID-EVIDENCE-AUTHORITY', invocation == {'mechanism': trusted['mechanism'], 'input_sha256': digest(inp)}, 'bound invocation source')
        assertion = attempt(lambda a=a: provider.payload(a['source_assertion_evidence']), 'exact assessment assertion')
        expected_assertion = {'mechanism': trusted['mechanism'], 'input_sha256': digest(inp), 'result': checked}
        assertion_ok = assertion is not None and check('INVALID-EVIDENCE-AUTHORITY', assertion == expected_assertion, 'independent result assertion; caller flags do not establish INVALID/VALID')
        recorded = {'status': a['complete_result'], 'bound': a['validated_bound']}
        result_ok = check('INCOMPLETE-EVIDENCE-UNIVERSE', recorded == {k: checked[k] for k in ('status', 'bound')}, 'returned result equals independently recomputed checker output')
        trace = [e for e in events.values() if e['assessment_id'] == a['assessment_id']]
        expected_trace = attempt(lambda a=a: provider.payload(trusted['trace_refs'][a['assessment_id']]), 'source complete invocation trace')
        if expected_trace is not None: check('INCOMPLETE-EVIDENCE-UNIVERSE', trace == expected_trace, 'complete read/control/return/error/retry/cache trace; null applicability exact')
        calls = [e for e in trace if e['event_kind'] == 'CALL']
        returns = [e for e in trace if e['event_kind'] == 'RETURN']
        check('INCOMPLETE-EVIDENCE-UNIVERSE', bool(calls) and bool(returns) and all(e['input_bytes'] == inp.hex() for e in calls) and all(e['output_bytes'] == canonical(checked).hex() for e in returns), 'exact complete invocation input and returned result bytes')
        qualified_assessment = all(role_ready.get(r) for r in ('policy-governance', 'assessor-competence', 'source-producer-correspondence', 'proof-soundness', 'non-vacuity'))
        if assertion_ok and result_ok and qualified_assessment:
            if checked['status'] == 'VALID':
                bounds[aid] = Fraction(*checked['bound'])
                check('INVALID-ACTION-CONTEXT', Fraction(*arg['claimed_bound']) >= bounds[aid], 'claimed bound cannot understate validated bound')
            elif checked['status'] == 'INVALID':
                code = EXPERIMENT_FAILURE[exp['kind']]; f.add(code, 'Qualified INVALID-ARGUMENT: ' + aid); result_codes.add(code)
            else: f.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'qualified UNAVAILABLE has no usable bound ' + aid)
    for oid, template in templates.items():
        o = indexes['OBLIGATION'].get(oid)
        if not o: continue
        check('INVALID-ACTION-CONTEXT', {k: o[k] for k in TEMPLATES['OBLIGATION']} == template, 'immutable obligation repeat ' + oid)
        computed = 'NOT-ESTABLISHED'
        if template['kind'] == 'EXACT':
            # Source assertion interpreted under the finite source-owned law.
            verdicts = [attempt(lambda ref=r: provider.payload(ref), 'exact obligation assertion') for r in o['exact_evidence_refs']]
            required = {'obligation_id': oid, 'model_digest': model.digest, 'result': 'EXACT-SATISFIED'}
            qualified_exact = oid in ledger['ready_obligations'] and all(role_ready.get(r) for r in ('model-ledger-classification', 'source-producer-correspondence', 'proof-soundness', 'observer-completeness', 'policy-governance'))
            if qualified_exact and verdicts and all(v == required for v in verdicts): computed = 'EXACT-SATISFIED'
            # A bare INVALID flag establishes neither its scope nor which protected
            # contract was violated. The finite source contract has no qualified
            # exact-counterexample decoder; retain inability, never invent actor risk.
            if any(isinstance(v, dict) and v.get('result') == 'EXACT-VIOLATION' for v in verdicts):
                f.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'Exact counterexample requires a qualified scoped decoder ' + oid)
            check('INVALID-PROFILE-SCHEMA', not o['argument_ids'], 'exact obligation has no computational waiver')
        elif oid in ledger['ready_obligations'] and o['argument_ids'] and all(a in bounds and oid in arguments[a]['obligation_ids'] for a in o['argument_ids']):
            computed = 'COMPUTATIONALLY-BOUNDED'
        dispositions[oid] = computed
        check('INCOMPLETE-EVIDENCE-UNIVERSE', computed not in ('NOT-ESTABLISHED', 'EXACT-VIOLATION') and o['disposition'] == computed, 'computed obligation disposition ' + oid)
    budget_results = {}
    for rid, rule in rules.items():
        c = indexes['COMPOSITION'].get(rid)
        if not c: continue
        if not check('INCOMPLETE-EVIDENCE-UNIVERSE', rid in ledger['ready_rules'], 'source-grounded and qualified composition prerequisites ' + rid): continue
        check('INVALID-ACTION-CONTEXT', {k: c[k] for k in TEMPLATES['COMPOSITION']} == rule, 'immutable composition repeat ' + rid)
        covered = trusted['coverage_terms'].get(rid)
        if not check('INCOMPLETE-EVIDENCE-UNIVERSE', covered is not None and c['argument_ids'] == covered['argument_ids'] and c['multiplicities'] == covered['multiplicities'], 'qualified whole-view decomposition and multiplicities ' + rid): continue
        if not check('INCOMPLETE-EVIDENCE-UNIVERSE', all(a in bounds for a in c['argument_ids']), 'no zero/default for invalid/unavailable terms ' + rid): continue
        if c['method'] == 'UNION':
            q = min(Fraction(1), sum((bounds[a]*m for a, m in zip(c['argument_ids'], c['multiplicities'])), Fraction()))
        else:
            theorem = attempt(lambda c=c: provider.payload(c['theorem_ref']), 'qualified composition theorem')
            # Exact selected LAB theorem supports a joint claim only. Unknown
            # product/tighter rules are inability, never a generic callback PASS.
            if not check('INCOMPLETE-EVIDENCE-UNIVERSE', theorem == {'method': 'SINGLE-JOINT-CLAIM-V1'} and len(c['argument_ids']) == 1 and c['multiplicities'] == [1], 'supported source-qualified theorem'): continue
            q = bounds[c['argument_ids'][0]]
        check('INVALID-ACTION-CONTEXT', pair(q) == c['composed_bound'], 'exact reduced composition result ' + rid)
        exp = experiments.get(c['experiment_id'])
        if exp:
            code = EXPERIMENT_FAILURE[exp['kind']]
            budget_results[exp['experiment_id']] = {'bound': pair(q), 'maximum': exp['maximum'], 'within_budget': q <= Fraction(*exp['maximum'])}
            if q > Fraction(*exp['maximum']): f.add(code, 'established budget exceeded ' + rid); result_codes.add(code)
    # A per-argument number cannot discharge a whole-view duty whose composition
    # is still unsupported/unqualified. An established over-budget value retains
    # its exact value and corresponding failure; it is never rounded away.
    for oid,template in templates.items():
        if template['kind']=='COMPUTATIONAL' and template['experiment_id'] not in budget_results:
            dispositions[oid]='NOT-ESTABLISHED'
            f.add('INCOMPLETE-EVIDENCE-UNIVERSE','whole-view composition not established for obligation '+oid)
    for a in indexes['POLICY-APPLICABILITY'].values():
        check('INVALID-ACTION-CONTEXT', a['mapping_digest'] == request.get('mapping_digest') == trusted['mapping_digest'] and a['stage'] == request.get('phase') and a['attempt_ordinal'] == request.get('attempt') and a['envelope_id'] == policy['envelope_id'], 'applicability exact mapping/context/phase/attempt')
        context = attempt(lambda a=a: provider.payload(a['context_source']), 'applicability source context')
        dependencies = attempt(lambda a=a: provider.payload(a['dependency_evidence']), 'complete consumed applicability dependencies')
        if context is not None:
            check('INVALID-ACTION-CONTEXT', context == trusted['applicability_context'], 'source context and selected two-bit adequacy')
            check('INVALID-ACTION-CONTEXT', isinstance(context, dict) and all(context.get(k) == [] for k in ('extra_material_predicates', 'extra_ordering', 'extra_effects')), 'selected two-component profile cannot acquire additional state/accounting/order/effects')
        else: f.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'applicability context unavailable')
        check('INCOMPLETE-EVIDENCE-UNIVERSE', dependencies == trusted['applicability_dependencies'], 'complete dependency closure; unchanged digest/bits cannot replace it')
        status = attempt(lambda a=a: provider.payload(a['source_status_evidence']), 'current source status')
        if status is not None: check('INVALID-ACTION-CONTEXT', status == {'status': 'VALID-FOR-DECLARED-LAB-SCOPE'}, 'source applicability status')
        else: f.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'applicability source status unavailable')
    observations = attempt(lambda: provider.payload(request['observations_ref']), 'authenticated exact observation facts')
    if observations is not None and all(role_ready.get(r) for r in ('observer-completeness', 'model-ledger-classification', 'source-producer-correspondence')):
        from .observations import observe
        attempt(lambda: observe(observations, f), 'full known observation checks')
    for scope, (_, parsed) in parsed_bundles.items():
        row = parsed['evidence']
        for kind, field in [('COLLISION', 'uniqueness_result'), ('CROSS-ACTION-TRACKING', 'correlation_result'), ('ACTOR-INFORMATION', 'actor_reconstruction_result')]:
            code = EXPERIMENT_FAILURE[kind]
            expected = 'FAIL' if code in f.reasons else 'PASS'
            check('INCOMPLETE-EVIDENCE-UNIVERSE', row[field] == expected, 'signed result cells must equal independent complete decision ' + scope + ':' + field)
    # Collect known failures first; never expose a qualified positive disposition
    # through missing/mismatched authentication or scope/outer joins.
    binding_failures = {'INVALID-PROFILE-SCHEMA','PROFILE-DIGEST-MISMATCH','INVALID-EVIDENCE-AUTHORITY',
        'MISSING-EVIDENCE','INVALID-EVIDENCE-AUTHENTICATION','INVALID-EVIDENCE-DIGEST','INVALID-ACTION-CONTEXT',
        'INVALID-SURFACE-LABELS','COMPONENT-COUNT-MISMATCH','UNNECESSARY-COMPONENT','COMPONENT-FAILURE'}
    unavailable = any(not reason.startswith('signed result cells must equal') for reason in f.reasons.get('INCOMPLETE-EVIDENCE-UNIVERSE', []))
    if not scopes['ready'] or unavailable or binding_failures.intersection(f.reasons):
        dispositions = {oid:'NOT-ESTABLISHED' for oid in templates}
        budget_results = {}
        scopes['ready'] = False
        scopes['qualification'] = 'NOT-ESTABLISHED'
        for status in scopes['scopes'].values():
            status['ready'] = False; status['qualification'] = 'NOT-ESTABLISHED'
        f.add('INCOMPLETE-EVIDENCE-UNIVERSE','authenticated three-scope ledger conclusion not established')
    scopes['signed_results_consistent'] = not any(reason.startswith('signed result cells must equal') for reason in f.reasons.get('INCOMPLETE-EVIDENCE-UNIVERSE', []))
    scopes['conditional_checks_pass'] = scopes['ready'] and scopes['signed_results_consistent'] and not f.reasons
    bindings = {'final_profile_sha256': digest(outer), 'model_sha256': model.digest, 'policy_id': policy['policy_id'],
                'policy_material_sha256': policy['policy_digest'], 'assumption_ids': policy['assumption_ids'],
                'qualification_ids': policy['qualification_ids'], 'computed_dispositions': dispositions,
                'computed_budgets': budget_results, 'ledger_validation': ledger, 'scope_validation': scopes, 'bundle_authentication': authentication, 'laboratory_hypotheses': list(ROLES),
                'meaning': 'Local conditional binding/admission checks only; actual qualification and full-stream identities remain unestablished'}
    return f.result(mode, bindings)


def collect(request, trusted=None, *, adapter=None):
    f = Failures()
    try:
        return _collect(request, trusted, f, adapter)
    except (ValidationError, ValueError, KeyError, TypeError, IndexError, OverflowError, OSError) as e:
        # Malformed dependent input cannot erase already collected authentication.
        code = getattr(e, 'category', 'INVALID-PROFILE-SCHEMA')
        from .failures import ORDER
        f.add(code if code in ORDER else 'INVALID-PROFILE-SCHEMA', 'Unusable dependent input: ' + str(e))
        return f.result(request.get('mode', 'ACTUAL') if isinstance(request, dict) else 'ACTUAL')
