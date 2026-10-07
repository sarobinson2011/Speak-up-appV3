"""Source-owned finite ledger acquisition and executable correspondence checks.

This concrete acquisition grammar is laboratory mechanism metadata, not an
extension of the accepted V4 template/record grammar or an actual qualification.
"""
from collections import Counter
from v4_ingest.records import canonical,digest,exact,require,ValidationError
from admission_kernel.sources import MissingMaterial
from .coverage import normalized,union,contains,potential_stripe_counts,weighted_count

EXACT_DUTIES=('SOURCE-OWNERSHIP','DECLARATION-RECORD-JOINS','EXPOSURE',
              'COALITION-VISIBILITY','SOURCE-ESTABLISHED-LINKAGE','CANONICAL-ENCODING',
              'PROTECTED-ACTOR-INFORMATION','OBSERVED-COUNTEREXAMPLES')
CLASS_ROLES=('policy-governance','model-ledger-classification','source-producer-correspondence')
COMP_ROLES=CLASS_ROLES+('composition-decomposition','assessor-competence','proof-soundness','observer-completeness','non-vacuity')

def nv_inputs(security,model_digest):
    # No final profile/result in this STATIC construction input; avoids self-digest cycles.
    return {'policy':security['policy'],'experiments':security['experiments'],
            'envelope':security['operating_envelope'],'leakage':security['leakage'],
            'qualification_contracts':security['qualification_contracts'],
            'model_digest':model_digest}

