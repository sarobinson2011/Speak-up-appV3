"""Saved inventory attachment to the reviewed evaluator. No execution-count inference."""
import argparse,copy,hashlib,importlib.util,io,json,pathlib,stat,sys,traceback,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
SUPPLEMENT=(406472,'7e5dc2486e4fdf22ad844f55f27e56894b3c516c7a9eb51e21c6091f2b5e6ea3')
ORIGINAL=(451499,'0da08011fcd4e8068816bcc077e335cf236245fe60930212c43e90303c9ca34b')
EVALUATOR=(13520,'91d9db56aef8b622ae823b8e63ed52c971a3223fb736c5a27d2cf5800ab939ae')
BASE='/home/steve/dev/Engineering-288-execution/'
BOOT='I164-bootstrap-5002-test-xyhpeykd';REOPEN='I164-reopen-5002-test-v_pzlvyy'
GAPS=('read-recovery-invocations','managed-instances','backup-restoration-copies','diagnostic-interruption-evidence')
def need(v,msg):
 if not v:raise ValueError(msg)
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def same(a,b,msg):need(enc(a)==enc(b),msg)
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(b,p,msg):same(identity(b),dict(zip(('bytes','sha256'),p)),msg)
def parse(b):
 def pairs(xs):
  d={}
  for k,v in xs:need(k not in d,'DUPLICATE-JSON-KEY');d[k]=v
  return d
 return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda _:need(False,'NONFINITE'))
def read(p):
 p=pathlib.Path(p);need(stat.S_ISREG(p.lstat().st_mode),'REGULAR-FILE');return p.read_bytes()
def archive(raw):
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  names=z.namelist();need(len(names)==len(set(names)) and z.testzip() is None,'ZIP-CRC-MEMBERS')
  for i in z.infolist():
   p=pathlib.PurePosixPath(i.filename);need(not p.is_absolute() and '..' not in p.parts and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG),'ZIP-ENTRY')
  m=parse(z.read('MANIFEST.json'));same(sorted(names),sorted([*m,'MANIFEST.json']),'EXACT-MEMBERSHIP')
  files={n:z.read(n) for n in names}
  for n,v in m.items():same(identity(files[n]),v,'MANIFEST-HASH')
 return files

