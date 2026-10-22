"""Offline ingestion entry point. SQLite sources opened immutable/read-only."""
import sqlite3,json
from pathlib import Path
from common import *
from correspondence import Fold,verify_signature,BODIES,VERSION,intent,config_binding,signed_eth

def read_database(path):
 p=Path(path).resolve();need(p.is_file(),'MISSING-DATABASE')
 need(not Path(str(p)+'-wal').exists() or Path(str(p)+'-wal').stat().st_size==0,'UNACQUIRED-WAL')
 c=sqlite3.connect(p.as_uri()+'?mode=ro&immutable=1',uri=True)
 try:
  need(c.execute('PRAGMA integrity_check').fetchall()==[('ok',)],'SQLITE-INTEGRITY')
  return c
 except Exception:c.close();raise

def acquire(db,ownership,config,expected_head):
 digest(expected_head);d=read_database(db);o=read_database(ownership)
 try:
  heads=d.execute('select id,raw from head').fetchall();need(len(heads)==1 and heads[0][0]==1,'HEAD-ROW')
  meta=o.execute('select id,raw from meta').fetchall();need(len(meta)==1 and meta[0][0]==1,'META-ROW')
  return {'format':'I164-RETRY3-CORRESPONDENCE-EXPORT-1','config':config,'expected_head':expected_head,'head':heads[0][1].hex(),'events':[[a,b.hex()] for a,b in d.execute('select seq,raw from events order by seq')],'blobs':[[a,b.hex()] for a,b in d.execute('select ref,raw from blobs order by ref')],'journal':[[a,b.hex(),None if c is None else c.hex()] for a,b,c in d.execute('select challenge,request,response from journal order by challenge')],'ownership_meta':meta[0][1].hex(),'owners':[[a,b.hex(),c] for a,b,c in o.execute('select coord,raw,hash from coordinates order by coord')]}
 finally:d.close();o.close()

