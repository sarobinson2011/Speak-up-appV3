"""Offline expected output only; never calls inputs/_basis/derive/public validate.

The assembly dictionary is expected-output data, not an authenticated basis.
It is never sent to the future public harness as a basis or a validation result.
"""
import importlib.util,json,sys,hashlib
from pathlib import Path
sys.dont_write_bytecode=True
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def assemble(root,retained_public_result):
 root=Path(root);c=load(root/'code/managed_coverage.py','enter_return_offline_producer');a=load(root/'code/correspondence.py','enter_return_offline_adapter')
 raw=(root/'reference/enter/actual-receipt.json').read_bytes();assert a.identity(raw)==a.PARENT_RECEIPT
 prior=json.loads(raw);source=(root/'source-evidence/lab_bootstrap.py').read_bytes();bc=(root/'reference/cpython-3.12.14/bytecodes.c').read_bytes();tt=(root/'reference/cpython-3.12.14/typeobject.c').read_bytes()
 assert [r['context'] for r in prior['contexts']]==list(a.CONTEXTS)
 cats=[c.compile_enter_return(source,bc,tt,x['open_return_context_operand_correspondence']['declaration'],x['context_special_lookup_correspondence']['declaration'],x['enter_call_attempt_correspondence']['declaration']) for x in prior['contexts']]
 assert a.enc(cats[0])==a.enc(cats[1])
 public=json.loads(Path(retained_public_result).read_bytes());assert public=={'result':'PASS','contexts':list(a.CONTEXTS),'receipt':a.PARENT_RECEIPT,'actual_admission':False}
 expected_data={'fresh':{'root':root},'prior':prior,'catalogue':cats[0],'parent_public':public}
 return a.enc(a._assemble(expected_data))
if __name__=='__main__':
 data=assemble(sys.argv[1],sys.argv[2])
 with Path(sys.argv[3]).open('xb') as f:f.write(data)
 print(json.dumps({'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'role':'OFFLINE EXPECTED OUTPUT ONLY','public_calls':0,'authentication_calls':0,'authenticated_basis_captures':0}),flush=True)
