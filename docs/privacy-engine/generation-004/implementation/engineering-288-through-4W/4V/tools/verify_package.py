#!/usr/bin/env python3
import argparse,hashlib,json,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def verify(root):
 m=json.loads((root/'PACKAGE-MANIFEST.json').read_bytes());seen=set()
 for x in m['files']:
  p=Path(x['path']);assert not p.is_absolute() and '..' not in p.parts and x['path'] not in seen;seen.add(x['path']);q=root/p;assert not q.is_symlink() and q.stat().st_size==x['bytes'] and sha(q)==x['sha256'],str(p)
 actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='PACKAGE-MANIFEST.json'}
 assert actual==seen,'exact package membership'
 retained=json.loads((root/'evidence/RETAINED-IDENTITIES.json').read_bytes())
 for x in retained:assert (root/x['path']).stat().st_size==x['bytes'] and sha(root/x['path'])==x['sha256'],x['path']
 with zipfile.ZipFile(root/'evidence/Engineering-288-checkpoint-4U.zip') as z:
  old=json.loads(z.read('Engineering-288-checkpoint-4U/PACKAGE-MANIFEST.json'))
  for x in old['files']:
   with z.open('Engineering-288-checkpoint-4U/'+x['path']) as f:assert hashlib.file_digest(f,'sha256').hexdigest()==x['sha256']
 e=json.loads((root/'evidence/TEXTUAL-IDENTITY.json').read_bytes());b=json.loads((root/'ACTIVE-BINDINGS.json').read_bytes())
 assert b['model_sha256']==e['binding']['model_sha256'] and b['contract_sha256']==e['binding']['selected_contract_sha256']
 assert b['descriptor_sha256']==e['exact_inputs']['descriptor']['sha256'] and b['expected_text']==e['identity']
 assert b['actual_admission'] is False and b['model_changed'] is False
 return {'result':'PASS-4V-PACKAGE-INTEGRITY','members':len(seen),'retained_byte_exact_files':len(retained),'parent_4U_members':len(old['files']),'no_full_stream_computation':True,'actual_admission':False}
if __name__=='__main__':print(json.dumps(verify(ROOT),sort_keys=True))
