"""Pinned transaction-frontier obligations. Not proof of external non-execution."""
import ast,json,copy
from pathlib import Path
import semantic as s
import emission_sources as sources
m=s.m
# Source-derived, reviewed runtime ordering; no new transition semantics.
CUTS={
 'before_decision_commit':('NO-DECISION-COMMIT',None),
 'after_decision_commit':('DECISION-COMMITTED','DECIDED'),
 'after_sign_claim':('CLAIM-COMMITTED-SIGNATURE-UNKNOWN','SIGNING'),
 'after_signature_created':('CLAIM-COMMITTED-SIGNATURE-UNKNOWN','SIGNING'),
 'before_signature_commit':('CLAIM-COMMITTED-SIGNATURE-UNKNOWN','SIGNING'),
 'after_signature_commit':('EXACT-SIGNATURE-PERSISTED','SIGNED'),
 'before_release_commit':('RELEASE-NOT-COMMITTED','SIGNED'),
 'after_release_commit':('RELEASE-COMMITTED-RESPONSE-MAY-BE-LOST','SIGNED'),
 'before_retry_commit':('RETRY-NOT-COMMITTED','SIGNED'),
 'after_retry_commit':('RETRY-CHARGED-COMMITTED-RESPONSE-MAY-BE-LOST','SIGNED'),
 'before_observe_commit':('OBSERVATION-NOT-COMMITTED','SIGNED'),
 'after_observe_commit':('OBSERVATION-COMMITTED-DISPOSITION-GOVERNS',None)}
def cut_specs():
 tree=ast.parse(Path(__file__).read_bytes())
 return ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CUTS' for t in n.targets)))
def contract():
 rules=cut_specs()
 path='support/reference/runtime/authority.py';raw=(s.ROOT/path).read_bytes();tree,ctx=sources.tree_info(raw);faults={}
 for n in ast.walk(tree):
  if isinstance(n,ast.Call) and ast.unparse(n.func)=='fault' and isinstance(n.args[0],ast.Constant):faults[n.args[0].value]={'line':n.lineno,'expression':ast.get_source_segment(raw.decode(),n),'scope':ctx(n)[0],'guards':ctx(n)[1]}
 m.need(set(rules)<=set(faults),'CUT-SOURCE-COVERAGE')
 return {'source':m.ident(path),'cuts':{name:{'frontier':rule[0],'fixture_pending_phase':rule[1],'site':faults[name]} for name,rule in rules.items()},'outside_slice':sorted(set(faults)-set(rules)),'exception_rules':{'before_journal':'parse/context/authentication/role rejection is before journal insertion; absence alone is not external non-execution evidence','journal_commit':'packet with null response committed before action; challenge remains consumed','transaction':'BaseException rolls back active transaction; earlier commits survive','handle_exception':'Exception becomes authenticated error; BaseException may leave response null','response_bound':'response size or persistence failure may leave committed action and null response','recovered_sign':'SIGNED returns persisted action/tx without another save/signature; release stays false','ambiguous_sign':'SIGNING cannot be resigned or released; possible created/exported signature cannot be ruled out from local journal','known_failure':'FAILED-FROZEN stays blocked; no replacement/refund/resubmission right','unavailable':'retain pending/reconciliation, charges/holds; explicit exact-byte retry only under existing contract'},'final_binding':'BLOCKED','actual_admission':False}
