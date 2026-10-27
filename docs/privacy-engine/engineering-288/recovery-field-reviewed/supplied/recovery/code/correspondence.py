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


def derive_boundary(root=ROOT):
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


# New field-level connection. The historical boundary derivation above and the
# SOC-closed occurrence adapter remain unchanged and are consumed, not replayed.
def _module(path,name):
    m=types.ModuleType(name);m.__file__=str(path)
    exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__)
    return m


def field_inputs(root):
    root=Path(root)
    old=root/'retained/occurrence'
    p=old/'code/smoke_occurrences.py'
    require(identity(p.read_bytes())=={'bytes':31687,'sha256':'5cc79baac1813284768fcc79cc1cf00d50b3febe02ea6947511ddc8b7427d05b'},'SOC-CLOSED-ADAPTER')
    occurrence=_module(p,'_soc_closed_occurrence');ctx=occurrence.load(old)
    boundary=old/'retained/correction'
    # The existing validator verifies its pinned full root, source and bases.
    pins,basis,values=inputs(boundary)
    guards={}
    for name,sha in [('guard_relationships','97942b56af75398ad562da808d746787b7226d5400e1ca0a7dbe80fb98b9ac9b'),('guard_oracle','b46c25dedf8d72151b5be405dbc3f12fdb05ac47293ee9e118171f8ece9ebb2e')]:
        p=root/'retained/compiler'/(name+'.py');require(identity(p.read_bytes())['sha256']==sha,'GUARD-SOURCE:'+name);guards[name]=_module(p,'_field_'+name)
    coverage=_module(root/'code/managed_coverage.py','_extended_managed_coverage')
    return {'root':root,'old':old,'boundary':boundary,'occurrence':occurrence,'ctx':ctx,'pins':pins,'basis':basis,'values':values,'coverage':coverage,'guards':guards,
        'manager':ctx['c']['retained/candidate/compiler/live_connection.py']}


def field_catalogue(data):
    v=data['values'];g=data['guards']
    return data['coverage'].compile_status_fields(data['manager'],v['candidate/managed-route/model.json'],v['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'])


def check_catalogue(data,submitted):
    v=data['values'];g=data['guards']
    return data['coverage'].validate_status_fields(data['manager'],v['candidate/managed-route/model.json'],v['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'],submitted)


def connected_fields(data,catalogue,evidence=None):
    """Consume existing occurrence/value/embedding checks and connect their
    saved results. This internal seam never admits unpinned replacement evidence.
    """
    check_catalogue(data,catalogue)
    old=data['occurrence'];ctx=dict(data['ctx'])
    if evidence is not None:ctx['e']=evidence
    observed=old.derive(ctx)  # includes existing fixed_status, source states and SOC fixes
    trace=json.loads(ctx['e']['evidence/execution-trace.json'])['events']
    normal={e['frame']:e for e in trace if e['event']=='return' and e['normal_return']}
    calls={e['frame']:e for e in trace if e['event']=='call' and not e['resumed_generator']}
    fields=catalogue['declarations'];rows=[]
    for frame,call in calls.items():
        if call['function']!='ManagedAuthority.status':continue
        ret=normal[frame];parent=calls[call['parent']];projection=[]
        for field in fields:
            name=field['name'];value=ret['value'][name]
            require(type(value).__name__==field['type'],'STATUS-OBSERVED-FIELD-TYPE:'+name)
            selector=field['value']
            if selector['op']=='literal':require(enc(value)==enc(selector['value']),'STATUS-OBSERVED-CONSTANT')
            else:require(enc(value)==enc(ret['state'][selector['name']]),'STATUS-OBSERVED-SELECTOR')
            projection.append({'declaration':field['id'],'value':copy.deepcopy(value),'return_pointer':f"/events/{ret['seq']}/value/{name}",
                'snapshot_pointer':None if selector['op']=='literal' else f"/events/{ret['seq']}/state/{selector['name']}",
                'source_expression':copy.deepcopy(selector),
                'origin_evidence':'Exact saved value/snapshot and supported successful source route; source assignment execution is not a separately recorded line event'})
        embedding=None
        if parent['function']=='ManagedAuthority.recover':
            par=normal[parent['frame']];key=catalogue['source']['recovery_embedding'][0]['key']
            embedding={'parent_frame':parent['frame'],'source':copy.deepcopy(catalogue['source']['recovery_embedding'][0]),
                'field_links':[{'declaration':f['id'],'child_pointer':f"/events/{ret['seq']}/value/{f['name']}",'parent_pointer':f"/events/{par['seq']}/value/{key}/{f['name']}"} for f in fields],
                'validation':'Existing fixed_status checks actual parent/child and exact whole-result equality; no fabricated frames'}
        rows.append({'frame':frame,'call_pointer':f"/events/{call['seq']}",'fields':projection,'recovery_embedding':embedding})
    return observed,rows


