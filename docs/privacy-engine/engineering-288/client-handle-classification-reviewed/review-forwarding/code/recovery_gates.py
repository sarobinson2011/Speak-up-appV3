"""Current strict predecessor gate only; does not load any runtime or prior validator."""
from pathlib import Path
import json,types,hashlib,sys
w=Path(__file__).resolve().parents[2];out=w/'ch-review/results/recovery-gates.json';rows=[]
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
p=w/'ch-input/code/correspondence.py';m=types.ModuleType('review_gate');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__)
for root in ('ch-input','ch-recovered-2'):
 r=m.predecessor_root(w/root);assert r==w/root/'retained/handle';rows.append({'root':root,'result':'ACCEPTED','source':identity(p.read_bytes()),'prior_code_loaded':False})
try:m.predecessor_root(w/'ch-recovered')
except ValueError as e:
 assert str(e)=='CLIENT-UNDECLARED-OR-NONREGULAR';rows.append({'root':'ch-recovered','result':'REJECTED','error':str(e),'prior_code_loaded':False,'earlier_refusal_completed_assertions':0})
else:raise AssertionError('UNEXPECTED-ACCEPTANCE')
original=json.loads((w/'ch-review/failures/recovered-root-membership/PRESERVATION.json').read_bytes());item=original['unexpected'][0];b=(w/'ch-recovered'/item['path']).read_bytes();assert identity(b)=={k:item[k] for k in ('bytes','sha256')} and b==(w/'ch-review/failures/recovered-root-membership'/item['preserved']).read_bytes()
rows.append({'check':'original undeclared file preserved byte-exact','result':'PASS','identity':identity(b),'cause':'UNKNOWN','included_as_declared_recovery_input':False})
out.write_text(json.dumps({'result':'PASS','checks':rows,'no_predecessor_execution':True},indent=2)+'\n');print('PASS strict recovery gate; 2 declared roots accepted, refused root rejected; original bytes preserved')
