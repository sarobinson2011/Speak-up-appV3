"""Bounded source-parameterized comparison computation. Operational permit always false."""
import sys,json,hashlib,subprocess,copy,os,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'accepted'),str(ROOT/'adapter')]
import expr_v2 as x
import owning_selected as ow
from profile_body import validate_body
from bridge import wire,sha,context
VERSION='I164-TYPED-COMPARISON-PROVIDER-1'
DOMAIN=b'I164-CONDITIONAL-COMPARISON-SOURCE-V1\n' # engineering carrier, not renamed V2 privacy evidence
BACKEND=ROOT/'adapter/retained/collector/kernel/crypto_backend/bin/pe-rfc8032-stream'
BACKEND_SHA='3d8b65ea87eb5b5a680c9c51c6897a8c32641f1580947046d1cc6c7f765c152b'
CODES=['INVALID-IDENTITY','UNREGISTERED-IDENTITY','DIGEST-MISMATCH','INVALID-PROFILE','INVALID-AUTHORIZATION','INVALID-OPENING','UNAUTHENTICATED-STATE']
HEADER='serialization-domain successor-generation-id mapping-id mapping-sha256 profile-id profile-sha256 authorization-id transition-occurrence-id determination-id authorized-state-id successor-state-relation-definition-id ordering-coordinate-set-digest dependency-coordinate-set-digest component-count'.split()
BIND='component_order component_id binding_mode canonical_type_id authorization_context_digest bound_value'.split()
ATTEMPT='comparison_attempt_id generation_id mapping_id mapping_sha256 profile_id profile_sha256 authorization_id authorization_sha256 transition_occurrence_id determination_id authorized_state_id authorized_state_sha256 current_state_id current_state_sha256 stage result failure_code'.split()
class Invalid(ValueError):
 def __init__(self,code,reason):self.code=code;super().__init__(reason)
def require(ok,code,reason):
 if not ok:raise Invalid(code,reason)
def load(p):
 
 with Path(p).open('rb') as f:b=f.read(16*1024**2+1)
 require(len(b)<=16*1024**2,'INVALID-PROFILE','conditional carrier size')
 def unique(rows):
  d={}
  for k,v in rows:require(k not in d,'INVALID-PROFILE','duplicate key');d[k]=v
  return d
 a=json.loads(b,object_pairs_hook=unique);require(wire(a)==b,'INVALID-PROFILE','noncanonical carrier');return a,b
def program(p,root=None):
 t=x.Types(tuple((r[0],r[1],tuple(r[2])) for r in p['types']))
 ds=[x.Definition(d['id'],tuple(d['inputs']),d['output'],x.parse(d['expression']),d['kind'],d['source'],d['anchor']) for d in p['definitions']]
 cs=[x.Component(**c) for c in p['components']];fs=[x.Field(**f) for f in p['fields']]
 return x.Profile(t,ds,cs,fs,root or p['root_definition'],tuple(p['root_fields']) if root is None else tuple(p['comparison_inputs'][root]),tuple((g[0],tuple(g[1]),g[2]) for g in p['groups']))
def canonical_program(spec):
 p=program(spec)
 return wire({'types':list(p.types.rows.items()),'definitions':[d.__dict__ for d in p.defs.values()],'components':[c.__dict__ for c in p.components.values()],'fields':[f.__dict__ for f in p.fields.values()],'root_definition':p.root_definition,'root_fields':p.root_fields,'groups':p.groups})
def semantics_identity():
 return sha(wire({n:sha((ROOT/'accepted'/n).read_bytes()) for n in ['expr_v2.py','profile_body.py','owning_selected.py']}))
def objects(p,rows):
 require(set(rows)==set(p.fields),'UNAUTHENTICATED-STATE','complete exact field acquisition')
 out={}
 for f,r in rows.items():
  require(set(r)=={'object_id','value','source','anchor','evidence_id','evidence','endpoint','authoritative','valid','authenticated'},'UNAUTHENTICATED-STATE','read fields')
  require(all(type(r[k]) is bool for k in ['authoritative','valid','authenticated']),'UNAUTHENTICATED-STATE','validation status types')
  require(all(r[k] for k in ['authoritative','valid','authenticated']),'UNAUTHENTICATED-STATE','invalid acquired read facts')
  require((r['source'],r['anchor'])==(p.fields[f].source,p.fields[f].anchor),'UNAUTHENTICATED-STATE','field ownership')
  v={**r,**{k:bytes.fromhex(r[k]) for k in ['value','evidence','endpoint']}}
  require(p.types.decode(v['value'])[0]==p.fields[f].type,'UNAUTHENTICATED-STATE','typed read')
  out[f]=x.ReadObject(**v)
 return out
