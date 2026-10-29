from pathlib import Path,PurePosixPath
import sys,json,ast
sys.path.insert(0,str(Path(__file__).resolve().parent))
from integrity import check_tree,ident
root=Path(sys.argv[1]);m=json.loads((root/'MANIFEST.json').read_bytes());names=set(m)|{'MANIFEST.json'};dirs={str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'};check_tree(root,names,dirs,m,ident((root/'MANIFEST.json').read_bytes()))
def one(name):
 p=list(root.rglob(name));assert len(p)==1;return p[0]
p=one('prospective_entry.py');raw=p.read_bytes();t=ast.parse(raw);route=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='_run');control=next(n for n in t.body if isinstance(n,ast.ClassDef) and n.name=='_Control');method=next(n for n in control.body if isinstance(n,ast.FunctionDef) and n.name=='status');parents={c:(n,field) for n in ast.walk(t) for field,v in ast.iter_fields(n) for c in (v if isinstance(v,list) else [v]) if isinstance(c,ast.AST)}
def find(kind,expr):
 ns=[n for n in ast.walk(route) if isinstance(n,kind) and ast.unparse(n)==expr];assert len(ns)==1;return ns[0]
owner=find(ast.Assign,'owner = _Owner(wrapper)');token=find(ast.Assign,'token = object()');store=find(ast.Assign,'_OWNERS[token] = owner');call=find(ast.Call,'control(_Control(token))');revoke=find(ast.Call,'_OWNERS.pop(token, None)')
def chain(n):
 r=[]
 while n in parents:
  q,f=parents[n];r.append((q,f));n=q
 return r
assert any(isinstance(n,ast.If) and ast.unparse(n.test)=='control is not None' and field=='body' for n,field in chain(call))
assert any(isinstance(n,ast.Try) and field=='finalbody' for n,field in chain(revoke))
assert owner.lineno<=token.lineno<=store.lineno<call.lineno<revoke.lineno
assert [ast.unparse(n) for n in method.body]==['owner = _OWNERS.get(self.__token)','if owner is None:\n    _fail()','return owner.wrapper.status()']
assert not any(isinstance(n,ast.Try) for n in ast.walk(method))
fail=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='_fail');r=fail.body[0];assert isinstance(r,ast.Raise) and ast.unparse(r.exc.func)=='ClientFailure' and ast.literal_eval(r.cause) is None
out={'result':'PASS','source':{'path':p.relative_to(root).as_posix(),**ident(raw)},'control_handoff_condition':'control is not None','token_creation':'object()','token_to_owner_map':'_OWNERS[token] = owner','owner_guard':'owner is None','owner_failure_guard':False,'READY_guard':False,'revoke_in_finally':True,'no_forwarder_catch':True,'fixed_failure':{'class':'ClientFailure','message':ast.literal_eval(r.exc.args[0]),'explicit_cause':None,'ambient_context_absence_inferred':False},'positions':{k:{'line':v.lineno,'end_line':v.end_lineno,'expression':ast.get_source_segment(raw.decode(),v)} for k,v in [('owner',owner),('token',token),('store',store),('control_call',call),('revoke',revoke)]},'runtime_execution':False}
Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print('PASS independent control handoff, owner/token guard and finally revocation audit')
