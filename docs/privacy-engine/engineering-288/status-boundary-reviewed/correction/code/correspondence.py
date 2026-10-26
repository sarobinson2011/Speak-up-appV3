"""Additive status boundary binding; no canonical allocation or full-model claim."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import types

ROOT = Path(__file__).resolve().parents[1]
ENTRY_SHA = 'a1d80c523ae220228a6b27cac42b5e57a006336e858a8e7db0a75355d6cf2ae9'
BASIS_SHA = '5d4e9d144d16c3d517985fa0bcdb98bdbb43ab832838d004ed251e52721ce017'


def enc(x):
    return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def identity(raw):
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def require(value, reason):
    if not value:raise ValueError(reason)


def inputs(root):
    root=Path(root);entry=root/'code/prospective_entry.py';raw=entry.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==ENTRY_SHA,'ENTRY-SOURCE')
    m=types.ModuleType('_status_binding_entry');m.__file__=str(entry)
    exec(compile(raw,str(entry),'exec'),m.__dict__)
    pins=m.verify_inputs(root)
    raw=(root/'provenance/basis-pins.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==BASIS_SHA,'BASIS-PINS')
    basis=json.loads(raw)
    values={}
    for name,expected in basis['members'].items():
        b=m._regular(root/'basis'/name)
        require(identity(b)==expected,'BASIS-SOURCE:'+name)
        values[name]=json.loads(b)
    return pins,basis,values


def anchor(root, path, qualified):
    raw=(root/path).read_bytes();text=raw.decode();nodes=ast.parse(text).body
    for name in qualified.split('.'):
        choices=[n for n in nodes if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name==name]
        require(len(choices)==1,'ANCHOR:'+qualified);node=choices[0];nodes=node.body
    return {'path':path,**identity(raw),'qualified':qualified,'line':node.lineno,'end_line':node.end_lineno,
            'ast_sha256':hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest(),
            'exact_source':ast.get_source_segment(text,node)}


def derive(root=ROOT):
    root=Path(root);pins,basis,values=inputs(root)
    manager='retained/candidate/compiler/live_connection.py'
    launcher='retained/launcher/code/lab_bootstrap.py'
    entry='code/prospective_entry.py'
    observed='retained/candidate/compiler/managed_observations.py'
    contexts=json.loads((root/'retained/candidate/candidate/contexts.json').read_bytes())
    contexts=[a['context'] for a in contexts['associations']]
    require(contexts==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'CONTEXTS')
    decision=json.loads((root/'contract/DECISION.json').read_bytes())
    contract=pins['contract/CONTRACT-draft-1.txt']
    require({k:decision['contract'][k] for k in ('bytes','sha256')}==contract,'CONTRACT-DECISION')
    defs=[
      ('manager-status',manager,'ManagedAuthority.status','internal status return; six exact fields; lock waiting observable; no automatic persistence'),
      ('recover-embedding',manager,'ManagedAuthority.recover','existing child status and embedded return preserved; no general client recovery route'),
      ('managed-entry',manager,'open_session','existing recovered manager and scheduler kept behind launcher; recovery return discarded'),
      ('scheduler-capability','retained/candidate/support/reference/runtime/authority.py','Scheduler.__init__','scheduler.a retains manager; launcher discards scheduler; never returned by new facade'),
      ('launcher-forwarder',launcher,'ManagedSession.status','internal wrapper forwarding only; wrapper retained by trusted owner'),
      ('launcher-diagnostic-and-evidence',launcher,'_session','status diagnostic/read and create-only exact bootstrap record; existing failure records and close preserved'),
      ('launcher-entry',launcher,'session','original environment, metadata and cooperative ownership route retained'),
      ('excluded-historical-stdout',launcher,'main','historical status print preserved but unreachable from prospective CLI; not authorized as general output'),
      ('general-entry',entry,'run','client callback receives only Client; no control argument; no callback result forwarded'),
      ('trusted-control-entry',entry,'run_controlled','separate designated owner path; explicit control callback only; authorization is external premise'),
      ('internal-diagnostic',entry,'_Control.status','exact status value to designated internal caller; no serializer/logger added'),
      ('owner-routing',entry,'_run','token-scoped owner table; original failure passed to retained launcher before generic boundary failure; revoke before cleanup'),
      ('client-state',entry,'Client.state','detached source-shaped state only; no status or manager access'),
      ('client-handle',entry,'Client.handle','exact packet/response bytes only; no scheduler or recovery capability'),
      ('dispatch-and-failure',entry,'_dispatch','data-only results; preserve original exception for existing retention; fixed general failure; no automatic raw error output'),
      ('data-detachment',entry,'_data','exact supported JSON types only; reject object capabilities and subclasses, no copy hooks'),
      ('prospective-output',entry,'main','fixed completion or uncertain-failure output only; no status/state serialization or raw traceback'),
      ('existing-observation-check',observed,'fixed_status','existing status field/constants/phase/epoch/recovery-child check; reason string type only'),
      ('existing-observation-scope',observed,'Recorder.__call__','existing tracked frame/seq/nearest-parent; launcher frames not retrospectively supplied'),
    ]
    sites=[{'id':name,'anchor':anchor(root,path,fn),'role':role} for name,path,fn,role in defs]
    prof=values['candidate/managed-route/profile.json']
    model=values['candidate/managed-route/model.json']
    producers=values['candidate/managed-route/producers.json']
    directories=values['candidate/managed-route/directory-relations.json']
    duties=values['prospective_outputs/managed-route/procedure-duty.json']
    required=['managed:entry','managed:normal','managed:restored','managed:obligation-preservation']
    for key,rows,field in [('requirements',prof['requirements'],'id'),('mappings',producers['mappings'],'requirement'),('directories',directories['managed_directories'],'requirement'),('duties',duties['duties'],'requirement')]:
        require(set(required)<=set(r[field] for r in rows),'INHERITED-JOIN:'+key)
    locals_required=['managed-local:phase','managed-local:epoch','managed-local:lock','managed-local:recovery-result']
    require(set(locals_required)<=set(r['id'] for r in model['local_declarations']),'LOCAL-DECLARATION-JOIN')
    status=anchor(root,manager,'ManagedAuthority.status')
    node=ast.parse(status['exact_source'].lstrip()).body[0]
    returned=next(n.value for n in ast.walk(node) if isinstance(n,ast.Return))
    fields=[ast.literal_eval(k) for k in returned.keys]
    binding={'format':'I164-MANAGED-STATUS-BOUNDARY-1','contract':contract,
      'adoption':pins['contract/DECISION.json'],'entry':identity((root/entry).read_bytes()),
      'basis':basis,'source_bindings':pins,'sites':sites,
      'contexts':[{'context':context,'inherited_requirements':required,'inherited_local_declarations':locals_required,
        'status_fields':fields,'site_ids':[s['id'] for s in sites],
        'relationships':[
          {'from':'manager-status','to':'recover-embedding','relation':'actual child return embedded; exact equality only where supported trace exists'},
          {'from':'manager-status','to':'launcher-diagnostic-and-evidence','relation':'own call vs retained bootstrap embedding; distinct occurrence/copy identities'},
          {'from':'launcher-forwarder','to':'internal-diagnostic','relation':'only explicit trusted control route; actual calls never merged by equal values'},
          {'from':'launcher-diagnostic-and-evidence','to':'owner-routing','relation':'wrapper retained internally; token not global call/instance identity'},
          {'from':'client-state','to':'dispatch-and-failure','relation':'data-only state boundary; no status substitution'},
          {'from':'client-handle','to':'dispatch-and-failure','relation':'exact authenticated packet/response; inherited errors remain in those exact bytes'},
          {'from':'owner-routing','to':'prospective-output','relation':'no status/callback return forwarding; coarse failure/timing remains observable'}],
        'classification':'UNKNOWN','multiplicity':None,'canonical_class':None,'ordinal':None,
        'complete_symbolic_coverage':False} for context in contexts],
      'occurrence_contract':{'retained_identity':['capture/acquisition','artifact exact bytes/hash','context','source identity','supported managed-instance binding','record location','frame/parent/seq where actually recorded'],
        'copies':'Distinct retained copy/observer relationship; never an extra invocation solely from recopying',
        'historical_launcher_frames':'UNAVAILABLE; standalone handoff/close assertions remain bounded records, not manufactured invocations',
        'fresh_test_fixtures':'Synthetic backend controls only; no target/legacy acquisition occurrence join',
        'reason_provenance':'Existing validator only checks string type; no complete provenance or bounded domain established',
        'epoch':'Per managed instance only; no global call or durable ownership identity',
        'timing':'Ordering, lock contention, completion/refusal and failure observation remain relevant; no wall-clock/fairness bound'},
      'limits':copy.deepcopy(prof['limits']),
      'unchanged_obligations':pins['retained/remaining-obligations.json'],
      'inventory_unknown_totals':4,'lifetime_unknown_totals':14,
      'full_model_binding':False,'profile_policy_adoption':False,
      'trusted_boundary':'Single-threaded trusted Python integration; no protection against private-attribute/module/frame introspection, monkeypatching, hostile callbacks, OS streams, competing owners or rollback',
      'missing_external_premises':['Caller/evidence-workflow qualification and custody','Complete operating/security experiment scope and repetition bounds','Historical handoff/close producer and launcher-frame lineage','Real storage and exclusive-owner evidence']}
    require(binding['limits']['actual_admission'] is False,'ADMISSION')
    return binding


def validate(root, saved):
    # Exact serialization contract: sorted compact JSON, UTF-8, final LF.
    require(type(saved) is bytes and saved==enc(derive(root)),'STALE-OR-ALTERED-CORRESPONDENCE')
    return {'result':'PASS','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'actual_admission':False,'full_model_binding':False}


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('operation',choices=['write','check']);p.add_argument('output');a=p.parse_args()
    if a.operation=='write':
        with open(a.output,'xb') as f:f.write(enc(derive()))
    else:print(json.dumps(validate(ROOT,Path(a.output).read_bytes()),sort_keys=True))
