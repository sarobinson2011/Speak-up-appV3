"""Formal-Lab[6] new offline recovery-field checks; no producer operations."""
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
   path=os.fsdecode(args[0])
   if path.startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
   if path.startswith(str(root)+'/') and len(args)>2 and type(args[2]) is int and args[2]&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC):raise AssertionError('INPUT-WRITE')
 sys.addaudithook(audit)
 def profile(frame,event,arg):
  name=frame.f_code.co_filename.rsplit('/',1)[-1]
  if event=='call' and (name in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') or name=='prospective_entry.py' and frame.f_code.co_name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status')):raise AssertionError('APPLICATION-EXECUTION')
 sys.setprofile(profile);checks=[];constructed=[];failure=None;pins={n:identity((root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 def record(label,result='PASS',category='independent',error=None):
  row={'check':label,'result':result,'category':category}
  if error is not None:row['error']=error
  checks.append(row)
  with (out/'progress.jsonl').open('ab') as f:f.write((json.dumps(row,sort_keys=True)+'\n').encode())
 def good(label,v=True,category='independent'):assert v,label;record(label,category=category)
 def reject(label,fn,category='negative'):
  try:fn()
  except (ValueError,TypeError,KeyError,IndexError,FileNotFoundError) as ex:record(label,'REJECTED',category,{'type':type(ex).__name__,'message':str(ex)});return
  raise AssertionError('UNEXPECTED ACCEPTANCE: '+label)
 try:
  m=module(root/'code/correspondence.py','review_recovery');data=m.recovery_inputs(root);cat=m.recovery_catalogue(data);savedraw=(root/'results/recovery-field-correspondence.json').read_bytes();saved=json.loads(savedraw)
  good('legitimate public exact receipt',m.validate(root,savedraw)['result']=='PASS')
  observed,capture,joined=m.connected_recovery(data,cat);good('legitimate semantic connection')
  good('legitimate exact derivation',m.enc(m.derive_recovery(data,cat))==savedraw)
  oracle=module(Path(__file__).with_name('source_oracle.py'),'independent_source');model=data['values']['candidate/managed-route/model.json'];source=oracle.audit(data['manager'],data['authority'],cat,model)
  (out/'source-audit.json').write_text(json.dumps(source,indent=2)+'\n');good('independent source fields chain guards and ordering')
  evidence=data['ctx']['e'];trace=json.loads(evidence['evidence/execution-trace.json']);events=trace['events'];x=json.loads(evidence['evidence/recovery-export-0.json']);headraw=bytes.fromhex(x['head']);head=json.loads(headraw)
  def event(t,fn,kind='return'):return next(v for v in t['events'] if v['function']==fn and v['event']==kind)
  ret=event(trace,'ManagedAuthority.recover');returned=ret['value'];status=event(trace,'ManagedAuthority.status')['value'];validate_ret=event(trace,'ManagedAuthority._validate')
  old=json.loads((root/'retained/references/results/reference-correspondence.json').read_bytes())
  for view,previous in zip(saved['contexts'],old['contexts']):
   oracle.audit(data['manager'],data['authority'],view['recovery_field_declarations'],model);good('independent source audit '+view['context'])
   good('all preceding context fields preserved '+view['context'],all(previous[k]==view[k] for k in previous))
   row=view['saved_recovery_fields'][0];occ=next(o for v in observed['contexts'] if v['context']==view['context'] for o in v['occurrences'] if o.get('frame')==row['frame'])
   assert row['occurrence']==occ['id'] and row['trace_identity']==identity(evidence['evidence/execution-trace.json'])
   assert row['parent']==event(trace,'ManagedAuthority.recover','call')['parent'] and len(row['fields'])==3
   for f in row['fields']:
    pointer=f['return_pointer'].split('/');assert pointer[:2]==['','events'];value=events[int(pointer[2])][pointer[3]][pointer[4]];assert m.enc(value)==m.enc(f['value'])
    if f['head_relation']:
     h=f['head_relation'];assert h['export']['sha256']==identity(evidence['evidence/recovery-export-0.json'])['sha256'] and h['decoded_head']['identity']==identity(headraw)
     assert f['value']==x['expected_head']==head['head'] and h['validator_scalar_pointer'] is None and h['state_or_ingest_frame'] is None
    else:assert type(f['value']) is bool
   good('exact recorded value export and occurrence joins '+view['context'])
  good('validator scalar absence is real','value' not in validate_ret and capture['scalar_return_recorded'] is False)
  good('eighteen invocations and separate observer preserved',sum(v['event']=='call' and not v['resumed_generator'] for v in events)==18 and saved['new_recovery_slice_limits']['separate_observer_Client_state_call']==1 and saved['new_recovery_slice_limits']['observer_frame'] is None)
  def catneg(label,edit,d=None):
   c=copy.deepcopy(cat);edit(c);reject(label,lambda:m.check_recovery_catalogue(data if d is None else d,c),'catalogue_negative')
  for i,name in enumerate([v['name'] for v in cat['declarations']]):
   def omission(c,i=i,name=name):c['source']['fields'].pop(i);c['declarations'].pop(i);c['source']['keys'].remove(name)
   catneg('coordinated field/expected membership omission '+name,omission)
   if not a.recovered:
    catneg('changed type '+name,lambda c,i=i:c['declarations'][i].update(type='int'))
    catneg('changed origin '+name,lambda c,i=i:c['source']['fields'][i]['origin'].update(expression='unrelated'))
    catneg('missing return guard '+name,lambda c,i=i:c['declarations'][i]['origin']['origin'].update(guards=[]))
    catneg('missing return continuation '+name,lambda c,i=i:c['source']['fields'][i]['return_site'].update(continuation=[]))
  if not a.recovered:
   for name in cat['source']['head_chain']:catneg('omitted head dependency '+name,lambda c,name=name:c['source']['head_chain'].pop(name))
   for i,row in enumerate(cat['source']['programs']):catneg('omitted source program '+row['owner'],lambda c,i=i:c['source']['programs'].pop(i))
   for i in (1,2):catneg('coordinated wrong boolean constant '+str(i),lambda c,i=i:(c['declarations'][i]['origin'].update(value=not c['declarations'][i]['origin']['value']),c['source']['fields'][i].update(value=not c['source']['fields'][i]['value'])))
   catneg('missing embedded status relationship',lambda c:c['source']['status_embedding'].clear())
   catneg('false allocation and full model claim',lambda c:c['limits'].update(multiplicity=0,full_model_binding=True,actual_admission=True))
   sites=[cat['source']['return']]+[cat['source']['head_chain'][k] for k in ('state_assignment','export_assignment','ingest_call','validator_return')]+[f['assignment'] for f in cat['source']['fields'] if f['kind']=='validated-state-head']
   for row in sites:
    d=dict(data);d['values']=copy.deepcopy(data['values']);inv=d['values']['candidate/managed-route/producers.json']['source_inventory']['sites'];inv[:]=[v for v in inv if v['site']!=row['site']]
    reject('cached producer omission '+row['site'],lambda d=d:m.recovery_catalogue(d),'catalogue_negative')
   for key,oldbytes,newbytes in [('manager',b"'recovery_only':True",b"'recovery_only':False"),('authority',b'SELECT raw FROM head WHERE id=1',b'SELECT raw FROM head WHERE id=2')]:
    d=dict(data);d[key]=data[key].replace(oldbytes,newbytes);assert d[key]!=data[key];reject('stale '+key+' defining source',lambda d=d:m.recovery_catalogue(d),'catalogue_negative')
   d=dict(data);d['values']=copy.deepcopy(data['values']);next(v for v in d['values']['candidate/managed-route/model.json']['existing_declarations'] if v.get('template_id')=='HEAD:/head')['native_template']['type']='OBJECT'
   reject('substituted inherited head declaration',lambda:m.recovery_catalogue(d),'catalogue_negative')
  # Projection is conditional algebra; arbitrary strings are not authenticated
  # HEAD evidence and do not change the production domain or impose a new cap.
  for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
   for text in (['','\x00λ\n','x'*16385] if not a.recovered else ['\x00λ\n']):
    value=copy.deepcopy(returned);value['head']=text;projected=m.recovery_projection(data,cat,value,text,status)
    assert projected[0]['value']==text and type(projected[1]['value']) is bool and projected[1]['value'] is True and projected[2]['value'] is False
    constructed.append({'context':context,'head':text,'result':projected,'actual_observation':False,'authentication_established':False});good('constructed explicit-premise projection '+context+' length '+str(len(text)),category='constructed_only')
  for name,value in ([('head',None),('head',0),('head',b'0'),('head',[]),('recovery_only',1),('recovery_only',False),('recovery_only','true'),('new_attempt_authorized',0),('new_attempt_authorized',True),('new_attempt_authorized',None)] if not a.recovered else [('recovery_only',1),('new_attempt_authorized',0)]):
   altered=copy.deepcopy(returned);altered[name]=value;reject('conditional exact type/constant '+name+' '+repr(value),lambda altered=altered:m.recovery_projection(data,cat,altered,returned['head'],status),'constructed_negative')
  def evneg(label,edit):
   e=dict(evidence);t=copy.deepcopy(trace);export=copy.deepcopy(x);edit(e,t,export);e['evidence/execution-trace.json']=m.enc(t)
   if 'evidence/recovery-export-0.json' in e:e['evidence/recovery-export-0.json']=m.enc(export)
   reject(label,lambda:m.connected_recovery(data,cat,e),'saved_evidence_negative')
  for name in ['head','recovery_only','new_attempt_authorized']:
   evneg('missing observed '+name,lambda e,t,x,name=name:event(t,'ManagedAuthority.recover')['value'].pop(name))
  for name,val in [('head','1'+returned['head'][1:]),('recovery_only',1),('new_attempt_authorized',0)]:
   evneg('wrong observed '+name,lambda e,t,x,name=name,val=val:event(t,'ManagedAuthority.recover')['value'].update({name:val}))
  if not a.recovered:
   evneg('missing required export',lambda e,t,x:e.pop('evidence/recovery-export-0.json'))
   evneg('invented validator scalar',lambda e,t,x:event(t,'ManagedAuthority._validate').update(value=returned['head']))
   evneg('wrong validator completion',lambda e,t,x:event(t,'ManagedAuthority._validate').update(normal_return=False))
   evneg('wrong recovery embedding parent',lambda e,t,x:event(t,'ManagedAuthority.status','call').update(parent=8))
   def basic_head(e,t,x):
    new='1'+returned['head'][1:];h=json.loads(bytes.fromhex(x['head']));h['head']=new;x['head']=m.enc(h).hex();x['expected_head']=new;event(t,'ManagedAuthority.recover')['value']['head']=new
   evneg('coordinated three-field head substitution',basic_head)
   def status_change(e,t,x):
    for v in t['events']:
     if v['function']=='ManagedAuthority.status':v['state']['_epoch']=2
     if v['event']=='return' and v['function']=='ManagedAuthority.status':v['value']['connection_epoch']=2
    event(t,'ManagedAuthority.recover')['value']['status']['connection_epoch']=2
   evneg('coordinated status parent child and snapshots',status_change)
  def public(label,edit):
   b=copy.deepcopy(saved);edit(b);reject(label,lambda:m.validate(root,m.enc(b)),'public_negative')
  for i in (0,1):
   public('public omitted field context '+str(i),lambda b,i=i:b['contexts'][i]['recovery_field_declarations']['declarations'].pop())
   if not a.recovered:public('public stale head context '+str(i),lambda b,i=i:b['contexts'][i]['saved_recovery_fields'][0]['fields'][0].update(value='1'+returned['head'][1:]))
  if not a.recovered:
   public('public duplicated contexts',lambda b:b['contexts'].__setitem__(1,copy.deepcopy(b['contexts'][0])))
   public('public stale predecessor receipt',lambda b:b['prior_reference_receipt'].update(sha256='0'*64))
   public('public false observed scalar',lambda b:b['contexts'][0]['saved_recovery_fields'][0]['fields'][0]['head_relation'].update(validator_scalar_pointer='/events/0/value'))
   public('public UNKNOWN and readiness escalation',lambda b:b['new_recovery_slice_limits'].update(multiplicity=0,inventory_unknown_totals=0,lifetime_unknown_totals=0,readiness='READY',actual_admission=True))
  answer=m.validate(root,savedraw);answer['contexts'].reverse();answer['receipt'].clear();cat['source']['fields'].clear();joined['fields'].clear();saved['contexts'][0]['recovery_capture_contract'].clear()
  good('mutable returned objects cannot change pristine expectations',m.validate(root,savedraw)['result']=='PASS')
  good('implementation source unchanged',pins=={n:identity((root/'code'/n).read_bytes()) for n in pins})
 except BaseException as ex:
  failure={'type':type(ex).__name__,'message':str(ex),'traceback':traceback.format_exc()};(out/'failure.txt').write_text(failure['traceback']);raise
 finally:
  (out/'constructed-values.json').write_text(json.dumps(constructed,indent=2)+'\n');categories={k:sum(r['category']==k for r in checks) for k in sorted({r['category'] for r in checks})}
  result={'result':'PASS focused controls' if failure is None else 'FAIL','assertions':len(checks),'categories':categories,'checks':checks,'failure':failure,'separate_coordinated_probe_not_included_in_pass_count':True,'source':pins,'recovered':a.recovered,'environment':{'python':sys.version,'optimization':sys.flags.optimize,'cryptography_installed':importlib.metadata.version('cryptography')},'constructed_cases':len(constructed),'no_runtime_session_database_operations':True,'no_completed_review_rerun':True}
  (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS',len(checks),'focused checks',categories)
if __name__=='__main__':main()
