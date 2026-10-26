"""Two explicit retained acquisition contracts; no source/SQLite access."""
import hashlib,io,json,os,stat,zipfile
from pathlib import Path,PurePosixPath
CONTEXTS=['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
class Rejected(ValueError):pass
def need(v,m):
 if not v:raise Rejected(m)
def enc(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()+b'\n'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def parse(b):
 def pairs(rows):
  d={}
  for k,v in rows:need(k not in d,'DUPLICATE-KEY');d[k]=v
  return d
 return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda _:need(False,'NONFINITE'))
def same(a,b,m):need(enc(a)==enc(b),m)
def read(p):
 p=Path(p);need(stat.S_ISREG(p.lstat().st_mode),'REGULAR-FILE')
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:return f.read()
def write(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(enc(v))
def archive(raw,pin,manifest='PACKAGE-MANIFEST.json'):
 same(ident(raw),pin,'ARCHIVE-PIN')
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  names=z.namelist();need(len(names)==len(set(names)) and z.testzip() is None,'ZIP-CRC-UNIQUE')
  for n in z.infolist():
   p=PurePosixPath(n.filename);need(not p.is_absolute() and '..' not in p.parts and str(p)==n.filename and not n.is_dir() and stat.S_IFMT(n.external_attr>>16) in [0,stat.S_IFREG],'ZIP-SAFE')
  data={n:z.read(n) for n in names};m=parse(data[manifest]);same(sorted(data),sorted([*m,manifest]),'ZIP-MEMBERS')
  for n,v in m.items():same(ident(data[n]),v,'ZIP-MEMBER:'+n)
  return data

def request_evidence(a,export,legacy=False):
 """Wire envelopes are evidence, not commands. Semantic signatures/fold validated by ingest.
 A null response is permitted by ingest.validate_export; missing request bytes are not.
 A legacy saved-head triad is explicit evidence and must remain exact if present.
 """
 need(type(export['journal']) is list,'JOURNAL-LIST');seen=set();rows=[]
 for row in export['journal']:
  need(type(row) is list and len(row)==3,'JOURNAL-ROW')
  challenge,q,r=row;need(challenge not in seen,'DUPLICATE-CHALLENGE');seen.add(challenge)
  need(type(q) is str and bool(q),'MISSING-REQUEST')
  raw=bytes.fromhex(q);packet=parse(raw);need(set(packet)=={'request','signature'},'REQUEST-ENVELOPE')
  same(packet['request']['challenge'],challenge,'REQUEST-CHALLENGE')
  if r is not None:
   need(type(r) is str and bool(r),'MISSING-RESPONSE-BYTES');response=parse(bytes.fromhex(r))
   need(set(response)=={'response','signature'},'RESPONSE-ENVELOPE')
   same(response['response']['challenge'],challenge,'RESPONSE-CHALLENGE')
   same(response['response']['request'],ident(raw)['sha256'],'RESPONSE-REQUEST')
  rows.append({'challenge':challenge,'request':ident(raw),'response':None if r is None else ident(bytes.fromhex(r))})
 names={'saved-head/EVIDENCE-MANIFEST.json','saved-head/request.bin','saved-head/response.bin'}
 present={n for n in a if n.startswith('saved-head/')}
 if legacy or present:
  need(names<=present,'MISSING-SAVED-HEAD-EVIDENCE')
  q=parse(a['saved-head/request.bin'])['request'];r=parse(a['saved-head/response.bin'])['response']
  need(q['method']=='head' and r['ok'] is True,'SAVED-HEAD-TYPE')
  same([x for x in export['journal'] if x[0]==q['challenge']],[[q['challenge'],a['saved-head/request.bin'].hex(),a['saved-head/response.bin'].hex()]],'SAVED-HEAD-JOURNAL')
  same(r['data'],parse(bytes.fromhex(export['head'])),'SAVED-HEAD-DATA')
 return {'journal_rows':len(rows),'rows':rows,'saved_head_present':bool(present),'absence_basis':'governing journal schema; no invented head request','schema':'support/code/ingest.py::validate_export'}

def target(a,pin):
 """Pure checker, called only after archive authentication by public acceptance."""
 aid=pin['acquisition_id'];result=parse(a['RESULT.json']);locked=parse(a['locked-copy.json'])
 same(result['acquisition_id'],aid,'ACQUISITION-ID');same(result['target'],pin['target'],'TARGET')
 before=parse(a['source-before.json']);after=parse(a['source-after.json'])
 same(before,after,'SOURCE-STABILITY');same(before,locked['before'],'LOCK-BEFORE');same(after,locked['after'],'LOCK-AFTER')
 same(sorted(before),sorted(pin['source_identities']),'NINE-SOURCE-ROLES');need(len(before)==9,'NINE-ENTRIES')
 same(before,pin['source_records'],'RETAINED-SOURCE-METADATA')
 same(locked['lineage'],pin['lineage'],'EXACT-LINEAGE');same(locked['guard_before'],locked['guard_after'],'RECORDED-GUARDS')
 need(locked['cross_acquisition_joins'] is False and result['cross_acquisition_joins'] is False,'NO-CROSS-ACQUISITION')
 same(locked['existing_lock'],pin['target']+'/.disposable-session.owner.lock','OWNER-LOCK-PATH')
 seen=set();members=set();links=[]
 for row in locked['lineage']:
  same(row['acquisition_id'],aid,'LINEAGE-ACQUISITION');src=row['source_path'];prefix=pin['target']+'/'
  need(src.startswith(prefix),'SOURCE-PATH');rel=src[len(prefix):];need(rel in before and rel not in seen,'SOURCE-LINEAGE-UNIQUE');seen.add(rel)
  member='databases/'+Path(rel).name if rel.startswith('disposable-session/state/') else 'records/'+rel
  same(row['copy_member'],member,'COPY-LAYOUT');need(member not in members,'COPY-UNIQUE');members.add(member)
  same(ident(a[member]),before[rel]['identity'],'COPIED-PAYLOAD');same(row['identity'],before[rel]['identity'],'LINEAGE-IDENTITY')
  links.append({'key':[aid,'ARCHIVE-MEMBER',member],'source_record':rel,'recorded_source_path':src,'identity':row['identity'],'source_metadata':before[rel]['metadata'],'support':'BYTES-MATCH-RETAINED-RECORD; copying operation and source ownership not independently observed'})
 same(sorted(seen),sorted(before),'LINEAGE-COVERAGE')
 same(sorted(n for n in a if n.startswith(('records/','databases/'))),sorted(members),'RECORDS-EXACT-LAYOUT')
 export=parse(a['export.json']);cfg=parse(a['records/reviewed-launcher/laboratory-configuration.json']);binding=parse(a['records/disposable-session/binding.json'])
 same(export['config'],pin['configuration'],'EXACT-CONFIG');same(cfg['config'],export['config'],'CONFIG-EXPORT');same(binding['configuration'],cfg,'BINDING-CONFIG')
 head=parse(bytes.fromhex(export['head']));meta=bytes.fromhex(export['ownership_meta'])
 same(head['binding'],pin['binding'],'HEAD-BINDING');same(ident(meta),pin['ownership_meta'],'OWNERSHIP-META');same(parse(meta)['incarnation'],pin['incarnation'],'INCARNATION')
 same(parse(a['records/disposable-session/BOOTSTRAP-COMPLETE.json'])['state'],head,'BOOTSTRAP-STATE')
 same(parse(a['records/managed-handoff.json'])['state'],head,'HANDOFF-STATE')
 same(result['observation_point_utc'],locked['observation_point_utc'],'OBSERVATION-POINT')
 return {'form':'QUIESCENT-NINE-RECORDS','acquisition_id':aid,'target':pin['target'],'session':export['config']['session'],'binding':head['binding'],'ownership_meta':ident(meta),'incarnation':pin['incarnation'],'links':links,'request_evidence':request_evidence(a,export),'recorded_observation_point':locked['observation_point_utc'],'factual_history':'UNKNOWN','history_cutoff':'UNKNOWN','physical_container_count':'UNKNOWN','physical_storage_bytes':'UNKNOWN','operational_assurance':False}

def legacy(a,aid):
 locked=parse(a['locked-copy.json']);before=parse(a['database-identities-before.json']);same(before,locked['before'],'LEGACY-BEFORE');same(before,locked['after'],'LEGACY-STABILITY')
 same(sorted(before),['ownership.sqlite','session.sqlite'],'LEGACY-TWO-DB')
 for n,v in before.items():same(ident(a['databases/'+n]),v,'LEGACY-PAYLOAD')
 for n,v in locked['source_records'].items():same(ident(a['session-records/'+n]),v,'LEGACY-RECORD')
 return {'form':'LEGACY-SAVED-HEAD','acquisition_id':aid,'request_evidence':request_evidence(a,parse(a['export.json']),True),'source_paths':locked['source_paths'],'source_records':locked['source_records']}
