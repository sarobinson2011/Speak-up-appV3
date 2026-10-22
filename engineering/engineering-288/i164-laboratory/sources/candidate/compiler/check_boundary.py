import sys,copy,json
from pathlib import Path
import compiler as m
c=m.setup(sys.argv[1]);r=Path(sys.argv[2]);out=[]
saved=json.loads((Path(sys.argv[3]) if len(sys.argv)>3 else Path(__file__).resolve().parents[1]/'preflight/result.json').read_bytes());m.same(c.binding,saved['binding'],'PREFLIGHT-EXACT-INPUTS');out.append({'check':'exact preflight candidate input bindings','result':'PASS'})
import static_declarations as sd
original=sd.schemas
g,o,p=original();g=copy.deepcopy(g);g['CONFIG']['version']={'unsupported_variant':True};sd.schemas=lambda:(g,o,p)
try:
 try:m.independent_coverage(c)
 except m.Invalid as e:out.append({'check':'unsupported defining schema construct','result':'PASS','rejection':str(e)})
 else:raise AssertionError('unsupported construct accepted')
finally:sd.schemas=original
compiled=m.compile_candidate(c)
# Exercise declaration-independent source membership once more after restoration.
a=m.independent_coverage(c);m.need(a['checked_families']==59 and len(a['runtime_body_fields'])==10,'coverage');out.append({'check':'restored independent coverage all ten method-body field sets','result':'PASS'})
r.write_bytes(m.enc({'checks':out,'count':len(out),'full_source_qualification':False}));print('PASS',len(out))
