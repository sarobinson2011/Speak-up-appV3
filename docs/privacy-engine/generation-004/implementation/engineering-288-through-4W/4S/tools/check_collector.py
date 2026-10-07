#!/usr/bin/env python3
"""Focused existing-kernel rejection checks, not a repeated regression suite."""
import argparse,hashlib,json,sys,tempfile,time,copy
from pathlib import Path
from common import R,save,load,sha
ap=argparse.ArgumentParser();ap.add_argument('--kernel',type=Path,required=True);ap.add_argument('--output',type=Path,default=R/'results/COLLECTOR-CHECKS.json');a=ap.parse_args();kernel=a.kernel.resolve()
m=load(R/'historical/4P/PACKAGE-MANIFEST.json');verified=0
for e in m['files']:
 if e['path'].endswith('.py') or e['path'] in ['crypto_backend/BUILD-MANIFEST.json','crypto_backend/bin/pe-rfc8032-stream','link_recovery/worker','rebinding/selected-contract.json']:
  assert sha(kernel/e['path'])==e['sha256'],e['path'];verified+=1
sys.path.insert(0,str(kernel))
from fixtures.construct import dataset,wire
from fixtures.integrated import export
from integrated_auth.collector import run
from link_recovery.cli import create_key
rows=[];start=time.monotonic()
with tempfile.TemporaryDirectory(prefix='4s-focused-') as td:
 d=Path(td);key=d/'key';create_key(key);q,t=dataset()
 def check(name,mutate=None,expected=()):
  request,trust=copy.deepcopy(q),copy.deepcopy(t);base=d/name
  manifest,trusted=export(base,request,trust)
  if mutate:mutate(manifest,trusted,base)
  result=run(manifest,trusted,d/(name+'.job'),key,new_bytes=10000000,seconds=45,chunk_bytes=65536)
  assert result['processing_complete'] and not result['profile_admitted'] and not result['actual_qualification_established']
  if expected:assert all(x in result['failures'] for x in expected),result
  else:assert result['failures']==[],result
  rows.append({'name':name,'result':'PASS','failures':result['failures'],'earliest_failure':result['earliest_failure'],'actual_admission':result['profile_admitted']})
  return manifest,trusted
 baseline=check('unchanged-conditional-fixture')
 def wrong_join(m,t,b):
  x=load(m);x['canonical_model_sha256']=load(R/'candidate/ACTIVE-IDENTITIES.json')['model_sha256'];m.write_bytes(wire(x))
 check('candidate-digest-cannot-relabel-historical-source',wrong_join,['INVALID-ACTION-CONTEXT'])
 def wrong_profile(m,t,b):
  x=load(m);x['request']['profile_digest']='1'*64;m.write_bytes(wire(x))
 check('stale-outer-profile',wrong_profile,['PROFILE-DIGEST-MISMATCH'])
 def changed_model(m,t,b):
  model=load(b/'model.json');model['equality_stream']['sha256']='1'*64;(b/'model.json').write_bytes(wire(model));x=load(m)
  x['model'].update(bytes=(b/'model.json').stat().st_size,sha256=sha(b/'model.json'));x['canonical_model_sha256']=sha(b/'model.json');m.write_bytes(wire(x))
 check('rehashing-carrier-cannot-rebind-owning-model',changed_model,['INVALID-ACTION-CONTEXT'])
 manifest,trusted=baseline;x=load(manifest);x['canonical_model_sha256']='2'*64;manifest.write_bytes(wire(x))
 try:run(manifest,trusted,d/'unchanged-conditional-fixture.job',key,resume=True,new_bytes=10000000,seconds=45)
 except ValueError as e:
  assert 'stale' in str(e) or 'binding' in str(e);rows.append({'name':'historical-journal-rejects-new-input','result':'PASS','error':str(e)})
 else:raise AssertionError('stale receipt accepted')
save(a.output,{'result':'PASS','checks':rows,'verified_retained_code_files':verified,'seconds':time.monotonic()-start,'kernel_changed':False,'full_model_witness_executed':False,'full_stream_processed':False,'qualification_established':False})
print(json.dumps({'result':'PASS','focused_collector_checks':len(rows)}))
