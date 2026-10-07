#!/usr/bin/env python3
"""Verify saved 4T evidence only. No generation, replay or native worker invocation.
Usage: python3 -B verify-4T-return.py KIT_ZIP SNAPSHOT_ZIP OUTPUT_JSON
Requires Linux libcrypto.so.3 for bounded SHA-256 state finalization.
"""
import sys,json,hashlib,zipfile,tempfile,subprocess,importlib.util,ctypes,struct
from pathlib import Path
sys.dont_write_bytecode=True
KIT='98a1027a7968da0f940e501a6b0a65eeb4a066a301645c4110a2e637a757fa5f'
SNAP='83138fdbb8e3a66ed638b32c85ddd1127775bdc2473a0e15c6344254a130fbf8'
STREAM='dc5776088dfc860e25a42e260b245b607969f6c49346bd6912eecc0ef53d8a74'
def check(ok,msg):
 if not ok:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def filehash(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
class CTX(ctypes.Structure):
 _fields_=[('h',ctypes.c_uint32*8),('Nl',ctypes.c_uint32),('Nh',ctypes.c_uint32),('data',ctypes.c_uint32*16),('num',ctypes.c_uint),('md_len',ctypes.c_uint)]
lib=ctypes.CDLL('libcrypto.so.3');lib.SHA256_Final.argtypes=[ctypes.c_void_p,ctypes.POINTER(CTX)];lib.SHA256_Final.restype=ctypes.c_int
lib.SHA256_Init.argtypes=[ctypes.POINTER(CTX)];lib.SHA256_Init.restype=ctypes.c_int
lib.SHA256_Update.argtypes=[ctypes.POINTER(CTX),ctypes.c_void_p,ctypes.c_size_t];lib.SHA256_Update.restype=ctypes.c_int
# Check system ABI and finalization against standard hashlib, including a block boundary.
for b in [b'',b'abc',b'x'*67,b'y'*129]:
 c=CTX();out=(ctypes.c_ubyte*32)();check(lib.SHA256_Init(ctypes.byref(c))==1,'init');check(lib.SHA256_Update(ctypes.byref(c),b,len(b))==1,'update');check(lib.SHA256_Final(out,ctypes.byref(c))==1,'final');check(bytes(out).hex()==digest(b),'SHA256 ABI self-check')
def finalize(state):
 words,n,tail=state.split(':');n=int(n);tail=bytes.fromhex(tail)
 check(len(tail)==n%64,'state tail length')
 c=CTX();c.h[:]=struct.unpack('>8I',bytes.fromhex(words));c.Nl=(n*8)&0xffffffff;c.Nh=(n*8)>>32;c.num=len(tail);c.md_len=32
 ctypes.memmove(ctypes.addressof(c)+CTX.data.offset,tail,len(tail));out=(ctypes.c_ubyte*32)()
 check(lib.SHA256_Final(out,ctypes.byref(c))==1,'state finalize');return bytes(out).hex()
def extract(z,d):
 for e in z.infolist():
  p=Path(e.filename);check(not p.is_absolute() and '..' not in p.parts and '.env' not in p.parts,'unsafe path');check((e.external_attr>>16)&0o170000!=0o120000,'symlink')
 check(len(z.namelist())==len(set(z.namelist())),'duplicate member');z.extractall(d)
kit,snapshot,outpath=map(Path,sys.argv[1:])
check(filehash(kit)==KIT,'kit archive hash');check(filehash(snapshot)==SNAP,'snapshot archive hash')
with tempfile.TemporaryDirectory(prefix='cp4t-return-') as tmp:
 base=Path(tmp)
 with zipfile.ZipFile(kit) as z:extract(z,base)
 root=base/'Engineering-288-checkpoint-4T';task=base/'saved-task'
 with zipfile.ZipFile(snapshot) as z:
  m=json.loads(z.read('SNAPSHOT-MANIFEST.json'))
  names=[e['path'] for e in m['files']];check(len(names)==len(set(names)),'duplicate manifest')
  check(set(names)|{'SNAPSHOT-MANIFEST.json'}==set(z.namelist()),'snapshot membership')
  for e in m['files']:
   b=z.read(e['path']);check(len(b)==e['bytes'] and digest(b)==e['sha256'],'snapshot member '+e['path'])
  extract(z,task)
 spec=importlib.util.spec_from_file_location('cp4t_return',root/'run_task.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
 r.verify_package(root)
 ident=r.unseal(task/'supervisor/IDENTITY.json');check(ident['package_manifest_sha256']==filehash(root/'PACKAGE-MANIFEST.json')==m['package_manifest_sha256'],'manifest binding')
 check(ident['active']==r.read(root/'bindings/ACTIVE-IDENTITIES.json'),'active binding')
 check(ident['plan']==r.PLAN,'plan binding')
 check(ident['retained_code']==r.retained(root).identity(root/'inputs/links.txt'),'code/input binding')
 a=r.audit(root,task/'textual',r.PLAN);check(a==m['progress'],'snapshot progress')
 records,_=r.budget_records(task/'supervisor');limit=r.budget_limit(task/'supervisor',ident,r.PLAN)
 check(len(records)==13344,'attempt count')
 segs=sorted((task/'textual').glob('segment-*.json'));check(len(segs)==6672,'segment count')
 check(finalize(r.read(segs[0])['state_in'])==digest(r.HEADER),'header state')
 for p in segs:
  g=r.read(p);check(finalize(g['state_out'])==g['prefix_sha256'],'prefix state digest '+p.name)
 for i,x in enumerate(records):
  op='generate' if i<6672 else 'replay';k=i if i<6672 else i-6672
  check(x['status']=='FINISHED' and x['operation']==op,'attempt status/operation')
  check(x['reserved_seconds']==60 and x['verified_before']==(0 if i<6672 else k),'reservation')
  check(x['frontier_before']==(r.read(segs[k])['start'] if i<6672 else 426984),'attempt frontier')
  reserved={key:v for key,v in x.items() if key!='reservation_sha256'};reserved.update(status='RESERVED',charged_seconds=60)
  check(r.sha(r.wire(reserved))==x['reservation_sha256'],'reservation digest')
  log=r.read(task/f'supervisor/log-{i:05d}.json');check(log['operation']==op and log['returncode']==0 and log['stderr']=='','operation log')
  last=json.loads(log['stdout'].strip().splitlines()[-1])
  if op=='generate':check(last['segments']==k+1 and last['candidate_frontier']==r.read(segs[k])['end'],'generation log correspondence')
  else:check(last['verified_segments']==k+1 and last['previously_verified']==k and last['independent_generator'] is False,'replay log correspondence')
 c=r.unseal(task/'COMPLETION.json');used=sum(x['charged_seconds'] for x in records)
 for k,v in a.items():check(c[k]==v,'completion '+k)
 check(c['job_identity_sha256']==r.sha(r.wire(ident)) and c['package_manifest_sha256']==ident['package_manifest_sha256'],'completion binding')
 check(c['budget_charged_seconds']==used<=limit,'completion budget')
 check(a['complete'] and a['rows']==91161821721 and a['serialized_bytes']==19909380154846,'completion totals')
 check(a['generated_whole_stream_sha256']==a['replayed_whole_stream_sha256']==STREAM,'full digest')
 # Execute only the retained read-only completion checker, never run/resume/verify replay.
 cp=subprocess.run([sys.executable,'-B',str(root/'run_task.py'),'verify-completion','--task',str(task)],capture_output=True,text=True,timeout=60)
 check(cp.returncode==0,'retained completion check: '+cp.stderr)
 report={'result':'PASS-RETURNED-TEXTUAL-COMPLETION-EVIDENCE','snapshot_sha256':SNAP,'snapshot_bytes':snapshot.stat().st_size,'kit_sha256':KIT,'snapshot_members_verified':len(m['files']),'package_manifest_sha256':ident['package_manifest_sha256'],'job_identity_sha256':c['job_identity_sha256'],'active':ident['active'],'completion':c,'checks':{'all_snapshot_member_bytes_and_crc':'PASS','exact_kit_manifest':'PASS','model_contract_descriptor_code_bindings':'PASS','all_segment_intervals_counts_ordinals_and_chain':'PASS','all_6672_saved_prefix_states_finalized':'PASS','all_6672_replay_receipt_joins':'PASS','all_13344_attempts_reservations_and_logs':'PASS','completion_and_snapshot_consistency':'PASS','retained_read_only_verify_completion':'PASS'},'host_library_identities':'Preserved as recorded; Ubuntu host libraries unavailable here for fresh authentication. No source qualification claimed.','full_stream_generated_or_replayed_during_this_check':False,'independent_supplied_row_validation':False,'independent_generator':False,'actual_admission':False,'qualification_established':False,'trust':'Saved local execution/checksum evidence; not an independent recomputation of the full stream or source authentication.','next_bounded_task':'Bind the verified textual identity in a separate evidence/dependency checkpoint, preserving historical models and receipts. Determine affected model/profile fields from accepted schemas; do not invent absent profile inputs. Keep independent supplied-row validation and authoritative inputs unresolved.','verification_script_sha256':filehash(__file__)}
 Path(outpath).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'result':report['result'],'members_verified':len(m['files']),'generation_segments':6672,'replay_segments':6672,'whole_stream_sha256':STREAM,'receipt':str(outpath)}))
