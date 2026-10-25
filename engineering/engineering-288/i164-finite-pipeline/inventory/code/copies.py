"""Bounded O09 copy evidence. No database access or physical/lifetime inference."""
import zipfile,io,argparse,copy,hashlib,importlib.util,json,os,stat,sys,traceback
from pathlib import Path
COUNT_PIN={'bytes':3789194,'sha256':'d22b07f1d39bd45c4c306790ec83a40de1cf316e7ff57ad62ec2d9ee55a7ca32'}
COUNT_CODE='966ae0087a7806ac6748bdd04cde4800a95b03b8d3d49df125ff9a54fd7f98c6'
CONTEXTS=['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
def need(x,msg):
 if not x:raise ValueError(msg)
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p):
 p=Path(p);need(stat.S_ISREG(p.lstat().st_mode),'NONREGULAR');return p.read_bytes()
def parse(b):
 def pairs(rows):
  d={}
  for k,v in rows:need(k not in d,'DUPLICATE-JSON-KEY');d[k]=v
  return d
 return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda _:need(False,'NONFINITE'))
def same(a,b,msg):need(enc(a)==enc(b),msg)
def denied(event,args):
 if event in ('sqlite3.connect','socket.connect','socket.bind'):raise RuntimeError('FORBIDDEN-OPERATION:'+event)
