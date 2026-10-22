"""Bounded request-bound exception evidence. No capture hash is a semantic oracle.
Trace/SQL records remain trusted laboratory attestations, not operational proof.
"""
import ast,json,copy,hashlib
from pathlib import Path
import value_flow as vf
from value_observer import untyped
from observation_contract import AUTH,raw_source,fn,opnames,need,exact,position

def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def basis(root):
 raw=raw_source(root,AUTH);t=fn(raw,'Authority.transaction');h=fn(raw,'Authority.handle');s=fn(raw,'Authority.sign');fault=fn(raw,'fault')
 tries=[n for n in t.body if isinstance(n,ast.Try)];need(len(tries)==1,'BOUNDARY-SOURCE-TRANSACTION');tr=tries[0]
 need(len(tr.handlers)==1 and ast.unparse(tr.handlers[0].type)=='BaseException' and isinstance(tr.handlers[0].body[-1],ast.Raise),'BOUNDARY-SOURCE-ROLLBACK')
 handlers=[n for n in h.body if isinstance(n,ast.Try)];need(len(handlers)==1,'BOUNDARY-SOURCE-HANDLER');ht=handlers[0]
 need(len(ht.handlers)==1 and ast.unparse(ht.handlers[0].type)=='Exception','BOUNDARY-SOURCE-CATCH')
 need('COMMIT' in ast.unparse(tr.body) and 'ROLLBACK' in ast.unparse(tr.handlers[0].body),'BOUNDARY-SOURCE-SQL')
 need(not tr.finalbody and not tr.orelse and not ht.finalbody and not ht.orelse,'BOUNDARY-UNSUPPORTED-HANDLER')
 response=next(n for n in h.body if isinstance(n,ast.With) and 'UPDATE journal SET response' in ast.unparse(n))
 need(response.lineno>ht.end_lineno,'BOUNDARY-RESPONSE-OUTSIDE-CATCH')
 calls={n.args[0].value:n for n in ast.walk(s) if isinstance(n,ast.Call) and ast.unparse(n.func)=='fault' and isinstance(n.args[0],ast.Constant)}
 raises=[n for n in ast.walk(fault) if isinstance(n,ast.Raise)];need(len(raises)==1 and ast.unparse(raises[0].exc)=="OSError('INJECTED-' + point)",'BOUNDARY-FAULT-SOURCE')
 exitcall=next(n for n in ast.walk(fault) if isinstance(n,ast.Call) and ast.unparse(n.func)=='os._exit');need(len(exitcall.args)==1 and type(exitcall.args[0].value) is int,'BOUNDARY-EXIT-SOURCE')
 return {'sha256':sha(raw),'transaction':position(t),'handler':position(ht),'response_persistence':position(response),'fault_calls':{k:position(v) for k,v in calls.items()},'fault_raise':position(raises[0]),'yield_site':position(next(n for n in ast.walk(tr) if isinstance(n,ast.Yield))),'sign_dispatch':position(next(n for n in ast.walk(ht) if isinstance(n,ast.Call) and ast.unparse(n.func)=='self.sign')),'exit_code':exitcall.args[0].value,'catch':'Exception','rollback_catch':'BaseException'}