def inventory(raw):
 """Derive from authenticated retained records, never submitted receipt fields."""
 pin(raw,SUPPLEMENT,'SUPPLEMENT-PIN');f=archive(raw);pin(f['original-inventory.zip'],ORIGINAL,'ORIGINAL-PIN');old=archive(f['original-inventory.zip'])
 inv=parse(old['INVENTORY.json']);supp=parse(f['SUPPLEMENT.json']);need(not supp['gaps'],'SUPPLEMENT-GAP')
 rows=[];data={}
 for r in inv['records']:
  b=old[r['collected_member']];same(identity(b),r['identity'],'ORIGINAL-RECORD');need(r['record_id'] not in data,'DUPLICATE-RECORD');data[r['record_id']]=b
  rows.append({'record_id':r['record_id'],'source_path':r['source_path'],'identity':identity(b),'container':dict(zip(('bytes','sha256'),ORIGINAL)),'member':r['collected_member']})
 def oldobj(n):return parse(old['records/%05d.json'%n])
 for report,root,names in [(oldobj(1),BOOT,('runtime-recovery.json','stdout.log','stderr.log')),(oldobj(2),REOPEN,('reopened-state.json','stdout.log','stderr.log'))]:
  same(report['evidence'],BASE+root,'REPORT-ROOT')
  for name in names:
   member='records/'+root+'--'+name;b=f[member];same(identity(b),report['evidence_files'][name],'RECORDED-FILE-HASH')
   matching=[r for r in supp['record_classifications'] if r['source_path']==BASE+root+'/'+name];need(len(matching)==1,'SUPPLEMENT-RECORD-ID')
   rid=matching[0]['record_id'];need(rid not in data,'DUPLICATE-RECORD');data[rid]=b
   rows.append({'record_id':rid,'source_path':BASE+root+'/'+name,'identity':identity(b),'container':dict(zip(('bytes','sha256'),SUPPLEMENT)),'member':member})
 need(len(rows)==182 and len({r['source_path'] for r in rows})==182,'RECORD-UNIVERSE')
 bypath={r['source_path']:r for r in rows};oldsession=oldobj(8)['configuration']['config']['session'];newsession=oldobj(159)['configuration']['config']['session']
 for r in rows:
  path=r['source_path'];session=None;episode=None;scope='UNCLASSIFIED'
  if any(s in path for s in ('/composition/','/checkpoint/','/reviewed-launcher/')):scope='HISTORICAL-FIXTURE-OR-COMPONENT-PROVENANCE'
  elif '/'+BOOT+'/' in path or '/'+REOPEN+'/' in path or path.endswith(('SEND-TO-ANCHOR-bootstrap-test.json','SEND-TO-ANCHOR-reopen-test.json')):
   scope='SEPARATE-5002-HOST-FIXTURE';session=newsession;episode='REPORTED-REOPEN' if REOPEN in path or path.endswith('SEND-TO-ANCHOR-reopen-test.json') else 'REPORTED-BOOTSTRAP'
  elif any('/'+n+'/' in path for n in ('I164-lab-session-001','I164-managed-head-001','I164-head-acquisition-tg4mkg3l','I164-snapshot-acquisition-egpf25d9')) or path.endswith(('I164-managed-head-001-summary.json','I164-initialization-inspection-e0606cwa.json')):scope='ORIGINAL-4107-SESSION-RECORD';session=oldsession
  need(scope!='UNCLASSIFIED','UNCLASSIFIED-PROVENANCE')
  target=None
  for marker,dest in (('/saved-head/','I164-managed-head-001/'),('/saved-evidence/','I164-managed-head-001/'),('/session-records/','I164-lab-session-001/')):
   if marker in path:target=BASE+dest+path.split(marker,1)[1]
  if path.endswith('SEND-TO-ANCHOR-bootstrap-test.json') or path==BASE+REOPEN+'/bootstrap-result.json':target=BASE+BOOT+'/RESULT.json';episode='REPORTED-BOOTSTRAP'
  elif path.endswith('SEND-TO-ANCHOR-reopen-test.json'):target=BASE+REOPEN+'/RESULT.json'
  elif path.endswith('I164-managed-head-001-summary.json'):target=BASE+'I164-managed-head-001/SUMMARY.json'
  elif path.endswith('/original-binding.json') and session==oldsession:target=BASE+'I164-lab-session-001/binding.json'
  elif path.endswith('/original-bootstrap-complete.json') and session==oldsession:target=BASE+'I164-lab-session-001/BOOTSTRAP-COMPLETE.json'
  c=bypath.get(target);copyref=None
  if c is not None:
   need(data[c['record_id']]==data[r['record_id']],'COPY-BYTE-CONFLICT');copyref=c['record_id']
  r.update({'provenance_scope':scope,'recorded_session':session,'reported_episode':episode,'copy_of':copyref,'copy_basis':'RECORDED-COPY-ROLE-AND-CHECKED-BYTES' if copyref else None,'runtime_invocation_id':None,'runtime_instance_id':None,'adds_invocation':False,'physical_alias_relationship':'UNKNOWN'})
 # Preserve root corrections and verify against the original manifest, not summaries.
 cm=oldobj(10)
 for c in supp['manifest_root_corrections']:
  n=c['original_conflict']['member'];r=bypath[BASE+'I164-lab-bootstrap-reviewed-001/composition/'+n]
  same(r['identity'],cm[n],'COMPOSITION-ROOT');same(c['checked_identity'],r['identity'],'CORRECTION-BINDING');need(c['original_conflict'] in inv['manifest_checks'],'ORIGINAL-CONFLICT')
 same(len(supp['manifest_root_corrections']),3,'CORRECTION-COUNT')
 # Exact assertions are retained with their producer record; no execution inference.
 facts=[]
 selections=[(BASE+BOOT+'/runtime-recovery.json',()),(BASE+REOPEN+'/reopened-state.json',()),(BASE+BOOT+'/RESULT.json',('status',)),(BASE+REOPEN+'/RESULT.json',('status',)),(BASE+REOPEN+'/confirmed-close.json',()),(BASE+BOOT+'/confirmed-close.json',()),(BASE+'I164-snapshot-acquisition-egpf25d9/locked-copy.json',())]
 for path,selector in selections:
  r=bypath[path];value=parse(data[r['record_id']])
  for k in selector:value=value[k]
  facts.append({'record_id':r['record_id'],'identity':r['identity'],'selector':list(selector),'exact_recorded_value':value,'support':'SAVED-ASSERTION-ONLY','execution_independently_observed':False})
 return {'records':rows,'facts':facts,'manifest_root_corrections':supp['manifest_root_corrections'],'original_result':oldobj(128),'acquisition_validation':oldobj(129),'data':data,'paths':bypath}