def load_count(root):
 path=Path(root)/'code/evidence_counts.py';need(ident(read(path))['sha256']==COUNT_CODE,'COUNT-CODE-PIN')
 s=importlib.util.spec_from_file_location('o09_pinned_count',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def prepare(config):
 need(type(config) is dict and set(config)=={'count_archive','count_root','candidate','draft'},'CONFIGURATION')
 m=load_count(config['count_root']);raw=read(config['count_archive']);same(ident(raw),COUNT_PIN,'COUNT-ARCHIVE')
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  names=z.namelist();need(len(names)==len(set(names)) and z.testzip() is None,'COUNT-CRC')
  manifest=parse(z.read('MANIFEST.json'));same(sorted(names),sorted([*manifest,'MANIFEST.json']),'COUNT-MEMBERS')
  for n,v in manifest.items():same(ident(z.read(n)),v,'COUNT-MEMBER')
  files={n:z.read(n) for n in names}
 m.tree(config['count_root'],{n:ident(b) for n,b in files.items()})
 inputs=m._prepare(config['candidate'],config['draft'])
 # Reuse exact reviewed saved count output, not a new assertion supplied by caller.
 receipt=parse(files['results/build-001/receipt.json']);consumption=parse(files['results/build-001/consumption.json'])
 same(receipt['acquisition_id'],inputs['basis']['acquisition_id'],'ACQUISITION')
 same(receipt['obligations'],inputs['obligations'],'OBLIGATIONS')
 same(consumption['receipt_sha256'],ident(m.enc(receipt))['sha256'],'COUNT-RECEIPT')
 same([x['context'] for x in receipt['contexts']],CONTEXTS,'CONTEXTS')
 for n,v in receipt['bindings'].items():same(ident(read(Path(config['candidate'])/n)),v,'COUNT-SOURCE-BINDING')
 same(receipt['export_identity'],ident(inputs['archives']['acquisition']['export.json']),'EXPORT')
 import universe
 records=[{'acquisition_id':receipt['acquisition_id'],'context':r['context'],'export_sha256':receipt['export_identity']['sha256'],'counts':r['counts']} for r in receipt['contexts']]
 actual=universe.count_acquisition_bag(inputs['root'],inputs['universe'],records)
 same(actual,consumption['existing_counter_result'],'EXISTING-COUNT-CONSERVATION')
 same(consumption['obligations'],receipt['obligations'],'COUNT-OBLIGATIONS')
 return inputs,receipt,consumption,actual,files

def derive(inputs,count,consumption,actual,files):
 """Internal: requires authenticated prepare output. Not an independent admission API."""
 a,e=inputs['archives']['acquisition'],inputs['archives']['evaluation'];aid=count['acquisition_id']
 basis=inputs['basis'];refs={name:{k:basis['archives'][name][k] for k in ('bytes','sha256')} for name in ('acquisition','evaluation')}
 archives=[{'key':[aid,'ARCHIVE',role],'role':role,'identity':refs[role],'physical_container_identity':'UNKNOWN'} for role in refs]
 def key(role,n):return [aid,'ARCHIVE-MEMBER',role,n]
 def evidence(role,n):return {'archive':refs[role],'member':n,'identity':ident((a if role=='acquisition' else e)[n])}
 def role(n):
  if n.startswith('databases/'):return 'DATABASE-PAYLOAD'
  if n in ('export.json','preserved/export.json'):return 'EXPORT-BYTES'
  if n.endswith('/occurrences.json'):return 'PROJECTED-OCCURRENCES'
  if n.endswith('/procedure-result.json'):return 'PROCEDURE-RESULT'
  if n.endswith('locked-copy.json') or n=='database-identities-before.json':return 'RECORDED-CAPTURE-ASSERTIONS'
  return 'RETAINED-EVIDENCE-OR-SOURCE'
 members=[];relations=[]
 for ar,data in [('acquisition',a),('evaluation',e)]:
  for n,b in sorted(data.items()):
   members.append({'key':key(ar,n),'role':role(n),'identity':ident(b),'physical_container_identity':'UNKNOWN'})
   relations.append({'kind':'ARCHIVE-CONTAINS-MEMBER','from':[aid,'ARCHIVE',ar],'to':key(ar,n),'support':'INDEPENDENT-BYTE-CHECK'})
 locked=parse(a['locked-copy.json']);before=parse(a['database-identities-before.json'])
 same(set_as_list(before),set_as_list(locked['before']),'BEFORE-MEMBERS')
 same(before,locked['before'],'BEFORE-RECORDS');same(locked['before'],locked['after'],'RECORDED-STABILITY')
 names=['ownership.sqlite','session.sqlite'];same(sorted(before),names,'REQUIRED-DATABASE-ROLES')
 payloads=[];claims=[]
 for n in names:
  k=key('acquisition','databases/'+n);v=ident(a['databases/'+n])
  same(v,before[n],'COPY-PAYLOAD-BEFORE');same(v,locked['after'][n],'COPY-PAYLOAD-AFTER')
  claim=[aid,'RECORDED-SOURCE-PATH',n]
  claims.append({'key':claim,'recorded_path':locked['source_paths'][n],'recorded_identity':before[n],'support':'RECORDED-ASSERTION; ORIGINAL-NOT-INSPECTED','physical_identity':'UNKNOWN','evidence':evidence('acquisition','locked-copy.json')})
  payloads.append({'member':k,'role':n,'identity':v})
  relations.append({'kind':'RECORDED-COPY-OF','from':k,'to':claim,'support':'COPIED-BYTES-MATCH-RECORDED-IDENTITIES; COPYING-OPERATION-NOT-INDEPENDENTLY-OBSERVED','evidence':evidence('acquisition','locked-copy.json')})
 for n in ('export.json','locked-copy.json','saved-head/EVIDENCE-MANIFEST.json','saved-head/request.bin','saved-head/response.bin'):
  need(a[n]==e['preserved/'+n],'PRESERVED-LINEAGE-BYTES')
  relations.append({'kind':'EXACT-PRESERVED-MEMBER','from':key('evaluation','preserved/'+n),'to':key('acquisition',n),'support':'INDEPENDENT-BYTE-EQUALITY; NOT-A-NEW-ACQUISITION-OR-PHYSICAL-COPY-COUNT'})
 same(parse(e['predecessor.json'])['manifest'],parse(a['PACKAGE-MANIFEST.json']),'PREDECESSOR-MANIFEST')
 for n,v in locked['source_records'].items():same(ident(a['session-records/'+n]),v,'SESSION-RECORD-BINDING')
 # Existing authenticated exported rows remain exact evidence. Do not reconstruct DB state.
 export=parse(a['export.json']);request=parse(a['saved-head/request.bin']);response=parse(a['saved-head/response.bin'])
 challenge=request['request']['challenge'];matches=[r for r in export['journal'] if r[0]==challenge]
 same(matches,[[challenge,a['saved-head/request.bin'].hex(),a['saved-head/response.bin'].hex()]],'EXACT-WIRE-EXPORT-ASSOCIATION')
 same(response['response']['challenge'],challenge,'RESPONSE-CHALLENGE')
 contexts=[]
 for c in count['contexts']:
  ctx=c['context'];proc=e[ctx+'/procedure-result.json'];occ=e[ctx+'/occurrences.json']
  same(ident(proc),c['procedure_result_identity'],'PROCEDURE-IDENTITY');same(ident(occ),c['occurrence_identity'],'OCCURRENCE-IDENTITY')
  contexts.append({'context':ctx,'acquisition_id':aid,'export':key('acquisition','export.json'),'counts_identity':ident(enc(c['counts'])),'directory_entries':len(c['counts']),'occurrence_record':evidence('evaluation',ctx+'/occurrences.json'),'procedure_record':evidence('evaluation',ctx+'/procedure-result.json'),'membership_sha256':c['membership_sha256'],'finite_tokens':c['finite_tokens'],'physical_storage_multiplier':None})
 carriers=inputs['universe']['protected_carriers'];dispositions=[]
 for c in carriers:
  cid=c['id']
  if cid in ('session-head','event-history','journal','saved-responses','blob-store','ownership-ledger','charged-attempts','pending-uncertainty','backup-identifiers'):
   status='SAVED-EXPORT-AND-COUNT-EVIDENCE-BOUND';support=[evidence('acquisition','export.json')];gap='Physical database row-to-export correspondence not independently reexecuted; source installation completeness, lifetime multiplicity and operational state remain unestablished.'
  elif cid=='export-acquisitions':
   status='ONE-SELECTED-ACQUISITION-LINEAGE-BOUND';support=[evidence('evaluation','predecessor.json'),evidence('acquisition','locked-copy.json')];gap='Complete lifetime acquisition inventory and source-owned retention scope absent; repeated byte-identical members are not additional acquisitions.'
  elif cid=='backup-restoration-copies':
   status='SELECTED-ARCHIVE-MEMBERS-AND-DATABASE-PAYLOADS-BOUND';support=[evidence('acquisition','locked-copy.json')];gap='No physical container/alias/allocation or backup/restore completeness evidence; source path and archive-member multiplicity do not prove physical duplication.'
  else:
   status='GAP';support=[];gap='No complete managed-instance/invocation/diagnostic inventory in this selected acquisition; no zero-count or lifetime inference.'
  dispositions.append({'carrier_id':cid,'source_contract':copy.deepcopy(c),'status':status,'support':support,'gap':gap})
 return {'format':'I164-ACQUISITION-CARRIER-COPY-RECEIPT-1','acquisition_id':aid,'assessment':'SOURCE-ONLY','classification':'UNKNOWN','qualification':'UNAVAILABLE','archives':archives,'members':members,'relationships':relations,'recorded_source_claims':claims,'selected_database_payloads':payloads,'selected_database_payload_bytes':sum(r['identity']['bytes'] for r in payloads),'byte_total_scope':'TWO-SELECTED-DATABASE-MEMBER-PAYLOADS-ONLY; excludes archive/export/other members; no sum across contexts','capture_assertions':{'evidence':evidence('acquisition','locked-copy.json'),'recorded':copy.deepcopy(locked),'independently_established_lock_ownership':False,'independently_established_sidecar_absence':False,'independently_observed_capture':False},'contexts':contexts,'bindings':{'count_component':copy.deepcopy(COUNT_PIN),'count_receipt':ident(files['results/build-001/receipt.json']),'count_consumption':ident(files['results/build-001/consumption.json']),'existing_count_result':ident(enc(actual)),'candidate':copy.deepcopy(count['bindings']),'universe':ident(read(inputs['draft']/'source-only/universe/outputs/universe.json'))},'carrier_dispositions':dispositions,'obligations':copy.deepcopy(count['obligations']),'evidence_reuse':'Exact reviewed count/procedure outputs; no fresh projection/authentication-suite execution. New byte/lineage checks and existing count-only consumption only.','physical_container_count':'UNKNOWN','physical_storage_bytes':'UNKNOWN','global_lifetime_bound':'UNKNOWN','complete_acquisition_inventory':False,'cross_acquisition_joins':False,'operational_assurance':False,'canonical_registration':False,'full_expansion_ready':False,'final_binding':'BLOCKED','stream_identities':'UNCOMPUTED','actual_admission':False,'backup':'KERNEL-ONLY'}
def set_as_list(x):return sorted(x)
def run(config,submitted=None):
 inputs,count,consumption,actual,files=prepare(config);expected=derive(inputs,count,consumption,actual,files)
 if submitted is not None:same(submitted,expected,'CARRIER-COPY-CORRESPONDENCE')
 return copy.deepcopy(expected)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--submitted');ap.add_argument('--output',required=True);a=ap.parse_args()
 out=Path(a.output).absolute();need('/tmp' not in str(out) and not out.exists(),'NEW-PERSISTENT-OUTPUT');config=parse(read(a.config))
 protected=[Path(v).resolve() for k,v in config.items() if k in ('count_root','candidate','draft')]+[Path(__file__).resolve().parents[1]]
 need(all(out.resolve()!=p and p not in out.resolve().parents for p in protected),'PROTECTED-OUTPUT')
 out.mkdir(parents=True);sys.addaudithook(denied)
 try:
  submitted=parse(read(a.submitted)) if a.submitted else None
  if a.submitted:need(type(submitted) is dict,'SUBMITTED-TYPE')
  value=run(config,submitted);(out/'receipt.json').write_bytes(enc(value)+b'\n')
  (out/'result.json').write_bytes(enc({'status':'PASS bounded O09 copy correspondence','receipt':ident(read(out/'receipt.json')),'contexts':CONTEXTS,'selected_database_payload_bytes':value['selected_database_payload_bytes'],'obligations':len(value['obligations']['source_only']),'full_expansion_ready':False})+b'\n');print('PASS bounded O09; physical/lifetime bounds UNKNOWN; admission disabled')
 except BaseException:
  (out/'failure.txt').write_text(traceback.format_exc());raise
if __name__=='__main__':main()
