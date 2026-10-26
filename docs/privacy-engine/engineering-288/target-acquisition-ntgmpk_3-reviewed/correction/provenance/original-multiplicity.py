"""Source-bound carrier expressions; finite saved evidence, never lifetime closure."""
import argparse,ast,copy,hashlib,importlib.util,io,json,pathlib,stat,sys,traceback,zipfile
P=pathlib.Path(__file__).resolve().parents[1]
COPY={'bytes':12631,'sha256':'9e8934ce5b74b525cb141df21c7b95c7f167c5fb4b7e93e6d284f0975d265271'}
# Carrier id, domain, unit, summand, local ceiling (not lifetime bound).
RECIPES=(
 ('session-head','session_namespaces','head_rows','H',None),
 ('event-history','session_namespaces','events','E','MAX_EVENTS'),
 ('journal','journal_namespaces','journal_rows','J','MAX_ROWS'),
 ('saved-responses','journal_namespaces','response_rows','R',None),
 ('blob-store','session_namespaces','blob_rows','B',None),
 ('ownership-ledger','ledger_namespaces','ownership_coordinates','O','MAX_COORDINATES'),
 ('charged-attempts','opened_stages','charged_attempts','A',102),
 ('pending-uncertainty','acquisition_history_states','pending_U_states','P',None),
 ('backup-identifiers','opened_stages','backup_identifiers','K',85),
 ('export-acquisitions','retained_acquisition_receipts','acquisitions','X',None),
 ('read-recovery-invocations','managed_instances','invocations',['status','state','recover'],None),
 ('managed-instances','deployments','managed_instances','I',None),
 ('backup-restoration-copies','physical_retained_containers','physical_bytes','bytes',None),
 ('diagnostic-interruption-evidence','retained_traces','trace_events','length',None))
def need(v,m):
 if not v:raise ValueError(m)
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def parse(b):
 def pairs(xs):
  d={}
  for k,v in xs:need(k not in d,'DUPLICATE-JSON-KEY');d[k]=v
  return d
 return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:need(False,'NONFINITE'))
def read(p):
 p=pathlib.Path(p);need(stat.S_ISREG(p.lstat().st_mode),'REGULAR-FILE');return p.read_bytes()
def same(a,b,m):need(enc(a)==enc(b),m)
def write(p,v):
 with pathlib.Path(p).open('xb') as f:f.write(enc(v)+b'\n')
def load_module():
 p=P/'code/copies.py';same(ident(read(p)),COPY,'COPY-CODE-PIN');s=importlib.util.spec_from_file_location('reviewed_carriers',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def compile_expressions(lineage,root):
 """Exact source contracts are independently validated by the reviewed O09 API."""
 contracts=[v['source_contract'] for v in lineage['carrier_dispositions']]
 same([c['id'] for c in contracts],[r[0] for r in RECIPES],'CARRIER-DOMAIN')
 constants={}
 for name,path in [('MAX_ROWS','authority.py'),('MAX_EVENTS','authority.py'),('MAX_COORDINATES','ownership.py')]:
  raw=read(pathlib.Path(root)/'support/reference/runtime'/path);tree=ast.parse(raw)
  hits=[ast.literal_eval(n.value) for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)]
  need(len(hits)==1 and type(hits[0]) is int,'SOURCE-CONSTANT');constants[name]=hits[0]
 result=[]
 for c,(_,domain,unit,term,cap) in zip(contracts,RECIPES):
  for anchor in c['source_anchors']:
   raw=read(pathlib.Path(root)/anchor['path']);need(ident(raw)['sha256']==anchor['source_sha256'],'SOURCE-HASH')
   nodes=[n for n in ast.walk(ast.parse(raw)) if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==anchor['name'] and n.lineno==anchor['line']]
   need(len(nodes)==1 and hashlib.sha256(ast.dump(nodes[0],include_attributes=False).encode()).hexdigest()==anchor['ast_sha256'],'SOURCE-ANCHOR')
  # Explicit lowering; no eval of descriptive strings or inferred Cartesian domains.
  result.append({'id':c['id'],'source_contract':copy.deepcopy(c),'expression':{'op':'SUM_SCOPED','domain':domain,'unit':unit,'term':{'op':'ADD','variables':term} if type(term) is list else {'op':'VALUE','variable':term}},'local_ceiling':constants.get(cap,cap) if cap else None,'constraints':['R<=J'] if c['id']=='saved-responses' else ['slots+holds<=16'] if c['id']=='charged-attempts' else [],'global_domain_complete':False})
 return result

