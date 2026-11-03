"""Read each current evidence file once; preserve an explicitly partial snapshot."""
from pathlib import Path
import sys,zipfile,stat,datetime,json
sys.path.insert(0,str(Path(__file__).parent))
from integrity import BASE,enc,ident,file_ident,archive
out=Path(sys.argv[1]);assert not out.exists();manifest={}
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 def put(name,raw):
  info=zipfile.ZipInfo(name);info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,raw);manifest[name]=ident(raw)
 for sub in ('code','results','processes','failures'):
  for p in sorted((BASE/sub).rglob('*')):
   if p.is_file() and not p.is_symlink() and p.suffix!='.pyc':put('review/'+p.relative_to(BASE).as_posix(),p.read_bytes())
 put('PARTIAL-CHECKPOINT.json',enc({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PARTIAL LIVE EVIDENCE SNAPSHOT; not an inferred completion','prerun':{'library_file_id':'libfile_7f126a5fce6c81919621b2633e5497c8','bytes':193145485,'sha256':'0172a318cf0f03bc5158b5d97dae71a4cbe585de7f309a02c07118b76945f678'},'input_sha256':'da1b070d16deadcb9e4ff741f76b370bcf62a2353787bde7ae1a44badd9bc173','snapshot_semantics':'Each file read once; cross-file observations may be at different times. No missing stream reconstructed. Final reconciliation remains required.','retry_authorized':False,'admission_disabled':True}))
 info=zipfile.ZipInfo('MANIFEST.json');info.external_attr=(stat.S_IFREG|0o644)<<16;z.writestr(info,enc(manifest))
pin=file_ident(out);archive(out,pin,len(manifest)+1).close();print(json.dumps({'path':str(out),**pin,'entries':len(manifest)+1,'CRC_membership_hashes':'PASS'}),flush=True)
