"""Independent bounded config correspondence checks; saved inputs only."""
from pathlib import Path
import argparse,copy,hashlib,importlib.metadata,json,os,runpy,sys,traceback,types
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def module(p):
 m=types.ModuleType('independent_config');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def main():
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('output',type=Path);p.add_argument('--recovered',action='store_true');a=p.parse_args();root=a.root.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
 rows=[];error=None;constructed=[];calls=[];kinds={}
 def audit(event,args):
  if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+event)
  if event=='exec' and args[0].co_filename.rsplit('/',1)[-1].lower() in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('PRODUCER-EXECUTION')
  if event=='open' and isinstance(args[0],(str,bytes)):
   name=os.fsdecode(args[0]);flags=args[2] or 0
   if name.startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
   if name.startswith(str(root)+'/') and flags&(os.O_WRONLY|os.O_RDWR|os.O_TRUNC|os.O_CREAT):raise AssertionError('INPUT-WRITE')
 sys.addaudithook(audit)
 def trace(frame,event,arg):
  if event!='call':return
  f=frame.f_code.co_filename;kind=kinds.get(f)
  if kind is None:
   n=f.rsplit('/',1)[-1].lower();kind=1 if n in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') else 2 if n=='prospective_entry.py' else 0;kinds[f]=kind
  name=frame.f_code.co_name
  if kind==1 or kind==2 and name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status'):raise AssertionError('APPLICATION-EXECUTION')
  parent=frame.f_back.f_code.co_name if frame.f_back else None
  if name=='derive_binding' and parent=='_basis':calls.append({'function':'mandatory binding derive_binding','file':f,'source':identity(Path(f).read_bytes())})
  if name=='_compare_evidence' and parent=='_checked' and f==str(root/'code/correspondence.py'):
   l=frame.f_locals;path='evidence/recovery-export-0.json';expected=json.loads(l['basis']['evidence'][path])['config'];candidate=l['candidate'];value=None
   try:value=json.loads(candidate[path]).get('config')
   except (ValueError,TypeError,KeyError):pass
   calls.append({'function':'config comparison','expected':expected,'candidate':value})
 sys.settrace(trace)
 def record(label,category,result,**kw):
  r={'check':label,'category':category,'result':result,**kw};rows.append(r)
  with (out/'progress.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
 def check(label,fn,category='independent'):
  v=fn();assert v is not False,label;record(label,category,'PASS');return v
 def reject(label,fn,reason=None,category='negative'):
  try:fn()
  except (ValueError,TypeError,KeyError) as ex:
   if reason is not None:assert str(ex)==reason,(label,str(ex),reason)
   record(label,category,'REJECTED',error={'type':type(ex).__name__,'message':str(ex)});return
  raise AssertionError('UNEXPECTED-ACCEPTANCE:'+label)
 try:
  assert sys.version_info[:3]==(3,12,14) and not sys.flags.optimize
  m=module(root/'code/correspondence.py');data=m.inputs(root);cat=m.catalogue(data);c=data['coverage'];d=data['prior_data']['prior_data'];e=dict(d['ctx']['e']);source={n:identity((root/'code'/n).read_bytes()) for n in ('correspondence.py','managed_coverage.py')}
  oracle=runpy.run_path(str(Path(__file__).with_name('source_oracle.py')))
  audit_result=check('defining-source independent storage guard return and type audit',lambda:oracle['audit'](d['manager'],d['authority'],cat,d['values']['candidate/managed-route/model.json'],d['reference_module'].reference_catalogue(d),d['values']['candidate/managed-route/producers.json']['source_inventory']))
  (out/'source-audit.json').write_text(json.dumps(audit_result,indent=2)+'\n')
  claims=check('legitimate semantic correspondence',lambda:m.semantic(data,cat));bundle=check('legitimate derivation',lambda:m.derive_config(data,cat));saved=(root/'results/config-correspondence.json').read_bytes();check('derived exact saved receipt',lambda:enc(bundle)==saved)
  public=check('legitimate public validation',lambda:m.validate(root,saved));prior=json.loads((root/'retained/binding/results/binding-correspondence.json').read_bytes())
  ex=json.loads(e['evidence/recovery-export-0.json']);value=ex['config'];events=json.loads(e['evidence/execution-trace.json'])['events']
  check('two distinct ordered contexts',lambda:[r['context'] for r in claims]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
  check('missing getter execution stays unknown',lambda:all(x.get('function')!='ManagedAuthority.config' for x in events) and bundle['new_config_slice_limits']['actual_getter_count'] is None)
  premise={'phase':'READY','live_present':True,'retired_absent':True,'lock_enter_completed':True,'copy_completed':True,'lock_exit_completed':True}
  basis=m._basis(data)
  for i,row in enumerate(claims):
   name=row['context'];anchor=row['validated_configuration_anchor'];old=prior['contexts'][i];new=bundle['contexts'][i]
   check('preserve prior context '+name,lambda old=old,new=new:all(enc(new[k])==enc(v) for k,v in old.items()))
   check('configuration exact export values and bytes '+name,lambda anchor=anchor:enc(anchor['configuration'])==enc(value) and {k:anchor['record'][k] for k in ('bytes','sha256')}==identity(e[anchor['record']['artifact']]) and anchor['record']['pointer']=='/config')
   check('constructor occurrence and instance joins '+name,lambda anchor=anchor,old=old:anchor['instance']==old['hf01_evidence_binding']['instance'] and anchor['record']['acquisition']==old['binding_return_correspondence']['validated_binding_anchor']['record']['acquisition'] and anchor['recovery_occurrence']==old['hf01_evidence_binding']['occurrence']['id'] and events[int(anchor['constructor']['pointer'].split('/')[-1])]['frame']==anchor['instance']['managed_constructor_frame']==anchor['constructor']['frame'] and anchor['constructor']['parent']==anchor['recovery_parent'])
   check('no invented object or copy identity '+name,lambda row=row,anchor=anchor:row['classification']=='UNKNOWN' and row['getter_observations'] is row['actual_getter_count'] is None and all(anchor[k] is None for k in ('getter_frame','storage_assignment_frame','copy_identity_observations','underlying_connection_identity')))
   case={'kind':'CONSTRUCTED-CONDITIONAL-CONFIG','context':name,'anchor':copy.deepcopy(anchor),'premise':dict(premise),'constructor_input_at_copy':copy.deepcopy(value),'stored':copy.deepcopy(value),'returned':copy.deepcopy(value)}
   result=check('full anchored conditional copy '+name,lambda case=case:m.constructed_projection(data,cat,case),'constructed_only');constructed.append(result)
   if not a.recovered:
    bad=copy.deepcopy(case);bad['returned']=bad['constructor_input_at_copy'];reject('third live root cannot alias constructor input '+name,lambda bad=bad:m.constructed_projection(data,cat,bad),'COPY-MUTABLE-SHARING','constructed_negative')
    bad=copy.deepcopy(case);bad['anchor']['instance']['ownership_incarnation']='foreign';reject('equal values with wrong constructed instance '+name,lambda bad=bad:m.constructed_projection(data,cat,bad),'CONFIG-CASE-ANCHOR','constructed_negative')
   fields=list(value) if not a.recovered else ['session','start_nonce']
   for k in fields:
    missing=copy.deepcopy(value);missing.pop(k)
    reject('omitted typed field '+name+' '+k,lambda missing=missing:c.config_value_projection(cat,premise,value,missing),'CONFIG-VALUE-FIELDS','constructed_negative')
    bad=copy.deepcopy(value);bad[k]=True if type(value[k]) is int else 0
    reject('exact field type '+name+' '+k,lambda bad=bad:c.config_value_projection(cat,premise,value,bad),'CONFIG-VALUE-TYPE:'+k,'constructed_negative')
    if not a.recovered:
     bad=copy.deepcopy(value);bad[k]=value[k]+1 if type(value[k]) is int else value[k]+'-changed'
     reject('returned field correspondence '+name+' '+k,lambda bad=bad:c.config_value_projection(cat,premise,value,bad),'COPY-ATOM-VALUE','constructed_negative')
   # A different typed value is pure conditional algebra, never this saved instance.
   other=dict(value,start_nonce=value['start_nonce']+1)
   check('typed conditional variant not replacement anchor '+name,lambda:c.config_value_projection(cat,premise,other,copy.deepcopy(other)),'constructed_only')
   bad=copy.deepcopy(claims);bad[i]['validated_configuration_anchor']['instance']['managed_constructor_frame']+=1
   reject('semantic wrong instance '+name,lambda bad=bad:m.semantic(data,cat,bad),'CONFIG-ANCHOR-LINEAGE')
   bad=copy.deepcopy(claims);bad[i]['validated_configuration_anchor']['configuration']['start_nonce']+=1
   reject('derivation stale value '+name,lambda bad=bad:m.derive_config(data,cat,bad),'CONFIG-ANCHOR-VALUE')
   bad=copy.deepcopy(bundle);bad['contexts'][i].pop('config_return_correspondence')
   reject('public mandatory extension '+name,lambda bad=bad:m.validate(root,enc(bad)),'STALE-OR-ALTERED-CONFIG-CORRESPONDENCE','public_negative')
  for k in premise:
   if a.recovered and k not in ('phase','copy_completed'):continue
   bad=dict(premise);bad[k]='QUARANTINED' if k=='phase' else False
   reject('normal continuation '+k,lambda bad=bad:c.config_value_projection(cat,bad,value,dict(value)),category='constructed_negative')
   if not a.recovered and k!='phase':
    bad=dict(premise);bad[k]=1;reject('integer is not completion boolean '+k,lambda bad=bad:c.config_value_projection(cat,bad,value,dict(value)),category='constructed_negative')
  check('flat shallow result alone cannot identify copier',lambda:c.config_value_projection(cat,premise,value,dict(value)),'constructed_only')
  reject('same mutable config object is not copy',lambda:c.config_value_projection(cat,premise,value,value),'COPY-MUTABLE-SHARING','constructed_negative')
  # Independent concrete builtins, with recursive sharing and equal-but-distinct nodes.
  inner={'n':14,'scalars':[None,False,0,-0.0,'v']};shared=[inner];original={'first':shared,'alias':shared,'equal_but_separate':[copy.deepcopy(inner)]};original['cycle']=original
  stored=copy.deepcopy(original);returned=copy.deepcopy(stored)
  def facts(x,y):
   return x is not y and y['cycle'] is y and y['first'] is y['alias'] and y['first'] is not y['equal_but_separate'] and x['first'] is not y['first'] and x['first'][0] is not y['first'][0]
  for label,left,right in [('constructor',original,stored),('getter',stored,returned)]:
   check('independent nested identity facts '+label,lambda left=left,right=right:facts(left,right),'constructed_only')
   graph=c.copy_graph(left,right);relation=check('graph accepts source-required alias and cycle '+label,lambda graph=graph:c.validate_copy_graph(graph),'constructed_only');constructed.append({'label':label,'graph':graph,'relation':relation})
   reject('nested shallow substitution '+label,lambda left=left:c.validate_copy_graph(c.copy_graph(left,copy.copy(left))),'COPY-MUTABLE-SHARING','constructed_negative')
  # Alter alias topology while retaining equal ordinary values.
  shared=[{'x':3}];left={'a':shared,'b':shared};split={'a':copy.deepcopy(shared),'b':copy.deepcopy(shared)}
  reject('split required internal alias',lambda:c.validate_copy_graph(c.copy_graph(left,split)),'COPY-ALIAS-SPLIT','constructed_negative')
  distinct={'a':[3],'b':[3]};merged=[3]
  reject('merge distinct equal mutable nodes',lambda:c.validate_copy_graph(c.copy_graph(distinct,{'a':merged,'b':merged})),'COPY-ALIAS-MERGE','constructed_negative')
  snapshot=copy.deepcopy(original);original['first'][0]['n']=98
  check('later constructor caller mutation does not change stored values',lambda:stored['first'][0]['n']==14 and stored['alias'][0]['n']==14 and c.validate_copy_graph(c.copy_graph(snapshot,stored)),'constructed_only')
  returned['alias'][0]['n']=77
  check('returned mutation keeps internal aliases and isolates storage',lambda:returned['first'][0]['n']==77 and stored['first'][0]['n']==14,'constructed_only')
  if not a.recovered:
   for left,right,label in [(None,None,'none'),(False,False,'bool'),(19,19,'integer'),(-0.0,-0.0,'signed zero'),('x','x','string')]:check('immutable sharing '+label,lambda left=left,right=right:c.validate_copy_graph(c.copy_graph(left,right)),'constructed_only')
   for left,right,label in [([1],[True],'boolean versus integer'),([-0.0],[0.0],'signed zero'),([1],['1'],'string versus integer'),({},[],'container kind'),({'b':2,'a':1},{'a':1,'b':2},'key order'),([1,2],[2,1],'element order')]:reject('graph exact '+label,lambda left=left,right=right:c.validate_copy_graph(c.copy_graph(left,right)),category='constructed_negative')
   class DictSubclass(dict):pass
   for obj,label in [((), 'tuple'),(DictSubclass(a=1),'subclass'),(float('nan'),'nonfinite'),({1:'x'},'nonstring key')]:reject('unsupported projection domain '+label,lambda obj=obj:c.copy_graph(obj),category='constructed_negative')
   graph=c.copy_graph({'x':[]},{'x':[]});graph['nodes']['unreachable']={'kind':'list','items':[]};reject('undeclared symbolic mutable node',lambda:c.validate_copy_graph(graph),'COPY-UNREACHABLE-NODE','constructed_negative')
   graph=c.copy_graph([],[]);graph['roots'][1]['ref']='absent';reject('dangling symbolic reference',lambda:c.validate_copy_graph(graph),'COPY-DANGLING-REFERENCE','constructed_negative')
  # Source-derived coverage rejects coordinated descriptor changes before claims.
  badcat=copy.deepcopy(cat);badcat['source']['copy_call']['expression']='copy.copy(self._config)';badcat['declaration']['origin']['expression']='copy.copy(self._config)'
  reject('coordinated shallow origin semantic',lambda:m.semantic(data,badcat),'CONFIG-SOURCE-CATALOGUE')
  if not a.recovered:
   refs=d['reference_module'].reference_catalogue(d);g=d['guards'];v=d['values']
   for label,edit in [('constructor aliases input',lambda x:x['source']['constructor_storage'].update(expression='self._config=config')),('getter wrong receiver',lambda x:x['source']['origin'].update(expression='self._live.config')),('readiness omitted',lambda x:x['source']['return'].update(guards=[])),('field omitted',lambda x:x['declaration']['fields'].pop('model')),('type weakened',lambda x:x['declaration']['inherited_config']['native_template']['type']['object'].update(start_nonce='STRING'))]:
    bad=copy.deepcopy(cat);edit(bad);reject('producer rederives '+label,lambda bad=bad:c.validate_config_return(d['manager'],d['authority'],v['candidate/managed-route/model.json'],v['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'],refs,bad),'CONFIG-RETURN-CORRESPONDENCE','source_negative')
  # Change the model digest everywhere in JSON, including embedded JSON hex;
  # agreement of substituted reports must not become the expected config.
  old=value['model'];replacement=('f' if old[0]!='f' else 'e')+old[1:]
  def substitute(v):
   if type(v) is str:
    if v==old:return replacement
    try:nested=json.loads(bytes.fromhex(v))
    except (ValueError,UnicodeDecodeError):return v
    changed=substitute(nested);return enc(changed).hex() if changed!=nested else v
   if type(v) is list:return [substitute(x) for x in v]
   if type(v) is dict:return {k:substitute(x) for k,x in v.items()}
   return v
  altered=dict(e);changes={}
  for n,raw in e.items():
   if n.endswith('.json'):
    obj=json.loads(raw);changed=substitute(obj)
    if obj!=changed:altered[n]=enc(changed);changes[n]={'before':identity(raw),'after':identity(altered[n])}
  assert len(changes)>1 and json.loads(altered['evidence/recovery-export-0.json'])['config']['model']==replacement
  (out/'coordinated-substitution.json').write_text(json.dumps({'old':old,'replacement':replacement,'changed':changes},indent=2)+'\n')
  reject('coordinated changed configuration semantic',lambda:m.semantic(data,cat,evidence=altered),'CONFIG-VALIDATED-INSTANCE-VALUE')
  reject('coordinated changed configuration derivation',lambda:m.derive_config(data,cat,evidence=altered),'CONFIG-VALIDATED-INSTANCE-VALUE')
  if not a.recovered:
   candidate=dict(data);candidate['prior_data']=dict(data['prior_data']);candidate['prior_data']['prior_data']=dict(d);candidate['prior_data']['prior_data']['ctx']=dict(d['ctx']);candidate['prior_data']['prior_data']['ctx']['e']=altered
   reject('caller baseline cannot redefine expected config',lambda:m.semantic(candidate,cat),'CONFIG-VALIDATED-INSTANCE-VALUE')
  for label,edit in [('missing config',lambda x:x.pop('config')),('nonce bool',lambda x:x['config'].update(start_nonce=True)),('stale HEAD same config',lambda x:x.update(head=enc(dict(json.loads(bytes.fromhex(x['head'])),head='e'*64)).hex()))]:
   if a.recovered and label=='stale HEAD same config':continue
   rec=copy.deepcopy(ex);edit(rec);ev=dict(e);ev['evidence/recovery-export-0.json']=enc(rec)
   reject('evidence '+label,lambda ev=ev:m._compare_evidence(basis,ev),category='internal_relation')
  if not a.recovered:
   ev=dict(e);del ev['evidence/recovery-export-0.json'];reject('full missing recovery record',lambda:m.derive_config(data,cat,evidence=ev),'CONFIG-MISSING-EXPORT')
   for label,edit in [('wrong acquisition',lambda x:x['record'].update(acquisition='foreign')),('missing value',lambda x:x.pop('configuration')),('stale recovery',lambda x:x.update(recovery_occurrence='stale')),('invented observed copy',lambda x:x.update(copy_identity_observations={})),('mixed predecessor',lambda x:x['predecessor_receipt'].update(sha256='0'*64))]:
    bad=copy.deepcopy(claims);edit(bad[1]['validated_configuration_anchor']);reject('anchor '+label,lambda bad=bad:m._check_rows(basis,bad,claims),category='internal_relation')
  for label,edit in [('duplicated context',lambda b:b['contexts'].__setitem__(1,copy.deepcopy(b['contexts'][0]))),('false copy runtime and admission',lambda b:b['new_config_slice_limits'].update(actual_getter_count=1,saved_getter_execution_evidence='COMPLETE',actual_admission=True))]:
   if a.recovered and label=='duplicated context':continue
   bad=copy.deepcopy(bundle);edit(bad);reject('public '+label,lambda bad=bad:m.validate(root,enc(bad)),'STALE-OR-ALTERED-CONFIG-CORRESPONDENCE','public_negative')
  bad=copy.deepcopy(bundle)
  for row in bad['contexts']:
   anchor=row['config_return_correspondence']['validated_configuration_anchor'];anchor['configuration']['model']=replacement;anchor['instance']['binding']='f'*64
  reject('public coordinated instance and config both contexts',lambda:m.validate(root,enc(bad)),'STALE-OR-ALTERED-CONFIG-CORRESPONDENCE','public_negative')
  exact=enc(claims);other=enc(claims[1]);claims[0]['validated_configuration_anchor']['configuration'].clear();claims[0]['declaration']['copy_relation']['phases'].clear()
  check('contexts have independent nested result trees',lambda:enc(claims[1])==other)
  public['contexts'].reverse();public['receipt'].clear();bundle['contexts'].clear();catcopy=enc(cat);cat['declaration']['fields'].clear()
  check('catalogue mutation does not change new catalogue',lambda:enc(m.catalogue(data))==catcopy);cat=m.catalogue(data)
  check('pristine semantic after nested result mutations',lambda:enc(m.semantic(data,cat))==exact)
  check('pristine derivation after nested result mutations',lambda:enc(m.derive_config(data,cat))==saved)
  check('pristine public after nested result mutations',lambda:m.validate(root,saved))
  check('mandatory predecessor derive actually invoked',lambda:any(x['function']=='mandatory binding derive_binding' for x in calls))
  check('semantic comparison uses validated original config',lambda:any(x['function']=='config comparison' and x['expected']==value and x['candidate'] is not None and x['candidate'].get('model')==replacement for x in calls))
  check('candidate code and saved evidence unchanged',lambda:source=={n:identity((root/'code'/n).read_bytes()) for n in source} and e==d['ctx']['e'])
 except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};(out/'failure.txt').write_text(traceback.format_exc());raise
 finally:
  sys.settrace(None);r={'result':'PASS' if error is None else 'FAIL','assertions':len(rows),'categories':{c:sum(x['category']==c for x in rows) for c in sorted({x['category'] for x in rows})},'checks':rows,'error':error,'recovered':a.recovered,'environment':{'python':sys.version,'optimization':sys.flags.optimize,'cryptography_installed':importlib.metadata.version('cryptography')},'source':locals().get('source'),'database_connections':0,'session_operations':0,'completed_review_reruns':False,'constructed_cases_are_execution_evidence':False}
  (out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');(out/'call-observations.json').write_text(json.dumps(calls,indent=2)+'\n');(out/'constructed-cases.json').write_text(json.dumps(constructed,indent=2)+'\n')
 print('PASS',len(rows),'independent config checks')
if __name__=='__main__':main()
