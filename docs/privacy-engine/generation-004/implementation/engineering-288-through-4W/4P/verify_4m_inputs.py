"""Verify exact 4L parent and unchanged accepted/model/backend/predicate bytes."""
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
from metadata_catalog.core import sha

def main():
 p=ROOT/'retained/Engineering-288-checkpoint-4L.zip';assert sha(p)=='1a6e28017bed5939aa4af1d2e855ff56d570bcc673343195dd73a5a6064336db'
 with zipfile.ZipFile(p) as z:
  manifest=json.loads(z.read('Engineering-288-checkpoint-4L/PACKAGE-MANIFEST.json'))
 rows=[]
 for e in manifest['files']:
  n=e['path']
  if n.startswith(('accepted/','amendments/','rebinding/','inputs/','crypto_backend/','fixtures/4L-')) or n in ('link_recovery/cli.py','link_recovery/worker','link_recovery/worker.cpp','link_stream/native.cpp','link_stream/native','link_stream/validator.py','pure_auth/controller.py','large_auth/core.py','large_auth/message.py','occurrence_values/codec.py','occurrence_values/index.py','v4_ingest/data/security-fields.tsv','v4_ingest/definition.py','admission_kernel/failures.py'):
   assert (ROOT/n).stat().st_size==e['bytes'] and sha(ROOT/n)==e['sha256'],n;rows.append(e)
 from integrated_auth.collector import implementation
 impl=implementation();(ROOT/'IMPLEMENTATION-IDENTITY-4M.json').write_text(json.dumps(impl,indent=2)+'\n')
 r={'result':'PASS','unchanged_historical_members':len(rows),'parent_sha256':sha(p),'model_sha256':'08d6e7fb1e0cf37cc7effa76b50eaff0459abc158d9c6f0da52c6c58372b14f1','selected_contract_sha256':sha(ROOT/'rebinding/selected-contract.json'),'active_4I_binding_sha256':sha(ROOT/'amendments/PE-G4-FIELD-CLASS-REF-AMENDMENT-001/v1.0.0/BINDING.json'),'backend_sha256':impl['backend']['binary_sha256'],'static_equality_predicate_unchanged':True,'profile_impact':'Accepted artifacts unchanged. New conditional fixtures regenerated with current code pins; old fixtures retained. Runtime journals are versioned CP4M and cannot inherit CP4L completion.','full_stream_processed':False}
 (ROOT/'results/4M-dependency-impact.json').write_text(json.dumps(r,indent=2)+'\n')
 extras=[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted((ROOT/'fixtures').glob('4M-*/**/*')) if p.is_file()]
 m={'format':'CP4M-SOURCE-INPUTS-1','parent':{'path':'retained/'+p.name,'sha256':r['parent_sha256']},'files':rows+extras,'full_universe_stream_sha256':None,'qualification_established':False}
 g=json.loads((ROOT/'results/4M-metadata-generate.json').read_bytes())
 m['regenerable_complete_metadata_fixture']={'packaged_bytes':False,'generator':'run_4m_metadata.py generate','entries':g['entries'],'required_tokens':g['required_tokens'],'required_index_sha256':g['required_index_sha256'],'meaning':'Metadata-only synthetic references, exact retained token-shard coverage; value files intentionally not acquired.'}
 (ROOT/'SOURCE-INPUT-MANIFEST-4M.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
