"""Parent and protected-source continuity; no model expansion/full stream reads."""
import hashlib,json,zipfile
from pathlib import Path
from ledger_kernel.retained import sha
ROOT=Path(__file__).resolve().parent

def main():
    p=ROOT/'retained/Engineering-288-checkpoint-4F.zip';pin='905e2e55a0826adbcd339b1c8f2cf0150256c47060cd3d241a5fa3a57756cbb4';assert sha(p)==pin
    rows=[]
    with zipfile.ZipFile(p) as z:
        m=json.loads(z.read('Engineering-288-checkpoint-4F/PACKAGE-MANIFEST.json'))
        for e in m['files']:
            if e['path'].startswith(('accepted/','v4_ingest/','ledger_kernel/','scope_auth/','admission_kernel/','link_stream/','link_recovery/','large_auth/','inputs/')) or e['path']=='fixtures/construct.py':
                f=ROOT/e['path'];assert f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],e['path'];rows.append(e)
    u=json.loads((ROOT/'inputs/universe.json').read_bytes())
    r={'result':'PASS','parent_sha256':pin,'protected_files_unchanged':rows,'model':u['model_input'],'selected_contract_sha256':u['selected_contract_sha256'],'potential_pairs':u['potential_pairs'],'binary_stream_sha256':None,'full_link_stream_sha256':None,'expansion_rerun':False,'full_retained_stream_processed':False}
    (ROOT/'results/4G-source-input-manifest.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'result':'PASS','protected_files':len(rows)}))
if __name__=='__main__':main()
