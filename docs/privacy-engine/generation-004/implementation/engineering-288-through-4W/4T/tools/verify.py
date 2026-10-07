#!/usr/bin/env python3
import hashlib,json,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));import run_task as r
m=r.verify_package();actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=ROOT/'PACKAGE-MANIFEST.json'};assert actual=={e['path'] for e in m['files']}
a=r.read(ROOT/'bindings/ACTIVE-IDENTITIES.json');x=r.META
assert a['model_sha256']==x['candidate_model_sha256']=='dd946419e4fd4c657a0a0d663b145e958ddf3c4957bf006b94b5c3f7ec96e74d'
assert a['selected_contract_sha256']==x['selected_contract_sha256']==r.filehash(ROOT/'bindings/selected-contract.json')
assert r.filehash(ROOT/'inputs/prefix.bin')==x['prefix_table']['sha256'] and r.filehash(ROOT/'inputs/links.txt')==x['descriptor_sha256']
assert r.prefix(ROOT,0)==(0,67) and r.prefix(ROOT,r.PLAN['candidate_total'])==(r.PLAN['rows'],r.PLAN['serialized_bytes'])
assert r.PLAN['rows']==91161821721 and r.PLAN['serialized_bytes']==19909380154846
for f,h in r.read(ROOT/'bindings/IMPLEMENTATION.json')['native_and_controller_unchanged'].items():assert r.filehash(ROOT/f)==h
assert r.read(ROOT/'evidence/4S-receipt.json')['candidate_model']['sha256']==a['model_sha256']
assert not (ROOT/'runner/pairs').exists() and x['full_stream_sha256'] is None and m['full_stream_sha256'] is None
assert m['storage']['task_peak_bound_bytes_4KiB_blocks']<m['storage']['required_free_bytes']
print(json.dumps({'result':'PASS-FRESH-EXTRACTION-IDENTITIES','files':len(m['files']),'candidate_model_sha256':a['model_sha256'],'native_unchanged':True,'full_text_sha256':None,'actual_admission':False}))