def load_evaluator():
 p=ROOT/'code/multiplicity.py';pin(read(p),EVALUATOR,'EVALUATOR-PIN');s=importlib.util.spec_from_file_location('inventory_pinned_multiplicity',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def _relevant_records(records,cid):
 # Scope-aware document selectors, not counts of executions or physical copies.
 selected=[]
 for r in records:
  if r['provenance_scope']=='HISTORICAL-FIXTURE-OR-COMPONENT-PROVENANCE':continue
  p=r['source_path'];name=p.rsplit('/',1)[-1]
  include=(cid=='backup-restoration-copies' and (r['copy_of'] is not None or name in ('locked-copy.json','database-identities-before.json','PACKAGE-MANIFEST.json')))
  include=include or (cid=='managed-instances' and name in ('binding.json','environment.json','runtime-recovery.json','BOOTSTRAP-COMPLETE.json','RESULT.json'))
  include=include or (cid=='read-recovery-invocations' and name in ('reopened-state.json','before-state.json','after-state.json','before-status.json','after-status.json','managed-handoff.json','confirmed-close.json','MANAGED-CLOSE-RETURNED.json','worker-result.json','SUMMARY.json','RESULT.json'))
  include=include or (cid=='diagnostic-interruption-evidence' and (name.endswith(('.log','.txt')) or name in ('RESULT.json','worker-result.json','confirmed-close.json')))
  if include:selected.append(r['record_id'])
 return selected

def _attach(base,inv,raw,receipt_raw):
 """Internal derivation; public run always revalidates evaluator and inventory."""
 same(base['acquisition_id'],inv['original_result']['acquisition_id'],'ACQUISITION-LINEAGE')
 need(len(base['expressions'])==14,'EXPRESSION-DOMAIN')
 byid={x['id']:x for x in base['expressions']}
 for cid in GAPS:need(byid[cid]['selected']['value'] is None and byid[cid]['selected']['status']=='UNKNOWN','INVENTORY-TOTAL-UNKNOWN')
 need(all(x['lifetime']['value'] is None and x['lifetime']['status']=='UNKNOWN' for x in base['expressions']),'LIFETIME-UNKNOWN')
 # Original acquisition records must be the same exact members used by O09/counts.
 # Export validation binds the original session; 5002 records remain supporting context only.
 original_binding=inv['acquisition_validation']['binding']
 need(any(original_binding in row['key'] for row in byid['session-head']['scope_rows']),'SESSION-BINDING')
 associations=[]
 for cid in GAPS:
  associations.append({'expression_id':cid,'scope':byid[cid]['definition']['expression']['domain'],'unit':byid[cid]['definition']['expression']['unit'],'guard':byid[cid]['guard'],'source_contract':byid[cid]['definition']['source_contract'],'evidence_record_ids':_relevant_records(inv['records'],cid),'value':None,'status':'UNKNOWN','reason':byid[cid]['selected']['dependencies'],'evidence_use':'PARTIAL-RECORDED-INVENTORY; no numeric contribution or cross-acquisition join'})
 return {'format':'I164-INVENTORY-CARRIER-CONNECTION-1','acquisition_id':base['acquisition_id'],'bindings':{'code':identity(read(__file__)),'evaluator':dict(zip(('bytes','sha256'),EVALUATOR)),'inventory':identity(raw),'original_inventory':dict(zip(('bytes','sha256'),ORIGINAL)),'validated_expression_receipt':identity(receipt_raw),'count_and_procedure':copy.deepcopy(base['bindings']['count_and_procedure'])},'evaluation':copy.deepcopy(base),'contexts':copy.deepcopy(base['contexts']),'inventory_records':copy.deepcopy(inv['records']),'recorded_facts':copy.deepcopy(inv['facts']),'root_corrections':copy.deepcopy(inv['manifest_root_corrections']),'inventory_associations':associations,'record_count':len(inv['records']),'record_count_unit':'RETAINED-RECORDS-NOT-INVOCATIONS','runtime_93_file_claim':'RECORDED-ONLY; runtime member bytes not verified by this inventory','cross_acquisition_joins':False,'physical_storage_bytes':None,'global_lifetime_bound':None,'obligations':copy.deepcopy(base['obligations']),'classification':'UNKNOWN','assessment':'SOURCE-ONLY','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False,'streams':'UNCOMPUTED','global_O06_closed':False,'global_O09_closed':False}

def run(config,submitted=None):
 same(sorted(config),['expression_config','expression_receipt','inventory_archive'],'CONFIGURATION')
 raw=read(config['inventory_archive']);inv=inventory(raw);receipt_raw=read(config['expression_receipt']);m=load_evaluator();base=m.run(config['expression_config'],parse(receipt_raw))
 # Bind retained acquisition member bytes to the validated lineage's pinned archive.
 copy_raw=read(config['expression_config']['copy_receipt']);same(identity(copy_raw),base['bindings']['copy_receipt'],'VALIDATED-COPY-BYTES');role=parse(copy_raw)
 members={x['key'][-1]:x['identity'] for x in role['members'] if x['key'][2]=='acquisition'}
 prefix=BASE+'I164-snapshot-acquisition-egpf25d9/'
 for r in inv['records']:
  if r['source_path'].startswith(prefix):
   member=r['source_path'][len(prefix):]
   if member in members:same(r['identity'],members[member],'ACQUISITION-MEMBER-CORRESPONDENCE')
 result=_attach(base,inv,raw,receipt_raw)
 if submitted is not None:same(result,submitted,'INVENTORY-CONNECTION-CORRESPONDENCE')
 return copy.deepcopy(result)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);ap.add_argument('--submitted');a=ap.parse_args();cfg=parse(read(a.config));out=pathlib.Path(a.output).absolute();need('/tmp' not in str(out) and not out.exists(),'NEW-PERSISTENT-OUTPUT');out.mkdir(parents=True)
 try:
  r=run(cfg,parse(read(a.submitted)) if a.submitted else None);(out/'receipt.json').write_bytes(enc(r)+b'\n');(out/'result.json').write_bytes(enc({'status':'PASS bounded inventory connection','records':182,'inventory_totals':'UNKNOWN','lifetime_totals':'UNKNOWN','receipt':identity(read(out/'receipt.json'))})+b'\n');print('PASS 182 records; four inventory totals and all lifetime totals UNKNOWN')
 except BaseException:(out/'failure.txt').write_text(traceback.format_exc());raise
if __name__=='__main__':main()
