#!/usr/bin/env python3
"""Metadata and saved-evidence checks only. Never runs a stream worker."""
import argparse,json,zipfile,time,sys
from pathlib import Path
sys.dont_write_bytecode=True
from bind_text import *
def verified_zip(path,manifest_member):
 with zipfile.ZipFile(path) as z:
  m=json.loads(z.read(manifest_member));names={e['path'] for e in m['files']};pre=str(Path(manifest_member).parent)
  pre='' if pre=='.' else pre+'/'
  require(len(names)==len(m['files']),'manifest duplicates');require(len(z.namelist())==len(set(z.namelist())),'ZIP duplicates')
  require(set(z.namelist())=={pre+n for n in names}|{manifest_member},'ZIP exact membership')
  for e in m['files']:
   p=Path(e['path']);require(not p.is_absolute() and '..' not in p.parts,'unsafe ZIP member')
   with z.open(pre+e['path']) as f:h=hashlib.file_digest(f,'sha256').hexdigest()
   require(h==e['sha256'] and z.getinfo(pre+e['path']).file_size==e['bytes'],'ZIP exact bytes '+e['path'])
 return m

def check_preserved(root):
 hist=read(root/'inputs/PRESERVED-FILES.json')
 for e in hist:require(info(root/e['path'])=={k:e[k] for k in ('bytes','sha256')},'historical artifact mutation '+e['path'])
 return hist

