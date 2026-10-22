"""Bounded lab persistence oracle; not storage qualification or runtime attestation.
New entry points do not relax or replace EB01/SV01/SV02/VF01 validators.
"""
import ast,sys,dis,json,copy,hashlib
from pathlib import Path
from observation_contract import AUTH,raw_source,fn,codes,need,exact
from boundary_events import identity
from boundary_values import basis
import value_flow as vf

def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def err(t,m,c=None):return dict(type=t,message=m,context=c)
def span(n):return [n.lineno,n.end_lineno,n.col_offset,n.end_col_offset]
def contract(root):
 need(sys.implementation.name=='cpython' and sys.version_info[:3]==(3,12,14),'PF-INTERPRETER')
 raw=raw_source(root,AUTH);basis(root)
 fs={n:fn(raw,n) for n in ('Authority.handle','Authority.sign','Authority.transaction')};cs={n:next(c for c in codes(raw) if c.co_qualname==n) for n in fs}
 def call(n,s):return next(v for v in ast.walk(n) if isinstance(v,ast.Call) and ast.unparse(v.func)=='self.db.execute' and v.args and isinstance(v.args[0],ast.Constant) and v.args[0].value==s)
 h=fs['Authority.handle'];s=fs['Authority.sign'];ws=[v for v in ast.walk(h) if isinstance(v,ast.With)]
 admission=next(w for w in ws if 'INSERT INTO journal' in ast.unparse(w));response=next(w for w in ws if 'UPDATE journal SET response' in ast.unparse(w))
 sw=sorted([v for v in s.body if isinstance(v,ast.With)],key=lambda v:v.lineno);need(len(sw)==2,'PF-SOURCE-SIGN-WITH')
 need("'sign-claim'" in ast.unparse(sw[0]) and "'sign-persist'" in ast.unparse(sw[1]),'PF-SOURCE-KINDS')
 roles={'admission':('Authority.handle',admission),'claim':('Authority.sign',sw[0]),'signed':('Authority.sign',sw[1]),'response':('Authority.handle',response)}
 sqls={sql:call(fs['Authority.transaction'],sql) for sql in ('BEGIN IMMEDIATE','COMMIT','ROLLBACK')}
 update=call(response,'UPDATE journal SET response=? WHERE challenge=?')
 # Producer contract: encoded signed bytes are constructed before the With,
 # then passed as (raw, r['challenge']). No source path writes a null response.
 assign=next(n for n in h.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='raw' for t in n.targets))
 need(ast.unparse(assign.value)=="enc({'response': response, 'signature': sig('server', response)})" and assign.lineno<response.lineno,'PF-SOURCE-ENVELOPE-PRODUCER')
 need(len(update.args)==2 and ast.unparse(update.args[1])=="(raw, r['challenge'])",'PF-SOURCE-UPDATE-ARGUMENTS')
 limit=next(ast.literal_eval(n.value) for n in ast.parse(raw).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='RESPONSE_LIMIT' for t in n.targets))
 need(type(limit) is int and limit>0 and any(isinstance(n,ast.Call) and ast.unparse(n.func)=='need' and n.args and ast.unparse(n.args[0])=='len(raw) <= RESPONSE_LIMIT' and assign.lineno<=n.lineno<response.lineno for n in ast.walk(h)),'PF-SOURCE-RESPONSE-BOUND')
 dispatch=next(v for v in ast.walk(h) if isinstance(v,ast.Call) and ast.unparse(v.func)=='self.sign')
 return raw,cs,roles,sqls,update,dispatch,limit

