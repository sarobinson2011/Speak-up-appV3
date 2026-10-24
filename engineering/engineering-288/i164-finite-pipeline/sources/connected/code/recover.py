"""Exact-byte recovery of declared predecessors; no recovered procedures execute."""
import argparse, io, json, tarfile, traceback, zipfile
from pathlib import Path, PurePosixPath
import connect as m

def pin(size,sha):return {'bytes':size,'sha256':sha}
EXTERNAL={
'inputs':pin(45747644,'94791c65c3502d85fc452c0e9c100391f5d0199f7690462e92b91c1a600caa8b'),
'consumer':pin(6636286,'cb88382f2e16ee9fbd44a30f05033ef12c6e467b838784fa25fa16b88bc5e5f5'),
'ledger_review':pin(15248500,'9d1182af3d1121037380d5ba4a1f6989a674e82ecbfb3514d880d4d4e8fa3dd4'),
'draft':pin(13820246,'f26d73237597ad2998735d6c71810f341b9bdbbf705497b0360f2ae59fbd6ec3'),
'discriminator':pin(9280888,'a5a928a1d45e792059c70bc727a58fd4186865518fe158b9055fe4cdf861b218'),
'unknown':pin(31900862,'5c4f1f9960493de9c3c0ec8c80fda2da0b75b5fb70c079149f422f3d737c3aff')}
def put(p,raw):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(raw)
def unpack(raw,dest,expected):
 m.same(m.ident(raw),expected,'RECOVERY-ARCHIVE-PIN');p=dest.parent/(dest.name+'.zip');put(p,raw)
 files=m.archive(p,expected);m.need(not dest.exists(),'DESTINATION-EXISTS');dest.mkdir()
 for n,b in files.items():put(dest/n,b)
 m.tree(dest,m.members(files));return files,p

def recover(locations,dest):
 dest=Path(dest).absolute();m.need(not dest.exists() and not str(dest).startswith('/tmp/'),'NEW-PERSISTENT-RECOVERY');dest.mkdir(parents=True)
 try:
  m.same(sorted(locations),sorted(EXTERNAL),'REQUIRED-DEPENDENCIES')
  # Verify every external archive before recovering any source tree.
  for name,identity in EXTERNAL.items():m.archive(locations[name],identity)
  a={};paths={}
  for name,identity in EXTERNAL.items():a[name],paths[name]=unpack(m.read(locations[name]),dest/name,identity)
  ledger_raw=a['ledger_review']['inputs/I164-finite-ledger.zip'];a['ledger'],paths['ledger']=unpack(ledger_raw,dest/'ledger',m.pins()['archives']['ledger'])
  count_raw=a['inputs']['inputs/Engineering-288C-I164-evidence-count-receipts.zip'];a['counts'],paths['counts']=unpack(count_raw,dest/'counts',pin(3789194,'d22b07f1d39bd45c4c306790ec83a40de1cf316e7ff57ad62ec2d9ee55a7ca32'))
  so=a['draft']['inputs/source-only-integration.zip'];unpack(so,dest/'draft/source-only',pin(9569533,'7f58a377120157b379058f3aa4642de14625eda243792b8a5b681da9f969596d'))
  # Archive transport is outside the strict 163-member draft tree.
  (dest/'draft/source-only.zip').rename(dest/'source-only-transport.zip')
  unknown_raw=a['unknown']['inputs/Engineering-Anchor2-I164-unknown-method-correction.zip']
  u,_=unpack(unknown_raw,dest/'unknown-correction',pin(31116309,'9abf1042baae87bb0fb217aa6b88e30a6b9d10ae31106f3193125dfde016c14e'))
  disc_raw=a['discriminator']['inputs/Engineering-288C-I164-discriminator-type-correction.zip']
  d,_=unpack(disc_raw,dest/'discriminator-correction',pin(9148223,'910e80c30369ce8d63dca14f4f77f8193bdc646e9e58ad42a92bb34f397da358'))
  transport=m.parse(u['provenance/baseline-transport.json']);raw=u['inputs/baseline-root.tar.xz'];m.same(m.ident(raw),{k:transport[k] for k in ('bytes','sha256')},'BASELINE-TRANSPORT')
  old=m.parse(u['provenance/predecessor-members.json']);current=m.parse(u['provenance/current-root-members.json']);changes=m.parse(u['CHANGED-IDENTITIES.json']);root=dest/'candidate';root.mkdir()
  with tarfile.open(fileobj=io.BytesIO(raw),mode='r:xz') as t:
   entries=t.getmembers();m.need(len(entries)==len(old) and {i.name for i in entries}==set(old),'BASELINE-MEMBERSHIP')
   for i in entries:
    p=PurePosixPath(i.name);m.need(i.isfile() and not p.is_absolute() and '..' not in p.parts,'BASELINE-ENTRY')
    original=t.extractfile(i).read();m.same(m.ident(original),old[i.name],'BASELINE-BYTES')
    new=u['overlay/'+i.name] if i.name in changes else original;m.same(m.ident(new),current[i.name],'UNKNOWN-OVERLAY');put(root/i.name,new)
  m.tree(root,current);m.same(current,m.parse(d['provenance/predecessor-members.json']),'ORDERED-PREDECESSOR')
  for n,v in m.parse(d['CHANGED-IDENTITIES.json']).items():
   p=root/n;m.same(m.ident(m.read(p)),v['before'],'DISCRIMINATOR-BEFORE');raw=d['overlay/'+n];m.same(m.ident(raw),v['after'],'DISCRIMINATOR-AFTER');p.write_bytes(raw)
  m.tree(root,m.parse(a['inputs']['provenance/candidate-members.json']));m.tree(dest/'draft',m.parse(a['inputs']['provenance/draft-members.json']))
  config={name+'_archive':str(paths[name]) for name in ('inputs','consumer','ledger','counts')}
  config.update({name+'_root':str(dest/name) for name in ('inputs','consumer','ledger','counts')})
  config.update(candidate=str(root),draft=str(dest/'draft'),bundle=str(dest/'inputs/outputs/bundle.json'),model=str(dest/'consumer/outputs/native.json'),saved_ledger=str(dest/'ledger/outputs/ledger.json'))
  basis=m.preflight(config);m.write(dest/'config.json',config);m.write(dest/'recovery-result.json',{'status':'PASS exact recovery; no validator execution','basis':basis})
  print('PASS exact recovered inputs. Config:',dest/'config.json')
 except BaseException:
  (dest/'failure.txt').write_text(traceback.format_exc());raise
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--locations',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();recover(m.load(a.locations),a.output)