def verify(root=ROOT,model=None,outer_manifest=True):
 began=time.monotonic();hist=check_preserved(root)
 if outer_manifest:
  m=read(root/'PACKAGE-MANIFEST.json');names={e['path'] for e in m['files']}
  actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=root/'PACKAGE-MANIFEST.json'}
  require(names==actual and len(names)==len(m['files']),'outer package membership')
  for e in m['files']:require(info(root/e['path'])=={k:e[k] for k in ('bytes','sha256')},'package exact bytes '+e['path'])
 for stage in ('4S','4Q','4T','4P'):
  m=read(root/f'historical/{stage}/PACKAGE-MANIFEST.json');by={e['path']:e for e in m['files']}
  for e in hist:
   prefix=f'historical/{stage}/'
   if e['path'].startswith(prefix) and e['path'][len(prefix):] in by:
    b=by[e['path'][len(prefix):]];require(e['sha256']==b['sha256'] and e['bytes']==b['bytes'],'parent manifest correspondence')
 a,c,job,receipt,d=basis(root);e=read(root/'derived/TEXTUAL-IDENTITY.json');validate_envelope(e,root)
 require(info(root/'retained/Engineering-288-checkpoint-4T.zip')['sha256']==KIT,'retained kit hash')
 require(info(root/'retained/Engineering-288-4T-textual-completion.zip')['sha256']==SNAPSHOT,'retained snapshot hash')
 tm=verified_zip(root/'retained/Engineering-288-checkpoint-4T.zip','Engineering-288-checkpoint-4T/PACKAGE-MANIFEST.json')
 sm=verified_zip(root/'retained/Engineering-288-4T-textual-completion.zip','SNAPSHOT-MANIFEST.json')
 require(sha(wire(tm))==job['package_manifest_sha256']==sm['package_manifest_sha256'],'package manifest join')
 by={f['path']:f for f in tm['files']};require(by['inputs/links.txt']['sha256']==d['descriptor_sha256'],'descriptor identity');require(by['inputs/prefix.bin']['sha256']==d['prefix_table']['sha256'],'prefix identity')
 with zipfile.ZipFile(root/'retained/Engineering-288-checkpoint-4T.zip') as z:
  require(z.read('Engineering-288-checkpoint-4T/results/DESCRIPTOR-CORRESPONDENCE.json')==(root/(T+'results/DESCRIPTOR-CORRESPONDENCE.json')).read_bytes(),'descriptor report exact bytes')
 with zipfile.ZipFile(root/'retained/Engineering-288-4T-textual-completion.zip') as z:
  for p in ['COMPLETION.json','supervisor/IDENTITY.json','textual/IDENTITY.json','textual/HEAD.json','SNAPSHOT-MANIFEST.json']:
   require(z.read(p)==(root/(T+'snapshot/'+p)).read_bytes(),'snapshot extract substitution')
 require(sm['progress']['complete'] is True and sm['progress']['generation_segments']==sm['progress']['replayed_segments']==6672,'complete snapshot')
 cmp=read(root/'derived/MODEL-COMPARISON.json');oldcmp=read(root/(S+'results/MODEL-COMPARISON.json'))
 require(cmp['old']==cmp['new']==oldcmp['new'] and cmp['changes']==[] and cmp['arrays']==oldcmp['unchanged_arrays'],'model historical preservation')
 if model is not None:require(info(model)==cmp['new'],'exact unchanged external model bytes')
 w=read(root/'derived/WITNESS-ASSEMBLY.json');gap=read(root/'derived/GAP-REPORT.json');rs=read(root/'derived/REQUIREMENTS.json');g=read(root/'derived/DEPENDENCY-GRAPH.json');oldrs=[json.loads(l) for l in (root/(S+'inventory/REQUIREMENTS.jsonl')).read_text().splitlines()]
 require((root/'derived/REQUIREMENTS.jsonl').read_bytes()==b''.join(wire(r) for r in rs),'requirement representations')
 require(w['active']==a==gap['candidate']==read(root/'derived/ACTIVE-IDENTITIES.json'),'active binding metadata')
 require(w['full_static_links_sha256']==gap['text_stream_sha256']==TEXT and w['binary_stream_sha256']==BINARY,'distinct identity slots')
 require(w['static_text_identity']==gap['text_stream_identity']==ref(root,'derived/TEXTUAL-IDENTITY.json'),'envelope references')
 require(w['ready'] is False and w['actual_admission'] is False and w['qualification_established'] is False and w['final_outer_profile_sha256'] is None and w['live_recovery_job'] is None,'no final witness fabrication')
 require(len(rs)==67 and [r['id'] for r in rs]==[r['id'] for r in oldrs],'all requirements retained')
 require(gap['blocked']==[r['id'] for r in rs if r['status']=='BLOCKED'] and len(gap['blocked'])==64,'blocked duties not discharged')
 require(gap['available_mechanical']==['baseline','implementation','binary-stream'],'no broad duty closure')
 for old,new in zip(oldrs,rs):
  require(old['status']==new['status'] and new['qualification_status']==old['qualification_status'] and new['actual_admission'] is False,'historical qualification/disposition')
  if new['id'] not in ('text-stream','final-profile','execution-host'):require(new==old,'unaffected requirement mutation')
 require(next(r for r in rs if r['id']=='text-stream')['full_model_input'] is None,'physical file fabricated')
 count=graph_check(g);require(count==21,'dependency completeness')
 diffs=read(root/'derived/CHANGED-FIELDS.json');pairs=[('WITNESS-ASSEMBLY',read(root/(S+'candidate/WITNESS-ASSEMBLY.json')),w),('REQUIREMENTS',oldrs,rs),('GAP-REPORT',read(root/(S+'inventory/GAP-REPORT.json')),gap),('DEPENDENCY-GRAPH',read(root/(S+'dependencies/DEPENDENCY-GRAPH.json')),g)]
 require(diffs['changes']=={name:changes(old,new) for name,old,new in pairs},'exact changed fields')
 return {'result':'PASS-4U-TEXTUAL-IDENTITY-BINDING','snapshot_members_verified':len(sm['files']),'kit_members_verified':len(tm['files']),'historical_files_preserved':len(hist),'model_sha256':MODEL,'model_changed':False,'model_bytes_checked':model is not None,'binary_stream_sha256':BINARY,'textual_links_sha256':TEXT,'potential_rows':POTENTIAL,'structural_rows':STRUCTURAL,'total_rows':ROWS,'serialized_bytes':BYTES,'dependency_nodes':count,'requirements':67,'blocked_groups':64,'identity_subobligation_complete':True,'full_stream_processed':False,'kernel_tests_reused_not_rerun':True,'actual_admission':False,'qualification_established':False,'seconds':time.monotonic()-began}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=ROOT);ap.add_argument('--model',type=Path);ap.add_argument('--unsealed',action='store_true');ap.add_argument('--output',type=Path);args=ap.parse_args();v=verify(args.root,args.model,not args.unsealed)
 if args.output:save(args.output,v)
 print(json.dumps(v))
