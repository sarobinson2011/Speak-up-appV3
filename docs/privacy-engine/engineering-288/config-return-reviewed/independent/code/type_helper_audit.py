"""Static defining-type audit; never executes Authority or opens a database."""
from pathlib import Path
import ast,hashlib,json,sys
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]);expected='4565bb30cb637b3cef40a3f1da2b3722840b747ab110fa37eede0cbc2e3b313a'
p=root/'retained/binding/retained/hf01/original/retained/references/retained/fields/retained/occurrence/retained/correction/retained/candidate/support/reference/runtime/authority.py'
b=p.read_bytes();assert len(b)==23223 and hashlib.sha256(b).hexdigest()==expected
functions={x.name:x for x in ast.parse(b).body if isinstance(x,ast.FunctionDef)}
expected_functions={
 'exact':"def exact(x,keys):need(type(x) is dict and set(x)==set(keys),'FIELDS')",
 'integer':"def integer(x,lo,hi):need(type(x) is int and lo<=x<=hi,'INTEGER');return x",
 'label':"def label(x):need(type(x) is str and 0<len(x)<=128,'LABEL');return x",
 'digest':"def digest(x):need(type(x) is str and len(x)==64 and all(c in '0123456789abcdef' for c in x),'DIGEST');return x"}
for name,source in expected_functions.items():assert ast.dump(functions[name],include_attributes=False)==ast.dump(ast.parse(source).body[0],include_attributes=False)
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps({'result':'PASS','authority':{'path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':expected},'functions':{n:ast.get_source_segment(b.decode(),functions[n]) for n in expected_functions},'source_analysis_only':True,'new_assertion_group':1,'does_not_replace_predecessor_value_and_binding_validation':True},indent=2)+'\n')
print('PASS source helper exact-type audit')
