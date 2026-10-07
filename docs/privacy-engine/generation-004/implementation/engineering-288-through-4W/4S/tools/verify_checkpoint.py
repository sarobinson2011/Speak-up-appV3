#!/usr/bin/env python3
"""Verify metadata only. Does not invoke any native executable or stream runner."""
import argparse,hashlib,json,zipfile,time
from common import *

def graph_check(nodes):
 by={x['id']:x for x in nodes};assert len(by)==len(nodes)
 done=set();pending=set(by)
 while pending:
  ready={i for i in pending if set(by[i]['depends_on'])<=done}
  assert ready,'cyclic or missing dependency';done|=ready;pending-=ready
 return len(done)

def comparison_check(old,new,comparison):
 assert info(old)==comparison['old'] and info(new)==comparison['new']
 assert comparison['old']['sha256']==OLD
 assert comparison['changes']==[{'pointer':'/equality_stream/sha256','old':None,'new':STREAM}]
 edit=comparison['byte_edit'];off=edit['old_offset'];before=bytes.fromhex(edit['old_bytes_hex']);after=bytes.fromhex(edit['new_bytes_hex'])
 assert before==b'null' and after==json.dumps(STREAM).encode()
 with old.open('rb') as a,new.open('rb') as b:
  assert a.read(off)==b.read(off)
  assert a.read(len(before))==before and b.read(len(after))==after
  while True:
   x=a.read(1048576);y=b.read(1048576);assert x==y,'unexpected model mutation'
   if not x:break
 assert comparison['new']['bytes']==comparison['old']['bytes']+62