def validate(provider,trusted,security,model,indexes,role_ready,failures,mode):
    report={'source_acquired':False,'mechanical_coverage':False,'classification_ready':False,
            'ready_obligations':[],'ready_rules':[],'nv_ready':[],
            'qualification':'NOT-ESTABLISHED','actual_qualification_established':False,
            'profile_admitted':False}
    def check(code,ok,why):
        if not ok:failures.add(code,'ledger: '+why)
        return ok
    def attempt(fn,label):
        try:return fn()
        except MissingMaterial as e:failures.add('MISSING-EVIDENCE','ledger '+label+': '+str(e))
        except (ValidationError,ValueError,KeyError,TypeError,IndexError) as e:
            code=getattr(e,'category','INVALID-PROFILE-SCHEMA')
            failures.add(code,'ledger '+label+': '+str(e))
        return None
    ref=trusted.get('ledger_source_ref')
    if ref is None:
        failures.add('MISSING-EVIDENCE','independent ledger construction source bytes/reference absent')
        failures.add('INCOMPLETE-EVIDENCE-UNIVERSE','source-grounded complete classification/coverage unavailable')
        return report
    source=attempt(lambda:provider.payload(ref),'source acquisition')
    if source is None:
        failures.add('INCOMPLETE-EVIDENCE-UNIVERSE','ledger source cannot be reconstructed');return report
    report['source_acquired']=True;report['source_reference']=ref
    if attempt(lambda:provider.construction([ref]),'static ledger source dependency closure') is None:
        failures.add('INCOMPLETE-EVIDENCE-UNIVERSE','ledger construction dependency closure unavailable');return report
    def shape():
        exact(source,('format','model_digest','policy_id','target_ids','coalition_ids','obligations',
                      'duty_assignments','coverage','compositions','nv_input_sha256','whole_view_experiments'))
        require(source['format']=='CP4D-FINITE-LEDGER-SOURCE-V1','unsupported ledger acquisition grammar',category='INCOMPLETE-EVIDENCE-UNIVERSE')
        for k in ('obligations','duty_assignments','coverage','whole_view_experiments'):require(isinstance(source[k], list),'ledger '+k+' array')
        require(isinstance(source['compositions'], dict),'source composition directory')
        return True
    if not attempt(shape,'shape'):return report
    policy=security['policy']['record'];templates={o['obligation_id']:o for o in security['obligations']}
    experiments={x['experiment_id']:x for x in security['experiments']}
    rules={r['composition_id']:r for r in security['composition_rules']['records']}
    bound=check('INVALID-ACTION-CONTEXT',source['model_digest']==model.digest and source['policy_id']==policy['policy_id'],'exact model/policy source binding')
    bound=check('INCOMPLETE-EVIDENCE-UNIVERSE',source['target_ids']==policy['target_ids'] and source['coalition_ids']==policy['coalition_ids'],'complete independently sourced target/coalition directories') and bound
    from .construct import from_source
    constructed=attempt(lambda:from_source(source,model,policy),'canonical directory construction')
    if constructed is None:
        failures.add('INCOMPLETE-EVIDENCE-UNIVERSE','canonical source ledger directories could not be constructed');return report
    expected=constructed['obligations']
    bound=check('INCOMPLETE-EVIDENCE-UNIVERSE',expected==security['obligations'],'independently acquired immutable classification/templates (no issuer omissions)') and bound
    bound=check('INCOMPLETE-EVIDENCE-UNIVERSE',constructed['composition_rules']==security['composition_rules'],'independently constructed composition directory') and bound
    bound=check('INCOMPLETE-EVIDENCE-UNIVERSE',set(indexes['OBLIGATION'])==set(templates),'one external disposition for every template') and bound
    for oid,o in templates.items():
        def scope(o=o):
            model.obligation(o)
            require(set(o['target_ids'])<=set(policy['target_ids']) and o['coalition_id'] in policy['coalition_ids'],'obligation target/coalition scope',category='INVALID-ACTION-CONTEXT')
            if o['kind']=='COMPUTATIONAL':
                x=experiments.get(o['experiment_id']);require(x is not None,'computational experiment missing',category='INCOMPLETE-EVIDENCE-UNIVERSE')
                require(o['coalition_id']==x['coalition_id'] and set(o['target_ids'])=={x['target_id']},'obligation exact experiment target/view',category='INVALID-ACTION-CONTEXT')
            else:require(o['experiment_id'] is None,'exact obligation cannot take computational experiment')
            return True
        if not attempt(scope,oid):bound=False
    # Every exact duty family is explicitly assigned under the source contract.
    duties={};duties_ok=True
    for row in source['duty_assignments']:
        def duty(row=row):
            exact(row,('duty','obligation_ids'));d=row['duty'];require(d in EXACT_DUTIES,'unknown exact duty family')
            require(d not in duties,'conflicting/duplicate exact duty classification',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            ids=row['obligation_ids'];require(isinstance(ids, list) and ids and len(set(ids))==len(ids),'nonempty distinct exact obligation assignments')
            require(all(i in templates and templates[i]['kind']=='EXACT' for i in ids),'exact duty cannot be reassigned to a computational waiver',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            duties[d]=ids;return True
        if not attempt(duty,'exact duty'):duties_ok=False
    duties_ok=check('INCOMPLETE-EVIDENCE-UNIVERSE',set(duties)==set(EXACT_DUTIES),'missing required exact duty families') and duties_ok
    # Ordinal interval selectors are interpreted against this exact model. A
    # potential-left stripe includes ALL legal right endpoints under its predicate.
    coverage={};coverage_ok=True;n=len(model.tokens);m=len(model.edges);weights=potential_stripe_counts(model.tokens)
    for row in source['coverage']:
        def cover(row=row):
            exact(row,('obligation_id','nodes','structural','potential_left'))
            oid=row['obligation_id'];require(oid in templates and oid not in coverage,'duplicate/orphan coverage obligation',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            nr=normalized(row['nodes'],0,n);sr=normalized(row['structural'],1,m+1);pr=normalized(row['potential_left'],0,max(0,n-1))
            o=templates[oid]
            require(all(contains(nr,model.ids[t]) for t in o['node_ids']),'node reference not in claimed duty coverage',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            for e in o['edge_ids']:
                if e.startswith('G4-STRUCTURAL-EDGE-'):ok=contains(sr,int(e.rsplit('-',1)[1]))
                else:ok=contains(pr,int(e.split('-')[-2]))
                require(ok,'edge reference not in claimed duty coverage',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            coverage[oid]={'nodes':nr,'structural':sr,'potential_left':pr};return True
        if not attempt(cover,'coverage row'):coverage_ok=False
    coverage_ok=check('INCOMPLETE-EVIDENCE-UNIVERSE',set(coverage)==set(templates),'missing source coverage record') and coverage_ok
    nr=union([r['nodes'] for r in coverage.values()]);sr=union([r['structural'] for r in coverage.values()]);pr=union([r['potential_left'] for r in coverage.values()])
    coverage_ok=check('INCOMPLETE-EVIDENCE-UNIVERSE',nr==([[0,n]] if n else []) and sr==([[1,m+1]] if m else []) and weighted_count(pr,weights)==model.pair_count,'complete node, structural occurrence and potential set coverage') and coverage_ok
    # This concrete finite mechanism assigns each exact review family the entire
    # node/structural model and each whole-view experiment the entire graph.
    # A coverage union across different experiments cannot hide a missing view.
    for family,ids in duties.items():
        cs=[coverage[i] for i in ids if i in coverage]
        ok=union([c['nodes'] for c in cs])==([[0,n]] if n else []) and union([c['structural'] for c in cs])==([[1,m+1]] if m else [])
        coverage_ok=check('INCOMPLETE-EVIDENCE-UNIVERSE',ok,'exact duty family full model correspondence '+family) and coverage_ok
    for xid in experiments:
        cs=[coverage[oid] for oid,o in templates.items() if o['kind']=='COMPUTATIONAL' and o['experiment_id']==xid and oid in coverage]
        ok=union([c['nodes'] for c in cs])==([[0,n]] if n else []) and union([c['structural'] for c in cs])==([[1,m+1]] if m else []) and weighted_count(union([c['potential_left'] for c in cs]),weights)==model.pair_count
        coverage_ok=check('INCOMPLETE-EVIDENCE-UNIVERSE',ok,'complete full-graph interaction scope for experiment '+xid) and coverage_ok
    # Membership + normalized union prevents a duplicate stripe/count from filling a gap.
    report['coverage']={'nodes':sum(b-a for a,b in nr),'structural_occurrences':sum(b-a for a,b in sr),
                        'potential_pairs':weighted_count(pr,weights),'pair_enumeration':False}
    report['mechanical_coverage']=bool(bound and duties_ok and coverage_ok)
    class_ready=mode=='CONDITIONAL-LAB' and report['mechanical_coverage'] and all(role_ready.get(r) for r in CLASS_ROLES)
    report['classification_ready']=bool(class_ready)
    if not class_ready:failures.add('INCOMPLETE-EVIDENCE-UNIVERSE','qualified ledger classification/correspondence not established')
    if class_ready:report['qualification']='EXPLICIT-LAB-ASSUMPTIONS-ONLY' if mode=='CONDITIONAL-LAB' else 'NOT-ESTABLISHED'
    whole=source['whole_view_experiments']
    whole_ok=check('INCOMPLETE-EVIDENCE-UNIVERSE',len(whole)==len(set(whole)) and set(whole)==set(experiments),'complete whole-view experiment obligations, not edge-only privacy')
    comp_exp=[r['experiment_id'] for r in rules.values()]
    whole_ok=check('INCOMPLETE-EVIDENCE-UNIVERSE',len(comp_exp)==len(set(comp_exp)) and set(comp_exp)==set(experiments),'unique composition rule for every experiment') and whole_ok
    nv_binding=check('INVALID-ACTION-CONTEXT',source['nv_input_sha256']==digest(canonical(nv_inputs(security,model.digest))),'NV1-NV3 input binding to exact policy/world/envelope/model/qualification directories')
    # Assess NV even if there is no ARGUMENT: required experiments cannot evade NV by omission.
    for xid,x in experiments.items():
        nv=attempt(lambda x=x:provider.nonvacuity(x),'non-vacuity '+xid)
        if nv and nv['status']=='INVALID':failures.add('INVALID-ACTION-CONTEXT','ledger NV2: '+nv['reason'])
        if nv and nv['status']=='VALID' and class_ready and nv_binding and whole_ok and all(role_ready.get(r) for r in COMP_ROLES):report['nv_ready'].append(xid)
        else:failures.add('INCOMPLETE-EVIDENCE-UNIVERSE','NV support/whole-class/view qualification unavailable '+xid)
    compositions=source['compositions']
    check('INCOMPLETE-EVIDENCE-UNIVERSE',set(compositions)==set(rules),'complete source decomposition directory')
    for rid,rule in rules.items():
        def composition(rid=rid,rule=rule):
            row=compositions.get(rid);require(row is not None,'source decomposition missing',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            exact(row,('template','argument_ids','multiplicities','multiplicity_units','repetition_indices','obligation_ids','experiment_sha256','envelope_sha256'))
            require(row['template']==rule,'source rule template changed',category='INVALID-ACTION-CONTEXT')
            xid=rule['experiment_id'];x=experiments[xid]
            require(row['experiment_sha256']==digest(canonical(x)) and row['envelope_sha256']==digest(canonical(security['operating_envelope'])),'source decomposition exact experiment/envelope',category='INVALID-ACTION-CONTEXT')
            ids=row['argument_ids'];ms=row['multiplicities']
            require(isinstance(ids, list) and ids and len(set(ids))==len(ids) and isinstance(ms, list) and len(ids)==len(ms) and all(type(v) is int and v>0 for v in ms),'distinct aligned positive decomposition terms')
            units=row['multiplicity_units'];repetitions=row['repetition_indices']
            require(isinstance(units, list) and isinstance(repetitions, list) and len(units)==len(repetitions)==len(ids),'source repetition/unit alignment')
            limits={'COMPARISONS':'comparison_limit','ATTEMPTS':'attempt_limit','OCCURRENCES':'occurrence_limit'}
            for mult,unit,rs in zip(ms,units,repetitions):
                require(unit in limits,'unsupported source repetition unit',category='INCOMPLETE-EVIDENCE-UNIVERSE')
                cap=security['operating_envelope'][limits[unit]]
                require(isinstance(rs, list) and all(isinstance(r, list) and len(r)==2 and all(type(v) is int for v in r) for r in rs),'source repetition index ranges')
                require(all(0<=a<b<=cap for a,b in rs),'known repetition/envelope mismatch',category='INVALID-ACTION-CONTEXT')
                rr=normalized(rs,0,cap)
                require(sum(b-a for a,b in rr)==mult,'exact source repetition multiplicity mismatch',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            required={o['obligation_id'] for o in templates.values() if o['kind']=='COMPUTATIONAL' and o['experiment_id']==xid}
            require(required and len(row['obligation_ids'])==len(set(row['obligation_ids'])) and set(row['obligation_ids'])==required,'source whole-view obligations incomplete',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            actual=indexes['COMPOSITION'].get(rid)
            require(actual is not None and actual['argument_ids']==ids and actual['multiplicities']==ms,'exact source-qualified multiplicity/term correspondence',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            # Check all supplied arguments, not only the subset chosen by a composition row.
            require({a['argument_id'] for a in indexes['ARGUMENT'].values() if a['composition_id']==rid}==set(ids),'omitted/orphan argument in decomposition',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            covered=set()
            for aid in ids:
                a=indexes['ARGUMENT'].get(aid);require(a is not None,'decomposition argument absent',category='INCOMPLETE-EVIDENCE-UNIVERSE')
                require(a['experiment_id']==xid and a['composition_id']==rid and a['envelope_id']==policy['envelope_id'] and a['qualification_id']==rule['qualification_id'],'argument exact composition scope',category='INVALID-ACTION-CONTEXT')
                require(set(a['obligation_ids'])<=required,'wrong argument obligations',category='INCOMPLETE-EVIDENCE-UNIVERSE');covered.update(a['obligation_ids'])
            require(covered==required,'insufficient whole-view argument coverage',category='INCOMPLETE-EVIDENCE-UNIVERSE')
            return True
        ok=attempt(composition,rid)
        if ok and class_ready and whole_ok and rule['experiment_id'] in report['nv_ready'] and all(role_ready.get(r) for r in COMP_ROLES):report['ready_rules'].append(rid)
    for oid,o in templates.items():
        if class_ready and (o['kind']=='EXACT' or any(r['composition_id'] in report['ready_rules'] and r['experiment_id']==o['experiment_id'] for r in rules.values())):report['ready_obligations'].append(oid)
    return report
