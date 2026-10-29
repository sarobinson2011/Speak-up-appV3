"""Focused new status forwarding controls; no operational methods executed."""
import argparse,ast,copy,hashlib,json,runpy,sys,time,traceback,types
from pathlib import Path
def module(p):
 m=types.ModuleType('_status_controls');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--write',action='store_true');ap.add_argument('--recovered',action='store_true');a=ap.parse_args();a.root=a.root.resolve();a.output.mkdir(parents=True,exist_ok=False)
 runpy.run_path(str(a.root/'tests/guard.py'))['install'](a.root);start=time.monotonic();checks=[];cases=[];fixtures=[];error=None
 def check(name,fn):
  result=fn();assert result is not False,name;row={'check':name,'result':'PASS'};checks.append(row)
  with (a.output/'progress.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  print(len(checks),name,flush=True);return result
 def reject(fn):
  try:fn()
  except ValueError:return True
  raise AssertionError('Unexpected acceptance')
 try:
  m=module(a.root/'code/correspondence.py');d=m.inputs(a.root);cat=m.catalogue(d);c=d['coverage'];launcher,entry=m.sources(d);manager=m.inner(d)['manager']
  lt=ast.parse(launcher);et=ast.parse(entry);mt=ast.parse(manager)
  def method(tree,cls,name):return next(n for owner in tree.body if isinstance(owner,ast.ClassDef) and owner.name==cls for n in owner.body if isinstance(n,ast.FunctionDef) and n.name==name)
  session=method(lt,'ManagedSession','status');control=method(et,'_Control','status');status=method(mt,'ManagedAuthority','status')
  # Independently read defining expressions, never infer the required set from
  # the generated declarations or a saved summary.
  rs=next(n for n in ast.walk(status) if isinstance(n,ast.Return));names=[ast.literal_eval(x) for x in rs.value.keys];selectors={k:('state',v.attr) if isinstance(v,ast.Attribute) else ('literal',ast.literal_eval(v)) for k,v in zip(names,rs.value.values)}
  def source_value(snapshot):return {k:snapshot[x] if kind=='state' else x for k,(kind,x) in selectors.items()}
  phases=sorted({n.value for fn in mt.body if isinstance(fn,ast.ClassDef) and fn.name=='ManagedAuthority' for ass in ast.walk(fn) if isinstance(ass,ast.Assign) and any(isinstance(t,ast.Attribute) and t.attr=='_phase' for t in ass.targets) for n in ast.walk(ass.value) if isinstance(n,ast.Constant) and type(n.value) is str})
  order=['manager-return','session-return','control-return'];stages=['control-call','owner-lookup','owner-guard','session-call','manager-call','lock-enter','manager-result','lock-exit','manager-return','session-return','control-return']
  check('source-independent status selectors and complete hop ordering',lambda:list(cat['declarations'][0]['type']['fields'])==names and cat['ordered_hops']==order)
  check('source-independent phase assignments',lambda:cat['source']['source_phase_literals']==phases)
  check('source owner guard only tests absence',lambda:ast.unparse(control.body[1].test)=='owner is None' and not any(isinstance(n,ast.Try) for fn in (control,session) for n in ast.walk(fn)))
  check('source direct forwards without arguments',lambda:ast.unparse(session.body[0])=='return self.__managed.status()' and ast.unparse(control.body[2])=='return owner.wrapper.status()')
  check('source-controlled entry absent general-client status method',lambda:not any(isinstance(n,ast.FunctionDef) and n.name=='status' for cls in et.body if isinstance(cls,ast.ClassDef) and cls.name=='Client' for n in cls.body))
  check('fresh source validator accepts pristine catalogue',lambda:c.validate_status_forward(launcher,entry,m.manager_fields(d),m.inner(d)['ctx']['binding'],cat))
  # Coordinated source/pin changes still fail defining-shape checks.
  mutations=[('READY guard',entry.replace(b'if owner is None:\n            _fail()',b"if owner is None or owner.wrapper.phase != 'READY':\n            _fail()")),('owner-failure guard',entry.replace(b'if owner is None:\n            _fail()',b'if owner is None or owner.failure is not None:\n            _fail()')),('conversion',entry.replace(b'return owner.wrapper.status()',b'return _data(owner.wrapper.status())')),('copy',entry.replace(b'return owner.wrapper.status()',b'return dict(owner.wrapper.status())')),('wrong method',entry.replace(b'return owner.wrapper.status()',b'return owner.wrapper.state()')),('wrong token',entry.replace(b'owner = _OWNERS.get(self.__token)',b'owner = _OWNERS.get(None)')),('new catch',entry.replace(b'return owner.wrapper.status()',b'try: return owner.wrapper.status()\n        except BaseException: return None'))]
  for label,bad in mutations:
   assert bad!=entry
   boundary=copy.deepcopy(m.inner(d)['ctx']['binding']);pin={'bytes':len(bad),'sha256':hashlib.sha256(bad).hexdigest()}
   for site in boundary['sites']:
    if site['anchor']['path']=='code/prospective_entry.py':site['anchor'].update(pin)
   check('defining source rejects coordinated '+label,lambda bad=bad,boundary=boundary:reject(lambda:c.compile_status_forward(launcher,bad,m.manager_fields(d),boundary)))
  badlaunch=launcher.replace(b'def status(self):return self.__managed.status()',b'def status(self):return self.__managed.state()');assert badlaunch!=launcher
  check('defining source rejects wrapper wrong method',lambda:reject(lambda:c.compile_status_forward(badlaunch,entry,m.manager_fields(d),m.inner(d)['ctx']['binding'])))
  for label,mutate in [('omitted hop',lambda x:x['declarations'].pop()),('reordered hops',lambda x:x['ordered_hops'].reverse()),('omitted field',lambda x:x['declarations'][1]['fields'].pop()),('omitted guard',lambda x:x['source'].pop('owner_guard')),('altered origin',lambda x:x['declarations'][1]['source_origin'].update(expression='return None')),('general output',lambda x:x['destinations'].update(normal_status='stdout')),('READY assumption',lambda x:x['guard_semantics'].update(READY_required=True))]:
   bad=copy.deepcopy(cat);mutate(bad)
   check('independent expected catalogue rejects '+label,lambda bad=bad:reject(lambda:c.validate_status_forward(launcher,entry,m.manager_fields(d),m.inner(d)['ctx']['binding'],bad)))
  rows,basis=m._checked(d,cat);bundle=m._assemble(d,rows,basis);saved=m.enc(bundle)
  check('actual semantic entry validates evidence in both contexts',lambda:len(rows)==2 and [x['context'] for x in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
  for context in bundle['contexts']:
   prior=next(x for x in basis['prior']['contexts'] if x['context']==context['context']);check('every predecessor context field preserved '+context['context'],lambda:all(m.enc(context[k])==m.enc(v) for k,v in prior.items()))
  def make(row,label,snapshot=None,fail=None,kind='raise',owner_present=True,owner_failed=False,use_saved=False):
   anchor=row['instance_anchor'];inv=row['context']+':CONSTRUCTED:'+label;scope=m.invocation_scope(anchor,inv);refs=m.reference_premises(scope,owner_present,owner_failed);outcomes={};reached=[]
   for s in stages:
    outcomes[s]=kind if s==fail else 'normal'
    if s==fail:break
    reached.append(s)
    if s=='owner-guard' and not owner_present:outcomes['fixed-failure']=kind if fail=='fixed-failure' else 'intended-raise';break
   if 'manager-result' not in reached:snapshot=None
   returned=[]
   if snapshot is not None:
    for n in order:
     if n in reached:returned.append({'id':inv+'/'+n,'declaration':n,'manager_invocation':inv+'/manager-status','scope':copy.deepcopy(scope),'value':source_value(snapshot),'reference':copy.deepcopy(refs['result'])})
   mb={'kind':'unreached'} if snapshot is None else {'kind':'saved-manager-value','sample_occurrence':row['validated_manager_samples'][0]['occurrence']} if use_saved else {'kind':'constructed-snapshot','snapshot':copy.deepcopy(snapshot)}
   return {'kind':'CONSTRUCTED-INTERNAL-STATUS-FORWARD','context':row['context'],'anchor':copy.deepcopy(anchor),'owner_present':owner_present,'owner_failed':owner_failed,'manager_basis':mb,'projection':{'occurrence':inv,'scope':scope,'references':refs,'outcomes':outcomes,'manager_snapshot':copy.deepcopy(snapshot),'returned':returned}}
  for row in rows:
   ctx=row['context'];sample=row['validated_manager_samples'][0];snapshot=sample['snapshot']
   normal=make(row,'saved-normal',snapshot,use_saved=True);fixtures.append(copy.deepcopy(normal))
   project=lambda x:m._construct_checked(basis,rows,x)
   result=check('saved-value conditional chain '+ctx,lambda:project(normal));cases.append({'case':copy.deepcopy(normal),'result':copy.deepcopy(result)})
   check('exact value direct reference forwarding '+ctx,lambda:len(result['projection']['hops'])==3 and all(h['value']==sample['value'] and h['reference']==normal['projection']['references']['result'] for h in result['projection']['hops']))
   check('observer and absent runtime frames remain unjoined '+ctx,lambda:row['observer_join'] is None and row['runtime_forwarding_links'] is None and all(x['frame'] is None for x in row['conditional_links']))
   for phase in phases:
    snap={'_phase':phase,'_reason':'conditional \u03bb reason / not historical evidence','_epoch':17};case=make(row,'phase-'+phase,snap,owner_failed=True)
    got=check('source phase '+phase+' with prior failure '+ctx,lambda case=case:project(case));cases.append({'case':case,'result':got})
    check('no READY/failure guard or new output '+phase+' '+ctx,lambda got=got:got['projection']['completion']=='normal-return' and got['projection']['prior_owner_failure']['present'] and not got['projection']['new_output_permission'])
   for val in (0,1,101):
    case=make(row,'epoch-'+str(val),{'_phase':'CLOSED','_reason':'x'*70001,'_epoch':val})
    check('unbounded reason and instance-local epoch '+str(val)+' '+ctx,lambda case=case:project(case)['projection']['completion']=='normal-return')
   missing=make(row,'owner-absent',owner_present=False);got=check('source missing owner fixed failure '+ctx,lambda:project(missing))
   check('fixed raise distinct from absence of exception '+ctx,lambda:got['projection']['completion']=='intentional-fixed-raise' and got['projection']['outcome_classification']['terminal_python_exception_in_model'] is True and not got['projection']['hops'])
   for stage in stages+['fixed-failure']:
    for kind in ('raise','process-termination'):
     case=make(row,stage+'-'+kind,snapshot,fail=stage,kind=kind,owner_present=stage!='fixed-failure',use_saved=True)
     got=check('conditional '+stage+' '+kind+' '+ctx,lambda case=case:project(case));cases.append({'case':case,'result':got})
     if kind=='process-termination':
      check('termination supplies no exception/retention/cleanup '+stage+' '+ctx,lambda got=got:got['projection']['outcome_classification']['terminal_python_exception_in_model'] is None and got['projection']['retained_error'] is None and got['projection']['cleanup_completion'] is None and not got['projection']['authorization_renewed'])
   def rejectcase(label,mutate):
    bad=copy.deepcopy(normal);mutate(bad);check(label+' '+ctx,lambda:reject(lambda:project(bad)))
   rejectcase('omitted return hop',lambda x:x['projection']['returned'].pop(1))
   rejectcase('reordered return hops',lambda x:x['projection']['returned'].reverse())
   rejectcase('wrong return container type',lambda x:x['projection']['returned'][1].update(value=[]))
   for name in names:
    rejectcase('omitted field '+name,lambda x,name=name:x['projection']['returned'][1]['value'].pop(name))
    val='altered' if name in ('phase','reason') else True if name=='connection_epoch' else 0
    rejectcase('altered type/value '+name,lambda x,name=name,val=val:x['projection']['returned'][1]['value'].__setitem__(name,val))
   rejectcase('coordinated all-hop reason substitution',lambda x:[h['value'].__setitem__('reason','substituted') for h in x['projection']['returned']])
   rejectcase('coordinated snapshot plus all returns',lambda x:(x['projection']['manager_snapshot'].__setitem__('_epoch',17),[h['value'].__setitem__('connection_epoch',17) for h in x['projection']['returned']]))
   rejectcase('wrong-instance anchor',lambda x:x['anchor']['instance'].__setitem__('binding','f'*64))
   rejectcase('stale acquisition scope',lambda x:x['projection']['scope'].__setitem__('acquisition','other-acquisition'))
   rejectcase('wrong manager reference edge',lambda x:x['projection']['references']['session.managed'].__setitem__('symbol','wrong-instance'))
   rejectcase('coordinated result-reference substitution',lambda x:(x['projection']['references']['result'].__setitem__('symbol','different'),[h['reference'].__setitem__('symbol','different') for h in x['projection']['returned']]))
   rejectcase('stale saved manager occurrence',lambda x:x['manager_basis'].__setitem__('sample_occurrence','absent'))
   rejectcase('unreached extra stage',lambda x:x['projection']['outcomes'].__setitem__('dispatch','normal'))
   rejectcase('wrong phase snapshot',lambda x:(x['manager_basis'].update(kind='constructed-snapshot',snapshot={'_phase':'ADMITTED','_reason':'','_epoch':0}),x['manager_basis'].pop('sample_occurrence')))
   rejectcase('negative epoch snapshot',lambda x:(x['manager_basis'].update(kind='constructed-snapshot',snapshot={'_phase':'CLOSED','_reason':'','_epoch':-1}),x['manager_basis'].pop('sample_occurrence')))
   for field,value in [('destinations',[{'kind':'status-reference','to':'general-client'}]),('runtime_observation',True),('physical_object_identity_observed',True),('cleanup_completion',True)]:
    bad=copy.deepcopy(result['projection']);bad[field]=value;validated={k:copy.deepcopy(v) for k,v in normal['projection'].items() if k!='returned'}
    check('reject unsupported derived claim '+field+' '+ctx,lambda bad=bad,validated=validated:reject(lambda:c.validate_status_forward_projection(cat,normal['projection'],validated,bad)))
   changed=copy.deepcopy(rows);changed[0 if ctx=='SYMBOLIC-U-ONE' else 1]['validated_manager_samples'][0]['value']['reason']='mixed'
   check('semantic row checker rejects mixed sample '+ctx,lambda changed=changed:reject(lambda:m._check_rows(basis,changed,rows)))
  # Catalogue mutation cannot redefine independently sourced expectations.
  badcat=copy.deepcopy(cat);badcat['manager_fields']['declarations'].pop();badcat['declarations'][0]['fields'].pop()
  check('coordinated field/catalogue omission',lambda:reject(lambda:c.validate_status_forward(launcher,entry,m.manager_fields(d),m.inner(d)['ctx']['binding'],badcat)))
  basis_before=m.enc({'prior':basis['prior'],'catalogue':basis['catalogue'],'rows':rows});mutable=m._assemble(d,rows,basis);mutable['contexts'].reverse();mutable['contexts'][0]['internal_status_return_correspondence']['declaration']['manager_fields']['declarations'].clear();mutable['contexts'].clear()
  check('nested returned bundle mutations leave expectations isolated',lambda:m.enc({'prior':basis['prior'],'catalogue':basis['catalogue'],'rows':rows})==basis_before and m.enc(m._assemble(d,rows,basis))==saved)
  mutable=m._rows(basis);mutable[1]['validated_manager_samples'][0]['snapshot']['_epoch']=17;mutable[0]['conditional_links'].clear()
  check('nested returned rows leave expectations isolated',lambda:m.enc(m._rows(basis))==m.enc(rows))
  for bad in ([],rows[:1],list(reversed(rows))):check('both contexts mandatory '+str(len(bad))+' '+str(bad==list(reversed(rows))),lambda bad=bad:reject(lambda:m._check_rows(basis,bad,rows)))
  old=json.loads(saved);old['contexts'][0].pop('internal_status_return_correspondence')
  check('public validation rejects missing mandatory relation',lambda:reject(lambda:m.validate(a.root,m.enc(old))))
  if a.write:
   p=a.root/'results/status-forward-correspondence.json';assert not p.exists();p.write_bytes(saved)
   p=a.root/'fixtures/normal-cases.json';assert not p.exists();p.write_text(json.dumps({'cases':fixtures},indent=2)+'\n')
  else:check('recovered saved exact receipt',lambda:(a.root/'results/status-forward-correspondence.json').read_bytes()==saved)
  check('source/field producer predecessor inputs unchanged',lambda:m.enc(cat)==m.enc(m.catalogue(d)))
 except BaseException as e:error={'exception':repr(e),'traceback':traceback.format_exc()};raise
 finally:
  result={'result':'FAIL' if error else 'PASS','checks':len(checks),'rows':checks,'error':error,'seconds':time.monotonic()-start,'recovered':a.recovered,'constructed_cases_not_runtime':True,'previous_suites_rerun':False,'database_connections':0,'session_operations':0,'requests':0}
  (a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(a.output/'cases.json').write_text(json.dumps(cases,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
if __name__=='__main__':main()
