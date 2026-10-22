import strict_types as strict
"""C4 source-qualified assessment interface, bounded and OFFLINE ONLY.
This checks authenticated exact assessment correspondence, not NEAR consensus.
No operational trust provisioning route is present. Fixture trust is explicit.
"""
from pathlib import Path
import os,subprocess,json
from anchor import enc,sha,need,Blocked,parse
import outcome
ROOT=Path(__file__).resolve().parents[1]
BACKEND_SHA='3d8b65ea87eb5b5a680c9c51c6897a8c32641f1580947046d1cc6c7f765c152b'
DOMAIN=b'I164-C4-PROVIDER-ORIGINAL-MESSAGE-1\0'
MAX_ENVELOPE=3145728
OBLIGATIONS=['network-anchor','block-finality','receipt-inclusion','engine-code-at-execution','outcome-correspondence']
RULE='I164-C4-QUALIFIED-ASSESSMENT-1'
def signed_bytes(kind,claim):return DOMAIN+kind.encode('ascii')+b'\0'+enc(claim)
def authenticate(kind,packet,key):
 need(type(packet) is dict and strict.same(set(packet),{'claim','signature'}),'SIGNED-FIELDS')
 message=signed_bytes(kind,packet['claim']);need(len(message)<=MAX_ENVELOPE,'SIGNED-BOUND')
 pub=outcome.unhex(key,32);sig=outcome.unhex(packet['signature'],64);need(strict.same(len(pub),32) and strict.same(len(sig),64),'SIGNATURE-SIZE')
 # Execute the same opened inode that was hashed (Linux); pathname replacement
 # cannot select another executable. In-place writes and loader/runtime integrity
 # remain the reviewed immutable-code/trusted-runtime boundary.
 path=ROOT/'native/bin/pe-rfc8032-stream';fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  data=b''
  while True:
   b=os.read(fd,65536)
   if not b:break
   data+=b;need(len(data)<=500000,'BACKEND-SIZE')
  need(strict.same(sha(data),BACKEND_SHA),'BACKEND-IDENTITY')
  try:
   p=subprocess.run(['/proc/self/fd/'+str(fd),'verify',pub.hex(),sig.hex(),str(len(message)),str(len(message))],input=message,stdout=subprocess.PIPE,stderr=subprocess.PIPE,pass_fds=(fd,),timeout=3)
  except (OSError,subprocess.TimeoutExpired) as ex:raise Blocked('BACKEND-UNAVAILABLE') from ex
  need(strict.same(p.returncode,0),'RFC8032-AUTHENTICATION')
  result=json.loads(p.stdout);need(result.get('verified') is True and strict.same(result.get('bytes'),len(message)) and strict.same(result.get('sha256'),sha(message)),'BACKEND-RESULT')
 finally:os.close(fd)
 return packet['claim']