def admitted(f,pre,q):
 """Read-only branch admission over authenticated prestate; no Authority/signing.
 Pure Fold ownership, template and reservation checks are reused; local copies
 may be evaluated but no state, blob, signature or authorization is persisted.
 """
 from correspondence import BODIES,signed_eth
 from common import keys,digest,same,need,parse,enc
 keys(q['body'],BODIES[q['method']]);b=q['body'];method=q['method'];u=q['u'];state=copy.deepcopy(pre);f.s=state
 st=f.stage(state,u);p=st['pending'];i=f.own(state,u,st['nonce'])
 def ready():
  need(p is not None and p['first'] in st['transport'] and p['latest'] in st['transport'],'ATTEMPT-ANCESTRY')
  a=f.obj(p['action']);rec=f.obj(p['latest']);f.own(state,u,int(a['template']['nonce']))
  need(rec['binding']==f.binding and rec['u']==u and rec['intent']==state['u'][u]['intent'] and rec['action']==p['action'] and rec['sid']==st['sid'],'ATTEMPT-BINDING')
  return a
 def first():
  a=ready();entry=st['transport'][p['latest']]
  need(p['latest']==p['first'] and entry['slot']=='HELD' and not entry['queried'] and not entry['released'],'FIRST-RESERVATION');return a
 if method=='decide':
  need(p is None,'UNRESOLVED');kind=b['kind'];need(kind in ['begin','append','finalize','proceed','abandon','cleanup'],'ACTION')
  if kind=='abandon':need(st['manager'] in ['OPEN','AUTHENTICATED'] and st['branch'] in ['UNDECIDED','PROCEED'] and state['u'][u]['petition'] in ['NOT-ATTEMPTED','REVERTED'],'ABANDON-STATE')
  elif kind=='cleanup':need(st['manager'] in ['ABANDONED','FAILED','CONSUMED'],'CLEANUP-STATE')
  elif kind=='proceed':need(st['manager']=='AUTHENTICATED' and st['branch']=='UNDECIDED' and state['u'][u]['petition']=='NOT-ATTEMPTED','PROCEED-STATE')
  else:
   want='begin' if st['index']==0 else 'append' if st['index']<=st['n'] else 'finalize'
   need(st['branch']=='UNDECIDED' and kind==want and ((kind=='begin' and st['manager']=='UNUSED') or (kind!='begin' and st['manager']=='OPEN')),'STAGE-ORDER')
  f.reserve(state,st,i,kind);f.template(state,st,i,kind)
 elif method=='sign':
  need(p is not None and p['action']==b['action'] and p['phase']=='DECIDED','SIGN-CLAIM-ADMISSION');a=first()
  need(a['binding']==f.binding and a['sid']==st['sid'] and a['u']==u and a['intent']==state['u'][u]['intent'] and a['branch']==st['branch'],'SIGNER-AUTHORIZATION');need(not(a['kind']=='proceed' and st['branch']=='ABANDON'),'PERMANENT-WITHDRAWAL')
 elif method=='release':
  need(p is not None and p['action']==b['action'] and p['phase']=='SIGNED' and p['tx']==b['tx'] and not p['released'],'RELEASE-BINDING');a=first();signed_eth.validate(f.get(p['tx']),a['template'])
 elif method=='retry_release':
  digest(b['retry_id']);need(p is not None and p['phase']=='SIGNED' and p['released'] and p['query'] is None,'RETRY-STATE')
  need(p['action']==b['action'] and p['tx']==b['tx'] and p['latest']==b['prior_attempt'] and b['retry_id'] not in st['retry_ids'],'RETRY-BINDING')
  need(p['reconciliation'] is not None,'RECONCILIATION-REQUIRED');e=f.obj(p['reconciliation'])
  need(e['outcome']=='UNAVAILABLE' and e['query']['attempt']==p['latest'] and e['action']==p['action'] and e['transaction']==p['tx'],'RETRY-EVIDENCE');a=ready();signed_eth.validate(f.get(p['tx']),a['template']);f.reserve(state,st,i,a['kind'],retry=True)
 elif method=='observe':
  need(p is not None and p['query'] is not None and p['action']==b['action'] and p['tx'] is not None and p['tx']==b['transaction'] and enc(p['query'])==enc(b['query']),'OBSERVATION-BINDING')
  need(b['qualification']=='LAB-ASSUMED-QUALIFIED' and b['source']=='LAB-SYNTHETIC-NOT-FINALITY' and b['outcome'] in ['SUCCESS','REVERTED','UNAVAILABLE'] and type(b['nonce_consumed']) is bool,'OBSERVATION-EVIDENCE')
  need(p['phase']=='SIGNED' and p['released'],'OBSERVATION-STATE');a=f.obj(p['action']);kind=a['kind']
  if b['outcome']=='UNAVAILABLE':need(b['manager']==st['manager'] and not b['nonce_consumed'],'UNAVAILABLE-STATE')
  else:
   need(b['nonce_consumed'],'NONCE-UNRESOLVED');want={'begin':'OPEN','append':'OPEN','finalize':'AUTHENTICATED','proceed':'CONSUMED','abandon':'ABANDONED','cleanup':'CLEANED'}[kind]
   allowed=([want,'FAILED'] if kind in ['append','finalize'] else [want]) if b['outcome']=='SUCCESS' else [st['manager']]
   need(b['manager'] in allowed and st['transport'][p['first']]['slot']=='HELD','DISPOSITION-STATE')
 else:raise m.Invalid('UNSUPPORTED-BRANCH')
 return {'method':method,'u':u,'pre_head':pre['head'],'intent':pre['u'][u]['intent'],'reservation':pre['u'][u]['reservation'],'pending':copy.deepcopy(pre['u'][u]['stage']['pending'])}

