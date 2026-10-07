#!/usr/bin/env python3
"""4S metadata-only construction. No pair generator or kernel execution."""
import argparse,collections,hashlib,json,resource,time
from common import *

def construct(root):
 start=time.monotonic();old=root/'historical/model/model.json';assert sha(old)==OLD
 model=json.loads(old.read_bytes());raw=canonical(model);assert hashlib.sha256(raw).hexdigest()==OLD,'historical canonical law'
 assert set(model)=={'actor_graph_policy','equality_stream','surfaces','relations','tokens','structural_edges'}
 eq=model['equality_stream'];expected={'bytes':729259627770,'format':'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1','ordering':'lexicographic index pairs, i<j','predicate':'left.arbitrary OR right.arbitrary OR equal symbolic_digest','row_encoding':'U32-BE left index; U32-BE right index','rows':91157453467,'sha256':None};assert eq==expected
 receipt=load(root/'retained/Engineering-288-4R-return-verification.json');p=receipt['verified_progress']
 assert receipt['result']=='PASS-RETURNED-EXECUTION-EVIDENCE-VERIFICATION'
 assert sha(root/'retained/Engineering-288-4R-binary-completion.zip')==receipt['snapshot']['sha256']
 assert p['generated_whole_stream_sha256']==p['verified_whole_stream_sha256']==STREAM
 assert p['complete'] and not p['actual_admission'] and not p['qualification_established']
 assert (p['rows'],p['serialized_bytes'])==(eq['rows'],eq['bytes'])
 tokens=model['tokens'];assert len(tokens)==426984
 groups={};fixed=[];tokenh=hashlib.sha256()
 for i,t in enumerate(tokens):
  assert t['index']==i and type(t['arbitrary']) is bool
  tokenh.update(canonical(t))
  if not t['arbitrary']:fixed.append((i,groups.setdefault(t['symbolic_digest'],len(groups))))
 descriptor=(f'{len(tokens)} {len(fixed)}\n'+''.join(f'{i} {g}\n' for i,g in fixed)).encode()
 assert descriptor==(root/'historical/4R/inputs/pairs.txt').read_bytes()
 universe=load(root/'historical/4R/inputs/universe.json')
 assert tokenh.hexdigest()==universe['token_segment_concatenation_sha256']
 count=collections.Counter(g for i,g in fixed);excluded=len(fixed)*(len(fixed)-1)//2-sum(n*(n-1)//2 for n in count.values())
 assert excluded==1169 and len(tokens)*(len(tokens)-1)//2-excluded==eq['rows']
 assert 34+8*eq['rows']==eq['bytes']
 # Exact canonical byte edit plus equal suffix proves all other nested fields unchanged.
 needle=b'"sha256":null';offset=raw.index(needle)+len(b'"sha256":');assert offset<1024
 patched=raw[:offset]+json.dumps(STREAM).encode()+raw[offset+4:]
 oldlen=len(raw);del raw
 model['equality_stream']['sha256']=STREAM
 assert canonical(model)==patched,'candidate canonical serializer'
 target=root/'candidate/model.json';target.parent.mkdir(parents=True,exist_ok=True)
 tmp=target.with_suffix('.json.part')
 with tmp.open('wb') as f:f.write(patched);f.flush();os.fsync(f.fileno())
 os.replace(tmp,target);newsha=hashlib.sha256(patched).hexdigest();del patched
 arrays={}
 for k in ('surfaces','relations','tokens','structural_edges'):
  b=canonical(model[k]);arrays[k]={'rows':len(model[k]),'canonical_bytes':len(b),'old_sha256':hashlib.sha256(b).hexdigest(),'new_sha256':hashlib.sha256(b).hexdigest(),'identical':True};del b
 comparison={'format':'CP4S-EXACT-MODEL-COMPARISON-1','old':{'sha256':OLD,'bytes':oldlen},'new':info(target),'changes':[{'pointer':'/equality_stream/sha256','old':None,'new':STREAM}],'unchanged_arrays':arrays,'unchanged_top_level':['actor_graph_policy','relations','structural_edges','surfaces','tokens'],'byte_edit':{'old_offset':offset,'old_bytes_hex':b'null'.hex(),'new_bytes_hex':json.dumps(STREAM).encode().hex(),'exact_prefix_and_suffix_equal':True},'canonical_law':'json.dumps(sort_keys=True,separators=(comma,colon),ensure_ascii=True,allow_nan=False) plus LF','no_full_pair_or_link_processing':True}
 save(root/'results/MODEL-COMPARISON.json',comparison)
 bridge={'format':'CP4S-HISTORICAL-BINARY-CANDIDATE-CORRESPONDENCE-1','historical_model_sha256':OLD,'candidate_model_sha256':newsha,'completion_snapshot':info(root/'retained/Engineering-288-4R-binary-completion.zip'),'return_verification':info(root/'retained/Engineering-288-4R-return-verification.json'),'original_job_identity_sha256':receipt['job_identity_sha256'],'original_package_manifest_sha256':receipt['package_manifest_sha256'],'binary_identity':model['equality_stream'],'tokens':len(tokens),'fixed_tokens':len(fixed),'fixed_groups':len(groups),'excluded_pairs':excluded,'descriptor_sha256':hashlib.sha256(descriptor).hexdigest(),'token_jsonl_sha256':tokenh.hexdigest(),'proof':'All ordered tokens checked. Fixed groups reconstructed by exact symbolic_digest equality; descriptor bytes identical. Arbitrary tokens are precisely omitted fixed indices. Binary law exactly matches retained model and pinned pairs.cpp header/U32BE loops. Arrays and law preserved except stream SHA. No historical receipt is relabeled as a new-job receipt.','header_hex':b'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1\n'.hex(),'native_source':info(root/'historical/4R/runner/pairs.cpp'),'native_binary':info(root/'historical/4R/runner/pairs'),'trust':'Returned local trusted execution evidence; distinct predicate path shares traversal, serializer and SHA implementation. Not source authentication or independent qualification.','actual_admission':False,'qualification_established':False}
 save(root/'candidate/BINARY-CORRESPONDENCE.json',bridge)
 save(root/'results/CONSTRUCTION.json',{'result':'PASS','seconds':time.monotonic()-start,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'candidate':info(target),'full_stream_processed':False})
 print(json.dumps({'result':'PASS','candidate':info(target)}))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=R);a=ap.parse_args();construct(a.root)