def validate_policy(policy):
 need(type(policy) is dict and strict.same(set(policy),{'format','domain','governing','authority_key','qualification_key','provider','assessor','finality_basis'}),'POLICY-FIELDS')
 need(strict.same(policy['format'],'LAB-ASSUMPTIONS-NOT-OPERATIONAL-1'),'NO-OPERATIONAL-TRUST-LOADER')
 d=policy['domain'];need(strict.same(set(d),{'network','genesis_sha256','engine','engine_code_sha256','protocol','method'}),'DOMAIN')
 need(strict.same(d['network'],'near-testnet') and strict.same(d['engine'],'aurora') and strict.same(d['method'],'submit') and type(d['protocol']) is int,'DOMAIN-SCOPE')
 from anchor import digest
 need(digest(d['genesis_sha256']) and digest(d['engine_code_sha256']),'DOMAIN-HASH')
 need(strict.same(set(policy['governing']),{'model','profile','configuration'}),'GOVERNING')
 for v in policy['governing'].values():need(digest(v),'GOVERNING-HASH')
 need(strict.same(set(policy['finality_basis']),{'rule_sha256','trust_anchor_sha256','checkpoint_sha256'}) and all(digest(v) for v in policy['finality_basis'].values()),'FINALITY-BASIS')
 for role in ['provider','assessor']:
  member=policy[role];need(strict.same(set(member),{'id','key','appointment','qualification'}),'MEMBER')
  need(type(member['id']) is str and 0<len(member['id'])<=128,'IDENTITY')
  need(member['appointment'] is not None,'APPOINTMENT-UNAVAILABLE')
  a=authenticate('appointment',member['appointment'],policy['authority_key'])
  need(strict.same(a,{'subject':member['id'],'key':member['key'],'role':role,'domain':d,'governing':policy['governing'],'rule':RULE,'finality_basis':policy['finality_basis'],'assertion_scope':'OUTCOME-SOURCE' if role=='provider' else 'FINALITY-ASSESSMENT','laboratory_assumption':True}),'APPOINTMENT-SCOPE')
  if member['qualification'] is not None:
   q=authenticate('qualification',member['qualification'],policy['qualification_key'])
   need(strict.same(q,{'appointment_sha256':sha(enc(member['appointment'])),'subject':member['id'],'role':role,'domain':d,'governing':policy['governing'],'competence_contract':RULE,'finality_basis':policy['finality_basis'],'status':'ASSUMED-FOR-LAB-ONLY'}),'QUALIFICATION-SCOPE')
 return policy

def invocation(source,domain,finality_basis):
 z=outcome.obj(outcome.unhex(source['rpc_response_hex'],outcome.MAX_RESPONSE),outcome.MAX_RESPONSE)['result']
 rows=[z['transaction_outcome']]+z['receipts_outcome']
 return {'rule':RULE,'domain':domain,'finality_basis':finality_basis,'context':source['context'],'source_sha256':sha(enc(source)),
         'request_sha256':sha(bytes.fromhex(source['rpc_request_hex'])),'response_sha256':sha(bytes.fromhex(source['rpc_response_hex'])),
         'outcomes':[{'id':x['id'],'block_hash':x['block_hash'],'exact_record_sha256':sha(enc(x))} for x in rows]}