HARNESS_SHA256='0d3d8cc51ffef04d4200c1a9d94d5246f8016df7c851ee84ef279bab171d0419'
def inspect(x,root,context):
 need(context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'),'BOUNDARY-CONTEXT');root=Path(root);b=basis(root);need(x['source_sha256']==b['sha256'],'BOUNDARY-SOURCE')
 need(x['harness_sha256']==HARNESS_SHA256,'BOUNDARY-HARNESS');source_raw=raw_source(root,AUTH)
 vf.s.setup(root);import ingest,signed_eth
 ingest.validate_export(x['input']);iv=ingest.validate_export(x['reopened'])
 before=json.loads(bytes.fromhex(x['input']['head']));after=json.loads(bytes.fromhex(x['reopened']['head']));packet=bytes.fromhex(x['request_hex']);q=json.loads(packet)['request']
 need(q['method']=='sign' and q['expected']==before['head'],'BOUNDARY-REQUEST');u=q['u'];p=before['u'][u]['stage']['pending'];need(p['phase']=='DECIDED' and p['action']==q['body']['action'],'BOUNDARY-ANCESTRY')
 blobs=dict(x['input']['blobs']);action=json.loads(bytes.fromhex(blobs[p['action']]));attempt=json.loads(bytes.fromhex(blobs[p['latest']]))
 need(action['intent']==before['u'][u]['intent'] and attempt['action']==p['action'] and attempt['u']==u,'BOUNDARY-ATTEMPT')
 row=next((r for r in x['reopened']['journal'] if r[0]==q['challenge']),None);need(row is not None and row[1]==x['request_hex'],'BOUNDARY-JOURNAL')
 oldrows={r[0]:r for r in x['input']['journal']};need(q['challenge'] not in oldrows,'BOUNDARY-REPLAY');exact([r for r in x['reopened']['journal'] if r[0]!=q['challenge']],x['input']['journal'],'BOUNDARY-OTHER-JOURNAL')
 inject=x['inject'];plan=x['fault_plan'];need(plan in ('none','deny-response','base-after-claim'),'BOUNDARY-FAULT-PLAN')
 need(inject in (None,'after_sign_claim','before_signature_commit','after_signature_commit','exit:before_signature_commit','exit:after_signature_commit'),'BOUNDARY-UNSUPPORTED-PATH')
 need(plan!='base-after-claim' or inject is None,'BOUNDARY-MIXED-FAULTS');need(plan!='deny-response' or inject in (None,'after_sign_claim'),'BOUNDARY-DENY-DOMAIN')
 exit_=type(inject) is str and inject.startswith('exit:');point=inject[5:] if exit_ else inject
 persisted=plan!='base-after-claim' and point not in ('after_sign_claim','before_signature_commit')
 missing=exit_ or plan!='none';fault_ex=None if point is None or exit_ else {'type':'OSError','message':'INJECTED-'+point}
 need(x['process_code']==(b['exit_code'] if exit_ else 0),'BOUNDARY-PROCESS-EXIT')
 escape={'type':'DatabaseError','message':'not authorized'} if plan=='deny-response' else {'type':'KeyboardInterrupt','message':'BOUNDARY-LAB'} if plan=='base-after-claim' else None
 exact(x['escaped'],escape,'BOUNDARY-ESCAPED-EXCEPTION');need((x['returned'] is None)==missing,'BOUNDARY-RETURN-PRESENCE');exact(row[2],x['returned'],'BOUNDARY-SAVED-RESPONSE')
 # Source-derived phase effects are checked against complete authenticated history, not a submitted rollback label.
 newevents=x['reopened']['events'][len(x['input']['events']):];exact(x['reopened']['events'][:len(x['input']['events'])],x['input']['events'],'BOUNDARY-HISTORY')
 sign=fn(raw_source(root,AUTH),'Authority.sign');savecalls=sorted([n for n in ast.walk(sign) if isinstance(n,ast.Call) and ast.unparse(n.func)=='self.save'],key=lambda n:n.lineno)
 kinds=[ast.literal_eval(n.args[2]) for n in savecalls];phases=[ast.literal_eval(n.value) for n in sorted([n for n in ast.walk(sign) if isinstance(n,ast.Assign) and ast.unparse(n.targets[0])=="p['phase']"],key=lambda n:n.lineno)]
 need(len(newevents)==(2 if persisted else 1),'BOUNDARY-EVENT-COUNT');state=copy.deepcopy(before);tx=None
 for i,(seq,hx) in enumerate(newevents):
  pending=state['u'][u]['stage']['pending'];pending['phase']=phases[i]
  if i:
   tx=json.loads(bytes.fromhex(x['reopened']['head']))['u'][u]['stage']['pending']['tx'];raw=bytes.fromhex(dict(x['reopened']['blobs'])[tx]);need(sha(raw)==tx,'BOUNDARY-TX');signed_eth.validate(raw,action['template']);pending['tx']=tx
  previous=state.pop('head');state['seq']+=1;event={'previous':previous,'request':sha(enc(q)),'kind':kinds[i],'proof':tx if i else None,'after':state};exact([seq,hx],[state['seq'],enc(event).hex()],'BOUNDARY-EXACT-EVENT');state['head']=sha(bytes.fromhex(hx))
 exact(state,after,'BOUNDARY-EXACT-STATE');exact(after['counts'],before['counts'],'BOUNDARY-CHARGE-CONTINUITY');exact(after['resources'],before['resources'],'BOUNDARY-HOLD-CONTINUITY');exact(x['reopened']['owners'],x['input']['owners'],'BOUNDARY-OWNERSHIP')
 traces=x['trace'];need(type(traces) is list and traces,'BOUNDARY-MISSING-TRACE')
 ex=[];handle_requests=[];faults=[];denials=0;test_injections=0;responses=0;response_bytes=0;sign_requests=[];signed_observations=0;signed_seen=set();envelope_seen=set()
 expected_response={'request':sha(packet),'challenge':q['challenge'],'ok':fault_ex is None}
 if fault_ex:expected_response['error']=fault_ex['type']+':'+fault_ex['message']
 else:expected_response['data']={'action':p['action'],'tx':tx,'recovered':False,'release':False}
 for e in traces:
  if e['event']=='sql-attempt':continue
  if e['event']=='authorizer-denial':exact([e['table'],e['column']],['journal','response'],'BOUNDARY-AUTHORIZER');denials+=1;continue
  if e['event']=='test-injection':
   exact(e,{'event':'test-injection','type':'KeyboardInterrupt','message':'BOUNDARY-LAB','source':AUTH,'position':b['fault_calls']['after_sign_claim']},'BOUNDARY-BASE-INJECTION');test_injections+=1;continue
  need(e['function'] in ['Authority.handle','Authority.sign','Authority.transaction','fault'],'BOUNDARY-FUNCTION');need(bool(opnames(source_raw,e['function'],e['position'])),'BOUNDARY-SITE');need(e['line']==e['position']['line'],'BOUNDARY-LINE')
  vals={k:untyped(v) for k,v in e['values'].items()}
  if 'r' in vals:exact(vals['r'],q,'BOUNDARY-OBS-REQUEST')
  if 'packet' in vals:need(vals['packet']==packet,'BOUNDARY-OBS-PACKET')
  if 'inject' in vals:exact(vals['inject'],inject,'BOUNDARY-OBS-INJECT')
  if e['function']=='Authority.handle' and e['event']=='call':handle_requests.append(vals.get('packet'))
  if e['event']=='exception':ex.append((e['function'],e['exception'],e['position']))
  if e['function']=='fault' and e['event']=='call':faults.append(vals)
  if e['function']=='Authority.sign' and e['event']=='call':sign_requests.append([vals.get('r'),vals.get('inject')])
  if e['function']=='Authority.sign' and 'raw' in vals:
   need(type(vals['raw']) is bytes,'BOUNDARY-SIGNED-TYPE')
   if vals['raw'] not in signed_seen:signed_eth.validate(vals['raw'],action['template']);signed_seen.add(vals['raw'])
   signed_observations+=1
   if tx:need(sha(vals['raw'])==tx,'BOUNDARY-OBS-SIGNED-BYTES')
  if e['function']=='Authority.handle':
   if 'response' in vals:exact(vals['response'],expected_response,'BOUNDARY-OBS-RESPONSE-VALUE');responses+=1
   if 'raw' in vals:
    response_bytes+=1;envelope=json.loads(vals['raw']);exact(envelope['response'],expected_response,'BOUNDARY-OBS-ENVELOPE');
    if vals['raw'] not in envelope_seen:ingest.verify_signature('server',envelope['response'],envelope['signature']);envelope_seen.add(vals['raw'])
    need(row[2] is None or vals['raw'].hex()==row[2],'BOUNDARY-OBS-RESPONSE')
   if e['event']=='return':need(untyped(e['result'])==(None if missing else bytes.fromhex(row[2])),'BOUNDARY-HANDLE-RETURN')
 need(handle_requests==[packet],'BOUNDARY-HANDLE-CALL');exact(sign_requests,[[q,inject]],'BOUNDARY-SIGN-CALL');need(denials==(1 if plan=='deny-response' else 0) and test_injections==(1 if plan=='base-after-claim' else 0),'BOUNDARY-INJECTION-EVIDENCE')
 expected=[]
 if fault_ex:
  expected=[('fault',fault_ex),('Authority.sign',fault_ex)]+([('Authority.transaction',fault_ex)] if point=='before_signature_commit' else [])+[('Authority.handle',fault_ex)]
 if plan=='deny-response':expected += [('Authority.handle',escape),('Authority.transaction',escape)]
 exact([(f,e) for f,e,_ in ex],expected,'BOUNDARY-EXCEPTION-PROPAGATION')
 for f,e,pos in ex:
  if f=='Authority.transaction':exact(pos,b['yield_site'],'BOUNDARY-TRANSACTION-EXCEPTION-SITE')
  if f=='Authority.handle' and e==fault_ex:exact(pos,b['sign_dispatch'],'BOUNDARY-HANDLER-EXCEPTION-SITE')
  if f=='fault':exact(pos,b['fault_raise'],'BOUNDARY-EXCEPTION-SITE')
  if f=='Authority.sign':exact(pos,b['fault_calls'][point],'BOUNDARY-SIGN-EXCEPTION-SITE')
  if f=='Authority.handle' and e==escape:need(pos['line']==b['response_persistence']['line'],'BOUNDARY-RESPONSE-EXCEPTION-SITE')
 if not exit_ and plan!='base-after-claim':need(responses>0 and response_bytes>0,'BOUNDARY-MISSING-RESPONSE-OBSERVATION')
 if plan!='base-after-claim' and point!='after_sign_claim':need(signed_observations>0,'BOUNDARY-MISSING-SIGNED-OBSERVATION')
 ordered=sorted(b['fault_calls'],key=lambda k:(b['fault_calls'][k]['line'],b['fault_calls'][k]['column']));stop=0 if plan=='base-after-claim' else ordered.index(point)+1 if point else len(ordered)
 exact(faults,[{'point':p,'want':inject} for p in ordered[:stop]],'BOUNDARY-FAULT-PREFIX')
 sql=[e['sql'] for e in traces if e['event']=='sql-attempt' and e['sql'] in ('BEGIN IMMEDIATE','COMMIT','ROLLBACK')]
 wanted=['BEGIN IMMEDIATE','COMMIT']*2
 if plan!='base-after-claim' and point!='after_sign_claim':wanted+=['BEGIN IMMEDIATE']+([] if inject=='exit:before_signature_commit' else ['ROLLBACK' if point=='before_signature_commit' else 'COMMIT'])
 if not exit_ and plan!='base-after-claim':wanted+=['BEGIN IMMEDIATE','ROLLBACK' if plan=='deny-response' else 'COMMIT']
 exact(sql,wanted,'BOUNDARY-SQL-ATTEMPTS')
 if not missing:
  response=json.loads(bytes.fromhex(row[2]))['response'];need(response['ok'] is (fault_ex is None),'BOUNDARY-RESPONSE-KIND')
  if fault_ex:exact(response['error'],fault_ex['type']+':'+fault_ex['message'],'BOUNDARY-ERROR-TRANSFORMATION')
 from boundary_events import check as check_events
 event_contract=check_events(x,root)
 return {'event_contract':event_contract,'scope':'bounded laboratory boundary correspondence','context':context,'request':sha(packet),'action':p['action'],'attempt':p['latest'],'intent':action['intent'],'u':u,'phase':after['u'][u]['stage']['pending']['phase'],'charges':after['counts'],'obligations':vf.obligations(x['reopened']),'unanswered_request':row[2] is None,'external_nonexecution_established':False,'conflicting_action_authorized':False,'sql_attempts':sql,'persistence_basis':'fresh reopened authenticated export; SQL trace alone does not prove commit','propagation_trace_gap':'trace injection disables subsequent Python tracing' if plan=='base-after-claim' else None,'canonical_registration':False,'final_binding':'BLOCKED','actual_admission':False,'streams':'UNCOMPUTED'}
def validate(receipt,x,root,context):exact(receipt,inspect(x,root,context),'BOUNDARY-RECEIPT');return True
