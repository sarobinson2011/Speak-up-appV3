"""New recovery-field controls only. Saved evidence and pure constructed values.
No runtime, old suite, host smoke, database or acquisition is executed.
"""
import argparse,ast,copy,hashlib,json,os,sys,types
from pathlib import Path

def audit(event,args):
 if event in ('sqlite3.connect','socket.connect','socket.bind'):raise AssertionError('PROHIBITED:'+event)
 if event=='open' and isinstance(args[0],(str,bytes)) and os.fsdecode(args[0]).startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
sys.addaudithook(audit)
def profile(frame,event,arg):
 if event=='call' and frame.f_code.co_filename.rsplit('/',1)[-1] in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('APPLICATION-EXECUTION')
sys.setprofile(profile)
def module(p):
 m=types.ModuleType('_recovery_controls');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--write',action='store_true');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 rows=[];cases=[];error=None;original={n:identity((a.root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 def check(label,f):
  v=f();assert v is not False,label;rows.append({'check':label,'result':'PASS'});return v
 def reject(f):
  try:f()
  except (ValueError,TypeError,KeyError) as e:return str(e)
  raise AssertionError('Unexpected acceptance')
 try:
  m=module(a.root/'code/correspondence.py');data=m.recovery_inputs(a.root);cat=m.recovery_catalogue(data);mc=data['recovery_coverage'];g=data['guards'];source=cat['source']
  check('legitimate source catalogue',lambda:m.check_recovery_catalogue(data,cat))
  observed,capture,row=check('legitimate internal semantic connection',lambda:m.connected_recovery(data,cat))
  bundle=m.derive_recovery(data,cat);saved=m.enc(bundle)
  if a.write:
   with (a.root/'results/recovery-field-correspondence.json').open('xb') as f:f.write(saved)
  else:assert saved==(a.root/'results/recovery-field-correspondence.json').read_bytes()
  check('legitimate public saved receipt',lambda:m.validate(a.root,saved))
  # Independent AST selection, no expected membership derived from catalogue.
  tree=ast.parse(data['manager']);cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority');methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
  ret=next(n for n in ast.walk(methods['recover']) if isinstance(n,ast.Return));fields={ast.literal_eval(k):v for k,v in zip(ret.value.keys,ret.value.values)}
  selected={k:v for k,v in fields.items() if not isinstance(v,ast.Call)}
  check('independent return-field membership',lambda:set(selected)=={d['name'] for d in cat['declarations']}=={'head','recovery_only','new_attempt_authorized'})
  for name,node in selected.items():
   decl=next(d for d in cat['declarations'] if d['name']==name)
   check('independent source expression '+name,lambda node=node,decl=decl:decl['origin']['origin']['expression']==ast.get_source_segment(data['manager'].decode(),node))
   if isinstance(node,ast.Constant):
    check('independent literal type/value '+name,lambda node=node,decl=decl:type(node.value).__name__==decl['type'] and type(node.value) is bool and node.value is decl['origin']['value'])
   else:
    assignment=next(n for n in ast.walk(methods['recover']) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==node.id for t in n.targets))
    check('independent validator assignment',lambda:ast.unparse(assignment.value)=='self._validate(a)' and decl['origin']['assignment']['expression']==ast.get_source_segment(data['manager'].decode(),assignment))
  check('both contexts each retain three fields and unique occurrence identities',lambda:len(bundle['contexts'])==2 and all(len(v['recovery_field_declarations']['declarations'])==3 for v in bundle['contexts']) and bundle['contexts'][0]['saved_recovery_fields'][0]['occurrence']!=bundle['contexts'][1]['saved_recovery_fields'][0]['occurrence'])
  check('both reviewed extensions remain connected',lambda:all(v['field_declarations'] and v['reference_declarations'] for v in bundle['contexts']))
  check('missing scalar is explicit',lambda:capture['scalar_return_recorded'] is False and row['fields'][0]['head_relation']['validator_scalar_pointer'] is None)
  check('observer remains separate and UNKNOWN totals unchanged',lambda:bundle['inventory_unknown_totals']==4 and bundle['lifetime_unknown_totals']==14 and bundle['new_recovery_slice_limits']['observer_frame'] is None)
  def mutation(label,edit):
   c=copy.deepcopy(cat);edit(c);check(label,lambda:reject(lambda:m.check_recovery_catalogue(data,c)))
  for i,d in enumerate(cat['declarations']):
   name=d['name']
   mutation('omit declaration '+name,lambda c,i=i:c['declarations'].pop(i))
   mutation('omit source field '+name,lambda c,i=i:c['source']['fields'].pop(i))
   mutation('wrong type '+name,lambda c,i=i:c['declarations'][i].update(type='int'))
   mutation('alter origin '+name,lambda c,i=i:c['declarations'][i]['origin']['origin'].update(expression='invented'))
   mutation('omit guard '+name,lambda c,i=i:c['declarations'][i]['origin']['origin'].update(guards=[]))
   mutation('omit normal continuation '+name,lambda c,i=i:c['declarations'][i]['origin']['origin'].update(continuation=[]))
   mutation('coordinate source and declaration deletion '+name,lambda c,i=i:(c['source']['fields'].pop(i),c['declarations'].pop(i)))
  for i,d in enumerate(cat['declarations']):
   if d['origin']['kind']=='literal':mutation('wrong literal '+d['name'],lambda c,i=i:c['declarations'][i]['origin'].update(value=not c['declarations'][i]['origin']['value']))
  for key in source['head_chain']:
   mutation('alter head-chain origin '+key,lambda c,key=key:c['source']['head_chain'].update({key:None}))
  for i,program in enumerate(source['programs']):mutation('omit control programme '+program['owner'],lambda c,i=i:c['source']['programs'].pop(i))
  mutation('wrong head type basis',lambda c:c['declarations'][0]['inherited_head']['native_template'].update(type='OBJECT'))
  mutation('stale source identity',lambda c:c['source']['source'].update(sha256='0'*64))
  mutation('status embedding omission',lambda c:c['source'].update(status_embedding=[]))
  mutation('false repetition completion',lambda c:c['limits'].update(complete_repetition_coverage=True))
  fake=types.SimpleNamespace(key=g['guard_relationships'].key)
  def altered(raw):
   values,bad=g['guard_relationships'].derive(raw);values[source['return']['site']]=[];return values,bad
  fake.derive=altered
  check('independent oracle rejects coordinated guard omission',lambda:reject(lambda:mc.recovery_source(data['manager'],data['authority'],fake,g['guard_oracle'])))
  for label,key,old,new in [('manager source','manager',b"'recovery_only':True",b"'recovery_only':False"),('authority source','authority',b"SELECT raw FROM head WHERE id=1",b"SELECT raw FROM head WHERE id=2")]:
   d=dict(data);d[key]=data[key].replace(old,new);assert d[key]!=data[key];check('changed defining '+label,lambda d=d:reject(lambda:m.recovery_catalogue(d)))
  d=dict(data);d['values']=copy.deepcopy(data['values']);head=next(r for r in d['values']['candidate/managed-route/model.json']['existing_declarations'] if r.get('template_id')=='HEAD:/head');head['native_template']['type']='OBJECT'
  check('coordinated inherited HEAD substitution rejected',lambda:reject(lambda:m.recovery_catalogue(d)))
  d=dict(data);d['values']=copy.deepcopy(data['values']);sites=d['values']['candidate/managed-route/producers.json']['source_inventory']['sites'];sites[:]=[r for r in sites if r['site']!=source['return']['site']]
  check('missing inherited producer return site',lambda:reject(lambda:m.recovery_catalogue(d)))
  # Type/value projection algebra with explicit premises; these are not
  # authenticated states, forged evidence or claimed new runtime observations.
  trace=json.loads(data['ctx']['e']['evidence/execution-trace.json']);ret_event=next(e for e in trace['events'] if e['event']=='return' and e['function']=='ManagedAuthority.recover');actual=ret_event['value'];status=actual['status']
  for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
   for value in ('0'*64,'a'*64,'f'*64):
    value_object=copy.deepcopy(actual);value_object['head']=value
    projected=check('constructed projection '+context+' '+value[0],lambda value_object=value_object,value=value:m.recovery_projection(data,cat,value_object,value,status))
    cases.append({'kind':'CONSTRUCTED-VALUE-PROJECTION','context':context,'premises':{'validated_head_value':value,'status':status},'returned':value_object,'result':projected,'actual_observation':False,'head_authentication_proof':False})
  for name,wrong in [('head',None),('head',17),('head',b'0'*64),('recovery_only',1),('recovery_only',False),('new_attempt_authorized',0),('new_attempt_authorized',True)]:
   value_object=copy.deepcopy(actual);value_object[name]=wrong
   check('projection wrong type/constant '+name+' '+repr(wrong),lambda value_object=value_object:reject(lambda:m.recovery_projection(data,cat,value_object,actual['head'],status)))
  for name in fields:
   v=copy.deepcopy(actual);del v[name];check('projection omission '+name,lambda v=v:reject(lambda:m.recovery_projection(data,cat,v,actual['head'],status)))
  v=copy.deepcopy(actual);v['head']='a'*64;check('projection stale head',lambda:reject(lambda:m.recovery_projection(data,cat,v,actual['head'],status)))
  v=copy.deepcopy(actual);v['status']['connection_epoch']=17;check('projection inconsistent embedding',lambda:reject(lambda:m.recovery_projection(data,cat,v,actual['head'],status)))
  c=copy.deepcopy(cat);c['declarations']=[];c['source']['fields']=[];check('projection cannot trust coordinated submitted catalogue',lambda:reject(lambda:m.recovery_projection(data,c,actual,actual['head'],status)))
  def evidence_mutation(label,edit):
   e=dict(data['ctx']['e']);t=json.loads(e['evidence/execution-trace.json']);x=json.loads(e['evidence/recovery-export-0.json']);edit(e,t,x);e['evidence/execution-trace.json']=m.enc(t);e['evidence/recovery-export-0.json']=m.enc(x)
   check(label,lambda:reject(lambda:m.connected_recovery(data,cat,e)))
  def event(t,fn):return next(r for r in t['events'] if r['function']==fn and r['event']=='return')
  for name in selected:
   evidence_mutation('semantic missing field '+name,lambda e,t,x,name=name:event(t,'ManagedAuthority.recover')['value'].pop(name))
  for name,value in [('head','a'*64),('head',17),('recovery_only',1),('recovery_only',False),('new_attempt_authorized',0),('new_attempt_authorized',True)]:
   evidence_mutation('semantic wrong '+name+' '+repr(value),lambda e,t,x,name=name,value=value:event(t,'ManagedAuthority.recover')['value'].update({name:value}))
  evidence_mutation('semantic altered export head',lambda e,t,x:x.update(expected_head='a'*64))
  def raw_head(e,t,x):
   h=json.loads(bytes.fromhex(x['head']));h['head']='a'*64;x['head']=m.enc(h).hex()
  evidence_mutation('semantic substituted raw HEAD',raw_head)
  def coordinated(e,t,x):
   raw_head(e,t,x);x['expected_head']='a'*64;event(t,'ManagedAuthority.recover')['value']['head']='a'*64
  evidence_mutation('semantic coordinated returned/export/raw head substitution',coordinated)
  evidence_mutation('semantic inconsistent status embedding',lambda e,t,x:event(t,'ManagedAuthority.recover')['value']['status'].update(connection_epoch=17))
  evidence_mutation('semantic wrong child parent',lambda e,t,x:event(t,'ManagedAuthority.status').update(parent=5))
  evidence_mutation('semantic fabricated validator scalar',lambda e,t,x:event(t,'ManagedAuthority._validate').update(value=x['expected_head']))
  evidence_mutation('semantic interrupted validator cannot supply envelope',lambda e,t,x:event(t,'ManagedAuthority._validate').update(normal_return=False))
  evidence_mutation('semantic modified capture contract',lambda e,t,x:e.update({'preparation/worker.py':e['preparation/worker.py'].replace(b"'ManagedAuthority.status','ManagedAuthority.recover','main'",b"'ManagedAuthority.status','ManagedAuthority.recover','ManagedAuthority._validate','main'")}))
  evidence_mutation('semantic mixed capture instance',lambda e,t,x:t['events'][0].update(path='/other-acquisition/source.py'))
  evidence_mutation('preserve SOC-02-R1 close binding rejection',lambda e,t,x:event(t,'ManagedAuthority.close')['state'].update(binding={'wrong':'binding'}))
  # Every context remains mandatory; prior receipts cannot substitute for new.
  for idx in (0,1):
   b=copy.deepcopy(bundle);b['contexts'][idx]['recovery_field_declarations']['declarations'].pop();check('public omitted field context '+str(idx),lambda b=b:reject(lambda:m.validate(a.root,m.enc(b))))
   b=copy.deepcopy(bundle);b['contexts'][idx]['saved_recovery_fields'][0]['fields'][0]['value']='a'*64;check('public stale head context '+str(idx),lambda b=b:reject(lambda:m.validate(a.root,m.enc(b))))
  b=copy.deepcopy(bundle);b['contexts'].pop();check('public omitted context',lambda:reject(lambda:m.validate(a.root,m.enc(b))))
  b=copy.deepcopy(bundle)
  for v in b['contexts']:v['recovery_field_declarations']['declarations']=[];v['recovery_field_declarations']['source']['fields']=[];v['saved_recovery_fields'][0]['fields']=[]
  check('public coordinated deletions',lambda:reject(lambda:m.validate(a.root,m.enc(b))))
  b=copy.deepcopy(bundle);b['contexts'][1]=copy.deepcopy(b['contexts'][0]);check('public duplicated context',lambda:reject(lambda:m.validate(a.root,m.enc(b))))
  b=copy.deepcopy(bundle);b['prior_reference_receipt']['sha256']='0'*64;check('public stale predecessor',lambda:reject(lambda:m.validate(a.root,m.enc(b))))
  b=copy.deepcopy(bundle);b['contexts'][0]['saved_recovery_fields'][0]['instance']={'id':'other-acquisition'};check('public mixed instance',lambda:reject(lambda:m.validate(a.root,m.enc(b))))
  check('public rejects prior receipt substitution',lambda:reject(lambda:m.validate(a.root,(data['reviewed_reference_root']/'results/reference-correspondence.json').read_bytes())))
  answer=m.validate(a.root,saved);answer['contexts'].clear();answer['receipt'].clear();bundle['contexts'][0]['recovery_field_declarations']['source']['fields'].clear();bundle['contexts'][1]['saved_recovery_fields'][0]['fields'][0]['head_relation'].clear();cat['source']['head_chain'].clear();row['fields'].clear()
  check('nested returned mutations leave public expectations unchanged',lambda:m.validate(a.root,saved))
  pristine=m.recovery_catalogue(data);check('nested mutations leave catalogue expectations unchanged',lambda:m.check_recovery_catalogue(data,pristine))
  check('mutated returned catalogue remains rejected',lambda:reject(lambda:m.check_recovery_catalogue(data,cat)))
  assert original=={n:identity((a.root/'code'/n).read_bytes()) for n in original}
 except BaseException as ex:error=repr(ex);raise
 finally:
  (a.output/'constructed-values.json').write_text(json.dumps(cases,sort_keys=True,indent=2)+'\n')
  result={'result':'PASS' if error is None else 'FAIL','passed':len(rows),'checks':rows,'error':error,'source':original,'source_after':{n:identity((a.root/'code'/n).read_bytes()) for n in original},'root':str(a.root),'python':sys.version,'optimization':sys.flags.optimize,'prior_suites_rerun':False,'new_controls_only':True,'database_connections':0,'host_session_execution':False,'constructed_values_are_not_observations':True}
  (a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS',len(rows),'new recovery-field controls')
if __name__=='__main__':main()
