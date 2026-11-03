"""Preserve exact available prefixes/final files; never manufacture missing records."""
from pathlib import Path
import sys,datetime,json,hashlib,zipfile,stat,collections
W=Path(__file__).resolve().parents[1]
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def main():
 tag=sys.argv[1];assert tag.replace('-','').isalnum();name='I164-line174-NEW-replacement-'+tag+'.zip';target=W/name;assert not target.exists();data={};observations=[]
 for folder in ('processes','results'):
  for p in sorted((W/folder).rglob('*')):
   if not p.is_file():continue
   a=p.stat();raw=p.read_bytes();b=p.stat();n=p.relative_to(W).as_posix();data[n]=raw;observations.append({'path':n,'identity':ident(raw),'unchanged_size_mtime_during_read':a.st_size==b.st_size and a.st_mtime_ns==b.st_mtime_ns,'mtime_ns':b.st_mtime_ns})
 groups=[]
 for n in ('replacement-source','replacement-source-corrected','replacement-public'):
  rp='results/'+n+'/';pp='processes/'+n+'/';res=json.loads(data[rp+'RESULT.json']) if rp+'RESULT.json' in data else None;ex=json.loads(data[pp+'exit.json']) if pp+'exit.json' in data else None
  result=[] if res is None else res['rows'];progress=[];stdout=[];malformed=[]
  for key,dest,prefix in ((rp+'progress.jsonl',progress,b''),(pp+'stdout.log',stdout,b'CHECK ')):
   for i,line in enumerate(data.get(key,b'').splitlines(),1):
    if not line.startswith(prefix):continue
    try:dest.append(json.loads(line[len(prefix):]))
    except Exception:malformed.append({'path':key,'line':i,'identity':ident(line)})
  individual=[json.loads(raw) for key,raw in sorted(data.items()) if key.startswith(rp+'rows/') and key.endswith('.json')]
  streams={'RESULT':result,'progress':progress,'stdout':stdout,'individual':individual};maps={k:{row['ordinal']:row for row in rows} for k,rows in streams.items()};ords=set().union(*(set(x) for x in maps.values()));agreed=[i for i in sorted(ords) if all(i in x for x in maps.values()) and all(x[i]==maps['RESULT'][i] for x in maps.values())]
  group={'name':n,'result_status':None if res is None else res['result'],'exit':ex,'counts':{k:len(v) for k,v in streams.items()},'kinds':{k:dict(collections.Counter(x['result'] for x in v)) for k,v in streams.items()},'four_way_agreement_ordinals':agreed,'missing_ordinals':{k:sorted(ords-set(v)) for k,v in maps.items()},'malformed':malformed,'no_reconstruction':True}
  capture=json.loads(data[pp+'capture.json']) if pp+'capture.json' in data else None;stream_checks={}
  if capture is not None:
   for stream in ('stdout','stderr'):
    parts=capture['chunks'][stream];chunk_bytes=[data[pp+x['path']] for x in parts];joined=b''.join(chunk_bytes)
    stream_checks[stream]={'all_chunk_hashes_match':all(ident(b)==x['identity'] for b,x in zip(chunk_bytes,parts)),'joined_identity':ident(joined),'capture_manifest_matches':ident(joined)==capture['streams'][stream],'captured_file_matches':joined==data.get(pp+stream+'-captured.bin'),'append_log_matches':joined==data.get(pp+stream+'.log'),'exit_stream_matches':ex is not None and ident(joined)==ex['streams'][stream]}
  group['stream_checks']=stream_checks
  group['ordinal_sequences_valid']={k:[x['ordinal'] for x in rows]==list(range(1,len(rows)+1)) for k,rows in streams.items()}
  group['completed_and_fully_corroborated']=res is not None and res['result']=='PASS' and ex is not None and ex['exit']==0 and not ex['timed_out'] and all(v==result for v in streams.values()) and not malformed and all(group['ordinal_sequences_valid'].values()) and bool(stream_checks) and all(v for s in stream_checks.values() for k,v in s.items() if k!='joined_identity')
  groups.append(group)
 public=data.get('results/replacement-public/actual-public-result.json');entry={'format':'I164-NEW-REPLACEMENT-RESULT-SNAPSHOT-1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tag':tag,'active_checkpoint':json.loads((W/'PRERUN2-IDENTITY.json').read_bytes()),'active_checkpoint_library_id':'libfile_PENDING','groups':groups,'actual_public_result':None if public is None else json.loads(public),'sampling':observations,'missing_records_remain_missing':True,'independent_review':'PENDING','actual_admission':False,'environment_qualification':json.loads((W/'provenance/execution-environment-qualification.json').read_bytes())}
 receipt=W/'provenance/active-library-save.json'
 if receipt.exists():entry['active_checkpoint_library_id']=json.loads(receipt.read_bytes())['library_file_id']
 data['CHECKPOINT.json']=enc(entry)
 data['RECOVERY.txt']=b'This records available NEW replacement execution evidence. Recover code and fixtures from the exact pre-run2 checkpoint identified in CHECKPOINT.json. A partial snapshot is not completion. Preserve all original records, qualifiers and missing records. No automatic retry, test replay, Git save, database/session operation or admission.\n'
 for p in (W/'provenance').glob('*.json'):data['provenance/'+p.name]=p.read_bytes()
 data['HISTORY.txt']=(W/'HISTORY.txt').read_bytes();data['tools/snapshot.py']=Path(__file__).read_bytes()
 manifest={n:ident(b) for n,b in data.items()}
 with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n,b in sorted(data.items()):
   zi=zipfile.ZipInfo(n,(2026,11,3,0,0,0));zi.create_system=3;zi.external_attr=(stat.S_IFREG|0o644)<<16;zi.compress_type=zipfile.ZIP_DEFLATED;z.writestr(zi,b)
  zi=zipfile.ZipInfo('MANIFEST.json',(2026,11,3,0,0,0));zi.create_system=3;zi.external_attr=(stat.S_IFREG|0o644)<<16;zi.compress_type=zipfile.ZIP_DEFLATED;z.writestr(zi,enc(manifest))
 with zipfile.ZipFile(target) as z:
  assert len(z.namelist())==len(set(z.namelist()))==len(manifest)+1 and z.testzip() is None
  for n,pin in manifest.items():assert ident(z.read(n))==pin
 out={'name':name,**ident(target.read_bytes()),'entries':len(manifest)+1,'groups':groups};(W/(tag+'-IDENTITY.json')).write_bytes(enc(out));print(json.dumps({k:v for k,v in out.items() if k!='groups'},indent=2));print(json.dumps(groups,indent=2))
if __name__=='__main__':main()
