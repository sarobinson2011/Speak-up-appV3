from pathlib import Path
import sys,ast,copy,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);mode=sys.argv[3];error=None
ORDER=['manager-return','session-return','control-return']
STAGES=['control-call','owner-lookup','owner-guard','session-call','manager-call','lock-enter','manager-result','lock-exit','manager-return','session-return','control-return']
try:
 monitor=guard(root);m=module(root/'code/correspondence.py');monitor(m);d=m.inputs(root);c=d['coverage'];cat=m.catalogue(d);launch,entry=m.sources(d);manager=m.inner(d)['manager'];mt=ast.parse(manager);lt=ast.parse(launch);et=ast.parse(entry)
 def method(tree,cls,name):return next(n for owner in tree.body if isinstance(owner,ast.ClassDef) and owner.name==cls for n in owner.body if isinstance(n,ast.FunctionDef) and n.name==name)
 status=method(mt,'ManagedAuthority','status');session=method(lt,'ManagedSession','status');control=method(et,'_Control','status');init=method(et,'_Control','__init__');ret=next(n for n in ast.walk(status) if isinstance(n,ast.Return));fields={ast.literal_eval(k):v for k,v in zip(ret.value.keys,ret.value.values)}
 selectors={k:('state',v.attr) if isinstance(v,ast.Attribute) else ('literal',ast.literal_eval(v)) for k,v in fields.items()}
 def expected(s):return {k:s[v] if kind=='state' else v for k,(kind,v) in selectors.items()}
 cls=next(n for n in mt.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority');assigns=[n for n in ast.walk(cls) if isinstance(n,ast.Assign)];phases=sorted({v.value for a in assigns if any(isinstance(t,ast.Attribute) and t.attr=='_phase' for t in a.targets) for v in ast.walk(a.value) if isinstance(v,ast.Constant) and type(v.value) is str});epoch_init=[ast.literal_eval(a.value) for a in assigns if any(isinstance(t,ast.Attribute) and t.attr=='_epoch' for t in a.targets)];epoch_inc=[ast.literal_eval(a.value) for a in ast.walk(cls) if isinstance(a,ast.AugAssign) and isinstance(a.target,ast.Attribute) and a.target.attr=='_epoch' and isinstance(a.op,ast.Add)]
 rec.check('manager creates six-field dictionary under lock',lambda:len(fields)==6 and isinstance(status.body[0],ast.With) and ast.unparse(status.body[0].items[0].context_expr)=='self._lock')
 rec.check('source selectors and exact three false constants',lambda:selectors=={'phase':('state','_phase'),'reason':('state','_reason'),'connection_epoch':('state','_epoch'),'actual_admission':('literal',False),'external_nonexecution_established':('literal',False),'authorization_renewed':('literal',False)})
 rec.check('manager has no READY requirement in status',lambda:not any(isinstance(n,(ast.If,ast.Try)) or isinstance(n,ast.Call) and ast.unparse(n.func)=='self._require' for n in ast.walk(status)))
 rec.check('source forwards session result directly with no args or catch',lambda:ast.unparse(session.body[0])=='return self.__managed.status()' and len(session.body)==1)
 rec.check('source control stores token and owner guard only tests None',lambda:ast.unparse(init.body[0])=='self.__token = token' and ast.unparse(control.body[0])=='owner = _OWNERS.get(self.__token)' and ast.unparse(control.body[1].test)=='owner is None' and ast.unparse(control.body[2])=='return owner.wrapper.status()')
 rec.check('no copying conversion dispatch or local handler in forwarders',lambda:not any(isinstance(n,ast.Try) or isinstance(n,ast.Name) and n.id in ('copy','deepcopy','_data','_dispatch') for fn in (session,control) for n in ast.walk(fn)))
 rec.check('general Client has no status method',lambda:not any(isinstance(n,ast.FunctionDef) and n.name=='status' for owner in et.body if isinstance(owner,ast.ClassDef) and owner.name=='Client' for n in owner.body))
 rec.check('source-written phases and epoch initial/increment derived',lambda:phases==cat['source']['source_phase_literals'] and epoch_init==[0] and epoch_inc==[1] and cat['source']['epoch_initial']==0 and cat['source']['epoch_increment']==1)
 rec.check('exact dictionary fields and ordered source hops',lambda:cat['ordered_hops']==ORDER and list(cat['declarations'][0]['type']['fields'])==list(fields) and cat['declarations'][0]['type']['fields']=={'phase':'str','reason':'str','connection_epoch':'int','actual_admission':'bool','external_nonexecution_established':'bool','authorization_renewed':'bool'})
 rec.check('pristine catalogue validates against source',lambda:c.validate_status_forward(launch,entry,m.manager_fields(d),m.inner(d)['ctx']['binding'],cat))
 # Challenge source shape while coordinating its boundary pins in memory only.
 srcchanges=[('invented-copy',b'return owner.wrapper.status()',b'return dict(owner.wrapper.status())'),('invented-data',b'return owner.wrapper.status()',b'return _data(owner.wrapper.status())'),('wrong-method',b'return owner.wrapper.status()',b'return owner.wrapper.state()'),('wrong-token',b'owner = _OWNERS.get(self.__token)',b'owner = _OWNERS.get(None)'),('READY-gate',b'if owner is None:\n            _fail()',b"if owner is None or owner.wrapper.phase != 'READY':\n            _fail()"),('owner-failure-gate',b'if owner is None:\n            _fail()',b'if owner is None or owner.failure is not None:\n            _fail()')]
 for name,a,b in srcchanges:
  changed=entry.replace(a,b);assert changed!=entry;bound=copy.deepcopy(m.inner(d)['ctx']['binding'])
  for s in bound['sites']:
   if s['anchor']['path']=='code/prospective_entry.py':s['anchor'].update(identity(changed))
  rec.reject('coordinated source/pin '+name,lambda changed=changed,bound=bound:c.compile_status_forward(launch,changed,m.manager_fields(d),bound),'SOURCE-SHAPE')
 for name,mut in [('omit-hop',lambda x:x['declarations'].pop()),('reverse-hop',lambda x:x['ordered_hops'].reverse()),('omit-field',lambda x:x['declarations'][1]['fields'].pop()),('general-client-destination',lambda x:x['destinations'].update(normal_status='general-client')),('dispatch-guard',lambda x:x['guard_semantics'].update(dispatch_path=True)),('READY-restriction',lambda x:x['guard_semantics'].update(READY_required=True))]:
  bad=copy.deepcopy(cat);mut(bad);rec.reject('source catalogue '+name,lambda bad=bad:c.validate_status_forward(launch,entry,m.manager_fields(d),m.inner(d)['ctx']['binding'],bad),'SOURCE-CORRESPONDENCE')
 rows,basis=rec.check('full current predecessor-bound rows',lambda:m._checked(d,cat));bundle=m._assemble(d,rows,basis);saved=(root/'results/status-forward-correspondence.json').read_bytes();rec.check('current exact saved receipt derives',lambda:enc(bundle)==saved)
 rec.check('all prior context fields preserved',lambda:all(all(enc(n[k])==enc(v) for k,v in p.items()) for n,p in zip(bundle['contexts'],basis['prior']['contexts'])))
 rec.check('both contexts and missing runtime/observer join stay explicit',lambda:[r['context'] for r in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and all(r['observer_join'] is None and r['runtime_forwarding_links'] is None and r['actual_status_forwarding_count'] is None and all(x['frame'] is None for x in r['conditional_links']) for r in rows))
 def make(row,tag,snapshot,owner=True,failed=False,stop=None,kind='raise',saved_basis=False):
  anchor=row['instance_anchor'];occ=row['context']+'/independent/'+tag;scope={'context':row['context'],'acquisition':anchor['record']['acquisition'],'instance':copy.deepcopy(anchor['instance']),'frontier':anchor['recovery_occurrence'],'invocation':occ};refs={r:{'scope':copy.deepcopy(scope),'symbol':occ+'/'+r+'-symbol'} for r in ['control','token','owner','session','manager','result']}
  refs.update({'control.token':copy.deepcopy(refs['token']),'owners[token]':copy.deepcopy(refs['owner']) if owner else None,'owner.wrapper':copy.deepcopy(refs['session']),'session.managed':copy.deepcopy(refs['manager']),'owner_failed':failed})
  outcomes={};normal=[]
  for s in STAGES:
   outcomes[s]=kind if s==stop else 'normal'
   if s==stop:break
   normal.append(s)
   if s=='owner-guard' and not owner:outcomes['fixed-failure']=kind if stop=='fixed-failure' else 'intended-raise';break
  if 'manager-result' not in normal:snapshot=None
  hops=[{'id':occ+'/'+h,'declaration':h,'manager_invocation':occ+'/manager-status','scope':copy.deepcopy(scope),'value':expected(snapshot),'reference':copy.deepcopy(refs['result'])} for h in ORDER if h in normal]
  mb={'kind':'unreached'} if snapshot is None else {'kind':'saved-manager-value','sample_occurrence':row['validated_manager_samples'][0]['occurrence']} if saved_basis else {'kind':'constructed-snapshot','snapshot':copy.deepcopy(snapshot)}
  return {'kind':'CONSTRUCTED-INTERNAL-STATUS-FORWARD','context':row['context'],'anchor':copy.deepcopy(anchor),'owner_present':owner,'owner_failed':failed,'manager_basis':mb,'projection':{'occurrence':occ,'scope':scope,'references':refs,'outcomes':outcomes,'manager_snapshot':copy.deepcopy(snapshot),'returned':hops}}
 cases=[]
 for idx,row in enumerate(rows):
  ctx=row['context'];snap=row['validated_manager_samples'][0]['snapshot'];case=make(row,'normal',snap,saved_basis=True);project=lambda q:m._construct_checked(basis,rows,q);out=rec.check('legitimate bound status chain '+ctx,lambda:project(case))['projection'];cases.append({'input':case,'result':out})
  rec.check('direct three hops same reference exact source fields '+ctx,lambda:[h['declaration'] for h in out['hops']]==ORDER and all(h['value']==expected(snap) and h['reference']==case['projection']['references']['result'] for h in out['hops']))
  for phase in phases:
   q=make(row,'outside-ready-'+phase,{'_phase':phase,'_reason':'arbitrary constructed reason\u0000Ω','_epoch':2**80},failed=True);v=project(q)['projection']
   rec.check('source-admitted '+phase+' diagnostics with prior failure '+ctx,lambda v=v:v['completion']=='normal-return' and v['prior_owner_failure']['present'] is True and not v['prior_owner_failure']['cleared'] and v['destinations'][0]['to']=='designated internal control caller' and not v['new_output_permission'])
  q=make(row,'second',snap,saved_basis=True);v=project(q)['projection'];rec.check('equal values distinct invocations and occurrences '+ctx,lambda:v['hops'][0]['value']==out['hops'][0]['value'] and v['hops'][0]['id']!=out['hops'][0]['id'])
  q=make(row,'missing-owner',None,owner=False);v=project(q)['projection'];rec.check('missing owner intentional fixed raise without manager invocation '+ctx,lambda:v['completion']=='intentional-fixed-raise' and v['outcome_classification']['terminal_python_exception_in_model'] is True and not v['hops'] and not v['arguments'] and v['fixed_failure']['explicit_cause'] is None)
  stages=STAGES+['fixed-failure'] if mode=='primary' else ['owner-lookup','lock-enter','manager-result','lock-exit','session-return','control-return','fixed-failure']
  for s in stages:
   for kind in ['raise','process-termination']:
    q=make(row,s+'-'+kind,snap,owner=s!='fixed-failure',stop=s,kind=kind,saved_basis=True);v=project(q)['projection'];cl=v['outcome_classification']
    rec.check('path '+s+' '+kind+' '+ctx,lambda v=v,cl=cl,kind=kind:v['completion']==('unexpected-raise' if kind=='raise' else kind) and cl['terminal_python_exception_in_model'] is (True if kind=='raise' else None) and cl['dispatch_catch_applicable'] is False and cl['status_forwarder_local_catch'] is False and cl['runtime_exception_evidence']==cl['runtime_unwind_evidence']=='UNAVAILABLE' and v['retained_error'] is None and v['cleanup_completion'] is None and not v['authorization_renewed'])
  mutations=[('omit-hop',lambda x:x['projection']['returned'].pop(1)),('reverse-hop',lambda x:x['projection']['returned'].reverse()),('stale-instance',lambda x:x['anchor']['instance'].update(binding='f'*64)),('stale-acquisition',lambda x:x['projection']['scope'].update(acquisition='other')),('stale-invocation',lambda x:x['projection']['scope'].update(invocation='other')),('mixed-context',lambda x:x.update(context=rows[1-idx]['context'])),('wrong-manager-edge',lambda x:x['projection']['references']['session.managed'].update(symbol='other')),('stale-sample',lambda x:x['manager_basis'].update(sample_occurrence='other')),('extra-dispatch-stage',lambda x:x['projection']['outcomes'].update(dispatch='normal')),('missing-stage',lambda x:x['projection']['outcomes'].pop('lock-exit'))]
  for name,mut in mutations:
   q=copy.deepcopy(case);mut(q);rec.reject('bound path '+name+' '+ctx,lambda q=q:project(q))
  for field in fields:
   q=copy.deepcopy(case);q['projection']['returned'][1]['value'].pop(field);rec.reject('missing field '+field+' '+ctx,lambda q=q:project(q))
  for f in ['actual_admission','external_nonexecution_established','authorization_renewed']:
   for value in [0,True]:
    q=copy.deepcopy(case);q['projection']['returned'][1]['value'][f]=value;rec.reject('false constant '+f+' '+str(value)+' '+ctx,lambda q=q:project(q))
  for f,bad in [('_reason',None),('_reason',[]),('_phase',True),('_epoch',True),('_epoch',1.0),('_epoch',-1)]:
   s=copy.deepcopy(snap);s[f]=bad;rec.reject('snapshot type/range '+f+' '+type(bad).__name__+' '+ctx,lambda s=s:c.status_snapshot_value(cat,s))
  q=copy.deepcopy(case);q['projection']['manager_snapshot']['_epoch']=17
  for h in q['projection']['returned']:h['value']['connection_epoch']=17
  rec.reject('coordinated snapshot/returns cannot replace selected sample '+ctx,lambda:project(q),'PREMISE:manager_snapshot')
  q=copy.deepcopy(out);q['destinations'][0]['to']='general-client';validated={k:copy.deepcopy(v) for k,v in case['projection'].items() if k!='returned'};rec.reject('unsupported general-client destination '+ctx,lambda:c.validate_status_forward_projection(cat,case['projection'],validated,q),'PROJECTION-CORRESPONDENCE')
  q=copy.deepcopy(out);q['hops'][0]['value']['reason']='changed';q['reference_bindings']['manager']['scope']['instance']['binding']='f'*64;rec.check('nested projection result mutation isolated '+ctx,lambda:enc(project(case)['projection'])==enc(out))
  q=copy.deepcopy(rows);q[idx]['validated_manager_samples'][0]['value']['connection_epoch']=888;rec.reject('semantic wrong sample value '+ctx,lambda:m._check_rows(basis,q,m._rows(basis)),'SAMPLES')
 for label,changed in [('omitted',rows[:1]),('reversed',list(reversed(rows))),('duplicated',[rows[0],rows[0]])]:rec.reject('mandatory contexts '+label,lambda changed=changed:m._check_rows(basis,changed,rows))
 q=m._rows(basis);q[0]['conditional_links'].clear();q[1]['instance_anchor']['instance']['binding']='changed';rec.check('nested rows cannot mutate future expectations',lambda:enc(m._rows(basis))==enc(rows))
 rec.check('actual predecessor derive_client_state observed',lambda:any(v['function']=='derive_client_state' for v in CALLS))
 rec.save('constructed-cases.json',cases);rec.save('source-audit.json',{'manager':identity(manager),'launcher':identity(launch),'entry':identity(entry),'selector_expressions':{k:ast.unparse(v) for k,v in fields.items()},'phase_literals':phases,'epoch_initial':epoch_init,'epoch_increment':epoch_inc,'source_status_ast':ast.dump(status,include_attributes=False),'source_control_ast':ast.dump(control,include_attributes=False),'source_session_ast':ast.dump(session,include_attributes=False),'hops':ORDER,'no_runtime_operations':True})
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode)
