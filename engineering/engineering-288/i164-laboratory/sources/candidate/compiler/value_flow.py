"""Independent raw-evidence value reconstruction plus bounded exceptional obligations.
No Authority, signer, acquisition, lifecycle or full expansion is executed.
"""
import json,copy,base64,ast
from pathlib import Path
import semantic as s
m=s.m
D=lambda h:json.loads(bytes.fromhex(h))
def source_contract():
 paths=['support/code/ingest.py','support/code/correspondence.py','support/reference/runtime/authority.py','support/reference/runtime/accounting.py','support/reference/runtime/ownership.py','integration/candidate_pipeline.py','compiler/value_flow.py']
 out=[]
 for path in paths:
  raw=(s.ROOT/path).read_bytes();tree=ast.parse(raw)
  out.append({'identity':m.ident(path),'functions':[{'name':n.name,'line':n.lineno,'end':n.end_lineno,'exact_source':ast.get_source_segment(raw.decode(),n)} for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))]})
 return out

def reconstruct(x):
 # Independent raw directory walk, not Fold state, generated source lists or tracer output.
 # Existing deterministic ABI/RLP decoders are reused explicitly; no EVM signing.
 import abi,signed_eth
 records=[];origins=[]
 def add(k,v,path,transform,producer):
  records.append((k,copy.deepcopy(v)));origins.append({'record_index':len(records)-1,'family':k,'input':path,'transform':transform,'producer':producer})
 blobs={ref:bytes.fromhex(raw) for ref,raw in x['blobs']};obj=lambda ref:json.loads(blobs[ref]);events=[D(row[1]) for row in x['events']];head=D(x['head']);binding=head['binding']
 genesis={'binding':binding,'seq':0,'head':'0'*64,'counts':dict.fromkeys(['attempt','query','snapshot','verifier'],0),'partitions':dict.fromkeys(['query','snapshot','verifier'],0),'u':{},'active':None,'resources':dict.fromkeys(['slots','holds','query_holds','extra_queries'],0)}
 states=[genesis];qs=[];rs=[]
 add('CONFIG',x['config'],'/config','identity','Authority.__init__');add('OWNERSHIP-META',D(x['ownership_meta']),'/ownership_meta','canonical hex JSON','ownership.attach')
 for i,e in enumerate(events):
  state=dict(e['after'],head=m.sha(bytes.fromhex(x['events'][i][1])));states.append(state)
  add('EVENT',e,f'/events/{i}/1','canonical hex JSON','Authority.save');add('HEAD',state,f'/events/{i}/1','after + sha256(exact event bytes)','Authority.save')
 for i,(_,ph,rh) in enumerate(x['journal']):
  p=D(ph);q=p['request'];qs.append((i,q,p));add('REQUEST',q,f'/journal/{i}/1','canonical packet.request','Scheduler.packet / Authority.handle');add('PACKET',p,f'/journal/{i}/1','exact authenticated packet','Scheduler.packet / Authority.handle')
  if rh is not None:rs.append((i,q,D(rh)))
 for i,q,r in rs:add('RESPONSE',r,f'/journal/{i}/2','whole authenticated envelope, including signature','Authority.handle')
 for i,row in enumerate(x['owners']):add('OWNERSHIP-ROW',D(row[1]),f'/owners/{i}/1','canonical hex JSON','ownership.claim')
 attempts=set();actions=set()
 for state in states:
  for v in state['u'].values():
   if 'stage' not in v:continue
   st=v['stage'];attempts.update(st['transport'])
   for key in ['last','pending']:
    if st[key] is not None:actions.add(st[key]['action'])
 for ref in attempts:actions.add(obj(ref)['action'])
 for ref in sorted(attempts):add('ATTEMPT',obj(ref),'blob:'+ref,'canonical immutable blob','accounting.record')
 for ref in sorted(actions):
  a=obj(ref);add('ACTION',a,'blob:'+ref,'canonical immutable blob','Authority.apply decide');add('TEMPLATE',a['template'],'blob:'+ref+'/template','exact member','Authority.apply decide')
 retirement_order={};backup_order={}
 for event in events:
  q=next(q for _,q,_ in qs if m.sha(m.enc(q))==event['request'])
  if event['kind']=='retire':retirement_order[q['u']]=event['after']['seq']
  if event['kind']=='backup':backup_order[q['body']['id']]=event['after']['seq']
 for i,state in enumerate(states):
  origin='genesis' if i==0 else f'/events/{i-1}/1/after'
  for k in ['counts','partitions','resources']:add(k.upper(),state[k],origin+'/'+k,'exact state member','Authority.__init__ / accounting / Authority.apply')
  for u in sorted(state['u'],key=lambda u:retirement_order[u]):
   v=state['u'][u];path=origin+'/u/'+u;add('U-ENTRY',{'key':u,'value':v},path,'preserve directory key and value','Authority.apply retire/open/decide/observe')
   if 'stage' not in v:continue
   st=v['stage'];add('STAGE',st,path+'/stage','exact member','Authority.apply / Authority.sign')
   for key,kind in [('transport','TRANSPORT-ENTRY'),('retry_ids','RETRY-ID-ENTRY'),('backups','BACKUP-ENTRY')]:
    for k in sorted(st[key],key=lambda k:obj(k)['ordinal'] if key=='transport' else obj(st[key][k])['ordinal'] if key=='retry_ids' else backup_order[k]):
     val=st[key][k];add(kind,{'key':k,'value':val},path+'/stage/'+key+'/'+k,'preserve key and value','accounting.record / Authority.apply')
   for key in ['last','pending']:
    if st[key] is not None:add(key.upper(),st[key],path+'/stage/'+key,'nonnull exact member','Authority.apply / Authority.sign')
   if st['pending'] is not None and st['pending']['query'] is not None:add('QUERY',st['pending']['query'],path+'/stage/pending/query','nonnull exact member','accounting.query')
 for u,v in head['u'].items():
  original=obj(v['intent']);compact=original.get('format')=='I164-UNSIGNED-COMPACT-LAB-1'
  if compact:
   data=base64.b64decode(original['calldata_base64'],validate=True);i=dict(original['identity'],calldata_hex=data.hex(),arguments=abi.decode(original['identity']['method'],data))
  else:i=original
  add('COMPACT-INTENT' if compact else 'UNSIGNED-INTENT',original,'blob:'+v['intent'],'exact original representation, never normalized in place','Authority.apply retire')
  add('ABI-ARGUMENTS-'+i['method'],i['arguments'],'blob:'+v['intent'],'compact: base64 -> ABI decode; ordinary: exact arguments','unsigned_intent / abi.decode')
  add('CONDITIONAL-CAPSULE',D(i['conditional_comparison_hex']),'blob:'+v['intent'],'hex JSON capsule','unsigned_intent')
  if 'stage' in v:
   st=v['stage'];add('STAGE-META',obj(st['meta']),'blob:'+st['meta'],'canonical JSON','Authority.apply open');add('AUTHORIZED-MESSAGE',json.loads(blobs[st['message']][len(b'I164-ARCHITECTURE-A-AUTHORIZED-INPUTS-V2\n'):]),'blob:'+st['message'],'preserve blob; decode JSON after exact domain prefix','Authority.apply open / stage_carrier.decode')
 for e in events:
  if e['kind']=='observe':add('OBSERVATION',obj(e['proof']),'blob:'+e['proof'],'canonical exact evidence','Authority.apply observe')
  if e['kind']=='sign-persist':
   raw=blobs[e['proof']];add('SIGNED-TRANSACTION',{'raw_hex':raw.hex(),'decoded':signed_eth.decode(raw),'rlp_fields':[v.hex() for v in signed_eth.decode_rlp(raw)]},'blob:'+e['proof'],'exact raw bytes + deterministic RLP/transaction decode','Authority.sign')
 responses={m.sha(m.enc(q)):z['response'] for _,q,z in rs}
 for i,q,p in qs:
  add('BODY-'+q['method'],q['body'],f'/journal/{i}/1/request/body','exact member; candidate separately normalizes refused bodies','Scheduler.packet')
  res=responses.get(m.sha(m.enc(q)))
  if res is not None and res['ok']:
   if q['method']=='sign':add('SIGNED-RESULT',res['data'],f'/journal/{i}/2/response/data','exact success data','Authority.sign -> Authority.handle')
   if q['method'] in ['release','retry_release']:add('RELEASE-RESULT',res['data'],f'/journal/{i}/2/response/data','exact success data including release bytes','Authority.apply -> Authority.handle')
 for i,row in enumerate(x['journal']):add('JOURNAL',dict(zip(['challenge','request_hex','response_hex'],row)),f'/journal/{i}','exact raw strings including null','Authority.handle journal transactions')
 for ref,raw in x['blobs']:add('BLOB-STORE',{'ref':ref,'raw_hex':raw},'blob:'+ref,'exact original bytes, not digest replacement','Authority.blob')
 for i,row in enumerate(x['owners']):add('OWNERSHIP-ROW-SQL',dict(zip(['coord','raw_hex','hash'],row)),f'/owners/{i}','exact raw SQL tuple','ownership.claim')
 pub=json.loads((s.ROOT/'support/reference/public-keys.json').read_bytes());ref=s.ROOT/'support/reference'
 b={'ownership':m.sha(bytes.fromhex(x['ownership_meta'])),'ownership_code':m.sha((ref/'runtime/ownership.py').read_bytes()),'accounting_code':m.sha((ref/'runtime/accounting.py').read_bytes()),'code':m.sha((ref/'runtime/authority.py').read_bytes()),'config':x['config'],'principals':pub,'retained':{n:m.sha((ref/'retained'/n).read_bytes()) for n in ['anchor.py','stages.py','signed_eth.py','lab_evm.py']}}
 add('BINDING',b,'config + ownership_meta + pinned sources + public keys','exact construction inputs','Authority.__init__')
 return records,origins

