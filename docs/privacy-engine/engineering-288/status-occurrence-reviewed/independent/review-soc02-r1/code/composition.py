from pathlib import Path
import zipfile,io,json,hashlib,sys
r=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def archive(b):
 with zipfile.ZipFile(io.BytesIO(b)) as z:return {n:z.read(n) for n in z.namelist()}
priorraw=(r/'inputs/independent-review.zip').read_bytes()
assert identity(priorraw)=={'bytes':21550943,'sha256':'62340d3d729c6fd3caf5a204a55ecf82efbd3b3955c5f466609ff36792f6d8e5'}
prior=archive(priorraw);old=archive(prior['input/I164-SOC01-SOC02-correction.zip'])
checks=[]
def compare(prefix,expected):
 actual={p.relative_to(r/prefix).as_posix():p.read_bytes() for p in (r/prefix).rglob('*') if p.is_file()}
 assert actual==expected,prefix
 checks.append({'path':prefix,'exact_files':len(actual)})
compare('review',{n:b for n,b in prior.items() if not n.startswith('input/')})
compare('original',{'code/smoke_occurrences.py':old['corrected/code/smoke_occurrences.py']})
expected={n[len('corrected/'):]:b for n,b in old.items() if n.startswith('corrected/')}
expected['code/smoke_occurrences.py']=(r/'corrected/code/smoke_occurrences.py').read_bytes();compare('corrected',expected)
c=archive(expected['inputs/correction.zip']);compare('corrected/retained/correction',c)
pins=json.loads((r/'CHANGED-IDENTITIES.json').read_bytes());assert identity(expected['code/smoke_occurrences.py'])==pins['implementation_change']['after']
assert identity(old['corrected/code/smoke_occurrences.py'])==pins['implementation_change']['before']
assert identity(expected['results/occurrence-connection.json'])==pins['unchanged_receipt']
supplied=[]
for folder in ('fresh','recovered'):
 d=json.loads((r/'results'/folder/'RESULT.json').read_bytes());assert d['passed']==len(d['checks'])==35
 assert d['source_before']==d['source_after']==pins['implementation_change']['after'] and d['source_stable']
 supplied.append({'folder':folder,'controls':35,'reproductions':d['residuals_reproduced'],'inspected_not_run':True})
maps={n:len(json.loads(c['retained/launcher/provenance/'+n+'-members.json'])) for n in ('candidate','draft')}
assert maps=={'candidate':666,'draft':163}
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps({'result':'PASS','composition':checks,'intentional_change':pins,'supplied':supplied,'unchanged_identity_maps':maps,'scope':'byte continuity to completed prior review, not a completed-review rerun'},indent=2)+'\n')
print(json.dumps({'result':'PASS','composition':checks}))
