import strict_types as strict
"""Bounded C4 decoder. No network, authority oracle, or operational terminal permit.
Only the explicit one-hop Aurora submit receipt path is supported.
"""
import base64,json,struct
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from anchor import enc,sha,need,Blocked
SOURCE_PINS={'near-primitives-0.38.0-rc.3/src/views.rs': '134ea6778f7b2b6d406636aafa03293062d040744f1f1d421cd72b4fc949a44c', 'aurora/source/engine-types/src/parameters/engine.rs': 'dc574c56b5d1521e683484c18b1a9d71069086bf84b5db9937326bdef4b98e2b', 'build-source/transaction.go': '408ccff8159091b1176f250f64a00f82dc39fe42e916d97500554f980b47b88b'}
MAX_JSON=32768
MAX_RESULT=16384
MAX_RESPONSE=524288 # bounded implementation envelope, not a full-domain source-policy maximum
MAX_PACKET=3145728
DOMAIN=b'I164-C4-LAB-EVIDENCE-1\0'
ALPHABET='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58(raw):
 n=int.from_bytes(raw,'big');s=''
 while n:n,r=divmod(n,58);s=ALPHABET[r]+s
 return '1'*(len(raw)-len(raw.lstrip(b'\0')))+s
def hash32(s):
 need(type(s) is str and 1<=len(s)<=44,'BASE58-SIZE');n=0
 for c in s:need(c in ALPHABET,'BASE58');n=n*58+ALPHABET.index(c)
 raw=b'\0'*(len(s)-len(s.lstrip('1')))+(n.to_bytes((n.bit_length()+7)//8,'big') if n else b'')
 need(strict.same(len(raw),32) and strict.same(b58(raw),s),'BASE58-HASH');return raw
def unhex(s,limit):
 need(type(s) is str and strict.same(len(s)%2,0) and len(s)<=limit*2 and all(c in '0123456789abcdef' for c in s),'HEX-BOUND')
 return bytes.fromhex(s)
def obj(raw,limit=MAX_JSON):
 need(type(raw) is bytes and len(raw)<=limit,'JSON-BOUND')
 def pairs(xs):
  d={}
  for k,v in xs:need(k not in d,'DUPLICATE-JSON');d[k]=v
  return d
 try:return json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(Blocked('JSON-CONSTANT')))
 except (UnicodeError,RecursionError,json.JSONDecodeError) as ex:raise Blocked('JSON-DECODE') from ex
class Reader:
 def __init__(self,b):need(type(b) is bytes and len(b)<=MAX_RESULT,'RESULT-BOUND');self.b=b;self.i=0
 def take(self,n):
  need(type(n) is int and 0<=n<=len(self.b)-self.i,'TRUNCATED');a=self.b[self.i:self.i+n];self.i+=n;return a
 def number(self,n):return int.from_bytes(self.take(n),'little')
 def vec(self):return self.take(self.number(4))
def engine_result(raw):
 r=Reader(raw);need(strict.same(r.number(1),7),'UNSUPPORTED-SUBMIT-VERSION');tag=r.number(1)
 names=['SUCCESS','REVERTED','OutOfGas','OutOfFund','OutOfOffset','CallTooDeep','StackUnderflow','StackOverflow','InvalidJump','InvalidRange','DesignatedInvalid','CreateCollision','CreateContractLimit','InvalidCode','PCUnderflow','CreateEmpty','MaxNonce','UsizeOverflow','Other','CreateContractStartingWithEF']
 need(tag<len(names),'UNSUPPORTED-STATUS');output=b''
 if tag in (0,1,18):
  output=r.vec()
  if strict.same(tag,18):
   try:output.decode('utf-8')
   except UnicodeError as ex:raise Blocked('OTHER-UTF8') from ex
 elif strict.same(tag,13):output=r.take(1)
 gas=r.number(8);n=r.number(4);need(n<=128,'LOG-COUNT');logs=[]
 for _ in range(n):
  address=r.take(20);nt=r.number(4);need(nt<=64,'TOPIC-COUNT');topics=[r.take(32).hex() for _ in range(nt)];data=r.vec();logs.append({'address':address.hex(),'topics':topics,'data':data.hex()})
 need(strict.same(r.i,len(raw)),'TRAILING-RESULT')
 return {'status':names[tag],'evm_outcome':names[tag] if tag<2 else 'OTHER-EVM-FAILURE','output_hex':output.hex(),'gas_used':gas,'logs':logs,'sha256':sha(raw)}
def b64(s):
 need(type(s) is str and len(s)<=MAX_RESULT*2,'BASE64-BOUND')
 try:b=base64.b64decode(s,validate=True)
 except ValueError as ex:raise Blocked('BASE64') from ex
 need(strict.same(base64.b64encode(b).decode(),s),'BASE64-CANONICAL');return b

def context(config,binding,v,u,op,query_ordinal):
 from runtime import executor as e
 # Source IDs are immutable governing bindings, not evidence that the source is qualified.
 return {'service_binding':binding,'pilot':config['pilot'],'session':config['session'],'u':u,'intent_sha256':v['intent'],'evm_sha256':v['record']['tx_ref'],'attempt':v['attempt'],'observation_request':op,'query_ordinal':query_ordinal,'implementation':config['implementation'],'near_binding':v['near']}

def decode(packet,expected,evm):
 """Exact transport + source decoding; positive result remains laboratory-only.
 No caller field can appoint a finality authority. No operational verifier exists here.
 """
 from runtime import retained
 t=retained.t
 need(type(packet) is dict and strict.same(set(packet),{'claim','signature'}),'EVIDENCE-FIELDS')
 need(len(enc(packet))<=MAX_PACKET,'EVIDENCE-BOUND');c=packet['claim']
 need(type(c) is dict and strict.same(set(c),{'format','context','near_spec','near_hex','rpc_request_hex','rpc_response_hex','provenance'}),'CLAIM-FIELDS')
 strict.context(c['context']);strict.context(expected);strict.near_spec(c['near_spec'])
 need(c['format'] in ['C4-LAB-NEAR-SUBMIT-1','C4-SAVED-NEAR-SUBMIT-1'] and strict.same(c['context'],expected),'EVIDENCE-CONTEXT')
 need(any(strict.same(c['provenance'],v) for v in [{'kind':'INDEPENDENTLY-CONSTRUCTED-LAB-FIXTURE','source_authenticated':False,'qualification_established':False},{'kind':'SAVED-SOURCE-BYTES','source_authenticated':False,'qualification_established':False}]),'PROVENANCE')
 raw=unhex(c['near_hex'],t.MAX_NEAR);txid=t.exact_near(c['near_spec'],bytes(evm),raw);s=c['near_spec']
 need(strict.same(txid,expected['near_binding']['transaction_id']) and strict.same(sha(raw),expected['near_binding']['signed_sha256']) and strict.same(sha(enc({'near_spec':s,'near_hex':c['near_hex']})),expected['near_binding']['ref']),'PREPARED-NEAR-BINDING')
 reqraw=unhex(c['rpc_request_hex'],MAX_JSON);resraw=unhex(c['rpc_response_hex'],MAX_RESPONSE);q=obj(reqraw);response=obj(resraw,MAX_RESPONSE)
 need(type(q) is dict and strict.same(set(q),{'jsonrpc','id','method','params'}) and strict.same(q['jsonrpc'],'2.0') and type(q['id']) is str,'RPC-REQUEST')
 need(strict.same(q['method'],'tx') and strict.same(q['params'],{'tx_hash':b58(bytes.fromhex(txid)),'sender_account_id':s['signer'],'wait_until':'FINAL'}),'RPC-QUERY-BINDING')
 need(type(response) is dict and strict.same(set(response),{'jsonrpc','id','result'}) and strict.same(response['jsonrpc'],'2.0') and strict.same(response['id'],q['id']),'RPC-RESPONSE')
 z=response['result'];need(type(z) is dict,'RESULT-OBJECT')
 need(strict.same(set(z),{'final_execution_status','status','transaction','transaction_outcome','receipts_outcome'}),'RESULT-FIELDS')
 # This string is reported finality only. It never establishes authoritative finality.
 need(strict.same(z['final_execution_status'],'FINAL'),'REPORTED-FINALITY-UNAVAILABLE')
 tx=z['transaction'];strict.transaction(tx);need(type(tx) is dict,'TRANSACTION-VIEW')
 expectedtx={'hash':b58(bytes.fromhex(txid)),'signer_id':s['signer'],'public_key':'ed25519:'+b58(bytes.fromhex(s['public_key'])),'nonce':s['nonce'],'receiver_id':s['engine'],'actions':[{'FunctionCall':{'method_name':'submit','args':base64.b64encode(evm).decode(),'gas':s['gas'],'deposit':'0'}}],'signature':'ed25519:'+b58(raw[-64:])}
 need(type(tx.get('priority_fee',0)) is int and strict.same(tx.get('priority_fee',0),0),'UNSUPPORTED-PRIORITY')
 normalized=dict(tx);normalized.pop('priority_fee',None)
 need(strict.same(normalized,expectedtx),'TRANSACTION-VIEW-BINDING')
 root=z['transaction_outcome'];rs=z['receipts_outcome'];need(type(rs) is list and 1<=len(rs)<=32,'RECEIPT-BOUND')
 def outcome(x):
  need(type(x) is dict and strict.same(set(x),{'id','block_hash','proof','outcome'}),'OUTCOME-FIELDS');hash32(x['id']);hash32(x['block_hash']);need(type(x['proof']) is list and len(x['proof'])<=64,'PROOF-BOUND')
  for proof in x['proof']:
   need(type(proof) is dict and strict.same(set(proof),{'hash','direction'}) and proof['direction'] in ['Left','Right'],'PROOF-SCHEMA');hash32(proof['hash'])
  o=x['outcome'];need(type(o) is dict and strict.same(set(o),{'executor_id','status','receipt_ids','logs','gas_burnt','tokens_burnt','metadata'}),'OUTCOME-SCHEMA')
  need(type(o['status']) is dict and strict.same(len(o['status']),1),'STATUS-SCHEMA');need(type(o['receipt_ids']) is list and len(o['receipt_ids'])<=32 and strict.same(len(set(o['receipt_ids'])),len(o['receipt_ids'])),'RECEIPT-IDS')
  for h in o['receipt_ids']:hash32(h)
  need(type(o['gas_burnt']) is int and 0<=o['gas_burnt']<2**64,'GAS');need(type(o['tokens_burnt']) is str and o['tokens_burnt'].isdigit(),'TOKENS');need(type(o['logs']) is list and all(type(log) is str for log in o['logs']) and type(o['metadata']) is dict,'OUTCOME-METADATA')
  return o
 ro=outcome(root);need(strict.same(root['id'],expectedtx['hash']) and strict.same(ro['executor_id'],s['signer']),'ROOT-JOIN')
 need(strict.same(set(ro['status']),{'SuccessReceiptId'}),'NO-EXECUTION-RECEIPT')
 rid=ro['status']['SuccessReceiptId'];hash32(rid);need(rid in ro['receipt_ids'],'ROOT-RECEIPT-LINK')
 byid={}
 for x in rs:
  outcome(x);need(x['id'] not in byid and x['id']!=root['id'],'DUPLICATE-RECEIPT');byid[x['id']]=x
 need(rid in byid,'MISSING-ENGINE-RECEIPT')
 # Complete bounded DAG from transaction. Reject absent/extraneous/forked/cyclic receipt occurrences.
 todo=list(ro['receipt_ids']);seen=set()
 while todo:
  h=todo.pop();need(h not in seen and h in byid,'RECEIPT-CLOSURE');seen.add(h);todo.extend(byid[h]['outcome']['receipt_ids'])
 need(strict.same(seen,set(byid)),'EXTRA-RECEIPT')
 selected=byid[rid]['outcome'];need(strict.same(selected['executor_id'],s['engine']),'ENGINE-RECEIPT-OWNER')
 status=selected['status'];need(strict.same(z['status'],status),'CONFLICTING-FINAL-STATUS')
 # Selected path returns directly, never follows an async promise as if it were Engine output.
 need(set(status) in ({'SuccessValue'},{'Failure'}),'UNSUPPORTED-ASYNC-RESULT')
 for h,x in byid.items():
  if h!=rid:need(strict.same(x['outcome']['status'],{'SuccessValue':''}) and not x['outcome']['receipt_ids'],'UNSUPPORTED-AUXILIARY-OUTCOME')
 result=None
 if 'Failure' in status:
  need(type(status['Failure']) is dict and bool(status['Failure']),'FAILURE-SCHEMA');near='FAILURE';evmout='UNAVAILABLE'
 else:
  near='SUCCESS';result=engine_result(b64(status['SuccessValue']));evmout=result['evm_outcome']
 return {'source_pins':SOURCE_PINS,'format':'C4-CONDITIONAL-DECODE-1','context':expected,'packet_sha256':sha(enc(packet)),'near_transaction_id':txid,'near_bytes_sha256':sha(raw),'evm_bytes_sha256':sha(evm),'rpc_request_sha256':sha(reqraw),'rpc_response_sha256':sha(resraw),'engine_receipt_id':rid,'receipt_ids':sorted(seen),'near_execution':near,'evm_outcome':evmout,'engine_result':result,'reported_finality':'FINAL','authenticated_finality':False,'source_authenticated':False,'qualification_established':False,'authoritative_terminal':False,'actual_admission':False,'conditional_terminal':evmout if evmout in ('SUCCESS','REVERTED') else None}

def require_authoritative(result):
 raise Blocked('C4-AUTHENTICATED-APPLICABLE-FINALITY-SOURCE-APPOINTMENT-AND-QUALIFICATION-UNAVAILABLE')


def validate(packet,expected,evm,lab_public):
 r=decode(packet,expected,evm)
 need(strict.same(packet['claim']['format'],'C4-LAB-NEAR-SUBMIT-1'),'LEGACY-LAB-FORMAT')
 sig=unhex(packet['signature'],64);need(strict.same(len(sig),64) and type(lab_public) is bytes and strict.same(len(lab_public),32),'LAB-SIGNATURE')
 try:Ed25519PublicKey.from_public_bytes(lab_public).verify(sig,DOMAIN+enc(packet['claim']))
 except Exception as ex:raise Blocked('LAB-AUTHENTICATION') from ex
 return r
