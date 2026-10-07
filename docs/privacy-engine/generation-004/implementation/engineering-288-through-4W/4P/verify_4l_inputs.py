"""Verify historical normative identities and current implementation dependencies."""
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()

def main():
 parent=ROOT/'retained/Engineering-288-checkpoint-4K.zip'
 assert sha(parent)=='d4b75689e3531b890511e46ecdef5ba1298620e45152076bf05f867857abcb4d'
 with zipfile.ZipFile(parent) as z:
  assert z.testzip() is None
  prior=json.loads(z.read('Engineering-288-checkpoint-4K/PACKAGE-MANIFEST.json'))
 rows=[]
 for e in prior['files']:
  name=e['path']
  if name.startswith(('accepted/','amendments/','rebinding/','inputs/','crypto_backend/','fixtures/4K-','fixtures/4J-','fixtures/4I-','fixtures/4H-')) or name in ('link_recovery/cli.py','link_recovery/worker.cpp','link_recovery/worker','pure_auth/controller.py','large_auth/message.py','v4_ingest/data/security-fields.tsv','v4_ingest/definition.py'):
   assert (ROOT/name).stat().st_size==e['bytes'] and sha(ROOT/name)==e['sha256'],name
   rows.append(e)
 from integrated_auth.collector import implementation
 impl=implementation();(ROOT/'IMPLEMENTATION-IDENTITY-4L.json').write_text(json.dumps(impl,indent=2)+'\n')
 report={'result':'PASS','preserved_historical_members':len(rows),'active_4I_amendment_unchanged':True,'model_sha256':'08d6e7fb1e0cf37cc7effa76b50eaff0459abc158d9c6f0da52c6c58372b14f1','selected_contract_sha256':sha(ROOT/'rebinding/selected-contract.json'),'retained_index_sha256':sha(ROOT/'inputs/links.txt'),'backend_sha256':impl['backend']['binary_sha256'],'source_model_contract_profile_change':'Normative/model/contract unchanged. Current laboratory fixture code pins and resulting profile/object/signature identities regenerated; old fixtures retained as history. Runtime receipt bindings changed deliberately; old running jobs cannot be resumed as CP4L.','expansion_rerun':False,'full_stream_processed':False}
 (ROOT/'results/4L-dependency-impact.json').write_text(json.dumps(report,indent=2)+'\n')
 extra=[]
 for pattern in ('fixtures/4L-*/**/*',):
  for p in sorted(ROOT.glob(pattern)):
   if p.is_file():extra.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)})
 manifest={'format':'CP4L-SOURCE-INPUTS-1','files':rows+extra,'parent':{'path':str(parent.relative_to(ROOT)),'bytes':parent.stat().st_size,'sha256':sha(parent)},'full_universe_stream_digest':None,'qualification_established':False}
 (ROOT/'SOURCE-INPUT-MANIFEST-4L.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