def classify(eq,mc):
 if eq==1 and mc==1:return 'indeterminate','INCONSISTENT-BOTH-TRUE'
 if mc==1:return 'material-conflict','NONE'
 if eq==1 and mc==0:return 'equivalent','NONE'
 if eq==0 and mc==0:return 'indeterminate','INCOMPLETE-PROFILE-COVERAGE'
 return 'indeterminate','UNRESOLVED-REQUIRED-INPUT'
def compute(carrier,trust,expected):
 expected=context(expected);raw=wire(carrier);require(len(raw)<=16*1024**2,'INVALID-PROFILE','bounded carrier');fail=[];payload=None;eq=mc=None;authenticated=False;attempt=None;trace={}
 def check(ok,code,reason):require(ok,code,reason)
 try:
  check(set(carrier)=={'payload','signature'},'INVALID-PROFILE','carrier fields');payload=carrier['payload']
  check(set(payload)=={'format','source','context','program','reads','evaluation','authorization','bindings','values','history','attempt','state','mapping','owning'},'INVALID-PROFILE','source payload fields')
  check(payload['format']==VERSION,'INVALID-PROFILE','version')
  a=payload['attempt'];h=payload['authorization'];u=expected['u']
  for v in [u,payload['source'],a['comparison_attempt_id'],a['generation_id'],a['mapping_id'],a['profile_id'],a['authorization_id'],a['transition_occurrence_id'],a['determination_id'],a['authorized_state_id'],a['current_state_id'],payload['evaluation']['eid']]:check(x.identifier(v),'INVALID-IDENTITY','identifier')
  check(payload['source']==trust['source'],'UNREGISTERED-IDENTITY','source appointment')
  check(payload['context']==expected,'DIGEST-MISMATCH','operation/U/contract/config/cut context')
  check(sha(wire(payload['program']))==trust['program_sha256'],'DIGEST-MISMATCH','source-owned program identity')
  check(trust['outer_program_sha256']==sha(canonical_program(payload['program'])),'DIGEST-MISMATCH','exact immutable EXPRESSION-PROGRAM')
  check(trust['context_sha256']==sha(wire(expected)),'DIGEST-MISMATCH','appointment context')
  check(sha(BACKEND.read_bytes())==BACKEND_SHA,'INVALID-PROFILE','backend identity')
  p=program(payload['program']);x.revalidate_program(p)
  check(len(p.fields)<=1024 and len(p.defs)<=256 and len(p.components)<=64,'INVALID-PROFILE','bounded provider capability')
  check(all(v.source==payload['source'] for table in [p.defs,p.fields,p.components] for v in table.values()),'INVALID-PROFILE','source-owned declaration correspondence')
  check(payload['program']['mc_definitions'] and len(set(payload['program']['mc_definitions']))==len(payload['program']['mc_definitions']),'INVALID-PROFILE','ordered conflict coverage')
  for name in [payload['program']['eq_definition'],*payload['program']['mc_definitions']]:
   check(name in p.defs and p.defs[name].output==x.B and name in payload['program']['comparison_inputs'],'INVALID-PROFILE','comparison definition signature')
  check(set(h)==set(HEADER),'INVALID-AUTHORIZATION','exact authorization header')
  check(h['serialization-domain']=='PE-TSE-AUTHORIZATION-V1' and h['transition-occurrence-id']==u==a['transition_occurrence_id'],'INVALID-AUTHORIZATION','U authorization')
  check(payload['history']==[f'{u}-TSE-CMP-{n:06}' for n in range(1,len(payload['history'])+1)] and 0<len(payload['history'])<=999999 and a['comparison_attempt_id']==payload['history'][-1],'INVALID-AUTHORIZATION','complete authenticated history; occurrence code INVALID-ACTION-CONTEXT')
  check(set(a)==set(ATTEMPT)-{'result','failure_code'} and a['stage']=='PRE-COMMITMENT','INVALID-AUTHORIZATION','attempt fields/stage')
  for hn,an in [('successor-generation-id','generation_id'),('mapping-id','mapping_id'),('mapping-sha256','mapping_sha256'),('profile-id','profile_id'),('profile-sha256','profile_sha256'),('authorization-id','authorization_id'),('determination-id','determination_id'),('authorized-state-id','authorized_state_id')]:check(h[hn]==a[an],'INVALID-AUTHORIZATION','authorization attempt join '+hn)
  check(a['profile_sha256']==expected['profile'],'INVALID-AUTHORIZATION','collector profile join')
  mapping=payload['mapping'];check(mapping==trust['mapping'] and mapping['relation']==h['successor-state-relation-definition-id'] and mapping['relation']==payload['program']['eq_definition'],'INVALID-AUTHORIZATION','independently pinned mapping relation')
  header=x.tsv(['field_order','field_name','field_value'],[[f'{i:04}',k,h[k]] for i,k in enumerate(HEADER,1)])
  bindings=payload['bindings'];check(len(bindings)==len(p.components)==int(h['component-count']) and h['component-count']==f'{len(p.components):06}','INVALID-AUTHORIZATION','component completeness')
  for i,(row,c) in enumerate(zip(bindings,p.components.values()),1):
   check(set(row)==set(BIND) and row['component_order']==f'{i:04}' and row['component_id']==c.id and row['canonical_type_id']==c.canonical and row['authorization_context_digest']==sha(header),'INVALID-AUTHORIZATION','component/context join')
   v=payload['values'][c.id];canonical=bytes.fromhex(v['canonical_value']);represented=bytes.fromhex(v['represented_value']);check(p.types.decode(canonical)[0]==c.canonical and p.types.decode(represented)[0]==c.represented,'INVALID-OPENING','value types')
   if row['binding_mode']=='CANONICAL-VALUE':check(row['bound_value']==canonical.hex() and v['blind']==v['opening']==x.NA,'INVALID-OPENING','canonical binding')
   elif row['binding_mode']=='BLINDED-SHA256-COMMITMENT':
    blind=bytes.fromhex(v['blind']);check(len(blind)==32 and bytes.fromhex(v['opening'])==x.lp(canonical)+blind,'INVALID-OPENING','opening')
    pre=x.lp(b'PE-TSE-COMPONENT-COMMITMENT-V1')+bytes.fromhex(row['authorization_context_digest'])+x.lp(c.id.encode())+x.lp(c.canonical.encode())+x.lp(canonical)+blind;check(row['bound_value']==sha(pre),'INVALID-OPENING','commitment')
   else:check(False,'INVALID-OPENING','binding mode')
   check(payload['reads'][p.fid(c.id,'AUTHORIZED','VALUE')]['value']==canonical.hex(),'INVALID-OPENING','authorized projected value')
  check(set(payload['values'])==set(p.components),'INVALID-OPENING','extra/missing openings')
  auth=header+x.tsv(BIND,[[r[k] for k in BIND] for r in bindings]);check(a['authorization_sha256']==sha(auth),'DIGEST-MISMATCH','authorization bytes')
  owning=payload['owning'];privacy=ow.PrivacyProfile(owning['profile_id'],[ow.PrivacyComponent(**r) for r in owning['components']],{},False)
  privacy.source_owned_body=bytes.fromhex(owning['body_hex']);privacy.source_identities=owning['source_identities'];privacy.binding_sha256=expected['profile']
  check(sha(privacy.source_owned_body)==trust['outer_body_sha256'] and sha(wire(owning['components']))==trust['outer_components_sha256'],'DIGEST-MISMATCH','exact owning body and privacy register')
  scalars,_=validate_body(privacy.source_owned_body,p,privacy,privacy.source_identities)
  facts={k:owning['mapping_facts'][k] for k in ow.MAPPING_FACT_FIELDS};ow.mapping_facts(privacy,p,facts,scalars)
  # Pinned canonical pure Ed25519 consumes these original carrier bytes, not a digest.
  message=DOMAIN+wire(payload);sig=carrier['signature'];pk=trust['public_key']
  check(len(bytes.fromhex(sig))==64 and len(bytes.fromhex(pk))==32,'UNAUTHENTICATED-STATE','authentication encoding')
  proc=subprocess.run([str(BACKEND),'verify',pk,sig,str(len(message)),str(len(message))],input=message,capture_output=True,timeout=5)
  check(proc.returncode==0 and json.loads(proc.stdout).get('verified') is True,'UNAUTHENTICATED-STATE','source signature');authenticated=True
  obs=objects(p,payload['reads']);ev=payload['evaluation'];check(ev['did']==a['determination_id'],'INVALID-AUTHORIZATION','E/D join')
  pkg={k:bytes.fromhex(v) for k,v in ev['package'].items()}
  try:x.replay(p,obs,pkg,ev['eid'],ev['did'])
  except ValueError as exc:raise Invalid('DIGEST-MISMATCH','E/D exact replay correspondence: '+str(exc))
  # These source-owned state objects are engineering carriers. Their schema/type interpretation
  # is explicitly pinned in the laboratory source, not inferred from object names.
  state=payload['state'];check(set(state)=={'authorized','current'},'UNAUTHENTICATED-STATE','state objects')
  check(state['authorized']['id']==a['authorized_state_id'] and state['current']['id']==a['current_state_id'],'UNAUTHENTICATED-STATE','state identity')
  check(sha(wire(state['authorized']))==a['authorized_state_sha256'] and sha(wire(state['current']))==a['current_state_sha256'],'DIGEST-MISMATCH','state digest')
  check(state['current']['cut']==expected['cut'] and state['current']['configuration']==expected['configuration'],'UNAUTHENTICATED-STATE','current contract state projection')
  check(state['authorized']['determination_sha256']==sha(pkg['determination']),'DIGEST-MISMATCH','D/Q0 binding')
  cutfields=trust['mapping']['cut_fields'];check(set(cutfields)=={'AUTHORIZED','CURRENT'} and all(k in p.fields and p.fields[k].type==x.Y for k in cutfields.values()),'INVALID-PROFILE','source-owned cut interpretation')
  for side in ['AUTHORIZED','CURRENT']:
   st=state[side.lower() if side=='CURRENT' else 'authorized'];check(p.types.decode(obs[cutfields[side]].value)==(x.Y,bytes.fromhex(st['cut'])),'UNAUTHENTICATED-STATE','typed cut bytes correspondence');check(st['fields']=={f:r['value'] for f,r in payload['reads'].items() if '-'+side+'-' in f},'UNAUTHENTICATED-STATE','exact state/read projection')
  def evaluate(name):
   pp=program(payload['program'],name);ee=x.Evaluation(pp,obs,ev['eid']+'-CMP',ev['did']+'-CMP');v=ee.invoke('PE-TSE-OP-ROOT',root=True);trace[name]=sha(x.tsv(x.EVENT_HEADER,ee.events));return pp.types.decode(v)[1]
  eq=evaluate(payload['program']['eq_definition']);terms=[evaluate(n) for n in payload['program']['mc_definitions']];mc=1 if 1 in terms else 0 if all(v==0 for v in terms) else 2
  result,code=classify(eq,mc);attempt={**a,'result':result,'failure_code':code}
  records={'AUTHORIZATION-HEADER':[{k:h[k] for k in ow.SCHEMAS['AUTHORIZATION-HEADER']}],'COMPONENT-BINDING':[{k:r[k] for k in ow.SCHEMAS['COMPONENT-BINDING']} for r in bindings],'COMPARISON-ATTEMPT':[{k:attempt[k] for k in ow.SCHEMAS['COMPARISON-ATTEMPT']}],'COMPARISON-RESULT':[dict(zip(ow.SCHEMAS['COMPARISON-RESULT'],[a['comparison_attempt_id'],u,result,code]))],'RECOVERY-RESULT':[dict(zip(ow.SCHEMAS['RECOVERY-RESULT'],[u,a['comparison_attempt_id'],'PRE-COMMITMENT',result,x.NA if result=='equivalent' else 'UNRESOLVED','ACTIVE' if result=='equivalent' else 'TRANSITION-FAILURE']))],'OBSERVABILITY-OUTPUT':[{'transition_occurrence_id':u,'classification':result}]}
  for i,component in enumerate(p.components.values(),1):records[f'COMPONENT-{i:04}']=[{k:payload['values'][component.id][k] for k in privacy.schemas[f'COMPONENT-{i:04}']}]
  ow.owning_records(privacy,{u:records},p,{u:payload['history']},facts)
  trace['canonical_records_sha256']=sha(wire(records))
 except Invalid as e:result,code='indeterminate',e.code;fail.append({'code':e.code,'reason':str(e)})
 except (ValueError,KeyError,TypeError,IndexError,OverflowError,subprocess.TimeoutExpired) as e:result,code='indeterminate','INVALID-PROFILE';fail.append({'code':code,'reason':str(e)})
 return {'format':VERSION,'context':expected,'carrier_sha256':sha(raw),'trust_sha256':sha(wire(trust)),'provider_sha256':sha(Path(__file__).read_bytes()),'semantics_sha256':semantics_identity(),'evaluator_sha256':sha((ROOT/'accepted/expr_v2.py').read_bytes()),'backend_sha256':BACKEND_SHA,'result':result,'failure_code':code,'eq':eq,'mc':mc,'failures':fail,'source_signature_verified':authenticated,'source_truth_qualified':False,'conditional_equivalent':result=='equivalent' and not fail,'attempt':attempt,'owning_records_validated':bool(trace.get('canonical_records_sha256')),'trace_sha256':trace,'operational_permit':False,'actual_admission':False}

def acquire(path,trust_path,expected):
 carrier,_=load(path);trust,_=load(trust_path);return compute(carrier,trust,expected)

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--carrier',required=True);ap.add_argument('--trust',required=True);ap.add_argument('--context',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
 try:
  c,_=load(a.context);r=acquire(a.carrier,a.trust,c);Path(a.out).write_bytes(wire(r));print(json.dumps({'result':r['result'],'failure_code':r['failure_code'],'source_signature_verified':r['source_signature_verified'],'actual_admission':False}))
 except (Invalid,ValueError,OSError) as e:print(json.dumps({'result':'BLOCKED-ACQUISITION','reason':str(e),'actual_admission':False}));sys.exit(2)
