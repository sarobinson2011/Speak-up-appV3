"""Formal-Lab[6] new six-field review controls; saved data/source only."""
from pathlib import Path
import argparse,ast,copy,hashlib,importlib.metadata,json,os,sys,traceback,types
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def module(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--recovered',action='store_true');a=p.parse_args();root=a.root.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
 def audit(event,args):
  if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo'):raise AssertionError('PROHIBITED:'+event)
  if event=='open' and isinstance(args[0],(str,bytes)):
   f=os.fsdecode(args[0])
   if f.startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
   if f.startswith(str(root)+'/') and len(args)>2 and type(args[2]) is int and args[2]&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC):raise AssertionError('INPUT-WRITE')
 sys.addaudithook(audit)
 def profile(frame,event,arg):
  name=frame.f_code.co_filename.rsplit('/',1)[-1]
  if event=='call' and (name in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') or name=='prospective_entry.py' and frame.f_code.co_name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status')):raise AssertionError('APPLICATION-EXECUTION')
 sys.setprofile(profile);checks=[]
 def good(label,ok=True,category='independent'):
  assert ok,label;record({'check':label,'result':'PASS','category':category})
 def record(row):
  checks.append(row)
  with (out/'progress.jsonl').open('ab') as f:f.write((json.dumps(row,sort_keys=True)+'\n').encode())
 def reject(label,fn,category='negative'):
  try:fn()
  except (ValueError,TypeError,KeyError,IndexError,FileNotFoundError) as ex:record({'check':label,'result':'REJECTED','error':{'type':type(ex).__name__,'message':str(ex)},'category':category});return
  raise AssertionError('UNEXPECTED ACCEPTANCE: '+label)
 try:
  pins={n:identity((root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
  m=module(root/'code/correspondence.py','review_extension');data=m.field_inputs(root);cat=m.field_catalogue(data);raw=(root/'results/status-field-correspondence.json').read_bytes();saved=json.loads(raw);mc=data['coverage'];e=data['ctx']['e'];trace_name='evidence/execution-trace.json';trace=json.loads(e[trace_name]);src=data['manager']
  oracle=module(Path(__file__).with_name('source_oracle.py'),'review_source_oracle')
  source=oracle.audit(src,cat);good('independent source-derived fields writes guards continuations and origins')
  (out/'source-audit.json').write_text(json.dumps(source,indent=2)+'\n')
  good('internal catalogue accepts legitimate source',m.check_catalogue(data,cat) is True)
  good('public original receipt accepts',m.validate(root,raw)['result']=='PASS')
  good('derived original receipt unchanged',m.enc(m.derive(root))==raw)
  observed,rows=m.connected_fields(data,cat)
  prior=(root/'retained/occurrence/results/occurrence-connection.json').read_bytes()
  good('SOC-closed receipt preserved exactly',data['occurrence'].enc(observed)==prior)
  expected_names=[v['name'] for v in source['fields']]
  good('six required return fields',expected_names==['phase','reason','connection_epoch','actual_admission','external_nonexecution_established','authorization_renewed'])
  calls={v['frame']:v for v in trace['events'] if v['event']=='call' and not v['resumed_generator']};returns={v['frame']:v for v in trace['events'] if v['event']=='return' and v['normal_return']}
  status_frames={fid for fid,v in calls.items() if v['function']=='ManagedAuthority.status'}
  good('saved distinct status invocation count',len(status_frames)==2 and len(calls)==18)
  def pointer(p):
   x=trace
   for k in p.split('/')[1:]:x=x[int(k)] if isinstance(x,list) else x[k]
   return x
  for view in saved['contexts']:
   oracle.audit(src,view['field_declarations']);good('source audit '+view['context'])
   oldview=next(v for v in observed['contexts'] if v['context']==view['context'])
   good('status frame membership '+view['context'],{r['frame'] for r in view['saved_status_fields']}==status_frames and len(view['saved_status_fields'])==2)
   emb=0
   for row in view['saved_status_fields']:
    oldocc=next(v for v in oldview['occurrences'] if v.get('frame')==row['frame'])
    assert row['occurrence']==oldocc['id'] and row['instance']==oldview['instance'] and row['trace_identity']==identity(e[trace_name])
    assert row['call_pointer']==f"/events/{calls[row['frame']]['seq']}"
    assert [f['declaration'] for f in row['fields']]==['managed-status-field:'+n for n in expected_names]
    for f in row['fields']:
     assert m.enc(pointer(f['return_pointer']))==m.enc(f['value'])
     if f['snapshot_pointer'] is not None:assert m.enc(pointer(f['snapshot_pointer']))==m.enc(f['value'])
     else:assert type(f['value']) is bool and f['value'] is False
    if row['recovery_embedding']:
     emb+=1;link=row['recovery_embedding'];assert calls[row['frame']]['parent']==link['parent_frame'] and calls[link['parent_frame']]['function']=='ManagedAuthority.recover'
     assert len(link['field_links'])==6
     for pair in link['field_links']:assert m.enc(pointer(pair['child_pointer']))==m.enc(pointer(pair['parent_pointer']))
   good('all six exact source/value/pointer/instance joins '+view['context'])
   good('one six-field recovery parent-child embedding '+view['context'],emb==1)
   obs=[v for v in oldview['occurrences'] if v['kind']=='explicit-observer-call']
   good('separate observer and static limits '+view['context'],len(obs)==1 and obs[0]['frame'] is None and obs[0]['parent_frame'] is None and view['observation_limits']['observer_frame'] is None and view['complete_symbolic_coverage'] is False)
  def catneg(label,change,d=None):
   value=copy.deepcopy(cat);change(value);reject(label,lambda:m.check_catalogue(data if d is None else d,value),'catalogue')
  if not a.recovered:
   for i,name in enumerate(expected_names):
    def omit(c,i=i,name=name):
     c['declarations'].pop(i);c['source']['fields'].pop(i);c['owning_return']['field_ids'].pop(i)
     for b in c['source']['recovery_embedding']:b['fields'].remove(name)
    catneg('coordinated field omission '+name,omit)
    catneg('wrong field type '+name,lambda c,i=i:c['declarations'][i].update(type='bytes'))
    catneg('altered field origin '+name,lambda c,i=i:c['declarations'][i]['value'].update(expression='self._unobserved'))
   for w in source['writes']:
    site=w['site'];d=dict(data);d['values']=copy.deepcopy(data['values']);inventory=d['values']['candidate/managed-route/producers.json']['source_inventory']['sites'];inventory[:]=[r for r in inventory if r['site']!=site]
    def omit(c,site=site):
     c['source']['writes'][:]=[w for w in c['source']['writes'] if w['site']!=site]
     for f in c['declarations']:f['origin_ids'][:]=[s for s in f['origin_ids'] if s!='status-write:'+site]
    catneg('writer omission coordinated with cached inventory '+site,omit,d)
   for psite in source['reason_arguments']:
    site=psite['site'];catneg('omit reason parameter origin '+site,lambda c,site=site:c['source'].update(parameter_inputs=[x for x in c['source']['parameter_inputs'] if x['site']!=site]))
   # Exact conditional/handler/continuation expectations came from the reviewer
   # AST traversal above, not from an expected list copied from the catalogue.
   catneg('omit conditional true arm',lambda c:next(w for w in c['source']['writes'] if w['value']['op']=='choice')['value'].pop('yes'))
   catneg('omit conditional false arm',lambda c:next(w for w in c['source']['writes'] if w['value']['op']=='choice')['value'].pop('no'))
   catneg('omit captured phase dependency',lambda c:c['source']['local_captures'].clear())
   catneg('omit all transition calls',lambda c:c['source']['transition_calls'].clear())
   for method in ('_run','_dispose','recover'):
    def wrong_handler(c,method=method):
     for r in c['source']['writes']+c['source']['parameter_inputs']:
      if r['function']==method and r['exception_bindings']:
       r['exception_bindings'].clear();r['guards'][:]=[g for g in r['guards'] if g['kind'] not in ('Try','ExceptHandler')]
    catneg('coordinated handler omission '+method,wrong_handler)
   for method in ('_dispose','close','recover'):
    catneg('normal continuation removed '+method,lambda c,method=method:[w.update(continuation=[]) for w in c['source']['writes'] if w['function']==method])
   for name in expected_names[3:]:
    for value in (0,True):
     def alter(c,name=name,value=value):
      f=next(f for f in c['declarations'] if f['name']==name);f['literal_value']=value;f['value']['value']=value
      next(f for f in c['source']['fields'] if f['name']==name)['value']['value']=value
     catneg('exact False constant '+name+' '+repr(value),alter)
   catneg('epoch declared global',lambda c:c.update(epoch_scope='one global counter across all instances'))
   catneg('invented finite reason bound',lambda c:c['reason_domain'].update(finite_bound=0))
   catneg('source coverage escalation',lambda c:c.update(complete_symbolic_coverage=True,full_model_binding=True))
   catneg('stale defining identity',lambda c:c['source']['source'].update(sha256='0'*64))
   # Coordinated cached guards and generator are checked against independent
   # retained oracle; both are separately compared with our own source audit.
   gg=data['guards']['guard_relationships'];site=next(w['site'] for w in cat['source']['writes'] if w['exception_bindings'])
   def fake_generator(raw):
    g,u=gg.derive(raw);g[site]=[];return g,u
   fake=types.SimpleNamespace(key=gg.key,derive=fake_generator);d=dict(data);d['guards']=dict(data['guards'],guard_relationships=fake);d['values']=copy.deepcopy(data['values'])
   next(v for v in d['values']['candidate/managed-route/producers.json']['source_inventory']['sites'] if v['site']==site)['guards']=[]
   reject('coordinated generator and cached guard omission',lambda:m.field_catalogue(d),'catalogue')
   d=dict(data);d['manager']=src.replace(b"'not opened'",b"'changed source'");reject('stale defining source bytes',lambda:m.field_catalogue(d),'catalogue')
   # Pure constructed cases: compare model expressions to an independent
   # evaluator of the original AST. No exception __str__ or producer is called.
   def evaluate(n,inputs):
    if isinstance(n,ast.Constant):return n.value
    if isinstance(n,ast.Name):return inputs['locals'][n.id]
    if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=='self':return inputs['state'][n.attr]
    if isinstance(n,ast.Attribute):return inputs['exceptions'][n.value.args[0].id]['type_name']
    if isinstance(n,ast.Call):return inputs['exceptions'][n.args[0].id]['text']
    if isinstance(n,ast.BinOp):return evaluate(n.left,inputs)+evaluate(n.right,inputs)
    if isinstance(n,ast.Tuple):return tuple(evaluate(x,inputs) for x in n.elts)
    if isinstance(n,ast.Compare):return evaluate(n.left,inputs) in evaluate(n.comparators[0],inputs)
    if isinstance(n,ast.IfExp):return evaluate(n.body if evaluate(n.test,inputs) else n.orelse,inputs)
    raise AssertionError(ast.dump(n))
   sample={'state':{'_phase':'READY','_reason':'previous','_epoch':7},'locals':{'phase':'OPEN_FAILED','reason':'caller text'},'exceptions':{'e':{'type_name':'SyntheticError','text':'symbolic\n\x00λ'}}}
   for row in cat['source']['writes']+cat['source']['parameter_inputs']+cat['source']['local_captures']:
    actual=mc.status_expression_value(row['value'],sample);expected=evaluate(ast.parse(row['value']['expression'],mode='eval').body,sample)
    good('constructed source-expression agreement '+row['site'],type(actual) is type(expected) and actual==expected,'constructed_not_execution')
   choice=next(w['value'] for w in cat['source']['writes'] if w['value']['op']=='choice')
   for phase in ('OPEN_FAILED','VALIDATION_FAILED','READY','CLEANUP_UNCERTAIN','arbitrary future string'):
    inp=copy.deepcopy(sample);inp['locals']['phase']=phase;expected=evaluate(ast.parse(choice['expression'],mode='eval').body,inp)
    good('constructed recovered phase branch '+phase,mc.status_expression_value(choice,inp)==expected,'constructed_not_execution')
   argument=next(r['value'] for r in cat['source']['parameter_inputs'] if r['function']=='_run')
   for text in ('','\x00λ\n','x'*16385):
    inp=copy.deepcopy(sample);inp['exceptions']['e']['text']=text
    good('constructed exact exception text length '+str(len(text)),mc.status_expression_value(argument,inp)=='SyntheticError:'+text,'constructed_not_execution')
   inp=copy.deepcopy(sample);inp['exceptions']['e']['text']=0;reject('constructed exception operand wrong type',lambda:mc.status_expression_value(argument,inp),'constructed_not_execution')
   epoch=[w for w in cat['source']['writes'] if w['target']=='_epoch'];assert len(epoch)==2 and epoch[0]['value']['value']==0 and epoch[1]['value']['value']==1
   good('instance-local initialization and increment have no lifetime cap',cat['reason_domain']['finite_bound'] is None and saved['new_field_slice_limits']['epoch_lifetime_bound'] is None)
  else:
   catneg('recovered coordinated reason omission',lambda c:(c['source'].update(parameter_inputs=[]),c['declarations'].pop(1)))
   catneg('recovered guard branch omission',lambda c:next(w for w in c['source']['writes'] if w['value']['op']=='choice')['value'].pop('no'))
   catneg('recovered boolean type substitution',lambda c:c['declarations'][3].update(type='int',literal_value=0))
  def obsneg(label,change):
   t=copy.deepcopy(trace);change(t['events']);alt=dict(e);alt[trace_name]=m.enc(t);reject(label,lambda:m.connected_fields(data,cat,alt),'saved_evidence_mutation')
  statuses=[v for v in trace['events'] if v['function']=='ManagedAuthority.status' and v['event']=='return'];rec=next(v for v in trace['events'] if v['function']=='ManagedAuthority.recover' and v['event']=='return')
  if not a.recovered:
   for status in statuses:
    for name in expected_names:
     obsneg('observed wrong type frame '+str(status['frame'])+' '+name,lambda es,name=name,seq=status['seq']:es[seq]['value'].update({name:False if name=='connection_epoch' else 0 if name in expected_names[3:] else None}))
   for name in expected_names:
    obsneg('observed omitted field '+name,lambda es,name=name:es[statuses[0]['seq']]['value'].pop(name))
    value='different' if name in ('phase','reason') else 2 if name=='connection_epoch' else True
    obsneg('recovery parent-child disagreement '+name,lambda es,name=name,value=value:es[rec['seq']]['value']['status'].update({name:value}))
  def coordinated(es):
   for v in es:
    if v.get('state') and v['state'].get('_phase')=='READY':v['state']['_reason']='coordinated false'
    if v['event']=='return' and v['function']=='ManagedAuthority.status':v['value']['reason']='coordinated false'
    if v['event']=='return' and v['function']=='ManagedAuthority.recover':v['value']['status']['reason']='coordinated false'
  obsneg('coordinated observed reason fields snapshots and embedding',coordinated)
  obsneg('recovery false constant type',lambda es:es[rec['seq']]['value']['status'].update(actual_admission=0))
  if not a.recovered:
   for i in range(2):
    v=copy.deepcopy(saved);v['contexts'][i]['field_declarations']['declarations'].pop();reject('public omitted field context '+str(i),lambda:m.validate(root,m.enc(v)),'public')
    v=copy.deepcopy(saved);v['contexts'][i]['saved_status_fields'][0]['fields'][1]['value']='invented';reject('public invented observation context '+str(i),lambda:m.validate(root,m.enc(v)),'public')
   v=copy.deepcopy(saved);v['contexts'][1]['context']=v['contexts'][0]['context'];reject('public mixed contexts',lambda:m.validate(root,m.enc(v)),'public')
   v=copy.deepcopy(saved);v['prior_occurrence_receipt']['sha256']='0'*64;reject('public stale SOC receipt',lambda:m.validate(root,m.enc(v)),'public')
   v=copy.deepcopy(saved);v['new_field_slice_limits'].update(reason_string_bound=0,epoch_lifetime_bound=0,complete_repetition_coverage=True,actual_admission=True);reject('public unsupported bounds and readiness',lambda:m.validate(root,m.enc(v)),'public')
  answer=m.validate(root,raw);answer['contexts'].reverse();answer['receipt'].clear();cat['source']['writes'].clear();saved['contexts'][0]['saved_status_fields'][0]['fields'].clear();data_output=m.derive(root);data_output['contexts'][1]['field_declarations']['source']['parameter_inputs'].clear()
  good('returned nested mutations do not alter subsequent expectations',m.enc(m.derive(root))==raw and m.validate(root,raw)['result']=='PASS')
  good('implementation identities stable',pins=={n:identity((root/'code'/n).read_bytes()) for n in pins})
  result={'result':'PASS bounded six-field correspondence','assertions':len(checks),'checks':checks,'source_audit_counts':source['counts'],'source':pins,'receipt':identity(raw),'recovered':a.recovered,'environment':{'python':sys.version,'optimization':sys.flags.optimize,'cryptography_installed':importlib.metadata.version('cryptography')},'no_new_status_observations':True,'constructed_controls_not_execution_evidence':True,'supplied_suites_executed':False,'completed_review_reruns':False,'host_session_execution':False,'database_connections':0}
  (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'assertions':len(checks),'recovered':a.recovered,'result':result['result']}))
 except BaseException:
  (out/'PARTIAL.json').write_text(json.dumps({'checks':checks,'failure':traceback.format_exc()},indent=2)+'\n');raise
 finally:sys.setprofile(None)
if __name__=='__main__':main()
