"""Independent bounded handle correspondence checks; saved inputs only."""
from pathlib import Path
import argparse,copy,hashlib,importlib.metadata,json,os,runpy,sys,traceback,types
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey,Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def module(p):
 m=types.ModuleType('independent_handle');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def main():
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('output',type=Path);p.add_argument('--recovered',action='store_true');p.add_argument('--case',required=True);a=p.parse_args();root=a.root.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
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
  if name=='derive_handle' and parent=='_basis':calls.append({'function':'mandatory handle derive_handle','file':f,'source':identity(Path(f).read_bytes())})
  if name=='_compare_evidence' and parent=='_checked' and f==str(root/'code/correspondence.py'):
   l=frame.f_locals;path='evidence/recovery-export-0.json';expected=json.loads(l['basis']['evidence'][path]);candidate=l['candidate'];value=None
   try:value=json.loads(candidate[path])
   except (ValueError,TypeError,KeyError):pass
   calls.append({'function':'journal comparison','expected_journal':expected['journal'],'candidate_journal':None if value is None else value.get('journal'),'expected_export':identity(l['basis']['evidence'][path]),'candidate_export':None if path not in candidate else identity(candidate[path])})
 sys.settrace(trace)
 def record(label,category,result,**kw):
  r={'check':label,'category':category,'result':result,**kw};rows.append(r)
  with (out/'progress.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
 def check(label,fn,category='independent'):
  v=fn();assert v is not False,label;record(label,category,'PASS');return v
 def reject(label,fn,reason=None,category='negative'):
  try:fn()
  except (ValueError,TypeError,KeyError,IndexError,InvalidSignature) as ex:
   if reason is not None:assert str(ex)==reason,(label,str(ex),reason)
   record(label,category,'REJECTED',error={'type':type(ex).__name__,'message':str(ex)});return
  raise AssertionError('UNEXPECTED-ACCEPTANCE:'+label)
 try:
  assert sys.version_info[:3]==(3,12,14) and not sys.flags.optimize
  m=module(root/'code/correspondence.py');data=m.inputs(root);cat=m.catalogue(data);d=m.inner(data);e=dict(d['ctx']['e']);source={n:identity((root/'code'/n).read_bytes()) for n in ('correspondence.py','managed_coverage.py')}
  saved=(root/'results/client-handle-correspondence.json').read_bytes();assert identity(saved)=={'bytes':1719615,'sha256':'16ed6d696676e54e2a9465e62761b189ed52aa65261fa2e9aa52cc5907d4a4a5'}
  bundle=json.loads(saved);claims=[x['client_handle_return_correspondence'] for x in bundle['contexts']];export=json.loads(e['evidence/recovery-export-0.json'])
  fx=json.loads((root/'retained/handle/tests/constructed-envelopes.json').read_bytes())['cases'][0];q=json.loads(bytes.fromhex(fx['packet']['bytes_hex']));promoted=dict(e);ex=copy.deepcopy(export);ex['journal']=[[q['request']['challenge'],fx['packet']['bytes_hex'],fx['responses'][0]['response']['bytes_hex']]];promoted['evidence/recovery-export-0.json']=enc(ex)
  selected=a.case
  if selected=='legitimate':check('legitimate mandatory derivation equals exact receipt',lambda:enc(m.derive_client(data,cat))==saved)
  elif selected.startswith('wrong-instance-'):
   i=int(selected[-1]);bad=copy.deepcopy(claims)
   for row in (bad[i],bad[i]['manager_relation']):row['validated_scope']['instance']['binding']='e'*64;row['instance_request_context']['binding']='e'*64
   bad[i]['manager_relation']['validated_state_anchor']['instance']['binding']='e'*64
   reject('full semantic coordinated wrong instance '+str(i),lambda:m.semantic(data,cat,bad),'CLIENT-CONTEXT-CORRESPONDENCE')
  elif selected=='catalogue':
   bad=copy.deepcopy(cat);bad['source']['operation']='state';bad['source']['client_method']='state';bad['arguments'][0]['method']='state';bad['ordered_hops'].reverse()
   reject('full coordinated source delegation and hop substitution',lambda:m.semantic(data,bad),'CLIENT-SOURCE-CATALOGUE')
  elif selected in ('journal-semantic','journal-derivation'):
   bad=copy.deepcopy(claims)
   for x in bad:x['manager_relation']['saved_journal_rows']=1;x['manager_relation']['saved_journal_records']=[{'promoted_constructed_packet':fx['packet'],'promoted_constructed_response':fx['responses'][0]['response']}];x['packet_observation']=fx['packet'];x['runtime_forwarding_links']=[{'invented':True}]
   fn=m.semantic if selected=='journal-semantic' else m.derive_client
   reject('coordinated journal and claims '+selected,lambda:fn(data,cat,bad,promoted),'HANDLE-VALIDATED-JOURNAL')
   check('journal expectation is fresh validated empty evidence',lambda:any(x['function']=='journal comparison' and x['expected_journal']==[] and len(x['candidate_journal'] or [])==1 for x in calls))
  elif selected=='mutable-input':
   def clone(x):
    y=dict(x)
    if 'prior_data' in y:y['prior_data']=clone(y['prior_data'])
    if 'ctx' in y:y['ctx']=dict(y['ctx'])
    return y
   candidate=clone(data);m.inner(candidate)['ctx']['e']=promoted
   reject('mutable candidate baseline cannot redefine empty journal',lambda:m.semantic(candidate,cat),'HANDLE-VALIDATED-JOURNAL')
  elif selected=='missing-export':
   missing=dict(e);del missing['evidence/recovery-export-0.json'];reject('full missing export',lambda:m.semantic(data,cat,evidence=missing),'HANDLE-MISSING-EXPORT')
  elif selected=='stale-output':
   mixed=dict(e);mixed['evidence/smoke.stdout']=b'{"status":"READY"}\n'
   reject('semantic substituted saved output cannot create destination evidence',lambda:m.semantic(data,cat,evidence=mixed))
  elif selected in ('public-omission','public-status','public-contexts','public-stale'):
   bad=copy.deepcopy(bundle)
   if selected=='public-omission':bad['contexts'][1].pop('client_handle_return_correspondence')
   elif selected=='public-status':bad['new_client_slice_limits'].update(readiness='READY',actual_admission=True,runtime_chain='COMPLETE');bad['contexts'][0]['client_handle_return_correspondence']['runtime_forwarding_links']=[{'destination':'stdout'}]
   elif selected=='public-stale':bad['contexts'][0]['client_handle_return_correspondence']['manager_predecessor_receipt']['sha256']='0'*64
   else:bad['contexts'][1]=copy.deepcopy(bad['contexts'][0])
   reject(selected,lambda:m.validate(root,enc(bad)),'STALE-OR-ALTERED-CLIENT-CORRESPONDENCE','public_negative')
  elif selected=='semantic-alias':
   result=check('pristine full semantic before mutations',lambda:m.semantic(data,cat));assert enc(result)==enc(claims);other=enc(result[1]);pristine=enc(result)
   result[0]['declaration']['ordered_hops'].clear();result[0]['validated_scope']['instance']['binding']='bad';result[0]['manager_relation']['saved_journal_records'].append({'forged':True});result[0]['saved_general_output']['stdout'].clear();check('context nested trees isolated',lambda:enc(result[1])==other)
   catbytes=enc(cat);cat['source']['stages']['packet-check'].clear();check('catalogue mutation cannot update expected source',lambda:enc(m.catalogue(data))==catbytes);cat=m.catalogue(data)
   check('pristine semantic after nested mutations',lambda:enc(m.semantic(data,cat))==pristine)
  elif selected=='public-alias':
   result=check('pristine public before mutations',lambda:m.validate(root,saved));pristine=enc(result);result['contexts'].reverse();result['receipt'].clear()
   check('pristine public after nested mutations',lambda:enc(m.validate(root,saved))==pristine)
  else:raise AssertionError('unknown independent check')
  check('mandatory handle derivation actually invoked',lambda:any(x['function']=='mandatory handle derive_handle' for x in calls))
  check('candidate source evidence and saved receipt unchanged',lambda:source=={n:identity((root/'code'/n).read_bytes()) for n in source} and e==d['ctx']['e'] and (root/'results/client-handle-correspondence.json').read_bytes()==saved)
 except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};(out/'failure.txt').write_text(traceback.format_exc());raise
 finally:
  sys.settrace(None);r={'result':'PASS' if error is None else 'FAIL','assertions':len(rows),'categories':{cc:sum(x['category']==cc for x in rows) for cc in sorted({x['category'] for x in rows})},'checks':rows,'error':error,'recovered':a.recovered,'case':a.case,'environment':{'python':sys.version,'optimization':sys.flags.optimize,'cryptography_installed':importlib.metadata.version('cryptography')},'source':locals().get('source'),'database_connections':0,'session_operations':0,'requests_issued':0,'new_signatures':0,'completed_review_reruns':False,'constructed_cases_are_execution_evidence':False}
  (out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');(out/'call-observations.json').write_text(json.dumps(calls,indent=2)+'\n')
 print('PASS',a.case,len(rows),'independent entry checks')
if __name__=='__main__':main()
