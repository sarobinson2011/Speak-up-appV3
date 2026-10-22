"""Physical source-site census; never an execution, occurrence or custody claim."""
import ast, hashlib
from pathlib import Path
# Explicit admitted Python syntax. New syntax must receive a reviewable classification.
SYNTAX=frozenset('Add And Assign Attribute AugAssign BinOp BitAnd BoolOp Call ClassDef Compare Constant Continue Dict DictComp Div Eq ExceptHandler Expr FloorDiv For FunctionDef GeneratorExp Gt GtE If IfExp Import ImportFrom In Is IsNot List ListComp Load Lt LtE Module Mult Name Not NotEq NotIn Or Pow Raise Return Set SetComp Slice Store Sub Subscript Try Tuple UnaryOp With Yield alias arg arguments comprehension keyword withitem'.split())
FORMS=frozenset('Dict DictComp ListComp SetComp GeneratorExp If IfExp Compare BoolOp'.split())
PATHS=('support/reference/runtime/authority.py','support/reference/runtime/accounting.py','support/reference/runtime/ownership.py')
def site(n):
 return [n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__]
def census(raw,path):
 tree=ast.parse(raw);text=raw.decode();rows=[]
 unknown=sorted({type(n).__name__ for n in ast.walk(tree)}-SYNTAX)
 if unknown:raise ValueError('UNSUPPORTED-RUNTIME-SYNTAX:'+','.join(unknown))
 def walk(n,scope,assignment):
  if isinstance(n,(ast.FunctionDef,ast.ClassDef)):scope=scope+[n.name]
  if isinstance(n,ast.Assign):assignment=[ast.unparse(t) for t in n.targets]
  kind=type(n).__name__
  if kind in FORMS:
   role=('LAB-KEY-SEED-DERIVATION' if assignment==['SEEDS'] and scope==[] else 'LAB-PUBLIC-KEY-DERIVATION' if assignment==['PUB'] and scope==[] else 'GUARD-EXPRESSION' if kind in ['If','IfExp','Compare','BoolOp'] else 'COMPREHENSION-CONSTRUCTION' if kind!='Dict' else 'DICTIONARY-CONSTRUCTION')
   rows.append({'source':path,'sha256':hashlib.sha256(raw).hexdigest(),'site':site(n),'scope':scope or ['<module>'],'assignment':assignment,'kind':kind,'expression':ast.get_source_segment(text,n),'role':role,'occurrence_status':'NOT-INFERRED; emitted fields separately source-checked','qualified_evidence':False,'coverage_obligation':'syntax-site inventory only; control-flow/emission association proof remains unresolved'})
  for child in ast.iter_child_nodes(n):walk(child,scope,assignment)
 walk(tree,[],[])
 # Independent traversal: required physical sites derived directly from module AST.
 expected=sorted(site(n) for n in ast.walk(tree) if type(n).__name__ in FORMS)
 actual=sorted(r['site'] for r in rows)
 if actual!=expected or len(actual)!=len({tuple(s) for s in actual}):raise ValueError('RUNTIME-SITE-COVERAGE')
 return sorted(rows,key=lambda r:r['site'])
def inventory(root):
 return [r for p in PATHS for r in census((Path(root)/p).read_bytes(),p)]
def validate(root,rows):
 # A supplied expected-list, prior success or mutable inventory cannot remove a site.
 if rows!=inventory(root):raise ValueError('RUNTIME-INVENTORY-SUBSTITUTION')
 return True
