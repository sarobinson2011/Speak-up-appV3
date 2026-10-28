"""Static initial-HEAD type origin; no Authority or accounting code executes."""
from pathlib import Path
import ast,json,hashlib,sys
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]);p=root/'retained/config/retained/binding/retained/hf01/original/retained/references/retained/fields/retained/occurrence/retained/correction/retained/candidate/support/reference/runtime/authority.py'
raw=p.read_bytes();assert len(raw)==23223 and hashlib.sha256(raw).hexdigest()=='4565bb30cb637b3cef40a3f1da2b3722840b747ab110fa37eede0cbc2e3b313a'
owner=next(n for n in ast.parse(raw).body if isinstance(n,ast.ClassDef) and n.name=='Authority');init=next(n for n in owner.body if isinstance(n,ast.FunctionDef) and n.name=='__init__')
nodes=[n for n in ast.walk(init) if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='s'];assert len(nodes)==1;node=nodes[0]
def source_shape(n):
 if isinstance(n,ast.Dict):return {ast.literal_eval(k):source_shape(v) for k,v in zip(n.keys,n.values)}
 if isinstance(n,ast.Constant):return type(n.value).__name__
 if ast.unparse(n)=='self.binding':return 'str under unchanged reviewed binding-constructor premise'
 assert isinstance(n,ast.BinOp) and isinstance(n.op,ast.Mult) and isinstance(n.left,ast.Constant) and n.left.value=='0' and isinstance(n.right,ast.Constant) and type(n.right.value) is int and n.right.value==64
 return 'str'
shape=source_shape(node.value);receipt=json.loads((root/'results/state-correspondence.json').read_bytes())
def compare(value,expected):
 if type(expected) is dict:return type(value) is dict and set(value)==set(expected) and all(compare(value[k],v) for k,v in expected.items())
 return type(value).__name__==expected.split(' under ')[0]
for context in receipt['contexts']:assert compare(context['state_return_correspondence']['validated_state_anchor']['validated_state'],shape)
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps({'result':'PASS','source':{'path':p.relative_to(root).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},'constructor_assignment':ast.get_source_segment(raw.decode(),node),'source_derived_initial_shape':shape,'both_saved_contexts_match_shape':True,'classification':'STATIC SOURCE CHECK; not observed initialization or complete HEAD-state schema revalidation','unchanged_binding_type_support_reused':True},indent=2)+'\n');print('PASS static initial-HEAD type origin')
