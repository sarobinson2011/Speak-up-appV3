"""Construct canonical V4 static directories from exact acquired source data.

No result fields, final profile digest or assessment values enter these templates.
Classification is conditionally assumed only within the existing finite LAB source.
"""
from v4_ingest.records import validate_array,require

def from_source(source,model,policy):
    require(source['model_digest']==model.digest and source['policy_id']==policy['policy_id'],
            'ledger construction exact model/policy',category='INVALID-ACTION-CONTEXT')
    # Source snapshots are immutable and validators below are read-only.
    # Deepcopy would materialize lazy arrays and copy SQLite connections.
    obligations=source['obligations']
    validate_array('OBLIGATION',obligations,True)
    for o in obligations:
        model.obligation(o)
        require(o['coalition_id'] in policy['coalition_ids'] and set(o['target_ids'])<=set(policy['target_ids']),
                'constructed target/coalition references',category='INVALID-ACTION-CONTEXT')
    rules=sorted((row['template'] for row in source['compositions'].values()),key=lambda r:r['composition_id'])
    validate_array('COMPOSITION',rules,True)
    require(all(r['policy_id']==policy['policy_id'] for r in rules),'composition policy binding',category='INVALID-ACTION-CONTEXT')
    xs=[r['experiment_id'] for r in rules]
    require(len(xs)==len(set(xs)) and set(xs)==set(policy['experiment_ids']),
            'one constructed rule per required experiment',category='INCOMPLETE-EVIDENCE-UNIVERSE')
    return {'obligations':obligations,'composition_rules':{'directory_id':policy['composition_id'],'records':rules}}

def acquire(provider,ref,model,policy):
    provider.construction([ref])
    source=provider.payload(ref)
    require(source.get('format')=='CP4D-FINITE-LEDGER-SOURCE-V1','unsupported source ledger constructor',category='INCOMPLETE-EVIDENCE-UNIVERSE')
    for role in ('policy-governance','model-ledger-classification','source-producer-correspondence'):provider.role(role)
    result=from_source(source,model,policy)
    return {'result':'CONDITIONAL-STATIC-LEDGER-CONSTRUCTED','templates':result,
            'source_reference':ref,'model_digest':model.digest,
            'classification_basis':'EXPLICIT-FINITE-LAB-SOURCE-HYPOTHESES-ONLY',
            'qualification_established':False,'profile_admitted':False}