def conditional(definition, rows):
 """Pure arithmetic over declared conditional scopes; never authenticates facts."""
 e=definition['expression'];need(e['op']=='SUM_SCOPED','OP');term=e['term'];variables=term['variables'] if term['op']=='ADD' else [term['variable']];seen=set();missing=[];total=0
 if rows is None:return {'value':None,'unit':e['unit'],'status':'UNKNOWN','dependencies':['missing scope inventory: '+e['domain']],'global_bound':None}
 need(type(rows) is list,'SCOPE-ROWS')
 for row in rows:
  same(sorted(row),['domain','key','unit','values'],'ROW-SCHEMA');same(row['domain'],e['domain'],'SCOPE');same(row['unit'],e['unit'],'UNIT');need(type(row['key']) is list and row['key'] and all(type(x) is str and x for x in row['key']),'SCOPE-KEY');key=enc(row['key']);need(key not in seen,'DUPLICATE-SCOPE');seen.add(key)
  required=set(variables)|({'J'} if definition['id']=='saved-responses' else {'slots','holds'} if definition['id']=='charged-attempts' else set())
  need(type(row['values']) is dict and not set(row['values'])-required,'UNSUPPORTED-VARIABLE');known=True;v=0
  for name in required:
   x=row['values'].get(name)
   if x is None:missing.append({'scope':row['key'],'variable':name});known=False
   else:need(type(x) is int and x>=0,'COUNT-TYPE')
  if not known:continue
  v=sum(row['values'][n] for n in variables)
  if definition['id'] in ('session-head','export-acquisitions'):need(v==1,'SINGLETON-SCOPE')
  if definition['id']=='pending-uncertainty':need(v<=1,'PENDING-INDICATOR')
  if definition['local_ceiling'] is not None:need(v<=definition['local_ceiling'],'LOCAL-CEILING')
  if definition['id']=='saved-responses':need(v<=row['values']['J'],'RESPONSE-JOURNAL')
  if definition['id']=='charged-attempts':need(row['values']['slots']+row['values']['holds']<=16,'SLOT-HOLD')
  total+=v
 return {'value':None if missing else total,'unit':e['unit'],'status':'UNKNOWN' if missing else 'CONDITIONAL_SELECTED_SCOPES','dependencies':missing,'global_bound':None}

def snapshot_rows(definitions, export, lineage):
 """Source-derived selectors from exact retained export; no database read/replay."""
 aid=lineage['acquisition_id'];head=parse(bytes.fromhex(export['head']));binding=head['binding'];blobs=export['blobs'];events=export['events'];journal=export['journal'];owners=export['owners']
 for rows in (blobs,events,journal,owners):
  need(type(rows) is list,'EXPORTED-ROWS');keys=[enc(r[0]) for r in rows];need(len(keys)==len(set(keys)),'DUPLICATE-EXPORTED-KEY')
 need(type(head['u']) is dict,'U-MAP')
 states=[(str(seq),parse(bytes.fromhex(raw))['after']) for seq,raw in events]
 # Source initialization has no U and therefore contributes zero pending states.
 # Event after-states retain history identity; current head is not an extra history.
 if not events:need(head['seq']==0,'MISSING-HISTORY')
 else:need(states[-1][1]['seq']==head['seq'],'HISTORY-FRONTIER')
 values={'session-head':{'H':1},'event-history':{'E':len(events)},'journal':{'J':len(journal)},'saved-responses':{'R':sum(r[2] is not None for r in journal),'J':len(journal)},'blob-store':{'B':len(blobs)},'ownership-ledger':{'O':len(owners)},'export-acquisitions':{'X':1}}
 rows_by_id={};keys_by_id={}
 for d in definitions:
  cid=d['id'];e=d['expression']
  def row(key,vals):return {'domain':e['domain'],'unit':e['unit'],'key':[aid,*key],'values':vals}
  if cid in values:rows_by_id[cid]=[row([binding,cid],values[cid])]
  elif cid in ('charged-attempts','backup-identifiers'):
   rs=[];keys=[]
   for u,entry in sorted(head['u'].items()):
    if 'stage' not in entry:continue
    st=entry['stage'];need(type(st['transport']) is dict and type(st['backups']) is dict,'STAGE-MAPS')
    if cid=='charged-attempts':
     need(type(st['attempts']) is int and st['attempts']==len(st['transport']),'ATTEMPT-COUNT');vals={'A':st['attempts'],'slots':head['resources']['slots'],'holds':head['resources']['holds']};keys.extend([[aid,binding,u,k] for k in st['transport']])
    else:vals={'K':len(st['backups'])};keys.extend([[aid,binding,u,k] for k in st['backups']])
    rs.append(row([binding,u,st['sid']],vals))
   if cid=='charged-attempts':need(sum(x['values']['A'] for x in rs)==head['counts']['attempt'],'ATTEMPT-CONTINUITY')
   rows_by_id[cid]=rs;keys_by_id[cid]=keys
  elif cid=='pending-uncertainty':
   rs=[];keys=[]
   for seq,state in states:
    for u,entry in sorted(state['u'].items()):
     if 'stage' not in entry:continue
     st=entry['stage'];need('pending' in st,'MISSING-PENDING');v=int(st['pending'] is not None);rs.append(row([binding,seq,u],{'P':v}))
     if v:keys.append([aid,binding,seq,u])
   rows_by_id[cid]=rs;keys_by_id[cid]=keys
  else:rows_by_id[cid]=None
 keys_by_id.update({'session-head':[[aid,binding,'exported-head']], 'event-history':[[aid,binding,str(r[0])] for r in events], 'journal':[[aid,binding,r[0]] for r in journal], 'saved-responses':[[aid,binding,r[0],hashlib.sha256(bytes.fromhex(r[2])).hexdigest()] for r in journal if r[2] is not None], 'blob-store':[[aid,binding,r[0]] for r in blobs], 'ownership-ledger':[[aid,'exported-ledger',r[0]] for r in owners], 'export-acquisitions':[[aid]]})
 return rows_by_id,keys_by_id

