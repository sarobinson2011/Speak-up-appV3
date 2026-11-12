"""Assemble expected output only. No authentication or validation invocation."""
from pathlib import Path
import types,json,hashlib,sys,time,traceback,datetime
B=Path(__file__).resolve().parent;C=B/'candidate';O=B/'package';(O/'expected').mkdir(parents=True,exist_ok=False)
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(n,v):
 p=B/n
 with p.open('x') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n')
def module(p,n):
 m=types.ModuleType(n);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
counts={};forbidden=[];start=time.monotonic()
def profile(f,event,arg):
 if event=='call' and f.f_code.co_filename==str(C/'code/correspondence.py'):
  n=f.f_code.co_name;counts[n]=counts.get(n,0)+1
  if n in ('_basis','inputs','parent_root','derive','validate','_construct_checked','constructed_projection'):
   forbidden.append(n);raise RuntimeError('PREPARATION-AUTHENTICATION-FORBIDDEN:'+n)
def audit(event,args):
 if event in ('subprocess.Popen','os.system','sqlite3.connect','socket.connect','socket.bind'):raise RuntimeError('PREPARATION-OUT-OF-SCOPE:'+event)
 if event=='exec' and any(x in str(args[0].co_filename) for x in ('/source-evidence/','/retained/','/observer-reference/')):raise RuntimeError('RETAINED-OR-RUNTIME-EXECUTION-FORBIDDEN')
sys.addaudithook(audit)
try:
 a=module(C/'code/correspondence.py','_offline_expected_adapter');c=module(C/'code/managed_coverage.py','_offline_expected_producer');sys.setprofile(profile)
 raw=(C/'reference/res-null/actual-receipt.json').read_bytes();prior=json.loads(raw)
 files={n:(C/'reference/resolution/source'/n).read_bytes() for n in json.loads((C/'reference/resolution/source-index.json').read_bytes())}
 # Saved parent declarations are inputs to offline expected-output construction,
 # never represented as an actual returned authentication basis.
 parent_cat=prior['contexts'][0]['res_null_test_correspondence']['declaration']
 assert parent_cat==prior['contexts'][1]['res_null_test_correspondence']['declaration']
 cat=c.exit_decref_catalogue(parent_cat,files)
 expected_inputs={'fresh':{'root':C},'prior':prior,'catalogue':cat,'parent_public':{'result':'PASS','contexts':list(a.CONTEXTS),'receipt':ident(raw),'actual_admission':False}}
 expected=a.enc(a._assemble(expected_inputs));sys.setprofile(None)
 (O/'expected/expected-exit-decref-receipt.json').write_bytes(expected)
 (O/'expected/offline-exit-decref-catalogue.json').write_bytes(a.enc(cat))
 save('offline-assembly.json',{'status':'EXPECTED OUTPUT PREPARED, NOT AUTHENTICATED','expected_receipt':ident(expected),'catalogue':ident(a.enc(cat)),'catalogue_source':'fixed producer exit_decref_catalogue, defining bytes and saved predecessor declaration; no control suite replay','parent_receipt':ident(raw),'candidate_call_counts':counts,'forbidden_calls':forbidden,'authentication_calls':0,'public_calls':0,'authenticated_constructed_calls':0,'candidate_changes':0,'meaning':'Offline serializer input only; no returned basis, public acceptance or qualification claimed'})
 save('offline-assembly-exit.json',{'exit':0,'seconds':time.monotonic()-start,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});print(json.dumps({'expected_receipt':ident(expected),'candidate_calls':counts,'authentication_calls':0},indent=2))
except BaseException as e:
 sys.setprofile(None);save('offline-assembly-failure.json',{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()});save('offline-assembly-exit.json',{'exit':1,'seconds':time.monotonic()-start,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});raise
