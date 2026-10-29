from pathlib import Path
import sys,copy,json,traceback,ast
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None;findings=[]
class S(str):pass
try:
 monitor=guard(root);m=module(root/'code/correspondence.py');monitor(m);d=m.inputs(root);cat=m.catalogue(d);c=d['coverage'];manager=ast.parse(m.inner(d)['manager']);node=next(n for owner in manager.body if isinstance(owner,ast.ClassDef) and owner.name=='ManagedAuthority' for n in owner.body if isinstance(n,ast.FunctionDef) and n.name=='status');ret=next(n for n in ast.walk(node) if isinstance(n,ast.Return));rec.check('manager status keys are exact builtin str literals',lambda:all(isinstance(k,ast.Constant) and type(k.value) is str for k in ret.value.keys))
 for case in json.loads((root/'fixtures/normal-cases.json').read_bytes())['cases']:
  p=copy.deepcopy(case['projection']);val={k:copy.deepcopy(v) for k,v in p.items() if k!='returned'};bad=copy.deepcopy(p);v=bad['returned'][1]['value'];bad['returned'][1]['value']={S(k) if k=='phase' else k:x for k,x in v.items()};key=next(k for k in bad['returned'][1]['value'] if k=='phase');assert type(key) is S and enc(bad)==enc(p)
  try:r=c.status_forward_projection(cat,bad,val)
  except ValueError as e:rec.row('return dictionary literal key exact type '+case['context'],'REJECTED',error=str(e))
  else:
   assert r['completion']=='normal-return';rec.row('return dictionary accepts nonliteral exact key type '+case['context'],'DEFECT-ACCEPTED');findings.append({'id':'IS-01','API':'status_forward_projection','context':case['context'],'mutation':'one return value dictionary phase key -> S(str) with same text','value_container_exact_dict':True,'field_values_unchanged':True,'key_exact_str':False,'source_key_is_exact_str_literal':True,'serialization_equal':True,'normal_return_accepted':True})
 rec.save('key-type-witnesses.json',findings)
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,findings=findings)