def validate_export(x):
 pinned_sources();keys(x,'format config expected_head head events blobs journal ownership_meta owners');need(x['format']=='I164-RETRY3-CORRESPONDENCE-EXPORT-1','EXPORT-VERSION');digest(x['expected_head'])
 for n,limit in [('events',12000),('blobs',460),('journal',384000),('owners',4096)]:need(type(x[n]) is list and len(x[n])<=limit,'EXPORT-DIRECTORY:'+n)
 blobs={}
 for row in x['blobs']:
  need(type(row) is list and len(row)==2,'BLOB-ROW');ref,b=row;digest(ref);need(ref not in blobs,'DUPLICATE-BLOB');blobs[ref]=hexbytes(b)
 owners={}
 for row in x['owners']:
  need(type(row) is list and len(row)==3,'OWNER-ROW');coord,b,h=row;digest(coord);digest(h);raw=hexbytes(b);need(sha(raw)==h,'OWNER-HASH');v=parse(raw,262144);keys(v,'coordinate owner');digest(v['owner']);need(type(v['coordinate']) is list and len(v['coordinate'])==3,'COORDINATE');chain,address,nonce=v['coordinate'];decimal(chain);hexbytes(address,20);decimal(nonce);need(sha(enc(v['coordinate']))==coord and coord not in owners,'OWNER-COORDINATE');owners[coord]=v
 fold=Fold(x['config'],parse(hexbytes(x['ownership_meta'])),blobs,owners);requests={};packets={};responses={};envelopes={};challenges=set()
 for row in x['journal']:
  need(type(row) is list and len(row)==3,'JOURNAL-ROW');challenge,phex,rhex=row;digest(challenge);need(challenge not in challenges,'CHALLENGE-REPLAY');challenges.add(challenge)
  packet=hexbytes(phex);q=parse(packet);keys(q,'request signature');r=q['request'];keys(r,'version binding pilot session principal challenge expected method u body')
  need(r['version']==VERSION and r['binding']==fold.binding and r['pilot']==fold.config['pilot'] and r['session']==fold.config['session'],'CONTEXT');need(r['challenge']==challenge,'CHALLENGE-JOIN');digest(r['expected']);text(r['u']);need(type(r['method']) is str and type(r['body']) is dict,'REQUEST-TYPE');need(r['principal'] in ['executor','observer'],'PRINCIPAL');need((r['method']=='observe')==(r['principal']=='observer'),'ROLE');verify_signature(r['principal'],r,q['signature']);rh=sha(enc(r));need(rh not in requests,'REQUEST-DUPLICATE');requests[rh]=r;packets[rh]=packet
  if rhex is not None:
   raw=hexbytes(rhex);z=parse(raw,1048576);keys(z,'response signature');res=z['response'];boolean(res.get('ok'));keys(res,'request challenge ok '+('data' if res['ok'] else 'error'));need(res['request']==sha(packet) and res['challenge']==challenge,'RESPONSE-JOIN');verify_signature('server',res,z['signature'])
   if not res['ok']:text(res['error'],1048576)
   responses[rh]=res;envelopes[rh]=z
 histories={ZERO:fold.s};events_by_request={};objects=[('CONFIG',x['config']),('OWNERSHIP-META',parse(hexbytes(x['ownership_meta'])))]
 for row in x['events']:
  need(type(row) is list and len(row)==2,'EVENT-ROW');seq,rawhex=row;integer(seq,1,12000);need(seq==len(fold.occurrences)+1,'EVENT-ORDER');raw=hexbytes(rawhex);e=parse(raw,212992);digest(e['request']);need(e['request'] in requests,'MISSING-REQUEST');s=fold.advance(e,raw,requests[e['request']]);need(s['seq']==seq,'SEQ-JOIN');histories[s['head']]=s;events_by_request.setdefault(e['request'],[]).append(e)
  objects.extend([('EVENT',e),('HEAD',s)])
 head=parse(hexbytes(x['head']),196608);same(head,fold.s,'HEAD-HISTORY');need(head['head']==x['expected_head'],'EXPECTED-ANCHOR');need(fold.used==set(blobs),'UNOWNED-BLOB')
 for rh,res in responses.items():
  r=requests[rh];method=r['method'];ev=events_by_request.get(rh,[])
  if not res['ok']:continue # failed response may follow a committed cut; never erase that event
  need(method in BODIES,'SUCCESS-METHOD');keys(r['body'],BODIES[method]);data=res['data']
  if method=='head':
   need(not ev and r['expected'] in histories,'HEAD-READ-CONTEXT');same(data,histories[r['expected']],'HEAD-READ-EXACT')
  elif method=='sign':
   keys(data,'action tx recovered release');boolean(data['recovered']);need(data['release'] is False and data['action']==r['body']['action'],'SIGN-RESPONSE')
   if ev:
    need([e['kind'] for e in ev]==['sign-claim','sign-persist'] and data['recovered'] is False,'SIGN-EVENTS');st=histories[sha(enc(ev[-1]))]['u'][r['u']]['stage']
   else:
    need(data['recovered'] is True and r['expected'] in histories,'SIGN-RECOVERY');st=histories[r['expected']]['u'][r['u']]['stage']
   p=st['pending'];need(p is not None and p['phase']=='SIGNED' and data['action']==p['action'] and data['tx']==p['tx'],'SIGN-RECOVERY-BINDING')
  elif method in ['release','retry_release']:
   keys(data,'head action tx bytes lab_only'+(' attempt' if method=='retry_release' else ''));need(len(ev)==1 and ev[0]['kind']==('release' if method=='release' else 'retry-release'),'RELEASE-EVENT');s=histories[sha(enc(ev[0]))];p=s['u'][r['u']]['stage']['pending'];need(data['head']==s['head'] and data['action']==p['action'] and data['tx']==p['tx'] and data['lab_only'] is True,'RELEASE-RESPONSE');need(hexbytes(data['bytes'])==blobs[p['tx']],'RELEASE-EXACT-BYTES')
   if method=='retry_release':need(data['attempt']==p['latest'],'RETRY-RESPONSE')
  else:
   need(len(ev)==1,'SUCCESS-EVENT');same(data,histories[sha(enc(ev[0]))],'STATE-RESPONSE')
 # Metadata projection never grants canonical status or final binding.
 for rh,r in requests.items():objects.extend([('REQUEST',r),('PACKET',parse(packets[rh]))]);
 response_links=[]
 for rh,res in responses.items():
  response_links.append({'occurrence':len(objects),'request_hash':rh,'packet_hash':sha(packets[rh]),'challenge':res['challenge']})
  objects.append(('RESPONSE',envelopes[rh]))
 for row in owners.values():objects.append(('OWNERSHIP-ROW',row))
 for ref in sorted(fold.attempts):objects.append(('ATTEMPT',fold.obj(ref)))
 for ref in sorted(fold.actions):
  action=fold.obj(ref);objects.extend([('ACTION',action),('TEMPLATE',action['template'])])
 # Typed child records retain original wrappers and explicit keys; no opaque evidence leaves.
 for state in histories.values():
  objects.extend([('COUNTS',state['counts']),('PARTITIONS',state['partitions']),('RESOURCES',state['resources'])])
  for u,v in state['u'].items():
   objects.append(('U-ENTRY',{'key':u,'value':v}))
   if 'stage' not in v:continue
   st=v['stage'];objects.append(('STAGE',st))
   for key,value in st['transport'].items():objects.append(('TRANSPORT-ENTRY',{'key':key,'value':value}))
   for key,value in st['retry_ids'].items():objects.append(('RETRY-ID-ENTRY',{'key':key,'value':value}))
   for key,value in st['backups'].items():objects.append(('BACKUP-ENTRY',{'key':key,'value':value}))
   if st['last'] is not None:objects.append(('LAST',st['last']))
   if st['pending'] is not None:
    objects.append(('PENDING',st['pending']))
    if st['pending']['query'] is not None:objects.append(('QUERY',st['pending']['query']))
 for u,v in head['u'].items():
  raw=blobs[v['intent']];original=parse(raw,262144);resolved=intent(raw,u,x['config'])
  objects.append(('COMPACT-INTENT' if 'format' in original else 'UNSIGNED-INTENT',original));objects.append(('ABI-ARGUMENTS-'+resolved['method'],resolved['arguments']));objects.append(('CONDITIONAL-CAPSULE',parse(hexbytes(resolved['conditional_comparison_hex']),65536)))
  if 'stage' in v:
   st=v['stage'];objects.append(('STAGE-META',parse(blobs[st['meta']],262144)));objects.append(('AUTHORIZED-MESSAGE',parse(blobs[st['message']][41:],1048576)))
 for e in [parse(hexbytes(row[1]),212992) for row in x['events']]:
  if e['kind']=='observe':objects.append(('OBSERVATION',parse(blobs[e['proof']],262144)))
  if e['kind']=='sign-persist':objects.append(('SIGNED-TRANSACTION',{'raw_hex':blobs[e['proof']].hex(),'decoded':signed_eth.decode(blobs[e['proof']]),'rlp_fields':[v.hex() for v in signed_eth.decode_rlp(blobs[e['proof']])]}))
 for rh,r in requests.items():
  objects.append(('BODY-'+r['method'],r['body']))
  if rh in responses and responses[rh]['ok']:
   if r['method']=='sign':objects.append(('SIGNED-RESULT',responses[rh]['data']))
   if r['method'] in ['release','retry_release']:objects.append(('RELEASE-RESULT',responses[rh]['data']))
 for row in x['journal']:objects.append(('JOURNAL',{'challenge':row[0],'request_hex':row[1],'response_hex':row[2]}))
 for ref,b in blobs.items():objects.append(('BLOB-STORE',{'ref':ref,'raw_hex':b.hex()}))
 for row in x['owners']:objects.append(('OWNERSHIP-ROW-SQL',{'coord':row[0],'raw_hex':row[1],'hash':row[2]}))
 objects.append(('BINDING',{'ownership':sha(hexbytes(x['ownership_meta'])),'ownership_code':sha((ROOT/'reference/runtime/ownership.py').read_bytes()),'accounting_code':sha((ROOT/'reference/runtime/accounting.py').read_bytes()),'code':sha((ROOT/'reference/runtime/authority.py').read_bytes()),'config':x['config'],'principals':__import__('correspondence').PUB,'retained':{n:sha((ROOT/'reference/retained'/n).read_bytes()) for n in ['anchor.py','stages.py','signed_eth.py','lab_evm.py']}}))
 return {'status':'SUPPORTED-CORRESPONDENCE-ONLY','binding':fold.binding,'head':head['head'],'counts':head['counts'],'resources':head['resources'],'events':len(fold.occurrences),'attempts':len(fold.attempts),'actions':len(fold.actions),'action_kinds':sorted(fold.kinds),'journal_rows':len(x['journal']),'unanswered_requests':len(requests)-len(responses),'occurrences':fold.occurrences,'objects':objects,'response_links':response_links,'canonical_registration':False,'qualification':False,'actual_admission':False}

def ingest_file(path):return validate_export(parse(Path(path).read_bytes(),200000000))