def validate(packet,expected,evm,policy):
 # Copy caller-owned structures before any use. No mutation of a retired intent.
 packet=parse(enc(packet),MAX_ENVELOPE);policy=validate_policy(parse(enc(policy),MAX_ENVELOPE))
 need(strict.same(set(packet),{'statement','assessment','artifacts'}),'PROVIDER-PACKET')
 c=authenticate('outcome',packet['statement'],policy['provider']['key'])
 need(strict.same(set(c),{'provider','appointment','qualification','domain','governing','source','assessment_sha256'}),'OUTCOME-STATEMENT')
 need(strict.same(c['provider'],policy['provider']['id']) and strict.same(c['appointment'],sha(enc(policy['provider']['appointment']))) and strict.same(c['qualification'],sha(enc(policy['provider']['qualification'])) if policy['provider']['qualification'] else None),'PROVIDER-BINDING')
 need(strict.same(c['domain'],policy['domain']) and strict.same(c['governing'],policy['governing']),'PROVIDER-DOMAIN')
 src=c['source'];need(strict.same(src['format'],'C4-SAVED-NEAR-SUBMIT-1'),'SOURCE-FORMAT')
 decoded=outcome.decode({'claim':src,'signature':''},expected,evm)
 need(strict.same(src['near_spec']['network'],policy['domain']['network']) and strict.same(src['near_spec']['engine'],policy['domain']['engine']) and strict.same(src['near_spec']['method'],policy['domain']['method']),'SUBMISSION-DOMAIN')
 blockers=[]
 for role in ['provider','assessor']:
  if policy[role]['qualification'] is None:blockers.append('MISSING-'+role.upper()+'-QUALIFICATION')
 assessment=packet['assessment'];artifacts=packet['artifacts'];need(type(artifacts) is dict and len(artifacts)<=16,'ARTIFACT-COUNT')
 for ref,raw in artifacts.items():need(strict.same(sha(outcome.unhex(raw,32768)),ref),'FINALITY-ARTIFACT-BYTES')
 if assessment is None:
  need(c['assessment_sha256'] is None and not artifacts,'MISSING-ASSESSMENT-BINDING');blockers.append('MISSING-FINALITY-ASSESSMENT')
 else:
  need(strict.same(c['assessment_sha256'],sha(enc(assessment))),'ASSESSMENT-BINDING')
  need(all(ref in artifacts for ref in policy['finality_basis'].values()),'MISSING-FINALITY-BASIS-BYTES')
  a=authenticate('assessment',assessment,policy['assessor']['key'])
  need(strict.same(set(a),{'assessor','appointment','qualification','invocation','trace','result'}),'ASSESSMENT-FIELDS')
  need(strict.same(a['assessor'],policy['assessor']['id']) and strict.same(a['appointment'],sha(enc(policy['assessor']['appointment']))) and strict.same(a['qualification'],sha(enc(policy['assessor']['qualification'])) if policy['assessor']['qualification'] else None),'ASSESSOR-BINDING')
  inv=invocation(src,policy['domain'],policy['finality_basis']);need(strict.same(a['invocation'],inv),'ASSESSMENT-INVOCATION')
  trace=a['trace'];need(type(trace) is list and strict.same(len(trace),len(OBLIGATIONS)),'TRACE-COVERAGE')
  refs=set();states=[]
  for obligation,t in zip(OBLIGATIONS,trace):
   need(type(t) is dict and strict.same(set(t),{'obligation','invocation_sha256','evidence_refs','status'}),'TRACE-FIELDS')
   need(strict.same(t['obligation'],obligation) and strict.same(t['invocation_sha256'],sha(enc(inv))),'TRACE-INVOCATION')
   need(t['status'] in ['VALID','INVALID','UNAVAILABLE'],'TRACE-STATUS')
   need(type(t['evidence_refs']) is list and len(t['evidence_refs'])<=16 and strict.same(len(set(t['evidence_refs'])),len(t['evidence_refs'])),'TRACE-REFERENCES')
   need(all(ref in artifacts for ref in t['evidence_refs']),'MISSING-FINALITY-ARTIFACT')
   need(t['status']!='VALID' or bool(t['evidence_refs']),'EMPTY-VALID-EVIDENCE')
   refs.update(t['evidence_refs']);states.append(t['status'])
  need(strict.same(refs,set(artifacts)),'EXTRA-FINALITY-ARTIFACT')
  final='INVALID' if 'INVALID' in states else 'UNAVAILABLE' if 'UNAVAILABLE' in states else 'VALID'
  need(strict.same(a['result'],{'status':final,'invocation_sha256':sha(enc(inv)),'trace_sha256':sha(enc(trace)),'finalized_blocks':sorted(set(x['block_hash'] for x in inv['outcomes']))}),'RESULT-TRACE-CORRESPONDENCE')
  if final!='VALID':blockers.append('FINALITY-ASSESSMENT-'+final)
 # The trusted assessment process must establish consensus finality, inclusion,
 # network anchor and Engine code applicability. These are NOT replayed here.
 # There is intentionally no boolean caller switch that makes this operational.
 terminal=decoded['conditional_terminal'] if not blockers else None
 return dict(decoded,format='C4-AUTHENTICATED-ASSESSMENT-CORRESPONDENCE-1',packet_sha256=sha(enc(packet)),
   policy_sha256=sha(enc(policy)),provider_signature_verified=True,assessment_signature_verified=assessment is not None,
   finality_assessment_correspondence_checked=assessment is not None,
   technical_finality_validation='EXTERNAL-ASSESSMENT-NOT-REEXECUTED',
   source_authenticated=False,authenticated_finality=False,qualification_established=False,
   laboratory_assumptions=True,blockers=blockers,conditional_terminal=terminal,authoritative_terminal=False,actual_admission=False)

def require_operational(*args,**kwargs):
 raise Blocked('GENUINE-APPOINTMENT-QUALIFICATION-AND-APPLICABLE-FINALITY-ASSESSMENT-NOT-ESTABLISHED')
