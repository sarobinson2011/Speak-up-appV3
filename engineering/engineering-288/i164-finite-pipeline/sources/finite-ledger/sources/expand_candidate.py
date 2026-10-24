"""Segmented metadata-only model extension. Never enumerate equality pairs."""
import json,hashlib,mmap,sys,os,time,shutil,resource,gzip
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'prior-code'));sys.path.insert(0,str(R/'retained/kernel/adapter/retained/collector/kernel'))
from model_kernel.catalog import Catalog,CONTEXTS,ROLES,PARSER_FIELDS
from model_kernel.expand import record_keys
import executor_records_v2 as executor_records
W=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
H=lambda b:hashlib.sha256(b).hexdigest()
def need(x,msg):
 if not x:raise ValueError(msg)
def load(p):return json.loads(Path(p).read_bytes())
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def atomic(p,b):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.pending')
 with tmp.open('wb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 os.replace(tmp,p);fd=os.open(p.parent,os.O_RDONLY);os.fsync(fd);os.close(fd)
def save(p,v):atomic(p,W(v)+b'\n')
class Model:
 def __init__(self,p):
  self.f=open(p,'rb');self.m=mmap.mmap(self.f.fileno(),0,access=mmap.ACCESS_READ);self.ranges={}
  keys=['actor_graph_policy','equality_stream','relations','structural_edges','surfaces','tokens']
  for i,k in enumerate(keys):
   prefix=('"'+k+'":').encode();a=self.m.find(prefix)+len(prefix);b=self.m.find((',"'+keys[i+1]+'":').encode(),a) if i+1<len(keys) else len(self.m)-2
   need(a>=len(prefix) and b>a,'model layout');self.ranges[k]=(a,b)
 def small(self,k):a,b=self.ranges[k];return json.loads(self.m[a:b])
 def copy(self,k,out,h,inside=False):
  a,b=self.ranges[k];a+=inside;b-=inside
  for pos in range(a,b,1048576):raw=self.m[pos:min(b,pos+1048576)];out.write(raw);h.update(raw)
class Seq:
 def __init__(self,keys):self.keys=keys;self.lookup=None;self.prefixes=None
 def __len__(self):return len(self.keys)
 def at(self,i):return (i+1,None) if isinstance(self.keys,range) else self.keys[i]
 def span(self,prefix):
  if self.prefixes is None:
   self.prefixes={}
   for i,(r,p) in enumerate(self.keys):
    key=str(r).split(':',1)[0]
    if key not in self.prefixes:self.prefixes[key]=[i,i+1]
    else:self.prefixes[key][1]=i+1
  return self.prefixes.get(prefix,[0,0])
 def pos(self,k):
  if isinstance(self.keys,range):
   try:n=int(k)
   except (ValueError,TypeError):return None
   return n-1 if str(n)==str(k) and 1<=n<=len(self) else None
  if self.lookup is None:self.lookup={str(r):i for i,(r,p) in enumerate(self.keys)}
  return self.lookup.get(str(k))
class Group:
 def __init__(self):self.parts=[]
 def add(self,start,seq,new):self.parts.append((start,seq,new))
 def __len__(self):return sum(len(s) for _,s,_ in self.parts)
 def entries(self,prefix=None):
  for start,seq,new in self.parts:
   lo,hi=(0,len(seq)) if prefix is None else seq.span(prefix)
   for i in range(lo,hi):
    rec,parent=seq.at(i);yield start+i,rec,parent,new
 def get(self,rec):
  for start,seq,new in self.parts:
   pos=seq.pos(rec)
   if pos is not None:return start+pos,new
  return None

def prepare(parent,base):
 pm=Model(parent);bm=Model(base);oldrows=load(R/'retained/registers/fields.json');cat=Catalog(R/'sources');c=load(R/'sources/selected-contract.json');new=executor_records.declarations()
 counts={'EXECUTOR-META':1,'EXECUTOR-STATUS':1024,'EXECUTOR-STATE-ENTRY':65536,'EXECUTOR-BACKUP':130}
 for r in new:r['slots']=counts.get(r['record'],r['slots']);r['multiplicity_status']='ADOPTED-SHARED-ALLOWANCES-2026-10-11'
 # Explicit accounting records, their fields and containing/framing classes.
 account={'EXECUTOR-ALLOWANCE-BINDING':['pilot','accounting_code','wrapper_code','policy'],'ALLOWANCE-BINDING':['pilot','limits','version'],'ALLOWANCE-CHARGE':['pilot','operation','kind','request_id','previous','ordinal'],'ALLOWANCE-STATE':['pilot','sequence','head','query','snapshot'],'ALLOWANCE-RECEIPT':['sequence','kind','ordinal','record_sha256','pilot']}
 for name,fields in account.items():
  for f in fields+['$record','presence','availability','encoding_length']:
   new.append({'node_id':'I164:'+name+'.'+f,'record':name,'selector':f,'slots':1 if name in ('ALLOWANCE-BINDING','EXECUTOR-ALLOWANCE-BINDING') else 2179 if name=='ALLOWANCE-STATE' else 1154,'declared_exposure':'UNKNOWN','reuse':'NONE','owner_source_id':'I164-ACCOUNTED-PROFILE-1','source_anchor':name+'/'+f,'source_file':'code/allowances.py','source_sha256':sha(R/'code/allowances.py'),'genuine_value':'UNAVAILABLE','qualification':'UNAVAILABLE'})
 # Exact defining source for executor binding, including virtual framing selectors.
 for row in new:
  if row['record']=='EXECUTOR-ALLOWANCE-BINDING':
   row['source_file']='code/executor_accounted.py';row['source_sha256']=sha(R/row['source_file']);row['source_anchor']='Session.__init__:binding/'+row['selector']
 # Explicit nested map members from exact source structures, not opaque object leaves.
 for schema,pointers in {'EXECUTOR-META':['code/'+x for x in ['executor/session.py','executor/abi.py','contract/PetitionRegistryPilot.sol','contract/ABI.json','contract/method-identifiers.json']], 'EXECUTOR-BACKUP':['job/version','job/job']+['job/code/'+x for x in ['executor/session.py','executor/abi.py','contract/PetitionRegistryPilot.sol','contract/ABI.json','contract/method-identifiers.json']], 'ALLOWANCE-BINDING':['limits/query','limits/snapshot']}.items():
  template=next(r for r in new if r['record']==schema)
  for pointer in pointers:
   q=dict(template);q.update(node_id='I164:'+schema+'.F'+H(pointer.encode())[:24],selector=pointer);new.append(q)
 if not any(r['record']=='PROJECTION' and r['selector']=='$record' for r in oldrows):
  q=dict(next(r for r in oldrows if r['record']=='PROJECTION'));q.update(node_id='I164:PROJECTION.$record',selector='$record');new.append(q)
 # Every ABI argument record receives a containing-record class (not an opaque carrier).
 for name in sorted({r['record'] for r in new}):
  if not any(r['record']==name and r['selector']=='$record' for r in new):
   q=dict(next(r for r in new if r['record']==name));q.update(node_id='I164:'+name+'.$record',selector='$record');new.append(q)
 framing=[]
 for r in list(new):
  for tag in ('PRESENCE','STATUS','ENCODING-LENGTH'):
   q=dict(r);q.update(node_id='I164:ACCOUNTED-FRAME.F'+H((r['node_id']+'#'+tag).encode())[:24],selector=r['selector']+'#'+tag,framing_of=r['node_id']);framing.append(q)
 new.extend(framing)
 nodes=pm.small('surfaces');rels=pm.small('relations');old_node_n=len(nodes);old_rel_n=len(rels)
 for r in new:nodes.append({'node_id':r['node_id'],'kind':'OWNING-SCHEMA','owner_source_id':r['owner_source_id'],'owner_anchor':r.get('source_anchor','source record'),'declared_exposure':'UNKNOWN','reuse':'NONE','source_data':''})
 need(len({n['node_id'] for n in nodes})==len(nodes),'duplicate class')
 dirs=dict(c['schema_directories']);dirs['FIELD-LABEL']=list(dirs['FIELD-LABEL'])+[f'I164-FIELD-LABEL-{i:06}' for i in range(len(dirs['FIELD-LABEL'])+1,len(nodes)+1)]
 custom={}
 for r in oldrows+new:
  if r['record'] in custom:need(custom[r['record']]==r['slots'],'schema multiplicity')
  custom[r['record']]=r['slots']
 for name,n in custom.items():dirs[name]=[f'I164-{name}-{i:06}' for i in range(1,n+1)]
 cnew=dict(c,schema_directories=dirs,field_label_surfaces=[n['node_id'] for n in nodes]);cnew['format']='I164-ACCOUNTED-FINITE-PRODUCER-CONTRACT-1';cnew['i164_extension']={'approval_sha256':sha(R/'records/approval.json'),'parent_contract_sha256':sha(R/'sources/selected-contract.json'),'shared_query_limit':1024,'shared_snapshot_limit':130,'status_entry_max_per_response':64,'new_U_or_configuration_refill':False,'actual_admission':False};catnew=Catalog(R/'sources');catnew.schemas=sorted(dirs)
 groups={};append=[];seqcache={}
 def group(sid,ctx):return groups.setdefault((sid,ctx),Group())
 # Original CP2 tokens only; the 4.5m parent extension has analytical contiguous groups.
 base_tokens=bm.small('tokens');bucket={}
 for t in base_tokens:bucket.setdefault((t['surface'],t['context']),[]).append(t)
 for (sid,ctx),ts in bucket.items():
  # Original source preserves per-class groups but repeated slots may be separate ranges.
  run=[];start=None;last=None
  for t in ts:
   if last is not None and t['index']!=last+1:
    group(sid,ctx).add(start,Seq(run),False);run=[];start=None
   if start is None:start=t['index']
   rec=t['record'];parent=None
   if isinstance(rec,str) and ':REF:' in rec:
    parent=rec.split(':REF:')[0]
    if sid.startswith('CP2-REFERENCE-MATERIAL:'):parent=parent.split(':',1)[1]
   if isinstance(rec,str) and ':PARSE:' in rec:parent=rec.split(':',1)[1].rsplit(':PARSE:',1)[0]
   run.append((rec,parent));last=t['index']
  group(sid,ctx).add(start,Seq(run),False)
 del base_tokens,bucket
 index=426984
 for ctx in CONTEXTS:
  for r in oldrows:
   group(r['node_id'],ctx).add(index,Seq(range(r['slots'])),False);index+=r['slots']
 need(index==4510432,'parent token coverage')
 for ctx in CONTEXTS:
  for n in cat.nodes:
   sel=cat.selectors[n['node_id']];key=tuple(sel)
   if key not in seqcache:
    oldkeys={str(r) for r,_ in record_keys(cat,c,sel)};keys=[x for x in record_keys(catnew,cnew,sel) if str(x[0]) not in oldkeys];seqcache[key]=Seq(keys)
   seq=seqcache[key]
   if len(seq):group(n['node_id'],ctx).add(index,seq,True);append.append((index,n['node_id'],ctx,seq));index+=len(seq)
  for r in new:
   seq=Seq(range(r['slots']));group(r['node_id'],ctx).add(index,seq,True);append.append((index,r['node_id'],ctx,seq));index+=len(seq)
 need(index<2**32,'U32 token capacity')
 rules=list(cat.join_rules)+['RETAINED-UNCHANGED']*(old_rel_n-len(cat.join_rules));details=[None]*len(rels)
 def relation(a,b,label,rule='SAME-RECORD',detail=None):rels.append({'from_node':a,'to_node':b,'relation':label});rules.append(rule);details.append(detail)
 for r in oldrows+new:
  for role in ROLES:relation(r['node_id'],'CP2-CUSTODIAN:'+role,'POTENTIAL-CUSTODY-UNKNOWN','CARTESIAN')
 for r in [*new,*[x for x in oldrows if x['record']=='PROJECTION']]:
  rec=next(x['node_id'] for x in new if x['record']==r['record'] and x['selector']=='$record')
  if rec!=r['node_id']:relation(r['node_id'],rec,'EXACT-OWNING-RECORD-FIELD')
 for r in framing:relation(r['node_id'],r['framing_of'],'PER-FIELD-FRAMING-CORRESPONDENCE')
 # Parser/owning-record correspondence for custom schemas, using exact source directory keys.
 for schema in custom:
  candidates=[r['node_id'] for r in oldrows+new if r['record']==schema and r['selector']=='$record']
  if not candidates:continue # PROJECTION fields have no separate containing record in retained schema.
  for f in PARSER_FIELDS:relation('CP2-RECORD-PARSER:'+f,candidates[0],'PARSER-RECORD-CORRESPONDENCE','CUSTOM-PARSER',schema)
 for method in ['signPetition','signPetitionWithZKProof']:
  owner=next(r['node_id'] for r in oldrows if r['record']=='OBSERVER-'+method and r['selector']=='/records/0/storage_words')
  for r in oldrows:
   if r['record']=='STORAGE-ENTRY-'+method:relation(r['node_id'],owner,'STORAGE-ENTRY-CONTAINING-OBSERVATION','PARENT-SLOT',144)
 # Status entries are per response and per U, not a single 64-entry directory.
 relation('I164:EXECUTOR-STATE-ENTRY.$record','I164:EXECUTOR-STATUS.$record','STATUS-ENTRY-OWNING-RESPONSE','PARENT-SLOT',64)
 # Exact content-addressed joins are conditional until genuine content exists; retain every legal counterpart.
 for a,b,label in [('RECORD','INTENT','INTENT-DIGEST-REFERENCE'),('RECORD','TRANSACTION','TRANSACTION-DIGEST-REFERENCE'),('RECORD','RECONCILIATION','RECONCILIATION-DIGEST-REFERENCE'),('RECORD','REJECTION','REJECTION-DIGEST-REFERENCE'),('BLOB','INTENT','BLOB-PARSER-INTENT'),('BLOB','TRANSACTION','BLOB-PARSER-TRANSACTION'),('BLOB','RECONCILIATION','BLOB-PARSER-RECONCILIATION'),('STATUS','STATE-ENTRY','STATUS-CONTAINS-STATE-ENTRIES')]:
  if label=='STATUS-CONTAINS-STATE-ENTRIES':continue
  relation('I164:EXECUTOR-'+a+'.$record','I164:EXECUTOR-'+b+'.$record',label,'CARTESIAN')
 need(len(rels)<1000000,'ordinal template wire limit')
 return {'pm':pm,'bm':bm,'nodes':nodes,'rels':rels,'rules':rules,'details':details,'groups':groups,'append':append,'new_fields':new,'dirs':dirs,'custom':custom,'token_count':index,'old_node_n':old_node_n,'old_rel_n':old_rel_n,'contract':cnew}

def pairs(p,number,ctx):
 r=p['rels'][number];rule=p['rules'][number];detail=p['details'][number];a=p['groups'][r['from_node'],ctx];b=p['groups'][r['to_node'],ctx];is_new=number>=p['old_rel_n']
 if rule=='RETAINED-UNCHANGED':return
 b_has_new=any(n for _,_,n in b.parts)
 if not is_new and not b_has_new and not any(n for _,_,n in a.parts):return
 prefix=detail if rule=='CUSTOM-PARSER' else r['to_node'].split(':',1)[1].split('.',1)[0] if rule in ('PARSER-SCHEMA','MATERIAL-FIELD') else None
 for i,rec,parent,anew in a.entries(prefix):
  if not is_new and not anew and not b_has_new:continue
  if rule=='CARTESIAN':
   for j,rr,pp,bnew in b.entries():
    if is_new or anew or bnew:yield i,j
  elif rule in ('SAME-RECORD','PARENT-RECORD','PARSER-SCHEMA','MATERIAL-FIELD','CUSTOM-PARSER','PARENT-SLOT'):
   target=rec
   if rule=='PARENT-RECORD':target=parent
   if rule=='PARSER-SCHEMA':
    schema=r['to_node'].split(':',1)[1].split('.',1)[0]
    if not str(rec).startswith(schema+':'):continue
    target=parent
   if rule=='MATERIAL-FIELD':
    schema,field=r['to_node'].split(':',1)[1].split('.',1)
    if not str(rec).startswith(schema+':') or ':REF:'+field+':' not in str(rec):continue
    target=parent
   if rule=='CUSTOM-PARSER':
    if not str(rec).startswith(detail+':'):continue
    target=int(parent.rsplit('-',1)[1])
   if rule=='PARENT-SLOT':target=(int(rec)-1)//detail+1
   found=b.get(target);need(found is not None,'dangling structural parent '+str((r,rec,target)))
   j,bnew=found
   if is_new or anew or bnew:yield i,j
  elif rule=='INHERITED-COMPONENT':continue # no added OLD tokens
  else:raise ValueError(rule)

def estimate(p):
 # Exact count by join cardinality, not pair enumeration. Indexed joins only.
 counts=[]
 for k,r in enumerate(p['rels']):
  rule=p['rules'][k];total=0
  if rule in ('RETAINED-UNCHANGED','INHERITED-COMPONENT'):counts.append(0);continue
  for ctx in CONTEXTS:
   a=p['groups'][r['from_node'],ctx];b=p['groups'][r['to_node'],ctx]
   if rule=='CARTESIAN':
    alln=len(a)*len(b);old_a=sum(len(s) for _,s,n in a.parts if not n);old_b=sum(len(s) for _,s,n in b.parts if not n)
    total+=alln if k>=p['old_rel_n'] else alln-old_a*old_b
   elif rule=='RETAINED-UNCHANGED':pass
   else:total+=sum(1 for _ in pairs(p,k,ctx))
  counts.append(total)
 added=sum(counts);tokens=p['token_count'];raw_upper=1816517788+(tokens-4510432)*600+added*110
 return {'token_count':tokens,'added_tokens':tokens-4510432,'surface_count':len(p['nodes']),'relation_count':len(p['rels']),'added_structural_rows':added,'structural_rows':8439026+added,'model_byte_upper_bound':raw_upper,'working_disk_upper_bound':raw_upper*2+2*1024**3,'memory_limit_bytes':3*1024**3,'estimated_runtime_seconds':[180,1200],'runtime_basis':'retained 1.8 GB metadata scan ~35 seconds; conservative additional encoding/join work, not a throughput benchmark','pair_rows_enumerated':0,'counts':counts}

def token_rows(p,skip=0):
 for start,sid,ctx,seq in p['append']:
  if skip>=len(seq):skip-=len(seq);continue
  begin=skip;skip=0
  for pos in range(begin,len(seq)):
   rec,parent=seq.at(pos);idx=start+pos
   yield {'index':idx,'id':'I164-ACCOUNTED-TOKEN-'+str(idx),'surface':sid,'context':ctx,'record':rec,'exposure':'UNKNOWN','reuse':'NONE','arbitrary':True,'symbolic_digest':H(b'ARBITRARY')}
def edge_rows(p,skip=0):
 for k,r in enumerate(p['rels']):
  count=p['counts'][k]
  if skip>=count:skip-=count;continue
  need(count%2==0,'context symmetry')
  for ctx in CONTEXTS:
   if skip>=count//2:skip-=count//2;continue
   for i,j in pairs(p,k,ctx):
    if skip:skip-=1;continue
    yield [i,j,k+1,r['relation']]

def segmented(name,rows,binding,stop_segments=None):
 d=R/'segments'/name;d.mkdir(parents=True,exist_ok=True);state=d/'state.json'
 s=load(state) if state.exists() else {'binding':binding,'segments':[],'rows':0,'complete':False}
 need(s['binding']==binding,'changed construction identity')
 for seg in s['segments']:need(sha(d/seg['file'])==seg['sha256'],'corrupt committed segment')
 if s['complete']:return s
 it=iter(rows(s['rows']))
 while True:
  chunks=[]
  for _ in range(100000):
   try:chunks.append(W(next(it))+b'\n')
   except StopIteration:break
  if not chunks:s['complete']=True;save(state,s);return s
  need(shutil.disk_usage(R).free>2*1024**3,'disk stop: committed segments retained')
  raw=b''.join(chunks);filename=f'{len(s["segments"]):06}.jsonl.gz';packed=gzip.compress(raw,compresslevel=1,mtime=0);atomic(d/filename,packed)
  s['segments'].append({'file':filename,'rows':len(chunks),'bytes':len(packed),'raw_bytes':len(raw),'sha256':H(packed),'raw_sha256':H(raw)});s['rows']+=len(chunks);save(state,s)
  if len(s['segments'])%10==0:print(json.dumps({'stage':name,'committed_rows':s['rows']}),flush=True)
  if stop_segments is not None and len(s['segments'])>=stop_segments:return s

def assemble(p,binding,states):
 out=R/'candidate/model.json.gz';tmp=out.with_suffix('.pending');h=hashlib.sha256();eq=dict(p['pm'].small('equality_stream'));n=4510432;a=p['token_count']-n
 eq.update(rows=eq['rows']+n*a+a*(a-1)//2,sha256=None);eq['bytes']=len(b'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1\n')+8*eq['rows']
 with gzip.open(tmp,'wb',compresslevel=1) as f:
  def put(b):f.write(b);h.update(b)
  put(b'{')
  for k in ['actor_graph_policy','equality_stream','relations','structural_edges','surfaces','tokens']:
   if k!='actor_graph_policy':put(b',')
   put(W(k)+b':')
   if k=='actor_graph_policy':put(W(p['pm'].small(k)));continue
   if k=='equality_stream':put(W(eq));continue
   put(b'[');p['pm'].copy(k,f,h,True)
   if k in ('surfaces','relations'):
    start=p['old_node_n'] if k=='surfaces' else p['old_rel_n']
    for row in p['nodes' if k=='surfaces' else 'rels'][start:]:put(b','+W(row))
   else:
    for seg in states[k]['segments']:
     with gzip.open(R/'segments'/k/seg['file'],'rb') as g:
      for line in g:put(b','+line.rstrip(b'\n'))
   put(b']')
  put(b'}\n');raw_size=f.tell()
 with tmp.open('rb') as fd:os.fsync(fd.fileno())
 os.replace(tmp,out)
 result={'model_sha256':h.hexdigest(),'model_bytes':raw_size,'compressed_bytes':out.stat().st_size,'compressed_sha256':sha(out),'tokens':p['token_count'],'structural_edges':8439026+states['structural_edges']['rows'],'equality_stream':eq,'textual_stream_sha256':None,'binding':binding,'actual_admission':False}
 save(R/'candidate/identity.json',result);return result

def main():
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['preflight','build']);ap.add_argument('--parent',required=True);ap.add_argument('--base',required=True);ap.add_argument('--stop-segments',type=int);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3));start=time.monotonic()
 need(sha(a.parent)=='8aeab1b1990df99f2e2df1b6502a1f9f24a1cd06618d1ba3823d40419c96d189','parent identity');need(sha(a.base)=='dd946419e4fd4c657a0a0d663b145e958ddf3c4957bf006b94b5c3f7ec96e74d','base identity')
 print('Verified parent/base; preparing indexed metadata',flush=True);p=prepare(a.parent,a.base);e=estimate(p);p['counts']=e['counts'];print('Exact structural cardinalities established',flush=True);save(R/'results/expansion-preflight.json',e)
 binding=H(W({'parent':sha(a.parent),'base':sha(a.base),'code':{n:sha(R/n) for n in ['code/expand_candidate.py','code/allowances.py','code/executor_accounted.py','prior-code/executor_records.py','prior-code/common.py','prior-code/model_kernel/catalog.py','prior-code/model_kernel/expand.py']},'sources':{str(x.relative_to(R)):sha(x) for x in sorted((R/'sources').rglob('*.tsv'))},'fields':sha(R/'retained/registers/fields.json'),'approval':load(R/'records/approval.json')}))
 save(R/'records/expanded-contract.json',p['contract']);save(R/'records/added-fields.json',p['new_fields']);save(R/'records/relation-rules.json',[{'relation':r,'rule':rule,'detail':d} for r,rule,d in zip(p['rels'],p['rules'],p['details'])])
 samples=[]
 for kind,iterator in [('tokens',token_rows(p)),('late_tokens',token_rows(p,e['added_tokens']-1000)),('structural',edge_rows(p)),('late_structural',edge_rows(p,e['added_structural_rows']-1000))]:
  import itertools
  raw=b''.join(W(x)+b'\n' for x in itertools.islice(iterator,1000));packed=gzip.compress(raw,compresslevel=1,mtime=0);samples.append({'kind':kind,'sample_bytes':len(raw),'compressed_bytes':len(packed),'ratio':len(packed)/len(raw),'conformance_evidence':False})
 save(R/'results/compression-preflight.json',{'samples':samples,'planning_compressed_ratio':0.15,'estimated_peak_bytes':int(e['model_byte_upper_bound']*0.15*2)+2*1024**3,'hard_free_disk_stop_bytes':2*1024**3,'no_output_stream_materialization':True})
 if a.action=='preflight':print(json.dumps({k:v for k,v in e.items() if k!='counts'}));return
 need(shutil.disk_usage(R).free>10*1024**3,'insufficient compressed construction planning space')
 ts=segmented('tokens',lambda skip:token_rows(p,skip),binding,a.stop_segments)
 if not ts['complete']:print('PAUSED token segments');return
 es=segmented('structural_edges',lambda skip:edge_rows(p,skip),binding,a.stop_segments)
 if not es['complete']:print('PAUSED structural segments');return
 need(ts['rows']==e['added_tokens'] and es['rows']==e['added_structural_rows'],'expansion row count mismatch')
 result=assemble(p,binding,{'tokens':ts,'structural_edges':es});result.update(seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);save(R/'results/construction.json',result);print(json.dumps(result))
if __name__=='__main__':main()
