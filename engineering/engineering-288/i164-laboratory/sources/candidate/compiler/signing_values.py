"""Source-anchored signing observation correspondence; laboratory attestation is separate."""
import ast,json,hashlib
from pathlib import Path
import program_coverage as pc,value_flow as vf
from value_observer import untyped
from observation_contract import validate_observations
AUTH='support/reference/runtime/authority.py';EVM='support/reference/retained/lab_evm.py';SIGNED='support/reference/retained/signed_eth.py'
def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def need(x,s):
 if not x:raise ValueError(s)
def exact(a,b,s):need(enc(a)==enc(b),s)
def function(raw,name):
 parts=name.split('.');body=ast.parse(raw).body
 for part in parts:
  n=next(x for x in body if isinstance(x,(ast.ClassDef,ast.FunctionDef)) and x.name==part);body=n.body
 return n

def correspondence(x,root):
 """Independent semantic checks over values and authenticated export; no capture-hash oracle."""
 root=Path(root)
 for source,h in x['source_hashes'].items():
  need(source in pc.literal('PINS') and h==pc.literal('PINS')[source] and sha((root/source).read_bytes())==h,'SOURCE-PIN')
 vf.s.setup(root);import ingest,signed_eth
 ingest.validate_export(x['input']);ingest.validate_export(x['export'])
 before=json.loads(bytes.fromhex(x['input']['head']));after=json.loads(bytes.fromhex(x['export']['head']));exact(before,x['before'],'BEFORE');exact(after,x['after'],'AFTER')
 packet=bytes.fromhex(x['request_hex']);q=json.loads(packet)['request'];response=json.loads(bytes.fromhex(x['response_hex']))['response']
 need(q['method']=='sign' and q['expected']==before['head'],'REQUEST-PRESTATE');need(response['request']==sha(packet),'REQUEST-RESPONSE')
 row=next((r for r in x['export']['journal'] if r[0]==q['challenge']),None);exact(row,[q['challenge'],x['request_hex'],x['response_hex']],'JOURNAL-ENVELOPE')
 exact(after['counts'],before['counts'],'SIGNING-CHARGE-CONTINUITY');exact(after['resources'],before['resources'],'SIGNING-OBLIGATIONS-CONTINUITY');exact(x['input']['owners'],x['export']['owners'],'NONCE-OWNERSHIP')
 need(x['export']['events'][:len(x['input']['events'])]==x['input']['events'],'IMMUTABLE-HISTORY')
 u=q['u'];p=before['u'][u]['stage']['pending'];ap=after['u'][u]['stage']['pending'];blobs=dict(x['input']['blobs']);action=json.loads(bytes.fromhex(blobs[p['action']]));attempt=json.loads(bytes.fromhex(blobs[p['latest']]))
 need(action['u']==u and action['intent']==before['u'][u]['intent'] and attempt['action']==p['action'] and attempt['u']==u,'ACTION-ATTEMPT-BINDING')
 completions=validate_observations(x,root)
 obs=x['observations'];open_frames={};observed_calls=[]
 for e in obs:
  need(e['event'] in ['call','return','exception'] and type(e['frame']) is int,'OBS-EVENT')
  need(e['source'] in x['source_hashes'],'OBS-SOURCE');raw=(root/e['source']).read_bytes();fn=function(raw,e['function']);need(fn.lineno==e['definition_line'] and fn.lineno<=e['line']<=fn.end_lineno,'OBS-SOURCE-SITE')
  for v in e['values'].values():untyped(v)
  if e['event']=='call':need(e['frame'] not in open_frames,'OBS-DUPLICATE-FRAME');open_frames[e['frame']]=(e['source'],e['function']);observed_calls.append(e)
  else:
   need(open_frames.get(e['frame'])==(e['source'],e['function']),'OBS-FRAME-ANCESTRY')
   if e['event']=='return':untyped(e['result']);del open_frames[e['frame']]
 need(not open_frames,'OBS-UNFINISHED-FRAME')
 def events(source,name,event):return [e for e in obs if e['source']==source and e['function']==name and e['event']==event]
 signcalls=events(AUTH,'Authority.sign','call');need(len(signcalls)==1,'SIGN-CALL');exact(untyped(signcalls[0]['values']['r']),q,'OBS-REQUEST');exact(untyped(signcalls[0]['values']['inject']),x['inject'],'OBS-INJECTION')
 txs=events(EVM,'tx','return');vals=events(SIGNED,'validate','return');signed=None
 if q['body']['action']!=p['action']:
  route='REJECT-WRONG-ACTION';need(not txs and not vals and not response['ok'] and response['error']=='Blocked:ACTION-BINDING','WRONG-ACTION-PATH');exact(before,after,'REJECTION-STATE')
 elif p['phase']=='SIGNING':
  route='REJECT-AMBIGUOUS';need(not txs and not vals and not response['ok'] and response['error']=='Blocked:SIGNING-AMBIGUOUS','AMBIGUOUS-PATH');exact(before,after,'AMBIGUOUS-STATE')
 elif p['phase']=='SIGNED':
  route='RECOVER-EXACT-SIGNED';need(not txs and not vals and response['ok'],'RECOVER-NO-RESIGN');exact(response['data'],{'action':p['action'],'tx':p['tx'],'recovered':True,'release':False},'RECOVER-RESULT');exact(before,after,'RECOVER-STATE');signed=bytes.fromhex(blobs[p['tx']]);signed_eth.validate(signed,action['template'])
 else:
  need(p['phase']=='DECIDED','UNSUPPORTED-ENTRY-PHASE');inject=x['inject'];need(inject in [None,'after_sign_claim','after_signature_created','before_signature_commit','after_signature_commit'],'UNSUPPORTED-FAULT-PATH')
  route='DECIDED:'+str(inject)
  if inject=='after_sign_claim':need(not txs and not vals,'PRE-SIGN-NO-TX')
  else:
   need(len(txs)==len(vals)==1,'TX-AND-VALIDATION-OBSERVATIONS');tx,validated=txs[0],vals[0];need(all(completions[obs.index(e)]['kind']=='NORMAL-RETURN' for e in [tx,validated]),'PRODUCER-NORMAL-COMPLETION');rawhex=untyped(tx['result']);need(type(rawhex) is str,'TX-RETURN-TYPE');signed=bytes.fromhex(rawhex);need(signed.hex()==rawhex,'TX-HEX')
   template=action['template'];expected={'nonce':int(template['nonce']),'to':template['target'],'data':bytes.fromhex(template['calldata']),'gas':int(template['gas_limit']),'key':1}
   for k,v in expected.items():need(type(untyped(tx['values'][k])) is type(v) and untyped(tx['values'][k])==v,'SIGNER-ARGUMENT:'+k)
   need(untyped(validated['values']['raw'])==signed,'VALIDATOR-EXACT-BYTES');exact(untyped(validated['values']['expected']),template,'VALIDATOR-TEMPLATE');exact(untyped(validated['result']),signed_eth.validate(signed,template),'VALIDATOR-RESULT')
   # These calls must be anchored to the exact producer expression, not an arbitrary same-line event.
   sign=function((root/AUTH).read_bytes(),'Authority.sign')
   for event,expr in [(tx,'evm.tx'),(validated,'signed_eth.validate')]:
    call=next(n for n in ast.walk(sign) if isinstance(n,ast.Call) and ast.unparse(n.func)==expr)
    exact(event['caller'],{'source':AUTH,'function':'Authority.sign','position':{'line':call.lineno,'end_line':call.end_lineno,'column':call.col_offset,'end_column':call.end_col_offset}},'PRODUCER-CALL-SITE')
   need(obs.index(tx)<obs.index(validated),'SIGN-VALIDATE-ORDER')
  persisted=inject in [None,'after_signature_commit']
  need(ap['phase']==('SIGNED' if persisted else 'SIGNING') and ap['released'] is False,'POST-SIGN-PHASE')
  if persisted:
   need(signed is not None and ap['tx']==sha(signed),'PERSISTED-TX-IDENTITY');need(dict(x['export']['blobs']).get(ap['tx'])==signed.hex(),'PERSISTED-EXACT-BYTES')
  else:need(ap['tx'] is None,'TRANSIENT-NOT-PERSISTED')
  if inject:
   need(not response['ok'] and response['error']=='OSError:INJECTED-'+inject,'FAULT-RESULT')
   failures=events(AUTH,'fault','exception');need(any(untyped(e['values']['point'])==inject and untyped(e['values']['want'])==inject and e['exception']=={'type':'OSError','message':'INJECTED-'+inject} for e in failures),'FAULT-OBSERVATION')
  else:exact(response['data'],{'action':p['action'],'tx':sha(signed),'recovered':False,'release':False},'SIGNED-RESULT')
 # Check captured sign locals and blob/get return values against immutable source evidence.
 all_blobs=dict(x['input']['blobs']);all_blobs.update(dict(x['export']['blobs']))
 for e in obs:
  values={k:untyped(v) for k,v in e['values'].items()}
  if e['source']==AUTH and e['function']=='Authority.sign':
   for k,want in [('r',q),('inject',x['inject']),('a_id',q['body']['action']),('a',action),('bound',action),('t',action['template'])]:
    if k in values:exact(values[k],want,'SIGN-LOCAL:'+k)
   if 'raw' in values:need(signed is not None and values['raw']==signed,'SIGN-LOCAL-RAW')
   if values.get('p') is not None:
    for k in ['action','first','latest']:exact(values['p'][k],p[k],'PENDING-IDENTITY:'+k)
  if e['source']==AUTH and e['event']=='return' and e['function']=='Authority.get':
   value=untyped(e['result'])
   if value is not None:need(type(value) is bytes and all_blobs.get(values['ref'])==value.hex(),'GET-EXACT-BYTES')
  if e['source']==AUTH and e['event']=='return' and e['function']=='Authority.blob':
   value=untyped(e['result'])
   if value is not None:need(type(values['raw']) is bytes and value==sha(values['raw']),'BLOB-EXACT-REFERENCE')
 signreturns=events(AUTH,'Authority.sign','return');need(len(signreturns)==1,'SIGN-RETURN-EVENT')
 signexceptions=events(AUTH,'Authority.sign','exception');terminal=completions[obs.index(signreturns[0])]['kind']
 if response['ok']:
  need(not signexceptions and terminal=='NORMAL-RETURN','SIGN-NORMAL-COMPLETION');exact(untyped(signreturns[0]['result']),response['data'],'SIGN-RESPONSE-VALUE')
 else:
  need(untyped(signreturns[0]['result']) is None and terminal=='UNWIND' and len(signexceptions)==1,'EXCEPTION-UNWIND')
  ex=signexceptions[0]['exception'];need(ex['type']+':'+ex['message']==response['error'],'SIGN-EXCEPTION-RESPONSE')
 from save_blob_contract import check
 check(x,root,signed)
 return {'route':route,'request':sha(packet),'u':u,'intent':action['intent'],'action':p['action'],'first_attempt':p['first'],'latest_attempt':p['latest'],'attempt':attempt,'branch':action['branch'],'kind':action['kind'],'reserved_nonce':action['template']['nonce'],'signed_hex':None if signed is None else signed.hex(),'persisted_tx':ap['tx'],'before':before['head'],'after':after['head'],'counts':after['counts'],'obligations':vf.obligations(x['export']),'external_outcome':'NOT-DETERMINED-BY-LOCAL-OBSERVATION','observation_scope':'bounded semantic correspondence under trusted observer; not operational attestation','final_binding':'BLOCKED','actual_admission':False,'stream_identities':'UNCOMPUTED'}
CATALOGUE_SHA256='52441e3a39253197463af2381108de8fd541464192278329cd9503986aa78e5b'
def catalogue_pin():return ast.literal_eval(next(n.value for n in ast.parse(Path(__file__).read_bytes()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CATALOGUE_SHA256' for t in n.targets)))
def capture_identity(x,root):
 raw=(Path(root)/'signing_observation_outputs/execution/INDEX.json').read_bytes();need(sha(raw)==catalogue_pin(),'CAPTURE-CATALOGUE');item=next((i for i in json.loads(raw) if i['name']==x.get('name')),None);b=enc(x);need(item is not None and len(b)==item['bytes'] and sha(b)==item['sha256'],'CAPTURE-BYTES');return True
def validate_capture(x,root):capture_identity(x,root);return correspondence(x,root)
def validate_receipt(value,x,root):exact(value,validate_capture(x,root),'OBSERVATION-RECEIPT');return True