def oracle(target,mode):
 """Source transaction semantics, not submitted outcome labels or capture hashes."""
 need((target=='none' and mode=='none') or (target in ('admission','claim','signed','response','rollback') and mode in ('deny','ack')) or (target=='signed' and mode=='double-deny'),'PF-UNSUPPORTED-PLAN')
 ops=[];active=False;durable={'admitted':False,'level':0,'response':False};working=None
 def record(role,sql,hit=False,context=None):
  nonlocal active
  before=active;ex=None;done=False
  if hit and mode in ('deny','double-deny'):ex=err('DatabaseError','not authorized',context)
  elif sql=='BEGIN IMMEDIATE' and active:ex=err('OperationalError','cannot start a transaction within a transaction',context)
  elif sql=='ROLLBACK' and not active:ex=err('OperationalError','cannot rollback - no transaction is active',context)
  else:
   done=True
   if sql=='BEGIN IMMEDIATE':active=True
   if sql in ('COMMIT','ROLLBACK'):active=False
   if hit and mode=='ack':ex=err('OSError','SIMULATED-ACK-LOSS-'+sql,context)
  ops.append(dict(role=role,sql=sql,in_transaction_before=before,in_transaction_after=active,sqlite_completed=done,exception=ex,injected=mode if hit else None));return done,ex
 def transact(role):
  nonlocal durable,working
  done,e=record(role,'BEGIN IMMEDIATE')
  if e:return e
  working=copy.deepcopy(durable)
  if role=='admission':working['admitted']=True
  if role=='claim':working['level']=1
  if role=='signed':working['level']=2
  if role=='response':
   record(role,'UPDATE journal SET response=? WHERE challenge=?');working['response']=True
  body=err('OSError','INJECTED-before_signature_commit') if role=='signed' and target=='rollback' else None
  if body:e=body
  else:
   done,e=record(role,'COMMIT',target==role)
   if done:durable=copy.deepcopy(working);working=None
  if e:
   done,re=record(role,'ROLLBACK',target=='rollback' or mode=='double-deny',e)
   if done:working=None
   return re or e
  return None
 escaped=transact('admission');dispatch_error=None;response_constructed=False
 if escaped is None:
  dispatch_error=transact('claim')
  if dispatch_error is None:dispatch_error=transact('signed')
  response_constructed=True;escaped=transact('response')
 return {'operations':ops,'durable':durable,'preclose':working if active else durable,'active':active,'escaped':escaped,'dispatch_error':dispatch_error,'response_constructed':response_constructed}

def frame_check(row,wanted,c,q):
 raw,cs,roles,sqls,update,dispatch,limit=c;sql=row['sql'];role=wanted['role'];caller,node=roles[role]
 expected=['Authority.handle'] if sql.startswith('UPDATE') else ['Authority.transaction',caller]+(['Authority.handle'] if caller=='Authority.sign' else [])
 exact([f['function'] for f in row['frames']],expected,'PF-FRAME-CHAIN')
 for i,f in enumerate(row['frames']):
  co=cs[f['function']];need(f['code']==identity(co),'PF-CODE-IDENTITY')
  instructions=list(dis.get_instructions(co,show_caches=True));matches=[v for v in instructions if type(f['offset']) is int and v.offset==f['offset']];need(len(matches)==1,'PF-OFFSET');ins=matches[0]
  exact([ins.opname,list(ins.positions)],[f['opname'],f['position']],'PF-INSTRUCTION')
  effective=next(v for v in reversed(instructions[:instructions.index(ins)+1]) if v.opname!='CACHE');need(effective.opname in ('CALL','BEFORE_WITH','WITH_EXCEPT_START'),'PF-CALL-OPERATION')
  wanted_pos=span(update) if sql.startswith('UPDATE') else span(sqls[sql]) if i==0 else span(node.items[0].context_expr) if i==1 else span(dispatch)
  exact(f['position'],wanted_pos,'PF-SOURCE-OPERATION')
  exact(f['request'],None if f['function']=='Authority.transaction' else q,'PF-FRAME-REQUEST')