def evaluate(definitions,export,lineage):
 rows,keys=snapshot_rows(definitions,export,lineage);result=[]
 for d in definitions:
  cid=d['id'];v=conditional(d,rows[cid]);c=d['source_contract'];selected=copy.deepcopy(v)
  selected['status']='CHECKED_SAVED_EXPORT_CALCULATION' if v['value'] is not None else 'UNKNOWN'
  selected['scope']='ONE_SELECTED_ACQUISITION_EXPORT; not physical installation or lifetime inventory'
  if rows[cid] is not None:
   need(v['value']==len(keys[cid]),'KEY-COUNT');selected['occurrence_keys']=keys[cid]
  else:selected['dependencies']=[c['missing_evidence']]
  result.append({'id':cid,'definition':copy.deepcopy(d),'selected':selected,'scope_rows':rows[cid], 'lifetime':{'value':None,'status':'UNKNOWN','unit':d['expression']['unit'],'expression':copy.deepcopy(d['expression']),'dependencies':[c['missing_evidence']],'global_bound':None},'guard':c['creation_guard'],'source_lifetime_scope':c['lifetime_scope']})
 return result

def run(config,submitted=None):
 need(type(config) is dict and set(config)=={'count_archive','count_root','candidate','draft','copy_receipt'},'CONFIGURATION')
 m=load_module();sys.addaudithook(m.denied);base={k:v for k,v in config.items() if k!='copy_receipt'};raw=read(config['copy_receipt']);lineage=m.run(base,parse(raw))
 # Exact byte-bound retained archive, already validated by O09. No acquisition.
 role=next(x for x in lineage['archives'] if x['role']=='acquisition');matches=[]
 for p in (pathlib.Path(config['count_root'])/'inputs').glob('*.zip'):
  b=read(p)
  if ident(b)==role['identity']:matches.append(b)
 need(len(matches)==1,'ACQUISITION-ARCHIVE')
 with zipfile.ZipFile(io.BytesIO(matches[0])) as z:export_raw=z.read('export.json')
 match=next(x for x in lineage['members'] if x['key']==[lineage['acquisition_id'],'ARCHIVE-MEMBER','acquisition','export.json']);same(ident(export_raw),match['identity'],'EXPORT-BYTES')
 export=parse(export_raw);definitions=compile_expressions(lineage,config['candidate']);expressions=evaluate(definitions,export,lineage)
 result={'format':'I164-CARRIER-MULTIPLICITY-EVALUATION-1','acquisition_id':lineage['acquisition_id'],'bindings':{'code':ident(read(__file__)),'reviewed_validator':COPY,'copy_receipt':ident(raw),'count_and_procedure':copy.deepcopy(lineage['bindings']),'export':ident(export_raw)},'expressions':expressions,'contexts':copy.deepcopy(lineage['contexts']),'context_use':'same acquisition-qualified carrier values; contexts are references, never physical multipliers','selected_database_payload_bytes':lineage['selected_database_payload_bytes'],'payload_scope':lineage['byte_total_scope'],'recorded_capture_assertions':copy.deepcopy(lineage['capture_assertions']),'obligations':copy.deepcopy(lineage['obligations']),'classification':'UNKNOWN','assessment':'SOURCE-ONLY','physical_storage_bytes':None,'global_lifetime_bound':None,'global_O06_closed':False,'global_O09_closed':False,'full_expansion_ready':False,'final_binding':'BLOCKED','canonical_registration':False,'stream_identities':'UNCOMPUTED','actual_admission':False,'backup':'KERNEL-ONLY'}
 if submitted is not None:same(result,submitted,'MULTIPLICITY-CORRESPONDENCE')
 return copy.deepcopy(result)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);ap.add_argument('--submitted');a=ap.parse_args();out=pathlib.Path(a.output).absolute();config=parse(read(a.config));need('/tmp' not in str(out) and not out.exists(),'NEW-PERSISTENT-OUTPUT');protected=[P]+[pathlib.Path(config[k]).resolve() for k in ('candidate','draft','count_root')];need(all(out.resolve()!=p and p not in out.resolve().parents for p in protected),'PROTECTED-INPUT');out.mkdir(parents=True)
 try:
  r=run(config,parse(read(a.submitted)) if a.submitted else None);write(out/'receipt.json',r);write(out/'result.json',{'status':'PASS bounded carrier expression evaluation','expressions':len(r['expressions']),'selected_known':sum(x['selected']['value'] is not None for x in r['expressions']),'lifetime_unknown':14,'receipt':ident(read(out/'receipt.json')),'obligations':11});print('PASS 14 expressions; lifetime UNKNOWN; admission disabled')
 except BaseException:(out/'failure.txt').write_text(traceback.format_exc());raise
if __name__=='__main__':main()
