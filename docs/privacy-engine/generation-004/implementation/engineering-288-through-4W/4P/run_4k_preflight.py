"""Bounded full retained index only: tiny supplied input, no pair enumeration."""
import json,subprocess,sys,time,hashlib
from pathlib import Path
from link_stream.cli import prepare,DESC,native
from v4_ingest.wire import LINK_HEADER
ROOT=Path(__file__).resolve().parent

def main():
 p=ROOT/'work/4K-preflight';p.mkdir(parents=True,exist_ok=True)
 tiny=p/'header.tsv';tiny.write_bytes(('\t'.join(LINK_HEADER)+'\n').encode())
 start=time.monotonic();desc=prepare();r=native(tiny,desc,DESC,hashlib.sha256(tiny.read_bytes()).hexdigest(),65536,1048576,50)
 assert r['model_tokens']==426984 and r['expected_potential_rows']==91157453467
 assert not r['complete'] and r['failure']['code']=='INCOMPLETE-EVIDENCE-UNIVERSE'
 r.update({'result_meaning':'PASS-FULL-RETAINED-INDEX-PREFLIGHT; EXPECTED-INCOMPLETE-HEADER-ONLY-INPUT','descriptor_bytes':desc.stat().st_size,'wall_seconds':time.monotonic()-start,'full_stream_processed':False,'potential_rows_enumerated':0,'active_contract':'rebinding/selected-contract.json','active_contract_sha256':hashlib.file_digest((ROOT/'rebinding/selected-contract.json').open('rb'),'sha256').hexdigest(),'model_provenance_binding':'rebinding/ledger/BINDING.json'})
 (ROOT/'results/4K-retained-index-preflight.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
