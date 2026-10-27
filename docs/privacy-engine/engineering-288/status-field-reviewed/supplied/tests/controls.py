"""New status-field extension controls only. No previous suite is invoked."""
import argparse,copy,hashlib,json,os,sys,types
from pathlib import Path

def audit(event,args):
 if event in ('sqlite3.connect','socket.connect','socket.bind'):raise AssertionError('PROHIBITED:'+event)
 if event=='open' and isinstance(args[0],(str,bytes)) and os.fsdecode(args[0]).startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
sys.addaudithook(audit)
def profile(frame,event,arg):
 if event=='call' and frame.f_code.co_filename.rsplit('/',1)[-1] in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('APPLICATION-EXECUTION')
sys.setprofile(profile)
def module(p):
 m=types.ModuleType('_field_controls');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--write',action='store_true');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 original={n:ident((a.root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 m=module(a.root/'code/correspondence.py');rows=[];error=None
 def check(label,fn):
  fn();rows.append({'check':label,'result':'PASS'})
 def reject(fn):
  try:fn()
  except (ValueError,TypeError,KeyError) as e:return str(e)
  raise AssertionError('Unexpected acceptance')
 try:
  data=m.field_inputs(a.root);catalogue=m.field_catalogue(data);mc=data['coverage'];source=catalogue['source']
  bundle=m.derive(a.root);raw=m.enc(bundle)
  if a.write:
   with (a.root/'results/status-field-correspondence.json').open('xb') as f:f.write(raw)
  else:assert raw==(a.root/'results/status-field-correspondence.json').read_bytes()
  check('legitimate public receipt',lambda:m.validate(a.root,raw))
  check('legitimate internal catalogue',lambda:m.check_catalogue(data,catalogue))
  def core():
   assert [f['name'] for f in catalogue['declarations']]==['phase','reason','connection_epoch','actual_admission','external_nonexecution_established','authorization_renewed']
   assert [f['type'] for f in catalogue['declarations']]==['str','str','int','bool','bool','bool']
   assert catalogue['reason_domain']['finite_bound'] is None
   assert len(bundle['contexts'])==2
   for c in bundle['contexts']:
    assert len(c['saved_status_fields'])==2
    assert all(len(r['fields'])==6 for r in c['saved_status_fields'])
    assert c['observation_limits']['separate_observer_Client_state_call']==1
    assert c['observation_limits']['observer_frame'] is None
    assert sum(r['recovery_embedding'] is not None for r in c['saved_status_fields'])==1
  check('six typed fields both contexts and separate observer',core)
  def mutation(label,edit):
   c=copy.deepcopy(catalogue);edit(c);check(label,lambda:reject(lambda:m.check_catalogue(data,c)))
  for i,f in enumerate(catalogue['declarations']):
   mutation('omit field '+f['name'],lambda c,i=i:c['declarations'].pop(i))
   mutation('wrong field type '+f['name'],lambda c,i=i:c['declarations'][i].update(type='bytes'))
   mutation('alter field origin '+f['name'],lambda c,i=i:c['declarations'][i]['value'].update(expression='invented'))
  for i in (3,4,5):
   for v in (0,True,None):mutation('wrong literal '+str(i)+' '+repr(v),lambda c,i=i,v=v:(c['declarations'][i].update(literal_value=v),c['declarations'][i]['value'].update(value=v)))
  for i,w in enumerate(source['writes']):
   mutation('omit source write '+w['site'],lambda c,i=i:c['source']['writes'].pop(i))
  for i,w in enumerate(source['parameter_inputs']):
   mutation('omit reason caller '+w['site'],lambda c,i=i:c['source']['parameter_inputs'].pop(i))
   mutation('alter reason caller expression '+w['site'],lambda c,i=i:c['source']['parameter_inputs'][i]['value'].update(expression='constant'))
  for i,w in enumerate(source['writes']):
   mutation('omit guarded origin '+w['site'],lambda c,i=i:c['source']['writes'][i]['guards'].pop())
   mutation('omit continuation '+w['site'],lambda c,i=i:c['source']['writes'][i].update(continuation=[]))
  conditional=next(i for i,w in enumerate(source['writes']) if w['value']['op']=='choice')
  for side in ('yes','no'):
   mutation('omit conditional phase arm '+side,lambda c,side=side:c['source']['writes'][conditional]['value'].pop(side))
  mutation('coordinated reason catalogue omissions',lambda c:(c['declarations'].pop(1),c['source']['fields'].pop(1),c['owning_return']['field_ids'].pop(1),c['source'].update(writes=[w for w in c['source']['writes'] if w['target']!='_reason'],parameter_inputs=[])))
  mutation('stale source binding',lambda c:c['source']['source'].update(sha256='0'*64))
  mutation('epoch global interpretation',lambda c:c.update(epoch_scope='global session/call identity'))
  mutation('invented reason bound',lambda c:c['reason_domain'].update(finite_bound=1024))
  mutation('invented repetition coverage',lambda c:c.update(complete_symbolic_coverage=True))
  mutation('alter local capture',lambda c:c['source']['local_captures'][0]['value'].update(name='_reason'))
  mutation('omit recovery field link',lambda c:c['source']['recovery_embedding'][0]['fields'].pop())
  mutation('alter recovery owning key',lambda c:c['source']['recovery_embedding'][0].update(key='head'))
  mutation('omit transition call',lambda c:c['source']['transition_calls'].pop())
  mutation('alter control programme',lambda c:c['source']['control_programs'][0].update(ast='invented'))
  # Independent oracle remains grounded in source when the reusable generator
  # and the cached inventory are coordinated to omit the same guard branch.
  fake=types.SimpleNamespace(key=data['guards']['guard_relationships'].key)
  def altered(raw):
   guards,unsupported=data['guards']['guard_relationships'].derive(raw)
   site=next(k for k,v in guards.items() if any(g['kind']=='ExceptHandler' for g in v));guards[site]=[]
   return guards,unsupported
  fake.derive=altered
  check('independent source oracle rejects generator guard omission',lambda:reject(lambda:mc.status_source(data['manager'],fake,data['guards']['guard_oracle'])))
  d=dict(data);d['manager']=data['manager'].replace(b"'not opened'",b"'altered initial'")
  check('altered defining source rejected',lambda:reject(lambda:m.field_catalogue(d)))
  d=dict(data);d['values']=copy.deepcopy(data['values']);inv=d['values']['candidate/managed-route/producers.json']['source_inventory']['sites'];site=source['writes'][0]['site'];next(v for v in inv if v['site']==site)['guards']=[]
  check('coordinated cached guard cannot override defining source',lambda:reject(lambda:m.field_catalogue(d)))
  # Explicitly constructed expression evaluations: no source method is called
  # and no observation/history is asserted by these examples.
  inputs={'state':{'_phase':'READY','_reason':'previous','_epoch':7},'locals':{'reason':'constructed argument','phase':'OPEN_FAILED'},'exceptions':{'e':{'type_name':'ExampleError','text':'constructed text\n\x00\u03bb'}}}
  for i,w in enumerate(source['writes']):
   def value_check(w=w):
    value=mc.status_expression_value(w['value'],inputs)
    if w['operation']=='add':value=inputs['state'][w['target']]+value
    assert type(value).__name__==next(f['type'] for f in source['fields'] if f['value'].get('name')==w['target'])
   check('constructed origin expression '+w['site'],value_check)
  for row in source['parameter_inputs']:
   check('constructed reason call argument '+row['site'],lambda row=row: type(mc.status_expression_value(row['value'],inputs)) is str or (_ for _ in ()).throw(AssertionError()))
  for phase,expected in [('OPEN_FAILED','OPEN_FAILED'),('VALIDATION_FAILED','VALIDATION_FAILED'),('READY','QUARANTINED')]:
   inp=copy.deepcopy(inputs);inp['locals']['phase']=phase
   def choice(inp=inp,expected=expected):assert mc.status_expression_value(source['writes'][conditional]['value'],inp)==expected
   check('constructed phase branch '+phase,choice)
  for text in ('','ordinary text','\n\x00\u03bb','x'*100000):
   inp=copy.deepcopy(inputs);inp['exceptions']['e']['text']=text
   row=next(w for w in source['parameter_inputs'] if w['function']=='_run')
   def exception(inp=inp,text=text,row=row):assert mc.status_expression_value(row['value'],inp)=='ExampleError:'+text
   check('constructed exception text exact length '+str(len(text)),exception)
  inp=copy.deepcopy(inputs);inp['exceptions']['e']['text']=17
  check('constructed wrong exception operand type rejected',lambda:reject(lambda:mc.status_expression_value(row['value'],inp)))
  # Saved-evidence seams call the existing source-state/parent-child checker.
  trace='evidence/execution-trace.json';base=json.loads(data['ctx']['e'][trace]);status_returns=[e for e in base['events'] if e['event']=='return' and e['function']=='ManagedAuthority.status'];recover=next(e for e in base['events'] if e['event']=='return' and e['function']=='ManagedAuthority.recover')
  def observation(label,edit):
   t=copy.deepcopy(base);edit(t);e=dict(data['ctx']['e']);e[trace]=m.enc(t)
   check(label,lambda:reject(lambda:m.connected_fields(data,catalogue,e)))
  for field in catalogue['declarations']:
   name=field['name'];seq=status_returns[0]['seq']
   observation('saved omitted field '+name,lambda t,name=name,seq=seq:t['events'][seq]['value'].pop(name))
   observation('saved wrong field type '+name,lambda t,name=name,seq=seq:t['events'][seq]['value'].update({name:[] if field['type']!='bool' else 0}))
  observation('inconsistent recovery reason embedding',lambda t:t['events'][recover['seq']]['value']['status'].update(reason='altered'))
  def coordinated(t):
   for e in t['events']:
    if e['function'] in ('ManagedAuthority.status','ManagedAuthority.recover'):
     if e.get('state') and e['state'].get('_phase')=='READY':e['state']['_reason']='coordinated false reason'
     if e['event']=='return':
      value=e['value'] if e['function']=='ManagedAuthority.status' else e['value']['status'];value['reason']='coordinated false reason'
  observation('coordinated saved reason values and snapshots',coordinated)
  for idx in (0,1):
   b=copy.deepcopy(bundle);b['contexts'][idx]['field_declarations']['declarations'].pop()
   check('public omitted field context '+str(idx),lambda b=b:reject(lambda:m.validate(a.root,m.enc(b))))
  b=copy.deepcopy(bundle)
  for c in b['contexts']:
   c['field_declarations']['source']['parameter_inputs']=[]
   c['saved_status_fields'][0]['fields'][1]['value']='coordinated'
  check('public coordinated contexts substitution',lambda:reject(lambda:m.validate(a.root,m.enc(b))))
  b=copy.deepcopy(bundle);b['prior_occurrence_receipt']['sha256']='0'*64
  check('public stale occurrence binding',lambda:reject(lambda:m.validate(a.root,m.enc(b))))
  answer=m.validate(a.root,raw);answer['contexts'].clear();answer['receipt'].clear();bundle['contexts'][0]['field_declarations']['source']['writes'].clear();catalogue['source']['fields'].clear()
  check('returned nested mutation does not change expectations',lambda: m.enc(m.derive(a.root))==raw or (_ for _ in ()).throw(AssertionError()))
  assert original=={n:ident((a.root/'code'/n).read_bytes()) for n in original}
 except BaseException as ex:error=repr(ex);raise
 finally:
  result={'result':'PASS' if error is None else 'FAIL','passed':len(rows),'checks':rows,'error':error,'source':original,'source_after':{n:ident((a.root/'code'/n).read_bytes()) for n in original},'root':str(a.root),'python':sys.version,'optimization':sys.flags.optimize,'new_controls_only':True,'prior_suites_rerun':False,'host_session_execution':False,'database_connections':0,'synthetic_expressions_are_not_observations':True}
  (a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS',len(rows),'new field-correspondence controls')
if __name__=='__main__':main()