def check_fixture(x,cut):
 import ingest,value_flow
 from correspondence import Fold
 # Every entry authenticates its own current detached evidence, even if a caller
 # previously validated another object or retained a success receipt.
 x=json.loads(m.enc(x));ingest.validate_export(x);obligations=value_flow.obligations(x)
 rules=cut_specs();m.need(type(cut) is str and cut in rules,'UNSUPPORTED-CUT')
 head=json.loads(bytes.fromhex(x['head']));unanswered=[row for row in x['journal'] if row[2] is None];m.need(len(unanswered)==1,'CUT-JOURNAL')
 packet=bytes.fromhex(unanswered[0][1]);q=json.loads(packet)['request'];qh=m.sha(m.enc(q))
 methods={'before_decision_commit':'decide','after_decision_commit':'decide','after_sign_claim':'sign','after_signature_created':'sign','before_signature_commit':'sign','after_signature_commit':'sign','before_release_commit':'release','after_release_commit':'release','before_retry_commit':'retry_release','after_retry_commit':'retry_release','before_observe_commit':'observe','after_observe_commit':'observe'}
 m.need(q['method']==methods[cut],'CUT-REQUEST-METHOD')
 blobs={ref:bytes.fromhex(raw) for ref,raw in x['blobs']};owners={coord:json.loads(bytes.fromhex(raw)) for coord,raw,_ in x['owners']};f=Fold(x['config'],json.loads(bytes.fromhex(x['ownership_meta'])),blobs,owners)
 histories={f.s['head']:copy.deepcopy(f.s)};requests={m.sha(m.enc(json.loads(bytes.fromhex(row[1]))['request'])):json.loads(bytes.fromhex(row[1]))['request'] for row in x['journal']};events=[]
 for _,rawhex in x['events']:
  raw=bytes.fromhex(rawhex);event=json.loads(raw);f.advance(event,raw,requests[event['request']]);histories[f.s['head']]=copy.deepcopy(f.s);events.append(event)
 m.need(q['expected'] in histories,'CUT-PRESTATE');pre=histories[q['expected']];binding=admitted(f,pre,q)
 ev=[e for e in events if e['request']==qh];kinds=[e['kind'] for e in ev]
 expected={'before_decision_commit':[],'after_decision_commit':['decide'],'after_sign_claim':['sign-claim'],'after_signature_created':['sign-claim'],'before_signature_commit':['sign-claim'],'after_signature_commit':['sign-claim','sign-persist'],'before_release_commit':[],'after_release_commit':['release'],'before_retry_commit':[],'after_retry_commit':['retry-release'],'before_observe_commit':[],'after_observe_commit':['observe']}[cut]
 m.same(kinds,expected,'CUT-COMMITTED-EVENTS')
 # The claimed frontier must be the current suffix, not an older surviving request.
 m.need(head['seq']==pre['seq']+len(ev),'CUT-NOT-CURRENT');m.need(all(e['request']==qh for e in events[pre['seq']:]),'CUT-INTERLEAVING')
 stage=head['u'][q['u']]['stage'];p=stage['pending']
 if q['method']=='sign':m.need(p is not None and p['action']==q['body']['action'] and p['phase']==('SIGNED' if len(ev)==2 else 'SIGNING'),'CUT-SIGN-PHASE')
 if cut=='before_release_commit':m.need(p is not None and not p['released'],'UNCOMMITTED-RELEASE')
 if cut in ['after_release_commit','after_retry_commit']:m.need(p is not None and p['released'],'COMMITTED-RELEASE')
 if cut=='after_retry_commit':m.need(p['latest']!=p['first'] and stage['transport'][p['latest']]['slot']=='CONSUMED','CHARGED-RETRY')
 compatible=['after_sign_claim','after_signature_created','before_signature_commit'] if q['method']=='sign' and kinds==['sign-claim'] else [cut]
 return {'cut':cut,'frontier':rules[cut][0],'compatible_frontiers':compatible,'observed_fault_location':None,'claim_scope':'authenticated current state/history and source-branch compatibility only; not proof that a named fault executed','committed_events':kinds,'request':qh,'packet':m.sha(packet),'export_sha256':m.sha(m.enc(x)),'head':head['head'],'branch_binding':binding,'phase':p['phase'] if p else None,'counts':head['counts'],'resources':head['resources'],'obligations':obligations,'external_execution':'NOT-DETERMINED-BY-LOCAL-CUT','obligations_preserved':True,'final_binding':'BLOCKED','actual_admission':False,'stream_identities':'UNCOMPUTED'}

def validate_receipt(value,x,cut):m.same(value,check_fixture(x,cut),'CUT-RECEIPT-SUBSTITUTION');return True

def validate_contract(value):m.same(value,contract(),'EXCEPTION-CONTRACT');return True
