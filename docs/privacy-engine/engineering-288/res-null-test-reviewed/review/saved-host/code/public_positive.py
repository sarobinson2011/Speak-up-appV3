"""Exactly ONE new res-null-test public positive; no focused/core/historical campaign.
Run only on separately authorized qualified Ubuntu after preflight and reservation.
"""
from pathlib import Path
import sys,os,json,hashlib,importlib.util,time,signal,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common_r1 import *
workspace=Path(sys.argv[1]).resolve();root=workspace/'candidate';out=workspace/'validation/results'
out.mkdir(parents=True,exist_ok=False);plan=json.loads((workspace/'PLAN.json').read_bytes())
start=time.monotonic();calls=[];observer=None;failure=None;public=None;basis_capture=False;constructed_calls=None
agreements={'lookup':False,'r1':False,'helper':False,'enter':False,'res_null':False,'return':False,'decref':False,'fast':False}
class Records:
 def save(self,name,v):save(out/name,v)
 def event(self,event,**kw):
  v={'utc':now(),'event':event,'seconds':time.monotonic()-start,**kw}
  with (out/'events.jsonl').open('a') as f:f.write(json.dumps(v,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
  print('EVENT '+json.dumps(v,sort_keys=True),flush=True)
r=Records()
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def byte_identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def count(path):return sum(x['file']==str(path) and x['function']=='validate' for x in calls)
def deadline(signum,frame):raise TimeoutError('RES-NULL-PUBLIC-SOFT-DEADLINE')
fast_path=root/'retained/fast';decref_path=fast_path/'retained/decref';return_path=decref_path/'retained/return';enter_path=return_path/'retained/enter';lookup_path=enter_path/'retained/lookup';r1_path=lookup_path/'retained/r1';helper_path=r1_path/'retained/helper-open'
try:
 r.save('input-root.json',exact_tree(root,json.loads((workspace/'expected/ASSEMBLED-ROOT-MANIFEST.json').read_bytes())))
 expected=(workspace/'expected/expected-res-null-receipt.json').read_bytes();need(byte_identity(expected)==plan['expected_receipt'],'EXPECTED-RECEIPT-PIN')
 r.save('expected-input.json',{'identity':byte_identity(expected),'role':'OFFLINE EXPECTED OUTPUT; not a returned basis or validation result','contexts':plan['contexts']})
 native=module(workspace/'observer-reference/native_observer.py','_res_null_native_observer');observer=native.Observer(root,out,r,calls)
 m=module(root/'code/correspondence.py','_res_null_candidate');observer.start(m)
 signal.signal(signal.SIGALRM,deadline);signal.setitimer(signal.ITIMER_REAL,plan['soft_seconds'])
 r.event('res-null-full-public-positive-start',attempt=plan['attempt'],expected_receipt=byte_identity(expected),public_calls_authorized=1)
 # SOLE new public invocation. It performs actual authentication internally.
 public=m.validate(root,expected)
 r.save('actual-public-result.json',public)
 need(public=={'result':'PASS','contexts':plan['contexts'],'receipt':plan['expected_receipt'],'actual_admission':False},'RES-NULL-PUBLIC-RESULT')
 need(len(observer.captures)==1,'EXACTLY-ONE-ACTUAL-RES-NULL-BASIS-RETURN')
 basis=observer.captures[0];basis_capture=True
 # Actual nested returned objects, not deserialized saved bases or offline data.
 fastmod=basis['parent_module'];fb=basis['parent_basis']
 need(Path(fastmod.__file__).resolve()==fast_path/'code/correspondence.py','ACTUAL-FAST-MODULE-ORIGIN')
 fast_bytes=fastmod.enc(fastmod._assemble(fb))
 need(fast_bytes==basis['fresh']['saved'] and byte_identity(fast_bytes)==plan['fast_receipt'],'ACTUAL-FAST-BASIS-RECEIPT');agreements['fast']=True
 decrefmod=fb['parent_module'];db=fb['parent_basis']
 need(Path(decrefmod.__file__).resolve()==decref_path/'code/correspondence.py','ACTUAL-DECREF-MODULE-ORIGIN')
 decref_bytes=decrefmod.enc(decrefmod._assemble(db))
 need(decref_bytes==fb['fresh']['saved'] and byte_identity(decref_bytes)==plan['decref_receipt'],'ACTUAL-DECREF-BASIS-RECEIPT');agreements['decref']=True
 retmod=db['parent_module'];retbasis=db['parent_basis']
 need(Path(retmod.__file__).resolve()==return_path/'code/correspondence.py','ACTUAL-RETURN-MODULE-ORIGIN')
 return_bytes=retmod.enc(retmod._assemble(retbasis))
 need(return_bytes==db['fresh']['saved'] and byte_identity(return_bytes)==plan['return_receipt'],'ACTUAL-RETURN-BASIS-RECEIPT');agreements['return']=True
 enter=retbasis['parent_module'];eb=retbasis['parent_basis']
 need(Path(enter.__file__).resolve()==enter_path/'code/correspondence.py','ACTUAL-ENTER-MODULE-ORIGIN')
 enter_bytes=enter.enc(enter._assemble(eb))
 need(enter_bytes==retbasis['fresh']['saved'] and byte_identity(enter_bytes)==plan['enter_receipt'],'ACTUAL-ENTER-BASIS-RECEIPT');agreements['enter']=True
 lookup=eb['parent_module'];lb=eb['parent_basis']
 need(Path(lookup.__file__).resolve()==lookup_path/'code/correspondence.py','ACTUAL-LOOKUP-MODULE-ORIGIN')
 lookup_bytes=lookup.enc(lookup._assemble(lb))
 need(lookup_bytes==eb['fresh']['saved'] and byte_identity(lookup_bytes)==plan['lookup_receipt'],'ACTUAL-LOOKUP-BASIS-RECEIPT');agreements['lookup']=True
 r1=lb['parent_module'];rb=lb['parent_basis']
 need(Path(r1.__file__).resolve()==r1_path/'code/correspondence.py','ACTUAL-R1-MODULE-ORIGIN')
 r1_bytes=r1.enc(r1._assemble(rb))
 need(r1_bytes==lb['fresh']['saved'] and byte_identity(r1_bytes)==plan['r1_receipt'],'ACTUAL-R1-BASIS-RECEIPT');agreements['r1']=True
 helper=rb['parent_module'];hb=rb['parent_basis']
 need(Path(helper.__file__).resolve()==helper_path/'code/correspondence.py','ACTUAL-HELPER-MODULE-ORIGIN')
 helper_bytes=helper.enc(helper._assemble(hb['fresh'],helper._rows(hb),hb))
 need(helper_bytes==rb['fresh']['saved'] and byte_identity(helper_bytes)==plan['helper_receipt'],'ACTUAL-HELPER-BASIS-RECEIPT');agreements['helper']=True
 r.save('actual-parent-provenance.json',{'capture_source':'actual new _basis return captured by unchanged native observer using exact code identity','fast_basis_source':'actual unchanged fast-completion _basis return inside new res-null _basis','fast_receipt':byte_identity(fast_bytes),'fast_validation':basis['parent_public'],'decref_basis_source':'actual unchanged enter-decref _basis return inside fast _basis','decref_receipt':byte_identity(decref_bytes),'decref_validation':fb['parent_public'],'return_basis_source':'actual unchanged enter-return _basis return inside enter-decref _basis','return_receipt':byte_identity(return_bytes),'return_validation':db['parent_public'],'enter_basis_source':'actual unchanged enter-call _basis return inside enter-return _basis','enter_receipt':byte_identity(enter_bytes),'enter_validation':retbasis['parent_public'],'lookup_basis_source':'actual unchanged lookup _basis return inside enter-call _basis','lookup_receipt':byte_identity(lookup_bytes),'lookup_validation':eb['parent_public'],'R1_basis_source':'actual unchanged R1 _basis return inside lookup _basis','R1_receipt':byte_identity(r1_bytes),'R1_validation':lb['parent_public'],'helper_basis_source':'actual unchanged helper _checked return inside R1 _basis','helper_receipt':byte_identity(helper_bytes),'helper_validation':rb['parent_public'],'deeper_public_predecessor':hb['public_predecessor'],'contexts':plan['contexts'],'thin_fast_decref_return_enter_lookup_R1_helper_validate_wrappers_called':False,'meaning':'Unchanged substantive authentication and receipt comparisons, actual returned objects. No stub, serialized basis or saved PASS substitution.'})
 derived=m.enc(m._assemble(basis));need(derived==expected,'ACTUAL-RES-NULL-ASSEMBLY-RECEIPT');agreements['res_null']=True
 with (out/'actual-derived-receipt.json').open('xb') as f:f.write(derived);f.flush();os.fsync(f.fileno())
 r.save('actual-receipt-comparison.json',{'result':'PASS','expected':byte_identity(expected),'actual':byte_identity(derived),'contexts':public['contexts'],'layer':'actual public validation and byte-for-byte assembly from actual returned authenticated basis','full_public_negative_derivations':0})
 need(count(root/'code/correspondence.py')==1,'RES-NULL-PUBLIC-CALL-COUNT')
 constructed_calls=sum(v for k,v in observer.entered.items() if k.startswith('code/correspondence.py::_construct_checked:'))
 need(constructed_calls==0,'UNEXPECTED-NEW-AUTHENTICATED-CONSTRUCTED-PATH')
 for name,path in [('fast',fast_path),('decref',decref_path),('return',return_path),('enter',enter_path),('lookup',lookup_path),('R1',r1_path),('helper',helper_path)]:need(count(path/'code/correspondence.py')==0,'UNEXPECTED-'+name+'-THIN-WRAPPER-CALL')
 r.event('res-null-full-public-positive-complete',result='PASS',contexts=public['contexts'],receipt=byte_identity(derived))
except BaseException as e:failure={'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()}
finally:
 signal.setitimer(signal.ITIMER_REAL,0)
 if observer is not None:
  try:observer.close()
  except BaseException as e:failure={'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'during':'observer cleanup','previous':failure}
 try:r.save('final-root.json',exact_tree(root,json.loads((workspace/'expected/ASSEMBLED-ROOT-MANIFEST.json').read_bytes())))
 except BaseException as e:failure={'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'during':'final byte audit','previous':failure}
 r.save('calls.json',calls)
 passed=failure is None and basis_capture and all(agreements.values())
 r.save('RESULT.json',{'attempt':plan['attempt'],'result':'PASS' if passed else 'FAILED-ATTEMPT','failure':failure,'public_result':public,'actual_returned_basis_captured':basis_capture,'receipt_agreements':agreements,'res_null_public_call_count':count(root/'code/correspondence.py'),'thin_wrapper_calls':{'fast':count(fast_path/'code/correspondence.py'),'decref':count(decref_path/'code/correspondence.py'),'return':count(return_path/'code/correspondence.py'),'enter':count(enter_path/'code/correspondence.py'),'lookup':count(lookup_path/'code/correspondence.py'),'R1':count(r1_path/'code/correspondence.py'),'helper':count(helper_path/'code/correspondence.py')},'full_public_positive':1 if passed else 0,'full_public_negative_derivations':0,'focused_checks_replayed':0,'historical_checks_replayed':0,'finished_utc':now(),'seconds':time.monotonic()-start,'independent_acceptance':'PENDING','actual_admission':False,'new_authenticated_constructed_call_count':constructed_calls,'authenticated_constructed_path':'UNEXECUTED' if constructed_calls==0 else 'UNESTABLISHED; inspect failure and counts','qualification':'Free monitoring slots alone do not establish complete event/callback cleanup; no application/helper/method execution, descriptor/file effects or new host qualification.'})
if failure:raise SystemExit(1)
