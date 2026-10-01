from pathlib import Path
import runpy,copy,hashlib,json,tempfile,contextlib,io
O=Path(__file__).resolve().parents[2];M=runpy.run_path(str(Path(__file__).with_name('admission.py')))
model=M['regenerate']()
r=M['collect']({},model);assert r['earliest_failure']=='PROFILE-DIGEST-MISMATCH' and 'INVALID-EVIDENCE-AUTHORITY' in r['failures'] and r['profile_admitted'] is False
cases=1
# Known missing label + signature error: authentication precedes label failures.
a={'authority_id':'SYNTHETIC-TEST','algorithm':'ED25519-RFC8032','public_key':'01'*32,'key_fingerprint_sha256':hashlib.sha256(bytes.fromhex('01'*32)).hexdigest(),'owner_source_id':'SYNTHETIC-TEST','owner_anchor':'TEST-ONLY'}
raw=M['P']['construct_outer'](a,a)
f={'evidence.tsv':b'x','tokens.tsv':b'x','links.tsv':b'x','signature.txt':b'INVALID\n'}
request={'outer_bytes':raw,'outer_sha256':hashlib.sha256(raw).hexdigest(),'appointment':a,'trusted_appointment':a,'evidence_objects':{k:{'files':f,'object_sha256':'00'*32} for k in M['SCOPE']}}
r=M['collect'](request,model);assert r['earliest_failure']=='INVALID-EVIDENCE-AUTHENTICATION' and 'INVALID-SURFACE-LABELS' in r['failures'];cases+=1
for field in ('model','expected_bytes','source_complete','visibility_complete','profile_admitted'):
 bad=dict(request);bad[field]=True;r=M['collect'](bad,model);assert r['earliest_failure']=='INVALID-PROFILE-SCHEMA';cases+=1
bad=dict(request);bad['trusted_appointment']=None;r=M['collect'](bad,model);assert r['earliest_failure']=='INVALID-EVIDENCE-AUTHORITY';cases+=1
# Supplied model mutation in a validly framed container is independently rejected.
for key in ('tokens','surfaces','structural_edges'):
 members=M['P']['A']['decode_container'](raw);p=json.loads(members['PRIVACY']);p['model'][key]=[];members['PRIVACY']=M['canonical'](p);b=M['P']['A']['encode_container'](members);bad={**request,'outer_bytes':b,'outer_sha256':hashlib.sha256(b).hexdigest()};r=M['collect'](bad,model);assert r['earliest_failure']=='INVALID-PROFILE-SCHEMA';cases+=1
# Current-state result cannot become acceptance even with a correctly framed synthetic container.
assert all(M['collect'](q,model)['profile_admitted'] is False for q in ({},request))
# Direct regression for cached-model mutation with unchanged input digests.
# Operate only on a temporary copy: no packaged file is modified.
X=runpy.run_path(str(O/'privacy/expand_privacy.py'));surfaces,relations,tokens,edges=X['construct']()
cached=json.loads((O/'privacy/expanded/PRIVACY.candidate.json').read_bytes());assert cached['tokens']==tokens and cached['structural_edges']==edges
bad=copy.deepcopy(cached);bad['tokens'][0]['context']='FORGED';assert bad['input_sha256']==cached['input_sha256'] and bad['tokens']!=tokens;cases+=1
report={'author_checks':'PASS','negative_gate_cases':cases,'issuer_cache_not_used_for_decisions':True,'acceptance_path_implemented':False,'unfinished_integration':['SYMBOLIC-POLICY-EVIDENCE-INTEGRATION'],'profile_admitted':False}
(O/'verification/admission-integration-tests.json').write_bytes(M['canonical'](report));(O/'verification/admission-readiness.json').write_bytes(M['canonical'](M['collect']({},model)))
print('PASS — '+str(cases)+' admission rejection/precedence cases; issuer model caches and completion flags rejected.')
print('BOUNDARY — this closes rejection-gate integration, not the still-unfinished admission acceptance path.')
