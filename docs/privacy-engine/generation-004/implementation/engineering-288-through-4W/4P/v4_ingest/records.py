"""Generic S90 ingestion. No issuer cache, model expansion or admission engine.

The frozen field register supplies types; this module implements them anew.
Source competence, truth and complete-model correspondence are not inferred.
"""
from .definition import ACTIVE
import csv
import hashlib
import json
import math
import re
from pathlib import Path


class ValidationError(ValueError):
    def __init__(self, message, path='$', category='LOCAL-VALIDATION'):
        self.path, self.category = path, category
        super().__init__(f'{path}: {message}')


def require(ok, message, path='$', category='LOCAL-VALIDATION'):
    if not ok:
        raise ValidationError(message, path, category)


with (Path(__file__).parent / 'data/security-fields.tsv').open() as f:
    FIELD_ROWS = list(csv.DictReader(f, delimiter='\t'))
SCHEMAS = sorted({r['schema'] for r in FIELD_ROWS})
SPEC = {s: {r['field']: r['type'] for r in FIELD_ROWS if r['schema'] == s} for s in SCHEMAS}
IDENTITY = {s: next(iter(SPEC[s])) for s in SCHEMAS}
ENUM = {
    'EXPERIMENT': {'COLLISION', 'CROSS-ACTION-TRACKING', 'ACTOR-INFORMATION'},
    'QUALIFIED': {'VALID', 'INVALID', 'UNAVAILABLE'},
    'EXPOSURE': {'PUBLIC', 'CONFIDENTIAL', 'PRIVATE-ACTOR'},
    'OBLIGATION': {'EXACT', 'COMPUTATIONAL'},
    'DISPOSITION': {'EXACT-SATISFIED', 'EXACT-VIOLATION', 'COMPUTATIONALLY-BOUNDED', 'NOT-ESTABLISHED'},
    'COMPOSITION': {'UNION', 'SOURCE-QUALIFIED-THEOREM'},
    'ASSESSOR-EVENT': {'READ', 'CALL', 'RETURN', 'ERROR', 'RETRY', 'CACHE'},
    'STAGE': {'STATIC-ADMISSION', 'E', 'PRE-EXECUTION', 'PRE-COMMITMENT'},
}
TEMPLATES = {
    'OBLIGATION': ('obligation_id', 'kind', 'target_ids', 'coalition_id', 'node_ids', 'edge_ids', 'experiment_id'),
    'COMPOSITION': ('composition_id', 'policy_id', 'experiment_id', 'method', 'theorem_ref', 'qualification_id'),
}
DEFAULT_MAX_BYTES = 16 * 1024 * 1024  # Local resource guard, NOT a protocol wire limit.
LOCAL_MAX_DEPTH = 128  # Explicit implementation budget, never a protocol grammar rule.


