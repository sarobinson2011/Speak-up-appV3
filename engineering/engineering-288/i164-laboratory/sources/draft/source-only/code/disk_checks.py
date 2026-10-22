import json,pathlib,sys,shutil
import scope_integration as s
out=pathlib.Path(sys.argv[1]);fixture=pathlib.Path(sys.argv[2]);fixture.mkdir();origin=s.P
shutil.copytree(origin/'scope',fixture/'scope');shutil.copytree(origin/'universe',fixture/'universe');s.P=fixture
rows=[]
def rejects(n,fn):
 try:fn()
 except (ValueError,FileNotFoundError) as e:rows.append({'case':n,'status':'PASS','rejection':str(e)})
 else:raise AssertionError(n)
s.verified_inputs();rows.append({'case':'copied recovered companion inputs accepted','status':'PASS'})
f=fixture/'scope/remaining-obligations.json';b=f.read_bytes();f.unlink();rejects('missing actual obligation file',s.verified_inputs);f.write_bytes(b)
f.write_bytes(b+b' ');rejects('altered actual obligation bytes',s.verified_inputs);f.write_bytes(b)
p=fixture/'scope/MANIFEST.json';b=p.read_bytes();p.write_bytes(b+b' ');rejects('altered manifest cannot supply new expectations',s.verified_inputs);p.write_bytes(b)
p=fixture/'scope/unsupported-exclusion.json';p.write_text('{}');rejects('unexpected input member',s.verified_inputs);p.unlink()
s.verified_inputs();rows.append({'case':'restored byte-exact inputs accepted','status':'PASS'});s.P=origin
out.write_text(json.dumps(rows,indent=2));print('PASS',len(rows),'disk/recovered-input checks')
