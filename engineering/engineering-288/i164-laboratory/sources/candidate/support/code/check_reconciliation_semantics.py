"""Self-consistent synthetic pins isolate semantic rejection from hash rejection."""
import tempfile,shutil,copy
from common import *
from reconcile_baseline import reconcile
source=ROOT/'results/reconciliation-fixture';original=parse((ROOT/'results/fixture-pin.json').read_bytes());results=[]
def repin(root):
 a=copy.deepcopy(original);base=root/'baseline';m=parse((base/'manifest.json').read_bytes())
 def update(directory,m):
  for n in m['files']:
   raw=(directory/n).read_bytes();m['files'][n]={'bytes':len(raw),'sha256':sha(raw)}
 update(base,m);raw=enc(m);(base/'manifest.json').write_bytes(raw);a['baseline_manifest_sha256']=head=sha(raw);current={r['id']:r for r in parse((base/'register/fields.json').read_bytes())};a['delta_sha256']=[]
 for i in [1,2]:
  droot=root/'deltas'/str(i).zfill(6);d=parse((droot/'manifest.json').read_bytes());update(droot,d);d.update(previous=head,baseline=a['baseline_manifest_sha256']);current.update({r['id']:r for r in parse((droot/'added-fields.json').read_bytes())});d['after_classes_sha256']=sha(enc([current[k] for k in sorted(current)]));raw=enc(d);(droot/'manifest.json').write_bytes(raw);head=sha(raw);a['delta_sha256'].append(head)
 a['head']=head;return enc(a)
cases=[('duplicate','baseline/register/fields.json',lambda r:r+r,'DUPLICATE-CLASS'),('conflict','deltas/000002/added-fields.json',lambda r:[dict(r[0],id='FIXTURE:ROOT')],'CLASS-CONFLICT'),('parent','deltas/000002/added-fields.json',lambda r:[dict(r[0],parent='MISSING')],'DELTA-PARENT'),('cycle','deltas/000002/added-fields.json',lambda r:[dict(r[0],parent=r[0]['id'])],'PARENT-CYCLE'),('source','deltas/000002/added-fields.json',lambda r:[dict(r[0],source_sha256=ZERO)],'CLASS-SOURCE'),('type','deltas/000002/added-fields.json',lambda r:[dict(r[0],type=3)],'DECLARATION-TYPE')]
for name,path,mut,error in cases:
 with tempfile.TemporaryDirectory() as td:
  root=Path(td)/'input';shutil.copytree(source,root);p=root/path;p.write_bytes(enc(mut(parse(p.read_bytes()))));pin=repin(root)
  try:reconcile(root,pin,sha(pin))
  except Invalid as e:need(error in str(e),'WRONG-BOUNDARY:'+str(e));results.append({'name':name,'status':'PASS','rejection':str(e)})
  else:raise AssertionError('accepted '+name)
(ROOT/'results/reconciliation-semantic-checks.json').write_bytes(enc(results));print(len(results),'semantic controls passed')
