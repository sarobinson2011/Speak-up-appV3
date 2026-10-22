"""Read-only selected predecessor acquisition. Never decompress the model or streams."""
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,b):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def js(p,v):save(p,(json.dumps(v,sort_keys=True,indent=2)+'\n').encode())
p=ROOT.parent/'historical_input/Engineering-288B-I164-review-corrected.zip'
assert p.stat().st_size==261512053 and sha(p.read_bytes())=='d5cf60d0455ecd6bdbdda8cb78f5486df5a1f81a6cc52fa02d6a122bc75e0030'
z=zipfile.ZipFile(p);prefix='Engineering-288B-I164-review-corrected/';manifest=json.loads(z.read(prefix+'MANIFEST.json'))['files'];picked={}
def take(n):
 b=z.read(prefix+n);v=manifest[n];assert len(b)==v['bytes'] and sha(b)==v['sha256'],n
 save('native/'+n,b);picked[n]=v;return b
sel=json.loads((ROOT/'support/provenance/SELECTED-PROVENANCE.json').read_bytes())
for v in sel['manifest_verified_selected']:
 b=take(v['member']);assert len(b)==v['bytes'] and sha(b)==v['sha256']
for n in ['retained/registers/custody.tsv','candidate/ledger/binding.json','candidate/ledger/node-duties.jsonl.gz','records/surface-delta.json','records/approval.json','records/candidate-delta.json','prior-code/model_kernel/catalog.py','retained/mapping/records/relationships-43.json']:
 take(n)
fields=json.loads((ROOT/'native/retained/registers/fields.json').read_bytes())+json.loads((ROOT/'native/records/added-fields.json').read_bytes())
for n in sorted(manifest):
 if n.startswith('sources/') or n in ['retained/candidate/custody-binding.json','retained/candidate/profile-binding.json']:
  take(n)
source_map=[]
for path,h in sorted(set((r['source_file'],r['source_sha256']) for r in fields)):
 matches=sorted(n for n,v in manifest.items() if v['sha256']==h)
 assert matches, (path,h)
 actual=next((n for n in matches if n.endswith(path)),matches[0]);take(actual)
 source_map.append({'native_reference':path,'sha256':h,'verified_archive_member':actual})
js('provenance/native-sources.json',source_map)
js('provenance/inheritance.json',{'archive':{'name':p.name,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'identity_basis':'retained retrieval identity; not original publication identity'},'members':picked,'canonical_prospective_registration':False})
# Read actual historical 90-file evidence from the reviewed retry input, without executing it.
p=ROOT.parent/'inputs/Formal-Lab-Engineering-288C-I164-prospective-retries-review(1).zip'
assert p.stat().st_size==6814208 and sha(p.read_bytes())=='f5e83e6aa463b6a0bfa53b1da65e1d9d56d066f72506ae3f98db9252aab2324f'
z=zipfile.ZipFile(p);prefix='Formal-Lab-Engineering-288C-I164-prospective-retries-review/'
inv=json.loads((ROOT/'support/provenance/historical-hashes.json').read_bytes())['files'];receipt=[]
for n,h in inv.items():
 b=z.read(prefix+'input/checkpoint/'+n);assert sha(b)==h,n
 save('historical90/'+n,b);receipt.append({'path':n,'bytes':len(b),'sha256':h})
js('provenance/historical90.json',{'review_archive_sha256':sha(p.read_bytes()),'fresh_read_only':True,'files':receipt})
for n in ['REPORT.md','SOURCE-REFERENCES.json','input/RECOVERY-MANIFEST.json']:
 save('provenance/retry-review/'+n,z.read(prefix+n))
print('Verified native selected members',len(picked),'source references',len(source_map),'historical files',len(receipt))
