"""Adopted Option A. Conditional laboratory accounting, no external transport."""
from anchor import need,enc,parse,MAX_INTENT

def validate(s):
 r=s['resources'];need(set(r)=={'slots','holds','query_holds','extra_queries'},'RESOURCE-FIELDS')
 for k,v in r.items():need(type(v) is int and 0<=v<= (2086 if k=='query_holds' else 16),'RESOURCE-TYPE')
 need(r['slots']+r['holds']<=16,'SLOT-CAP')
 need(s['counts']['query']+r['query_holds']<=3110 and s['partitions']['query']+r['query_holds']<=2086,'QUERY-RESERVATIONS')
 for d,limits in [(s['counts'],{'attempt':2070,'query':3110,'snapshot':130,'verifier':64}),(s['partitions'],{'query':2086,'snapshot':85,'verifier':18})]:
  for k,limit in limits.items():need(type(d[k]) is int and 0<=d[k]<=limit,'COUNTER')
 st=s['u'].get(s['active'],{}).get('stage') if s['active'] is not None else None
 if st:
  need(type(st['attempts']) is int and 0<=st['attempts']<=102,'ATTEMPT-CAP')
  need(type(st['retries']) is int and 0<=st['retries']<=16,'RETRY-CAP')
  log=st['transport'];need(len(log)<=102 and len(st['retry_ids'])<=16,'TRANSPORT-BOUND')
  need(sum(x['slot']=='HELD' for x in log.values())==r['holds'] and sum(x['slot']=='CONSUMED' for x in log.values())==r['slots'],'SLOT-ACCOUNTING')
  need(sum(not x['queried'] for x in log.values())==r['query_holds'],'QUERY-HOLD-ACCOUNTING')
  for x in log.values():
   need(set(x)=={'slot','queried','released'} and x['slot'] in ['HELD','CONSUMED','RELEASED'] and type(x['queried']) is bool and type(x['released']) is bool,'TRANSPORT-TYPES')

def reserve(a,s,st,kind,retry=False):
 r=s['resources'];need(s['counts']['attempt']<2070 and st['attempts']<102,'ATTEMPT-CAP')
 need(r['slots']+r['holds']<16,'SLOT-CAP')
 need(s['counts']['query']+r['query_holds']<3110 and s['partitions']['query']+r['query_holds']<2086,'QUERY-HEADROOM')
 i=a.intent(s,s['active'])
 if kind=='finalize' or (kind=='proceed' and i['method']=='signPetitionWithZKProof'):
  need(s['counts']['verifier']<64 and s['partitions']['verifier']<18,'VERIFIER-CAP');s['counts']['verifier']+=1;s['partitions']['verifier']+=1
 s['counts']['attempt']+=1;st['attempts']+=1;r['query_holds']+=1
 if retry:r['slots']+=1;st['retries']+=1
 else:r['holds']+=1

def record(a,s,st,request,action,parent=None,tx=None,retry_id=None):
 x={'binding':a.binding,'pilot':a.config['pilot'],'session':a.config['session'],'u':request['u'],'intent':s['u'][request['u']]['intent'],'sid':st['sid'],'action':action,'parent':parent,'transaction':tx,'ordinal':s['counts']['attempt'],'retry_id':retry_id,'request':__import__('hashlib').sha256(enc(request)).hexdigest()}
 ref=a.blob(enc(x));need(ref not in st['transport'],'ATTEMPT-DUPLICATE');st['transport'][ref]={'slot':'CONSUMED' if parent else 'HELD','queried':False,'released':False};return ref

def ready(a,s,u,first=False):
 st=a.stage(s,u);p=st['pending'];need(p is not None,'NO-PENDING');entry=st['transport'][p['latest']]
 act=parse(a.get(p['action']),MAX_INTENT);a.require_ownership(s,u,int(act['template']['nonce']))
 rec=parse(a.get(p['latest']),MAX_INTENT)
 need(rec['binding']==a.binding and rec['u']==u and rec['intent']==s['u'][u]['intent'] and rec['action']==p['action'] and rec['sid']==st['sid'],'ATTEMPT-BINDING')
 if first:need(p['latest']==p['first'] and entry['slot']=='HELD' and not entry['queried'] and not entry['released'],'FIRST-RESERVATION')
 validate(s);return act

def query(s,st,request):
 p=st['pending'];need(p is not None and p['phase']=='SIGNED' and p['released'] and p['query'] is None,'QUERY-STATE');r=s['resources'];e=st['transport'][p['latest']]
 if not e['queried']:need(r['query_holds']>0,'QUERY-HOLD');r['query_holds']-=1;e['queried']=True;classification='ATTEMPT'
 else:
  need(r['extra_queries']<16,'EXTRA-QUERY-CAP')
  need(s['counts']['query']+r['query_holds']<3110 and s['partitions']['query']+r['query_holds']<2086,'QUERY-CAP');r['extra_queries']+=1;classification='EXTRA'
 s['counts']['query']+=1;s['partitions']['query']+=1
 p['query']={'request':__import__('hashlib').sha256(enc(request)).hexdigest(),'ordinal':s['counts']['query'],'attempt':p['latest'],'classification':classification};p['reconciliation']=None

def settle(s,st,failed):
 p=st['pending'];e=st['transport'][p['first']];need(e['slot']=='HELD','ALREADY-CLASSIFIED')
 s['resources']['holds']-=1
 if failed:e['slot']='CONSUMED';s['resources']['slots']+=1
 else:e['slot']='RELEASED'
 # Retry entries are already permanently CONSUMED. No charge or evidence is removed.
 validate(s)