def obligations(x):
 import ingest
 x=json.loads(m.enc(x));ingest.validate_export(x)
 events=[D(r[1]) for r in x['events']];head=D(x['head']);blobs={r:D(b) if bytes.fromhex(b).startswith(b'{') else None for r,b in x['blobs']};byrequest={};last=None
 for e in events:
  st=e['after'];byrequest.setdefault(e['request'],[]).append(e['kind'])
  if last:
   for k in last['counts']:m.need(st['counts'][k]>=last['counts'][k],'PERMANENT-CHARGE')
   for u,v in last['u'].items():
    m.need(u in st['u'],'PERMANENT-U');m.same([st['u'][u][k] for k in ['intent','reservation','retired']],[v[k] for k in ['intent','reservation','retired']],'IMMUTABLE-U')
  last=st
 outstanding=[]
 for u,v in head['u'].items():
  if 'stage' not in v:continue
  st=v['stage'];log=st['transport'];r=head['resources'];m.need(sum(t['slot']=='HELD' for t in log.values())==r['holds'],'HELD-OBLIGATION');m.need(sum(t['slot']=='CONSUMED' for t in log.values())==r['slots'],'ONCE-ONLY-SLOT');m.need(sum(not t['queried'] for t in log.values())==r['query_holds'],'QUERY-OBLIGATION')
  for ref in log:
   a=blobs[ref];m.need(a['u']==u and a['intent']==v['intent'] and a['binding']==head['binding'],'ATTEMPT-BINDING')
   if a['parent'] is not None:
    m.need(a['parent'] in log,'MISSING-ANCESTRY');parent=blobs[a['parent']];m.need(parent['action']==a['action'] and parent['ordinal']<a['ordinal'],'ANCESTRY');m.need(log[ref]['slot']=='CONSUMED','RETRY-SLOT')
  p=st['pending']
  if p:
   phase=p['phase'];m.need(p['first'] in log and p['latest'] in log,'PENDING-ANCESTRY')
   if phase in ['DECIDED','SIGNING']:m.need(p['tx'] is None and p['released'] is False,'PRE-SIGN-RELEASE')
   if phase in ['SIGNED','FAILED-FROZEN']:m.need(p['tx'] in blobs,'SIGNED-BLOB')
   outstanding.append({'u':u,'phase':phase,'first':p['first'],'latest':p['latest'],'action':p['action'],'transaction':p['tx'],'released':p['released'],'held_slots':r['holds'],'query_holds':r['query_holds'],'prohibited':['conflicting action decision','replacement transaction','refund or renewed allowance']+(['sign again; signing may already have occurred','release without persisted exact transaction'] if phase=='SIGNING' else []),'execution':'UNRESOLVED unless qualified retained disposition; local status is not non-execution'})
 journal=[]
 for challenge,packet,response in x['journal']:
  q=D(packet)['request'];ev=byrequest.get(m.sha(m.enc(q)),[]);z=None if response is None else D(response)['response'];journal.append({'challenge':challenge,'method':q['method'],'events':ev,'response':'UNANSWERED' if z is None else 'SUCCESS' if z['ok'] else 'ERROR','obligation':'preserve committed events, exact packet, charges and pending obligations regardless of response availability','no_event_meaning':'no recorded state transition in this authenticated export; not proof of no external effect'})
 return {'outstanding':outstanding,'journal':journal,'unresolved_bounds':True,'backup':'KERNEL-ONLY','final_binding':'BLOCKED','canonical_registration':False,'actual_admission':False,'stream_identities':'UNCOMPUTED'}