def inspect(x,root,context):
 need(context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'),'PF-CONTEXT');root=Path(root);c=contract(root)
 need(x['format']=='I164-PERSISTENCE-LAB-1' and x['source_sha256']==sha(c[0]),'PF-SOURCE')
 exact(x['interpreter'],[3,12,14],'PF-CAPTURE-INTERPRETER')
 need(x['sqlite_version']=='3.53.1','PF-SQLITE-APPLICABILITY')
 need(x['harness_sha256']==sha((root/'persistence_tests/execute.py').read_bytes()),'PF-HARNESS')
 need(x['process_code']==0 and x['cleanup']=='explicit sqlite connection close before fresh-process reopen','PF-CLEANUP')
 # Unknown/missing evidence is never a successful preservation claim.
 need(all(x.get(k) is not None for k in ('operations','input','preclose','reopened')),'PF-INSUFFICIENT-EVIDENCE')
 o=oracle(x['target'],x['mode']);exact(x['inject'],'before_signature_commit' if x['target']=='rollback' else None,'PF-INJECT')
 vf.s.setup(root);import ingest,signed_eth
 before=json.loads(bytes.fromhex(x['input']['head']));packet=bytes.fromhex(x['request_hex']);envelope=json.loads(packet);q=envelope['request'];exact(x['request_hex'],enc(envelope).hex(),'PF-PACKET-BYTES');need(set(envelope)=={'request','signature'} and set(q)=={'version','binding','pilot','session','principal','challenge','expected','method','u','body'} and set(q['body'])=={'action'},'PF-PACKET-FIELDS');ingest.verify_signature(q['principal'],q,envelope['signature'])
 need(q['method']=='sign' and q['principal']=='executor' and q['expected']==before['head'] and q['binding']==before['binding'],'PF-REQUEST')
 for k in ('version','pilot','session'):exact(q[k],x['input']['config'][k],'PF-REQUEST-CONTEXT')
 u=q['u'];p=before['u'][u]['stage']['pending'];need(p['phase']=='DECIDED' and p['action']==q['body']['action'],'PF-ANCESTRY')
 blobs=dict(x['input']['blobs']);action=json.loads(bytes.fromhex(blobs[p['action']]));attempt=json.loads(bytes.fromhex(blobs[p['latest']]))
 need(action['intent']==before['u'][u]['intent'] and attempt['action']==p['action'] and attempt['u']==u,'PF-ATTEMPT')
 exact(x['escaped'],o['escaped'],'PF-EXCEPTION-PROPAGATION');exact(x['preclose_in_transaction'],o['active'],'PF-ACTIVE-TRANSACTION')
 need(len(x['operations'])==len(o['operations']),'PF-OPERATION-COVERAGE')
 response_raw=None;update_seen=False
 for row,wanted in zip(x['operations'],o['operations']):
  exact({k:row[k] for k in wanted if k!='role'},{k:v for k,v in wanted.items() if k!='role'},'PF-OPERATION-EFFECT');frame_check(row,wanted,c,q)
  if row['sql'].startswith('UPDATE'):
   params=row.get('params');need(type(params) is list and len(params)==2,'PF-RESPONSE-PARAMS')
   need(type(params[1]) is str and params[1]==q['challenge'],'PF-RESPONSE-CHALLENGE')
   value=params[0];need(type(value) is str and 0<len(value)<=2*c[6] and len(value)%2==0 and all(ch in '0123456789abcdef' for ch in value),'PF-RESPONSE-ARGUMENT-BYTES')
   need(not update_seen,'PF-DUPLICATE-UPDATE');response_raw=value;update_seen=True
  else:exact(row['params'],[],'PF-BOUNDARY-PARAMS')
 # Independently reconstruct permitted exact event/state prefix from source effects.
 tx=None
 for k,effect in (('preclose',o['preclose']),('reopened',o['durable'])):
  if effect['level']==2:
   tx=json.loads(bytes.fromhex(x[k]['head']))['u'][u]['stage']['pending']['tx'];raw=bytes.fromhex(dict(x[k]['blobs'])[tx]);need(sha(raw)==tx,'PF-TX-IDENTITY');signed_eth.validate(raw,action['template'])
 response={'request':sha(packet),'challenge':q['challenge'],'ok':o['dispatch_error'] is None}
 if o['dispatch_error']:response['error']=o['dispatch_error']['type']+':'+o['dispatch_error']['message']
 else:response['data']={'action':p['action'],'tx':tx,'recovered':False,'release':False}
 need(not (o['preclose']['response'] or o['durable']['response']) or update_seen,'PF-SAVED-RESPONSE-EVIDENCE')
 if update_seen:
  need(o['response_constructed'],'PF-UPDATE-BEFORE-CONSTRUCTION')
  env=json.loads(bytes.fromhex(response_raw));need(type(env) is dict and set(env)=={'response','signature'} and type(env['response']) is dict,'PF-ENVELOPE-FIELDS')
  need(type(env['signature']) is str and len(env['signature'])==128 and all(ch in '0123456789abcdef' for ch in env['signature']),'PF-ENVELOPE-SIGNATURE-TYPE')
  exact(env['response'],response,'PF-RESPONSE-VALUE');ingest.verify_signature('server',env['response'],env['signature']);exact(response_raw,enc(env).hex(),'PF-RESPONSE-BYTES')
 # If response BEGIN fails, construction did occur but raw bytes were not observed.
 exact(x['returned'],response_raw if o['escaped'] is None else None,'PF-RETURN')
 for k,effect in (('preclose',o['preclose']),('reopened',o['durable'])):
  y=x[k];state=copy.deepcopy(before);events=copy.deepcopy(x['input']['events']);newblobs=dict(blobs)
  for i in range(effect['level']):
   pending=state['u'][u]['stage']['pending'];pending['phase']=('SIGNING','SIGNED')[i]
   if i:
    pending['tx']=tx;newblobs[tx]=dict(y['blobs'])[tx]
   previous=state.pop('head');state['seq']+=1;e={'previous':previous,'request':sha(enc(q)),'kind':('sign-claim','sign-persist')[i],'proof':tx if i else None,'after':state};raw=enc(e);events.append([state['seq'],raw.hex()]);state['head']=sha(raw)
  exact(y['head'],enc(state).hex(),'PF-EXACT-STATE');exact(y['events'],events,'PF-HISTORY');exact(dict(y['blobs']),newblobs,'PF-BLOBS');exact(y['owners'],x['input']['owners'],'PF-OWNERS')
  rows=copy.deepcopy(x['input']['journal']);need(q['challenge'] not in {r[0] for r in rows},'PF-REPLAY')
  if effect['admitted']:rows.append([q['challenge'],x['request_hex'],response_raw if effect['response'] else None])
  exact(y['journal'],sorted(rows,key=lambda r:r[0]),'PF-SAVED-RESPONSE')
  for field in set(x['input'])-{'head','events','blobs','journal','expected_head'}:exact(y[field],x['input'][field],'PF-EXPORT-BINDING')
  exact(y['expected_head'],state['head'],'PF-HEAD')
 # Deduplicate only identical canonical bytes within this invocation; no object-history cache.
 seen=set()
 for k in ('input','preclose','reopened'):
  serialized=enc(x[k])
  if serialized not in seen:ingest.validate_export(x[k]);seen.add(serialized)
 return {'scope':'bounded injected persistence correspondence','context':context,'source':sha(c[0]),'request':sha(packet),'action':p['action'],'attempt':p['latest'],'intent':action['intent'],'u':u,'durable_effect':o['durable'],'preclose_effect':o['preclose'],'preclose_in_transaction':o['active'],'charges':before['counts'],'obligations':vf.obligations(x['reopened']),'saved_response':o['durable']['response'],'response_returned':x['returned'] is not None,'unanswered_request':o['durable']['admitted'] and not o['durable']['response'],'external_nonexecution_established':False,'conflicting_action_authorized':False,'storage_qualification':False,'uncertainty':'signed bytes may exist outside persistence; errors confer no retry/release right','final_binding':'BLOCKED','actual_admission':False,'streams':'UNCOMPUTED','canonical_registration':False}
def validate(receipt,x,root,context):exact(receipt,inspect(x,root,context),'PF-RECEIPT');return True
