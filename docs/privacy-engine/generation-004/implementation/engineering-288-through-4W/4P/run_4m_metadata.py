"""Metadata-only complete retained-token coverage; never opens pair/link rows."""
import json,hashlib,zipfile,time,sys,resource,os
from pathlib import Path
from metadata_catalog.core import DiskMap,write_directory,acquire,sha,wire
from v4_ingest.records import require
from integrated_auth.collector import implementation
ROOT=Path(__file__).resolve().parent
P=ROOT/'work/4M-metadata'
B={'source_id':'CP4M-SYNTHETIC-METADATA-ONLY','source_sha256':hashlib.sha256(b'CP4M metadata oracle').hexdigest(),'model_sha256':'08d6e7fb1e0cf37cc7effa76b50eaff0459abc158d9c6f0da52c6c58372b14f1','contract_sha256':sha(ROOT/'rebinding/selected-contract.json'),'profile_sha256':hashlib.sha256(b'NO REAL PROFILE').hexdigest(),'phase':'PRE-COMMITMENT','attempt':1,'mapping_digest':hashlib.sha256(b'LAB metadata').hexdigest()}
N=426984

def generate():
 from ledger_kernel.retained import archive
 P.mkdir(parents=True,exist_ok=True);db=DiskMap(P/'required.sqlite');files=DiskMap(P/'source-oracle.sqlite');refs=DiskMap(P/'reference-oracle.sqlite');count=0
 with zipfile.ZipFile(archive('2')) as z:
  prefix='Engineering-288-checkpoint-2/';manifest=json.loads(z.read(prefix+'PACKAGE-MANIFEST.json'));shards=[e for e in manifest['files'] if e['path'].startswith('results/expansion/tokens/') and e['path'].endswith('.jsonl')]
  for e in sorted(shards,key=lambda r:r['path']):
   h=hashlib.sha256();n=0
   with z.open(prefix+e['path']) as stream:
    for raw in stream:
     h.update(raw);n+=len(raw);t=json.loads(raw);k=t['id'];db.add(k,{a:t[a] for a in ('index','context','record','surface')})
     v=hashlib.sha256(('METADATA-ONLY:'+k).encode()).hexdigest();refs.add(k,{'owner_source_id':B['source_id'],'source_sha256':B['source_sha256'],'source_anchor':'TOKEN-'+str(t['index']),'material_sha256':v});files.add(v,{'path':'unacquired/'+v,'bytes':0,'sha256':v});count+=1
   assert n==e['bytes'] and h.hexdigest()==e['sha256'];print(json.dumps({'stage':'retained-token-metadata','rows':count}),file=sys.stderr,flush=True)
 assert count==N
 for d in (db,files,refs):d.commit()
 entries={'materials':write_directory(P/'materials.jsonl','materials',B,files.items(),N),'occurrence_bindings':write_directory(P/'occurrences.jsonl','occurrence_bindings',B,refs.items(),N)}
 (P/'entries.json').write_bytes(wire(entries));return {'required_tokens':count,'directory_bytes':sum(e['bytes'] for e in entries.values()),'required_index_sha256':sha(db.path),'entries':entries,'shards_verified':len(shards)}

def validate():
 entries=json.loads((P/'entries.json').read_bytes());db=DiskMap(P/'required.sqlite');oracle=DiskMap(P/'reference-oracle.sqlite');files=DiskMap(P/'source-oracle.sqlite');checks={};job={'implementation':implementation(),'binding':B,'required_index':sha(db.path)}
 for kind,expected in [('materials',files),('occurrence_bindings',oracle)]:
  e=entries[kind];count=0
  def check(k,v):
   nonlocal count
   require(k in expected and expected[k]==v,'independent exact metadata reference join')
   if kind=='occurrence_bindings':require(k in db and v['owner_source_id']==B['source_id'] and v['source_sha256']==B['source_sha256'],'required token/source ownership')
   count+=1
   if count%100000==0:print(json.dumps({'stage':kind,'rows':count}),file=sys.stderr,flush=True)
  x=acquire(P/e['path'],e,kind,B,P/'indexes',b'm'*32,job,validate=check)
  # Membership + unique primary keys + exact required cardinality; independent
  # oracle iterated too. No counts-only claim or probabilistic sample.
  assert len(x)==len(expected)==N
  for k in db:
   if kind=='occurrence_bindings':assert k in oracle
  checks[kind]={'complete_metadata_rows':len(x),'new_rows_checked':count,'database_bytes':x.path.stat().st_size,'database_sha256':sha(x.path)}
 return {'complete_metadata_coverage':True,'checks':checks,'model_token_count':N}

def scheduler():
 from metadata_catalog.receipts import freeze
 from recovery_schedule.state import Scheduler
 from link_recovery.cli import create_key
 key=P/'key'
 if not key.exists():create_key(key)
 s=Scheduler(P/'schedule',key,{'implementation':implementation(),'binding':B});inputs=DiskMap(P/'inputs.sqlite');prereqs=DiskMap(P/'prereqs.sqlite')
 # Metadata-only prerequisite identities, explicitly no executed-stage claim.
 refs=DiskMap(P/'reference-oracle.sqlite')
 for token,ref in refs.items():inputs[token]=ref['material_sha256'];prereqs['metadata:'+token]=ref['material_sha256']
 inputs.commit();prereqs.commit();print(json.dumps({'committed_inputs':len(inputs),'committed_prerequisites':len(prereqs)}),file=sys.stderr,flush=True);assert len(inputs)==len(prereqs)==N
 s.save('metadata-capacity-only',{'files':inputs},{'metadata_only':True},True,prereqs)
 receipt=s.root/(s.name('metadata-capacity-only')+'.json');s.close();s=Scheduler(P/'schedule',key,{'implementation':implementation(),'binding':B});r=s.read('metadata-capacity-only')
 assert len(r['inputs']['files'])==len(r['prerequisites'])==N
 # Streaming ordered equality avoids repeated random opens in this size test.
 assert all(a==b for a,b in zip(r['inputs']['files'].items(),inputs.items()))
 assert all(a==b for a,b in zip(r['prerequisites'].items(),prereqs.items()))
 return {'input_rows':N,'prerequisite_rows':N,'receipt_bytes':receipt.stat().st_size,'receipt_cap_bytes':1048576,'synthetic_prerequisites_executed':False,'catalogs_reopened_and_compared':True}
if __name__=='__main__':
 mode=sys.argv[1];start=time.monotonic();result=globals()[mode]();result.update(result='PASS',seconds=time.monotonic()-start,child_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,full_pair_or_link_stream_processed=False,actual_values_acquired=False,authentication_established=False,qualification_established=False,profile_admitted=False)
 (ROOT/('results/4M-metadata-'+mode+'.json')).write_bytes(wire(result));print(json.dumps(result))