def verify_values(x,projected):
 expected,origins=reconstruct(x);m.same(projected,expected,'PRODUCER-PROJECTION-VALUE');return origins

def inspect(x,context,candidate=True,cut=None):
 import ingest
 x=json.loads(m.enc(x));c=s.setup(s.ROOT);verified=ingest.validate_export(x);origins=verify_values(x,verified['objects']);obs=obligations(x)
 out={'format':'I164-VALUE-FLOW-1','binding':c.binding,'export_sha256':m.sha(m.enc(x)),'context':context,'source_contract_sha256':m.sha(m.enc(source_contract())),'origins':origins,'obligations':obs,'records':len(origins),'final_binding':'BLOCKED','actual_admission':False,'stream_identities':'UNCOMPUTED'}
 m.need(context in c.contexts,'CONTEXT')
 if candidate:
  occ=c.ingest(x,context,c.binding);byindex={}
  for link in occ['candidate_occurrences']:byindex.setdefault(link['record_index'],[]).append(link)
  for origin in origins:
   links=byindex.get(origin['record_index'],[]);m.need(links,'DROPPED-OCCURRENCE');origin['occurrence_count']=len(links);origin['classes']=sorted({l['class'] for l in links})
  out['occurrence_sha256']=m.sha(m.enc(occ));out['response_associations']=occ['response_associations'];out['blockers']=occ['blockers'];m.need(out['blockers'],'MISSING-BLOCKERS')
 if cut is not None:
  import exception_flow
  out['exceptional_cut']=exception_flow.check_fixture(x,cut)
 return out

def validate(out,x,context,cut=None):m.same(out,inspect(x,context,cut=cut),'VALUE-FLOW-SUBSTITUTION');return True