def derive_fields(root=ROOT):
    data=field_inputs(root);catalogue=field_catalogue(data)
    observed,rows=connected_fields(data,catalogue)
    saved=(data['old']/'results/occurrence-connection.json').read_bytes()
    require(data['occurrence'].enc(observed)==saved,'STALE-SOC-CLOSED-RECEIPT')
    boundary=derive_boundary(data['boundary'])
    # Existing source/site relationships, both contexts, duties and limits remain
    # the basis. Add only executable field correspondence and saved-field joins.
    boundary['format']='I164-MANAGED-STATUS-FIELD-CORRESPONDENCE-1'
    boundary['extension_components']={n:identity((Path(root)/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
    boundary['prior_occurrence_receipt']=identity(saved)
    trace=identity(data['ctx']['e']['evidence/execution-trace.json'])
    for context in boundary['contexts']:
        view=next(v for v in observed['contexts'] if v['context']==context['context'])
        context['field_declarations']=copy.deepcopy(catalogue)
        context['saved_status_fields']=copy.deepcopy(rows)
        for row in context['saved_status_fields']:
            occurrence=next(o for o in view['occurrences'] if o.get('frame')==row['frame'])
            row['occurrence']=occurrence['id'];row['instance']=copy.deepcopy(view['instance']);row['trace_identity']=copy.deepcopy(trace)
        context['observation_limits']={'traced_invocations':18,'separate_observer_Client_state_call':1,'observer_frame':None,'observer_parent':None,'two_contexts_are_not_extra_executions':True,
            'static_origins_not_observed':['initial and failure/quarantine/cleanup status returns','exception-derived reason values','additional recovery epochs or invocations'],
            'missing':'Sparse trace has no full lines, offsets, call arguments or live/retired snapshots; historical producer/frame gaps remain'}
    boundary['occurrence_contract']['reason_provenance']='All direct selected source assignments and guarded internal parameter origins are now bound statically. Saved successful reason values retain their exact source-snapshot checks. Exception content, unrecorded histories and finite lifetime/string bounds remain unestablished.'
    boundary['new_field_slice_limits']={'static_source_coverage_only':True,'reason_string_bound':None,'epoch_lifetime_bound':None,'multiplicity':None,'complete_repetition_coverage':False,
        'no_new_status_serialization':True,'no_automatic_logging':True,'no_policy_change':True,'all_eleven_obligations_preserved':True,'Decision_B':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False}
    return boundary


def validate_fields(root,saved):
    require(type(saved) is bytes and saved==enc(derive_fields(root)),'STALE-OR-ALTERED-FIELD-CORRESPONDENCE')
    return {'result':'PASS','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'receipt':identity(saved),'actual_admission':False,'complete_repetition_coverage':False}


# New reference slice. The previously reviewed field root and its receipt remain
# byte-for-byte retained; no historical test suite or producer is invoked.
def reference_inputs(root=ROOT):
    import os,stat
    root=Path(root);base=root/'retained/fields'
    require(stat.S_ISDIR(base.lstat().st_mode),'REFERENCE-BASE-ROOT-TYPE')
    p=base/'MANIFEST.json';require(stat.S_ISREG(p.lstat().st_mode),'REFERENCE-BASE-MANIFEST-TYPE');raw=p.read_bytes()
    require(identity(raw)=={'bytes':102850,'sha256':'30fdca495d02ad4da5883d93ec62af801d9577b20142fc0fd97b8dedb3f3aab1'},'REFERENCE-BASE-MANIFEST')
    manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'}
    directories={str(p) for n in expected for p in Path(n).parents if str(p)!='.'};seen=set();dirs=set()
    def walk(path):
        for entry in os.scandir(path):
            q=Path(entry.path);name=q.relative_to(base).as_posix();mode=entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                require(name in directories,'REFERENCE-UNDECLARED-DIRECTORY');dirs.add(name);walk(q)
            else:require(stat.S_ISREG(mode) and name in expected,'REFERENCE-UNDECLARED-OR-NONREGULAR');seen.add(name)
    walk(base);require(seen==expected and dirs==directories,'REFERENCE-BASE-MEMBERSHIP')
    for name,pin in manifest.items():require(identity((base/name).read_bytes())==pin,'REFERENCE-BASE-BYTES:'+name)
    prior=_module(base/'code/correspondence.py','_reviewed_field_correspondence')
    data=prior.field_inputs(base)
    data['reference_root']=root;data['field_root']=base;data['field_module']=prior
    data['reference_coverage']=_module(root/'code/managed_coverage.py','_reference_managed_coverage')
    data['authority']=data['ctx']['c']['retained/candidate/support/reference/runtime/authority.py']
    return data


def reference_catalogue(data):
    v=data['values'];g=data['guards']
    return data['reference_coverage'].compile_reference_transfers(data['manager'],v['candidate/managed-route/model.json'],v['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'],data['authority'])


def check_reference_catalogue(data,submitted):
    v=data['values'];g=data['guards']
    return data['reference_coverage'].validate_reference_transfers(data['manager'],v['candidate/managed-route/model.json'],v['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'],data['authority'],submitted)


def reference_path(data,case,submitted=None):
    mc=data['reference_coverage'];g=data['guards']
    if submitted is None:return mc.constructed_reference_path(data['manager'],g['guard_relationships'],g['guard_oracle'],case)
    return mc.validate_constructed_reference_path(data['manager'],g['guard_relationships'],g['guard_oracle'],case,submitted)


def derive_reference(data,catalogue,evidence=None):
    check_reference_catalogue(data,catalogue)
    ctx=dict(data['ctx'])
    if evidence is not None:ctx['e']=evidence
    # Reuse SOC-closed source/identity/completion/parent checks. No interpretation
    # of equal recorded binding dictionaries as equal runtime objects is added.
    observed=data['occurrence'].derive(ctx)
    fields=data['field_module'].derive(data['field_root'])
    saved=(data['field_root']/'results/status-field-correspondence.json').read_bytes()
    require(enc(fields)==saved,'REFERENCE-STALE-FIELD-RECEIPT')
    require(identity(saved)=={'bytes':293607,'sha256':'46d7acfacc3ef8fc06683564eaacec64e54b3559d5b9416f2575b53fb0213381'},'REFERENCE-FIELD-RECEIPT-PIN')
    trace=json.loads(ctx['e']['evidence/execution-trace.json'])['events']
    calls={e['frame']:e for e in trace if e['event']=='call' and not e['resumed_generator']}
    result=copy.deepcopy(fields);result['format']='I164-MANAGED-REFERENCE-CORRESPONDENCE-1'
    result['prior_field_components']=result.pop('extension_components')
    result['extension_components']={n:identity((data['reference_root']/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
    result['prior_field_receipt']=identity(saved)
    source=catalogue['source'];by_function={}
    for r in source['writes']+source['calls']:
        by_function.setdefault('ManagedAuthority.'+r['function'],[]).append(r.get('id','managed-reference-call:'+r['site']))
    for context in result['contexts']:
        context['reference_declarations']=copy.deepcopy(catalogue)
        view=next(v for v in observed['contexts'] if v['context']==context['context'])
        rows=[]
        for occurrence in view['occurrences']:
            frame=occurrence.get('frame');call=calls.get(frame)
            if call is None or call['function'] not in by_function:continue
            rows.append({'occurrence':occurrence['id'],'instance':copy.deepcopy(view['instance']),'frame':frame,'parent':call['parent'],
             'call_pointer':'/events/'+str(call['seq']),'trace_identity':identity(ctx['e']['evidence/execution-trace.json']),
             'source_relation_ids':copy.deepcopy(by_function[call['function']]),
             'join_meaning':'Observed invocation of a source function containing these conditional relations; not proof every relation executed',
             'observed_reference_transfers':None,'object_identity':None,'underlying_connection_identity':None,
             'missing':'Capture has no _live/_retired values or local a identity. Existing sparse completion checks remain bounded; no assignment-line or historical launcher frame is invented.'})
        context['saved_reference_scope']=rows
        context['reference_observation_limits']={'actual_reference_transfers':'UNAVAILABLE','equal_recorded_values_prove_identity':False,
         'separate_observer_Client_state_call':True,'observer_frame':None,'observer_parent':None,'new_executions':0,
         'outstanding_cleanup_obligations':'Not discharged by absence of reference snapshots or a source clear'}
    result['new_reference_slice_limits']={'source_conditional_only':True,'new_runtime_behavior':False,'complete_repetition_coverage':False,
     'multiplicity':None,'lifetime_bound':None,'reference_identity_is_not_record_equality':True,'no_new_logging_or_retention_permission':True,
     'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED',
     'SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False}
    return result


def derive_references(root=ROOT):
    data=reference_inputs(root)
    return derive_reference(data,reference_catalogue(data))


def validate_references(root,saved):
    require(type(saved) is bytes and saved==enc(derive_references(root)),'STALE-OR-ALTERED-REFERENCE-CORRESPONDENCE')
    return {'result':'PASS','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'receipt':identity(saved),'actual_admission':False,'complete_repetition_coverage':False}


# Recovery envelope slice. Historical code and receipts are retained unchanged
# in their own roots. No application/backend source is imported or executed.
def recovery_inputs(root=ROOT):
    import os,stat
    root=Path(root);base=root/'retained/references'
    require(stat.S_ISDIR(base.lstat().st_mode),'RECOVERY-BASE-ROOT-TYPE')
    p=base/'MANIFEST.json';require(stat.S_ISREG(p.lstat().st_mode),'RECOVERY-BASE-MANIFEST-TYPE');raw=p.read_bytes()
    require(identity(raw)=={'bytes':120341,'sha256':'fa6912f4b9296f2a73cb5e5a8a859bbfe94054c9b3873bec42532d71c8b08f5a'},'RECOVERY-BASE-MANIFEST')
    manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'}
    directories={str(p) for n in expected for p in Path(n).parents if str(p)!='.'};seen=set();dirs=set()
    def walk(path):
        for entry in os.scandir(path):
            q=Path(entry.path);name=q.relative_to(base).as_posix();mode=entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                require(name in directories,'RECOVERY-UNDECLARED-DIRECTORY');dirs.add(name);walk(q)
            else:require(stat.S_ISREG(mode) and name in expected,'RECOVERY-UNDECLARED-OR-NONREGULAR');seen.add(name)
    walk(base);require(seen==expected and dirs==directories,'RECOVERY-BASE-MEMBERSHIP')
    for name,pin in manifest.items():require(identity((base/name).read_bytes())==pin,'RECOVERY-BASE-BYTES:'+name)
    prior=_module(base/'code/correspondence.py','_reviewed_reference_correspondence');data=prior.reference_inputs(base)
    data.update(recovery_root=root,reference_module=prior,reviewed_reference_root=base,
        recovery_coverage=_module(root/'code/managed_coverage.py','_recovery_managed_coverage'))
    return data


def recovery_catalogue(data):
    v=data['values'];g=data['guards']
    return data['recovery_coverage'].compile_recovery_fields(data['manager'],data['authority'],v['candidate/managed-route/model.json'],v['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'])


def check_recovery_catalogue(data,submitted):
    v=data['values'];g=data['guards']
    return data['recovery_coverage'].validate_recovery_fields(data['manager'],data['authority'],v['candidate/managed-route/model.json'],v['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'],submitted)


def recovery_projection(data,catalogue,returned,validated_head,status_value):
    # This algebraic seam has explicit premises, not an evidence admission API.
    # Never let a supplied catalogue narrow its own required fields/constants.
    check_recovery_catalogue(data,catalogue)
    return data['recovery_coverage'].recovery_value_projection(catalogue,returned,validated_head,status_value)


def recovery_capture(raw):
    require(identity(raw)=={'bytes':12049,'sha256':'f75dce01a8dbc8de42c5f220ee523d90acd0315dc80fcdbbad4428d3fd1992d7'},'RECOVERY-CAPTURE-SOURCE')
    tree=ast.parse(raw);text=raw.decode();smoke=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='smoke')
    observer=next(n for n in smoke.body if isinstance(n,ast.FunctionDef) and n.name=='observer')
    normal=next(n for n in observer.body if isinstance(n,ast.If) and ast.unparse(n.test)=="event == 'return'")
    projections=[n for n in normal.body if isinstance(n,ast.If) and any(isinstance(a,ast.Assign) and any(ast.unparse(t)=="row['value']" for t in a.targets) for a in n.body)]
    require(len(projections)==1,'RECOVERY-CAPTURE-VALUE-PROJECTION');value=projections[0]
    require(isinstance(value.test,ast.Compare) and ast.unparse(value.test.left)=='name' and len(value.test.ops)==1 and isinstance(value.test.ops[0],ast.In),'RECOVERY-CAPTURE-VALUE-GUARD')
    names=ast.literal_eval(value.test.comparators[0]);require(type(names) is tuple and all(type(n) is str for n in names),'RECOVERY-CAPTURE-VALUE-NAMES')
    require([ast.unparse(n) for n in value.body]==["row['value'] = arg"],'RECOVERY-CAPTURE-VALUE-ORIGIN')
    exports=[n for n in normal.body if isinstance(n,ast.If) and any(isinstance(a,ast.Expr) and isinstance(a.value,ast.Call) and ast.unparse(a.value.func)=='EXPORTS.append' for a in n.body)]
    require(len(exports)==1,'RECOVERY-CAPTURE-EXPORT-PROJECTION');export=exports[0]
    require(ast.unparse(export.test)=="name == 'ManagedAuthority._validate' and row['normal_return']",'RECOVERY-CAPTURE-EXPORT-GUARD')
    require([ast.unparse(n) for n in export.body]==["EXPORTS.append(f.f_locals['x'])"],'RECOVERY-CAPTURE-EXPORT-ORIGIN')
    flush=next(n for n in ast.walk(smoke) if isinstance(n,ast.For) and ast.unparse(n.iter)=='enumerate(EXPORTS)')
    require(ast.unparse(flush.target)=='(i, x)' and [ast.unparse(n) for n in flush.body]==["write('recovery-export-' + str(i) + '.json', x)"],'RECOVERY-CAPTURE-EXPORT-FILE')
    def site(n):return {'line':n.lineno,'end_line':n.end_lineno,'exact_source':ast.get_source_segment(text,n)}
    return {'source':identity(raw),'value_functions':list(names),'value_projection':site(value),'export_projection':site(export),'export_file':site(flush),
        'export_local':'x','exported_function':'ManagedAuthority._validate','scalar_return_recorded':'ManagedAuthority._validate' in names,
        'meaning':'Trusted observer captures local export on normal validator completion, then writes it. This is not a separately observed validator scalar or ingest/state call.'}


def connected_recovery(data,catalogue,evidence=None):
    """Negative-control seam: source and semantic correspondence. Replacement
    evidence never becomes admitted input; public derive uses the pinned root.
    """
    check_recovery_catalogue(data,catalogue)
    ctx=dict(data['ctx'])
    if evidence is not None:ctx['e']=evidence
    e=ctx['e'];capture=recovery_capture(e['preparation/worker.py'])
    observed=data['occurrence'].derive(ctx) # exact existing head/completion/lineage and SOC checks
    events=json.loads(e['evidence/execution-trace.json'])['events']
    calls={a['frame']:a for a in events if a['event']=='call' and not a['resumed_generator']}
    normal={a['frame']:a for a in events if a['event']=='return' and a['normal_return']}
    for a in normal.values():require(('value' in a)==(a['function'] in capture['value_functions']),'RECOVERY-CAPTURE-VALUE-MEMBERSHIP')
    recover=[a for a in calls.values() if a['function']=='ManagedAuthority.recover'];require(len(recover)==1,'RECOVERY-SAVED-DOMAIN')
    call=recover[0];ret=normal[call['frame']]
    def child(fn):
        found=[a for a in calls.values() if a['function']==fn and a['parent']==call['frame']]
        require(len(found)==1,'RECOVERY-CHILD:'+fn);return found[0]
    validate_call=child('ManagedAuthority._validate');status_call=child('ManagedAuthority.status')
    validate_return=normal[validate_call['frame']];status_return=normal[status_call['frame']]
    require(call['seq']<validate_call['seq']<validate_return['seq']<status_call['seq']<status_return['seq']<ret['seq'],'RECOVERY-CHILD-ORDER')
    export_path='evidence/recovery-export-0.json';x=json.loads(e[export_path]);head_raw=bytes.fromhex(x['head']);head=json.loads(head_raw)
    selector=catalogue['source']['head_chain']['selector']
    require(enc(x['expected_head'])==enc(head[selector]),'RECOVERY-VALIDATED-STATE-HEAD')
    projections=recovery_projection(data,catalogue,ret['value'],head[selector],status_return['value'])
    rows=[]
    for projection in projections:
        d=next(a for a in catalogue['declarations'] if a['id']==projection['declaration'])
        rows.append(dict(copy.deepcopy(projection),return_pointer=f"/events/{ret['seq']}/value/{projection['name']}",
            source_origin=copy.deepcopy(d['origin']),
            head_relation=None if d['origin']['kind']=='literal' else {
                'export':{'path':export_path,**identity(e[export_path]),'expected_head_pointer':'/expected_head','raw_head_hex_pointer':'/head'},
                'decoded_head':{'identity':identity(head_raw),'selector':'/'+selector},
                'validator_frame':validate_call['frame'],'validator_normal_return_pointer':f"/events/{validate_return['seq']}",
                'validator_scalar_pointer':None,'state_or_ingest_frame':None,
                'relation':'Existing authenticated export/state correspondence plus exact source return chain and capture contract; no scalar/assignment event invented'}))
    return observed,capture,{'frame':call['frame'],'parent':call['parent'],'call_pointer':f"/events/{call['seq']}",'fields':rows,
        'status_embedding':{'child_frame':status_call['frame'],'child_pointer':f"/events/{status_return['seq']}/value",'parent_pointer':f"/events/{ret['seq']}/value/status",'validation':'Existing source/status embedding checks plus exact equality; separate actual invocation'},
        'limitations':'Only this saved normal recovery. Failure/interruption paths are source guards, not new observed executions. No observed _validate scalar, Authority.state or ingest frame.'}


def derive_recovery(data,catalogue,evidence=None):
    observed,capture,row=connected_recovery(data,catalogue,evidence)
    prior=data['reference_module'].derive(data['reviewed_reference_root']) # mandatorily retains both reviewed extensions
    saved=(data['reviewed_reference_root']/'results/reference-correspondence.json').read_bytes()
    require(enc(prior)==saved,'RECOVERY-STALE-REFERENCE-RECEIPT')
    require(identity(saved)=={'bytes':451987,'sha256':'61f93d2ade9436c0d8b6885cea7cb5bb96b84e963c98bb07d7adce37852b7c7f'},'RECOVERY-REFERENCE-RECEIPT-PIN')
    result=copy.deepcopy(prior);result['format']='I164-MANAGED-RECOVERY-FIELD-CORRESPONDENCE-1'
    result['prior_reference_components']=result.pop('extension_components');result['prior_reference_receipt']=identity(saved)
    result['extension_components']={n:identity((data['recovery_root']/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
    evidence=data['ctx']['e'] if evidence is None else evidence
    for context in result['contexts']:
        view=next(v for v in observed['contexts'] if v['context']==context['context'])
        actual=next(o for o in view['occurrences'] if o.get('frame')==row['frame'])
        context['recovery_field_declarations']=copy.deepcopy(catalogue)
        context['saved_recovery_fields']=[dict(copy.deepcopy(row),occurrence=actual['id'],instance=copy.deepcopy(view['instance']),trace_identity=identity(evidence['evidence/execution-trace.json']))]
        context['recovery_capture_contract']=copy.deepcopy(capture)
    result['new_recovery_slice_limits']={'static_source_coverage_only':True,'saved_recovery_invocations':1,'traced_invocations':18,'separate_observer_Client_state_call':1,
        'observer_frame':None,'observer_parent':None,'missing_validator_scalar':True,'missing_ingest_and_state_frames':True,'two_contexts_are_not_two_executions':True,
        'no_new_head_authentication_or_transitive_type_proof':True,'no_runtime_changes':True,'complete_repetition_coverage':False,'multiplicity':None,
        'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','SOURCE_ONLY':'UNCHANGED',
        'cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False}
    return result


def derive(root=ROOT):
    data=recovery_inputs(root)
    return derive_recovery(data,recovery_catalogue(data))


def validate(root,saved):
    require(type(saved) is bytes and saved==enc(derive(root)),'STALE-OR-ALTERED-RECOVERY-CORRESPONDENCE')
    return {'result':'PASS','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'receipt':identity(saved),'actual_admission':False,'complete_repetition_coverage':False}


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('operation',choices=['write','check']);p.add_argument('output');a=p.parse_args()
    if a.operation=='write':
        with open(a.output,'xb') as f:f.write(enc(derive()))
    else:print(json.dumps(validate(ROOT,Path(a.output).read_bytes()),sort_keys=True))
