"""Immutable review checkpoint packaging; no candidate execution."""
from pathlib import Path
import sys,zipfile,hashlib,json,stat
sys.path.insert(0,str(Path(__file__).parent))
from integrity import BASE,INPUT,enc,file_ident,archive
output=Path(sys.argv[1]);include_input='--input' in sys.argv[2:];assert not output.exists();manifest={}
with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 def add(n,p):
  assert p.is_file() and not p.is_symlink();manifest[n]=file_ident(p);z.write(p,n,compress_type=zipfile.ZIP_STORED if p.suffix=='.zip' else zipfile.ZIP_DEFLATED)
 if include_input:add('input/I164-line174-NEW-replacement-construction-1.zip',INPUT)
 for p in sorted(BASE.rglob('*')):
  if p.is_file() and not p.is_relative_to(BASE/'saves') and p.suffix!='.pyc':add('review/'+p.relative_to(BASE).as_posix(),p)
 zi=zipfile.ZipInfo('MANIFEST.json');zi.external_attr=(stat.S_IFREG|0o644)<<16;z.writestr(zi,enc(manifest))
pin=file_ident(output);z=archive(output,pin,len(manifest)+1);z.close();print(json.dumps({'path':str(output),**pin,'entries':len(manifest)+1,'manifested_hashes':len(manifest),'CRC_safe_membership_hashes':'PASS'}),flush=True)