def canonical(value):
    from semantic_stream.storage import Node, Hex, canonical as streamed
    def large(v):
        from metadata_catalog.core import DiskMap
        if isinstance(v, (Node, Hex, DiskMap)): return True
        if isinstance(v, dict): return any(large(x) for x in v.values())
        if isinstance(v, (list, tuple)): return any(large(x) for x in v)
        return False
    if large(value): return streamed(value)
    return (json.dumps(value, sort_keys=True, separators=(',', ':'),
                       ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')


def digest(raw):
    from semantic_stream.storage import Blob
    if isinstance(raw, Blob): return raw.sha()
    return hashlib.sha256(raw).hexdigest()


def field_digest(value):
    """S90: typed canonical JSON plus LF; BYTES hashes the hex JSON string."""
    return digest(canonical(value))


def _pairs(pairs):
    obj = {}
    for k, v in pairs:
        require(k not in obj, 'duplicate JSON key')
        obj[k] = v
    return obj


def _no_number(s):
    raise ValidationError('floating point/nonfinite number is forbidden')


def _json_int(s):
    try:
        return int(s)
    except ValueError as e:
        raise ValidationError('integer exceeds local conversion capacity; no partial acceptance', category='RESOURCE-LIMIT') from e


def parse(raw, max_bytes=DEFAULT_MAX_BYTES):
    from semantic_stream.storage import Blob
    if isinstance(raw, Blob): return raw.store.parse(raw)
    require(type(raw) is bytes, 'exact byte input required')
    require(type(max_bytes) is int and max_bytes > 0, 'invalid resource limit', category='RESOURCE-LIMIT')
    require(len(raw) <= max_bytes, 'input exceeds local byte budget; no partial acceptance', category='RESOURCE-LIMIT')
    # Bound nesting before the recursive JSON decoder/canonical serializer runs.
    # Quotes/escapes protect brackets in strings; structural validity is checked below.
    depth, quoted, escaped = 0, False, False
    for byte in raw:
        if quoted:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                quoted = False
        elif byte == 34:
            quoted = True
        elif byte in (91, 123):
            depth += 1
            require(depth <= LOCAL_MAX_DEPTH, 'local JSON nesting budget exceeded; no partial acceptance', category='RESOURCE-LIMIT')
        elif byte in (93, 125):
            depth -= 1
    try:
        value = json.loads(raw.decode('ascii'), object_pairs_hook=_pairs,
                           parse_int=_json_int, parse_float=_no_number, parse_constant=_no_number)
        require(canonical(value) == raw, 'noncanonical JSON bytes')
    except ValidationError:
        raise
    except (ValueError, UnicodeError, RecursionError, OverflowError, TypeError) as e:
        raise ValidationError('invalid JSON or unsupported local depth/integer size') from e
    return value


def exact(value, keys, path='$'):
    require(isinstance(value, dict) and set(value) == set(keys), 'exact object keys required', path)


def primitive(kind, value, path='$', field_register=None):
    if kind == 'ID':
        require(type(value) is str and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:#-]*', value, re.ASCII), 'canonical ASCII ID required', path)
    elif kind == 'FIELD-CLASS-REF':
        require(type(value) is str and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:#-]*(?:\.\$record)?', value, re.ASCII), 'canonical field-class spelling required', path)
        require(type(field_register) in (list, tuple, set, frozenset) and all(type(n) is str for n in field_register), 'explicit field-class register context required', path, category='INCOMPLETE-EVIDENCE-UNIVERSE')
        require(field_register is not None and value in field_register, 'exact complete source-owned field-class register membership required', path, category='INCOMPLETE-EVIDENCE-UNIVERSE')
    elif kind == 'DIGEST':
        require(type(value) is str and re.fullmatch(r'[0-9a-f]{64}', value), 'lowercase SHA256 required', path)
    elif kind == 'BYTES':
        from semantic_stream.storage import Hex
        if isinstance(value, Hex): return
        require(type(value) is str and re.fullmatch(r'(?:[0-9a-f]{2})*', value), 'lowercase even-length hex required', path)
    elif kind == 'UINT':
        require(type(value) is int and value >= 0, 'UINT excludes Boolean and negatives', path)
    elif kind == 'RATIONAL':
        require(isinstance(value, list) and len(value) == 2 and all(type(x) is int for x in value), 'integer rational pair required', path)
        a, b = value
        require(b > 0 and 0 <= a <= b and math.gcd(a, b) == 1, 'reduced probability in [0,1] required', path)
    elif kind == 'SOURCE-REF':
        exact(value, ('owner_source_id', 'source_sha256', 'source_anchor', 'material_sha256'), path)
        for key in value:
            primitive('DIGEST' if key.endswith('sha256') else 'ID', value[key], path + '.' + key)
    elif kind.startswith('LIST-'):
        require(isinstance(value, list), 'array required', path)
        for i, item in enumerate(value):
            primitive(kind[5:], item, f'{path}[{i}]')
        if kind == 'LIST-ID':
            require(len(set(value)) == len(value), 'duplicate identity in list', path)
    elif kind.startswith('ENUM-'):
        require(type(value) is str and value in ENUM[kind[5:]], 'invalid enum', path)
    else:
        raise ValidationError('unknown primitive type', path)


def profile_identity(value):
    """Active G4 binding of retained mapping/profile identity grammar."""
    match = re.fullmatch(r'PE-G4-TSE-PROFILE-([0-9]{6})-V0001', value) if type(value) is str else None
    require(match is not None and int(match[1]) > 0, 'active G4 profile identity grammar')
    return value


def validate_record(schema, rec, template=False, path='$', *, field_register=None):
    require(schema in SPEC, 'unknown schema', path)
    require(type(template) is bool and (not template or schema in TEMPLATES), 'invalid template selection', path)
    keys = TEMPLATES[schema] if template else SPEC[schema]
    exact(rec, keys, path)
    for field in keys:
        v = rec[field]
        if v is None:
            allowed = ((schema == 'ASSESSMENT' and field == 'validated_bound' and rec['complete_result'] in ('INVALID', 'UNAVAILABLE'))
                       or (schema == 'ASSESSOR-EVENT' and field in ('input_bytes', 'output_bytes'))
                       or (schema == 'OBLIGATION' and field == 'experiment_id' and rec['kind'] == 'EXACT')
                       or (schema == 'COMPOSITION' and field == 'theorem_ref' and rec['method'] == 'UNION'))
            require(allowed, 'unjustified null', path + '.' + field)
        else:
            primitive(SPEC[schema][field], v, path + '.' + field, field_register=field_register)
    if schema == 'ASSESSMENT':
        require(rec['complete_result'] == 'VALID' or rec['validated_bound'] is None, 'INVALID/UNAVAILABLE must have null bound', path)
    if schema == 'COMPOSITION':
        require(rec['method'] != 'UNION' or rec['theorem_ref'] is None, 'UNION has no theorem reference', path)
        if not template:
            require(len(rec['argument_ids']) == len(rec['multiplicities']) and all(x > 0 for x in rec['multiplicities']), 'aligned positive multiplicities required', path)
    if schema == 'OBLIGATION':
        require(rec['kind'] != 'EXACT' or rec['experiment_id'] is None, 'EXACT has no computational experiment', path)
    if schema == 'EXPERIMENT':
        require(rec['maximum'][0] < rec['maximum'][1], 'maximum must be strictly below one', path)
    if schema == 'ARTIFACT':
        require(digest(__import__('semantic_stream.storage',fromlist=['unhex']).unhex(rec['exact_bytes'])) == rec['digest'], 'artifact octet digest mismatch', path)
    if schema == 'POLICY':
        profile_identity(rec['profile_id'])
        require(rec['policy_digest'] == rec['policy_source']['material_sha256'], 'policy digest must name independently governing material', path)
    return rec


def validate_array(schema, values, template=False, path='$', *, field_register=None):
    require(isinstance(values, list), 'record directory must be an array', path)
    for i, rec in enumerate(values):
        validate_record(schema, rec, template, f'{path}[{i}]', field_register=field_register)
    ids = [r[IDENTITY[schema]] for r in values]
    require(ids == sorted(set(ids)) and all('::' not in x for x in ids), 'unique ASCII-sorted record identities without :: required', path)
    return values


def ingest_record(raw, schema, template=False, max_bytes=DEFAULT_MAX_BYTES, *, field_register=None):
    return validate_record(schema, parse(raw, max_bytes), template, field_register=field_register)


def _pending(duty, path):
    return {'duty': duty, 'path': path}


def local_joins(dirs, pending, phase=None, profile_digest=None, static=False):
    """Check supplied typed references, preserving deferred/unavailable destinations.

    Dirs contains None for unavailable/inapplicable external directories. We never
    turn those into complete empty directories. Local joins are not full coverage.
    """
    indexes = {s: None if vs is None else {v[IDENTITY[s]]: v for v in vs} for s, vs in dirs.items()}
    def resolve(schema, ident, path):
        if indexes[schema] is None:
            pending.append(_pending('referenced directory unavailable or not yet justified', path))
            return None
        require(ident in indexes[schema], f'orphan typed reference to {schema}: {ident}', path)
        return indexes[schema][ident]
    policies = dirs['POLICY']
    policy = policies[0] if policies else None
    directory_fields = {'experiment_ids': 'EXPERIMENT', 'coalition_ids': 'OBSERVER',
                        'assumption_ids': 'ASSUMPTION', 'qualification_ids': 'QUALIFICATION',
                        'field_label_ids': 'FIELD-LABEL'}
    if policy:
        for field, s in directory_fields.items():
            if indexes[s] is None:
                pending.append(_pending('policy directory equality requires available directory', 'POLICY.' + field))
            else:
                require(policy[field] == list(indexes[s]), f'policy directory mismatch: {field}', 'POLICY.' + field)
        for field, s in [('envelope_id', 'ENVELOPE'), ('leakage_id', 'LEAKAGE')]:
            resolve(s, policy[field], 'POLICY.' + field)
    else:
        pending.append(_pending('sole owning policy unavailable', 'POLICY'))
    refs = {
        'algorithm_id': 'ALGORITHM', 'algorithm_ids': 'ALGORITHM', 'artifact_ids': 'ARTIFACT',
        'certificate_artifact_ids': 'ARTIFACT', 'qualification_id': 'QUALIFICATION',
        'assumption_ids': 'ASSUMPTION', 'experiment_id': 'EXPERIMENT', 'experiment_ids': 'EXPERIMENT',
        'envelope_id': 'ENVELOPE', 'leakage_id': 'LEAKAGE', 'coalition_id': 'OBSERVER',
        'coalition_ids': 'OBSERVER', 'argument_id': 'ARGUMENT', 'argument_ids': 'ARGUMENT',
        'assessment_id': 'ASSESSMENT', 'predecessor_ids': 'ASSESSOR-EVENT',
        'obligation_ids': 'OBLIGATION',
    }
    for s, records in dirs.items():
        for rec in records or []:
            p = s + '[' + rec[IDENTITY[s]] + ']'
            if 'policy_id' in rec and s != 'POLICY':
                resolve('POLICY', rec['policy_id'], p + '.policy_id')
            if profile_digest is not None and 'profile_digest' in rec:
                require(rec['profile_digest'] == profile_digest, 'record/wrapper profile digest mismatch', p)
            for field, dest in refs.items():
                if field not in rec or rec[field] is None or field == IDENTITY[s]:
                    continue
                ids = rec[field] if isinstance(rec[field], list) else [rec[field]]
                for ident in ids:
                    resolve(dest, ident, p + '.' + field)
            if 'target_id' in rec or 'target_ids' in rec:
                targets = rec.get('target_ids', [rec.get('target_id')])
                if policy:
                    require(set(targets) <= set(policy['target_ids']), 'target outside policy directory', p)
                pending.append(_pending('independently regenerated protected target directory', p))
            if s == 'EXPERIMENT' and policy:
                require(rec['envelope_id'] == policy['envelope_id'] and rec['leakage_id'] == policy['leakage_id'], 'experiment owning envelope/leakage mismatch', p)
            if s == 'ARTIFACT':
                algo = resolve('ALGORITHM', rec['algorithm_id'], p)
                if algo:
                    require(rec['artifact_id'] in algo['artifact_ids'], 'artifact/algorithm inverse join mismatch', p)
            if s == 'ALGORITHM':
                for aid in rec['artifact_ids']:
                    art = resolve('ARTIFACT', aid, p)
                    if art:
                        require(art['algorithm_id'] == rec['algorithm_id'], 'algorithm/artifact inverse join mismatch', p)
            if s == 'ARGUMENT':
                rule = resolve('COMPOSITION', rec['composition_id'], p + '.composition_id')
                if rule:
                    require(rule['experiment_id'] == rec['experiment_id'], 'argument/composition experiment mismatch', p)
            if s == 'COMPOSITION' and 'argument_ids' in rec:
                for aid in rec['argument_ids']:
                    arg = resolve('ARGUMENT', aid, p)
                    if arg:
                        require(arg['experiment_id'] == rec['experiment_id'] and arg['composition_id'] == rec['composition_id'], 'composition/argument owning rule mismatch', p)
            if s == 'ASSESSMENT':
                arg = resolve('ARGUMENT', rec['argument_id'], p)
                if arg:
                    require(arg['qualification_id'] == rec['qualification_id'], 'assessment mechanism mismatch', p)
            if s == 'ASSESSOR-EVENT':
                for pred in rec['predecessor_ids']:
                    prev = resolve('ASSESSOR-EVENT', pred, p)
                    if prev:
                        require(prev['assessment_id'] == rec['assessment_id'] and pred != rec['event_id'], 'event predecessor context mismatch/self reference', p)
            if s == 'POLICY-APPLICABILITY' and phase is not None:
                require(rec['stage'] == phase, 'applicability stage/wrapper mismatch', p)
            if s == 'FIELD-LABEL':
                pending.append(_pending('full-model field coverage and source-qualified visibility', p))
    # Composition records are per-experiment rules/results, never policy directory IDs.
    if dirs['COMPOSITION'] is not None and dirs['EXPERIMENT'] is not None:
        experiments = [r['experiment_id'] for r in dirs['COMPOSITION']]
        require(len(set(experiments)) == len(experiments) and set(experiments) == set(indexes['EXPERIMENT']), 'one composition record for each supplied experiment required', 'COMPOSITION')
    # One FIELD-LABEL per supplied surface; full-model coverage is later.
    labels = dirs['FIELD-LABEL']
    if labels is not None:
        require(len({r['surface_id'] for r in labels}) == len(labels), 'duplicate field surface labels', 'FIELD-LABEL')
    # Causal predecessor cycles are a decidable local trace defect. This checks
    # only supplied events; complete invocation acquisition is still deferred.
    events = dirs['ASSESSOR-EVENT']
    if events:
        successors = {r['event_id']: [] for r in events}
        indegree = {r['event_id']: len(r['predecessor_ids']) for r in events}
        for event in events:
            for pred in event['predecessor_ids']:
                # resolve() above already checked presence and same assessment.
                successors[pred].append(event['event_id'])
        ready = [eid for eid, degree in indegree.items() if degree == 0]
        count = 0
        while ready:
            eid = ready.pop()
            count += 1
            for child in successors[eid]:
                indegree[child] -= 1
                if indegree[child] == 0:
                    ready.append(child)
        require(count == len(events), 'cyclic event predecessor trace', 'ASSESSOR-EVENT')


def _source_refs(value, path='$'):
    if isinstance(value, dict):
        if set(value) == {'owner_source_id', 'source_sha256', 'source_anchor', 'material_sha256'}:
            yield path, value
        else:
            for k, v in value.items():
                yield from _source_refs(v, path + '.' + k)
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from _source_refs(v, f'{path}[{i}]')


def inspect_materials(value, material_lookup=None):
    """Exact-byte integrity only. Lookup receives a digest, never a filesystem path.

    Missing material remains explicit. Caller lookup cannot establish ownership,
    semantic interpretation, construction dependencies or qualification.
    """
    results = []
    for path, ref in _source_refs(value):
        raw = material_lookup(ref['material_sha256']) if material_lookup is not None else None
        if raw is None:
            status = 'UNAVAILABLE'
        else:
            require(type(raw) is bytes and digest(raw) == ref['material_sha256'], 'referenced exact material digest mismatch', path)
            status = 'EXACT-BYTES-PRESENT-UNQUALIFIED'
        results.append({'path': path, 'material_sha256': ref['material_sha256'], 'status': status})
    return results


def _report(value, dirs, availability, pending, materials):
    result = {
        'result': 'LOCALLY-VALID-UNQUALIFIED', 'profile_admitted': False,
        'source_qualification_established': False, 'model_validation_complete': False,
        'sha256': digest(canonical(value)), 'record_counts': {s: len(v or []) for s, v in dirs.items()},
        'availability': availability, 'source_material': materials,
        'pending': pending,
        'deferred': ['complete-model expansion/provenance and wire cardinalities',
                     'source-qualified parsing/preimages, ownership, visibility and competence',
                     'acyclic exact-byte construction and evidence-to-immutable-model binding',
                     'non-vacuity, assessment truth, complete dependencies/coverage and ordered admission'],
    }
    return result


def ingest_evidence(raw, *, material_lookup=None, max_bytes=DEFAULT_MAX_BYTES, field_register=None):
    value = parse(raw, max_bytes)
    exact(value, ('format', 'profile_digest', 'phase', 'records'))
    require(value['format'] == 'PE-G4-SECURITY-RECORDS-V4', 'wrong external format')
    primitive('DIGEST', value['profile_digest'], '$.profile_digest')
    primitive('ENUM-STAGE', value['phase'], '$.phase')
    exact(value['records'], SCHEMAS, '$.records')
    dirs, availability, pending = {}, {}, []
    for s in SCHEMAS:
        d = value['records'][s]
        path = '$.records.' + s
        exact(d, ('status', 'justification', 'instances'), path)
        require(type(d['status']) is str and d['status'] in ('PRESENT', 'UNAVAILABLE', 'INAPPLICABLE'), 'availability status', path)
        if d['justification'] is not None:
            primitive('SOURCE-REF', d['justification'], path + '.justification')
        validate_array(s, d['instances'], path=path + '.instances', field_register=field_register)
        require((d['status'] == 'PRESENT') == bool(d['instances']), 'status/instance mismatch', path)
        require(d['status'] != 'INAPPLICABLE' or d['justification'] is not None, 'INAPPLICABLE needs owning source justification', path)
        if s in ('POLICY', 'ENVELOPE', 'LEAKAGE') and d['status'] == 'PRESENT':
            require(len(d['instances']) == 1, 'single owning record required', path)
        dirs[s] = d['instances'] if d['status'] == 'PRESENT' else None
        availability[s] = {'status': d['status'], 'usable_as_qualified_evidence': False}
        if d['status'] != 'PRESENT':
            pending.append(_pending('UNAVAILABLE blocks discharge' if d['status'] == 'UNAVAILABLE' else 'INAPPLICABLE requires independent source validation', path))
        for rec in d['instances']:
            if s == 'ASSESSMENT':
                availability[s].setdefault('completed_results', []).append({
                    'assessment_id': rec['assessment_id'], 'result': rec['complete_result'],
                    'validated_bound': rec['validated_bound'], 'usable_numerical_term': False})
            if s == 'ASSESSOR-EVENT':
                for field in ('input_bytes', 'output_bytes'):
                    if rec[field] is None:
                        pending.append(_pending('event null applicability requires qualified owning grammar', path + '.' + rec['event_id'] + '.' + field))
    local_joins(dirs, pending, phase=value['phase'], profile_digest=value['profile_digest'])
    return value, _report(value, dirs, availability, pending, inspect_materials(value, material_lookup))


def ingest_security(raw, *, material_lookup=None, max_bytes=DEFAULT_MAX_BYTES, field_register=None):
    """The exact security_contract subobject, with immutable templates only."""
    value = parse(raw, max_bytes)
    exact(value, ('contract_sha256', 'policy', 'schema_sha256', 'qualification_interface_sha256',
                  'experiments', 'assumptions', 'qualification_contracts', 'operating_envelope',
                  'leakage', 'obligations', 'composition_rules'))
    for k in ('contract_sha256', 'schema_sha256', 'qualification_interface_sha256'):
        primitive('DIGEST', value[k], '$.' + k)
    p = value['policy']
    exact(p, ('record', 'algorithms', 'artifacts', 'observers', 'field_labels'), '$.policy')
    dirs = {s: None for s in SCHEMAS}
    validate_record('POLICY', p['record'], path='$.policy.record')
    dirs['POLICY'] = [p['record']]
    for k, s in [('algorithms', 'ALGORITHM'), ('artifacts', 'ARTIFACT'), ('observers', 'OBSERVER'), ('field_labels', 'FIELD-LABEL')]:
        dirs[s] = validate_array(s, p[k], path='$.policy.' + k, field_register=field_register)
    for k, s in [('experiments', 'EXPERIMENT'), ('assumptions', 'ASSUMPTION'), ('qualification_contracts', 'QUALIFICATION'), ('obligations', 'OBLIGATION')]:
        dirs[s] = validate_array(s, value[k], s == 'OBLIGATION', '$.' + k)
    for k, s in [('operating_envelope', 'ENVELOPE'), ('leakage', 'LEAKAGE')]:
        dirs[s] = [validate_record(s, value[k], path='$.' + k)]
    c = value['composition_rules']
    exact(c, ('directory_id', 'records'), '$.composition_rules')
    primitive('ID', c['directory_id'])
    require(c['directory_id'] == p['record']['composition_id'], 'composition directory join')
    dirs['COMPOSITION'] = validate_array('COMPOSITION', c['records'], True, '$.composition_rules.records')
    pending = []
    local_joins(dirs, pending, static=True)
    for s, vs in dirs.items():
        if vs == []:
            pending.append(_pending('empty applicable directory requires qualified inapplicability; no default completion', s))
    availability = {s: {'status': 'STATIC-TEMPLATE' if s in TEMPLATES else 'PRESENT' if vs else 'NOT-IN-STATIC-CONTRACT', 'usable_as_qualified_evidence': False} for s, vs in dirs.items()}
    return value, _report(value, dirs, availability, pending, inspect_materials(value, material_lookup))
