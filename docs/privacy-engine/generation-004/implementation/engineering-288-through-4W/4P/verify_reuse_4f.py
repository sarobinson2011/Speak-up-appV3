"""Verify saved parent/member identities; never regenerate the model or streams."""
import hashlib,json,zipfile
from pathlib import Path
from ledger_kernel.retained import archive,sha,PINS
ROOT=Path(__file__).resolve().parent

def main():
    parent=ROOT/'retained/Engineering-288-checkpoint-4E.zip';expected='02b231f4ef29f38f73dd862fcaf9771fca3827d3d251f87be95088f29b4a108e'
    assert sha(parent)==expected
    protected=('accepted/','v4_ingest/','scope_auth/','ledger_kernel/','admission_kernel/','link_stream/','link_recovery/','inputs/')
    rows=[]
    with zipfile.ZipFile(parent) as z:
        manifest=json.loads(z.read('Engineering-288-checkpoint-4E/PACKAGE-MANIFEST.json'))
        for e in manifest['files']:
            if e['path'].startswith(protected):
                p=ROOT/e['path'];assert p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],e['path'];rows.append(e)
    ancestors=[]
    for stage in PINS:
        p=archive(stage);ancestors.append({'checkpoint':stage,'bytes':p.stat().st_size,'sha256':sha(p)})
    with zipfile.ZipFile(archive('2')) as z:
        names=[n for n in z.namelist() if n.endswith('.zip') and 'checkpoint-1' in n];assert len(names)==1
        raw=z.read(names[0]);h=hashlib.sha256(raw).hexdigest();assert h=='2e3d0c30d9ae260ede5f2915e61b1711c4cc4f84623cf3215fbf10afeb950719';ancestors.append({'checkpoint':'1','bytes':len(raw),'sha256':h})
    u=json.loads((ROOT/'inputs/universe.json').read_bytes())
    report={'result':'PASS','parent_4E_sha256':expected,'protected_files_unchanged':rows,'retained_ancestors':ancestors,'canonical_model':u['model_input'],'selected_contract_sha256':u['selected_contract_sha256'],'potential_pairs':u['potential_pairs'],'binary_stream_sha256':None,'full_link_stream_sha256':None,'expansion_rerun':False,'full_stream_processed':False}
    (ROOT/'results/4F-source-input-manifest.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'result':'PASS','protected_files':len(rows),'ancestors':len(ancestors)}))
if __name__=='__main__':main()
