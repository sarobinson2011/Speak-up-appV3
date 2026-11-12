"""New one-attempt service; reused unchanged runtime/observer/supervisor guards."""
from pathlib import Path
import sys,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common_r1 import *
w=Path(sys.argv[1]).resolve();plan=json.loads((w/'PLAN.json').read_bytes());rc=1
try:
 # Recheck every original preparation member before a child can start. Runtime
 # outputs and recovered inputs are deliberately outside this fixed membership.
 for n,pin in json.loads((w/'MANIFEST.json').read_bytes()).items():need(identity(w/n)==pin,'SERVICE-PREPARATION-BYTES:'+n)
 p=load('runtime_profile').check(w/'observer-reference',json.loads((w/'code/expected-runtime.json').read_bytes()))
 save(w/'service-runtime-profile.json',p);need(p['matches'],'SERVICE-RUNTIME-MISMATCH')
 save(w/'service-root-verification.json',exact_tree(w/'candidate',json.loads((w/'expected/ASSEMBLED-ROOT-MANIFEST.json').read_bytes())))
 need(identity(w/'expected/expected-exit-decref-receipt.json')==plan['expected_receipt'],'SERVICE-EXPECTED-RECEIPT')
 load('recovery').verify_harness(w/'observer-reference')
 s=load('supervisor');rc=s.run(w/'validation/process',plan['hard_seconds'],[sys.executable,'-I','-B',str(w/'code/public_positive.py'),str(w)],plan['attempt']+'; exactly one new exit-decref-attempt public positive; no focused or historical replays')
 result_path=w/'validation/results/RESULT.json'
 if result_path.is_file():
  result=json.loads(result_path.read_bytes());ex=json.loads((w/'validation/process/exit.json').read_bytes());passed=bool(rc==0 and ex['child_exit']==0 and not ex['timed_out'] and ex['supervisor_failure'] is None and result['result']=='PASS' and result['exit_decref_public_call_count']==1 and result['actual_returned_basis_captured'] and result['new_authenticated_constructed_call_count']==0 and all(result['receipt_agreements'].values()) and all(v==0 for v in result['thin_wrapper_calls'].values()))
  save(w/'validation/RECONCILIATION.json',{'status':'PASS' if passed else 'FAILED-OR-QUALIFIED','attempt':plan['attempt'],'child_exit':ex,'result_identity':identity(result_path),'exactly_one_exit_decref_public_call':result['exit_decref_public_call_count']==1,'expected_receipt':plan['expected_receipt'],'full_public_negative_derivations':0,'independent_acceptance':'PENDING','admission':False})
  if not passed:rc=1
 else:save(w/'validation/RECONCILIATION-FAILURE.json',{'status':'MISSING-RESULT','no_completion_inferred':True});rc=1
except BaseException as e:
 save(w/'service-failure.json',{'utc':now(),'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()});rc=1
save(w/'service-exit.json',{'utc':now(),'exit':rc,'meaning':'Service wrapper only; public result and supervisor/manager exits remain separate'})
raise SystemExit(rc)