def verify(root,manifest=True):
 began=time.monotonic();checked=0
 if manifest:
  m=load(root/'PACKAGE-MANIFEST.json');listed={e['path'] for e in m['files']}
  actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='PACKAGE-MANIFEST.json'}
  # Nested historical manifests ARE included, only root manifest is excluded.
  actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=root/'PACKAGE-MANIFEST.json'}
  assert actual==listed,('package membership',actual^listed)
  for e in m['files']:
   p=root/e['path'];assert p.resolve().is_relative_to(root.resolve()) and info(p)=={k:e[k] for k in ('bytes','sha256')},e['path'];checked+=1
 cmp=load(root/'results/MODEL-COMPARISON.json');comparison_check(root/'historical/model/model.json',root/'candidate/model.json',cmp)
 active=load(root/'candidate/ACTIVE-IDENTITIES.json');assert active['model_sha256']==cmp['new']['sha256'] and active['model_bytes']==cmp['new']['bytes'] and active['final_profile_sha256'] is None
 bridge=load(root/'candidate/BINARY-CORRESPONDENCE.json');assert bridge['candidate_model_sha256']==active['model_sha256'] and bridge['historical_model_sha256']==OLD
 assert bridge['binary_identity']['sha256']==STREAM and bridge['binary_identity']['rows']==91157453467 and bridge['binary_identity']['bytes']==729259627770
 assert info(root/'retained/Engineering-288-4R-binary-completion.zip')==bridge['completion_snapshot']
 assert info(root/'retained/Engineering-288-4R-return-verification.json')==bridge['return_verification']
 p=load(root/'retained/Engineering-288-4R-return-verification.json');assert p['job_identity_sha256']==bridge['original_job_identity_sha256']
 assert p['verified_progress']['generated_whole_stream_sha256']==p['verified_progress']['verified_whole_stream_sha256']==STREAM
 with zipfile.ZipFile(root/'retained/Engineering-288-4R-binary-completion.zip') as z:
  completion=json.loads(z.read('COMPLETION.json'));job=json.loads(z.read('supervisor/IDENTITY.json'));binary=json.loads(z.read('binary/IDENTITY.json'))
 for sealed in (completion,job):assert hashlib.sha256(canonical(sealed['payload'])).hexdigest()==sealed['sha256']
 assert job['sha256']==bridge['original_job_identity_sha256'] and completion['payload']['job_identity_sha256']==job['sha256']
 assert job['payload']['active']==load(root/'historical/4Q/assembly/ACTIVE-IDENTITIES.json')
 assert binary==job['payload']['retained_code']
 assert binary['binary_sha256']==bridge['native_binary']['sha256'] and binary['engine_source_sha256']==bridge['native_source']['sha256'] and binary['descriptor_sha256']==bridge['descriptor_sha256']
 for key,value in p['verified_progress'].items():assert completion['payload'][key]==value,key
 for key in ('selected_contract_sha256','amendment_binding_sha256','canonical_backend_sha256','implementation_identity_sha256'):assert job['payload']['active'][key]==active[key]
 assert sha(root/'historical/4R/inputs/pairs.txt')==bridge['descriptor_sha256']
 assert info(root/'historical/4R/runner/pairs.cpp')==bridge['native_source'] and info(root/'historical/4R/runner/pairs')==bridge['native_binary']
 # Every copied historical member compared to its unchanged parent manifest.
 preserved=0
 for stage in ('4Q','4R','4P'):
  hist=root/'historical'/stage;entries={e['path']:e for e in load(hist/'PACKAGE-MANIFEST.json')['files']}
  for file in hist.rglob('*'):
   if not file.is_file() or file==hist/'PACKAGE-MANIFEST.json':continue
   rel=file.relative_to(hist).as_posix();assert rel in entries,rel
   assert info(file)=={k:entries[rel][k] for k in ('bytes','sha256')},rel;preserved+=1
 cp2={e['path']:e for e in load(root/'historical/CP2/PACKAGE-MANIFEST.json')['files']}
 assert cp2['results/expansion/model.json']['sha256']==OLD
 unchanged=load(root/'dependencies/UNCHANGED-ARTIFACTS.json');assert unchanged['contract_sha256']==CONTRACT==active['selected_contract_sha256']
 for e in unchanged['reused']:
  assert info(root/e['historical_path'])==info(root/e['candidate_path'])=={k:e[k] for k in ('bytes','sha256')}
 contract=load(root/'candidate/reused/selected-contract.json');assert sha(root/'candidate/reused/selected-contract.json')==CONTRACT and not list(pointers(contract,OLD))
 for e in unchanged['source_checks']:assert sha(root/e['physical_path'])==e['sha256']==contract['source_inputs'][e['logical_path']]
 ledger=load(root/'candidate/ledger/BINDING.json');assert ledger['model_sha256']==active['model_sha256'] and ledger['selected_contract_sha256']==CONTRACT
 for k,path in [('model_comparison','results/MODEL-COMPARISON.json'),('binary_correspondence','candidate/BINARY-CORRESPONDENCE.json'),('potential_domain','candidate/ledger/potential-domain.json'),('reused_artifact_index','dependencies/UNCHANGED-ARTIFACTS.json')]:assert ledger[k]==info(root/path)
 domain=load(root/'candidate/ledger/potential-domain.json');original=load(root/'historical/4P/rebinding/ledger/potential-domain.json');original.update(model_sha256=active['model_sha256'],serialized_stream_sha256=STREAM);assert domain==original and domain['disposition']=='NOT-ESTABLISHED'
 inv=load(root/'candidate/ledger/inventory-result.json');assert inv['binding_sha256']==sha(root/'candidate/ledger/BINDING.json') and inv['model_sha256']==active['model_sha256']
 graph=load(root/'dependencies/DEPENDENCY-GRAPH.json');n=graph_check(graph['nodes']);assert graph['candidate_model_sha256']==active['model_sha256']
 for d in load(root/'dependencies/DIRECT-MODEL-REFERENCES.json'):
  path=root/d['historical_path'];assert info(path)=={k:d[k] for k in ('bytes','sha256')}
  if path.suffix=='.json':assert list(pointers(load(path),OLD))==d['model_pointers']
 requirements=[json.loads(s) for s in (root/'inventory/REQUIREMENTS.jsonl').read_text().splitlines()];gaps=load(root/'inventory/GAP-REPORT.json');assert len(requirements)==gaps['requirements']==67
 assert [x['id'] for x in requirements if x['status']=='BLOCKED']==gaps['blocked'] and len(gaps['blocked'])==64
 assert all(x['candidate_required_binding']==active for x in requirements)
 assert next(x for x in requirements if x['id']=='binary-stream')['status']=='AVAILABLE-MECHANICAL'
 assert gaps['final_profile_sha256'] is None and gaps['text_stream_sha256'] is None and not gaps['qualification_established'] and not gaps['actual_admission']
 witness=load(root/'candidate/WITNESS-ASSEMBLY.json');assert witness['active']==active and not witness['ready'] and witness['final_outer_profile_sha256'] is None and witness['live_recovery_job'] is None
 assert witness['rebound_provenance']['sha256']==sha(root/'candidate/ledger/BINDING.json')
 return {'result':'PASS','manifested_files':checked,'historical_members_preserved':preserved,'dependency_nodes':n,'candidate':cmp['new'],'changed_fields':['/equality_stream/sha256'],'full_stream_processed':False,'actual_admission':False,'seconds':time.monotonic()-began}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=R);ap.add_argument('--output',type=Path);a=ap.parse_args();result=verify(a.root)
 if a.output:save(a.output,result)
 print(json.dumps(result))
