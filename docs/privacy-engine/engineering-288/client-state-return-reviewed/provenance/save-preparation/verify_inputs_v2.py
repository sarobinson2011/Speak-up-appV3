"""Archive/read-only identity check only: never import candidate code."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, stat, zipfile
B=Path(__file__).resolve().parents[1]
R=B/'git-client-state';R.mkdir(exist_ok=True)
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(x):return (json.dumps(x,sort_keys=True,indent=2)+'\n').encode()
def verify(raw,expected,count):
 assert ident(raw)==expected
 z=zipfile.ZipFile(io.BytesIO(raw));infos=z.infolist();names=[i.filename for i in infos]
 assert len(names)==count and len(set(names))==count and z.testzip() is None
 for i in infos:
  n=i.filename;p=PurePosixPath(n)
  assert not p.is_absolute() and p.as_posix()==n and all(x not in ('','..','.') for x in p.parts)
  assert not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
 manifest=json.loads(z.read('MANIFEST.json'));members=manifest.get('members',manifest)
 assert set(names)==set(members)|{'MANIFEST.json'}
 for n,pin in members.items():assert ident(z.read(n))==pin,(n,pin)
 return z,{'identity':ident(raw),'entries':count,'manifest':ident(z.read('MANIFEST.json')),'manifested_files':len(members),'CRC_safe_unique_regular_membership_and_hashes':'PASS'}
reviewraw=(B/'upload/Formal-Lab6-I164-client-state-return-correspondence-independent-review(1).zip').read_bytes()
review,rv=verify(reviewraw,{'bytes':60792892,'sha256':'a8762d3b81d5f5cbedfb95e5afd8d2c083143ed759f88f2b550cfebfb6de4bf6'},91)
targetraw=review.read('input/I164-client-state-return-correspondence-1.zip')
target,tv=verify(targetraw,{'bytes':61624841,'sha256':'0ae24141a77f42eb96ed0f8d144f612d7a8045e04f7aa47dcaa8d1750f886907'},1688)
scratch=B/'I164-client-state-return-correspondence-1.zip'
scratch_id=ident(scratch.read_bytes())
root=R/'target';root.mkdir()
for n in target.namelist():
 p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(target.read(n))
names=set(target.namelist());dirs={str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'}
dest=R/'review';dest.mkdir()
for n in review.namelist():
 if n.startswith('input/'):continue
 p=dest/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(review.read(n))
prior=json.loads((B/'git-client-state-tools/prior-save-receipt.json').read_bytes())
assert prior['status']=='PASS' and prior['push_status']=='CONFIRMED'
assert prior['commit']==prior['remote_main']=='a8e9f0c022b0e437b83ecf4293fc486ded1aed15'
assert prior['selection']['manifest']=={'bytes':71661,'sha256':'d456335eb58104bc61ac359ccc5e9d904a72b570824a2cf8b3e57b8479780cf3'}
report={'independent_review':rv,'reviewed_target':tv,'local_target_exact_files':len(names),'local_target_exact_directories':len(dirs),'prior_save_receipt':ident((B/'git-client-state-tools/prior-save-receipt.json').read_bytes()),'prior_commit':prior['commit'],'scratch_archive_mismatch_preserved':scratch_id,'selected_root':'exact embedded reviewed target','new_tests_reviews_sessions_database_operations':0}
(R/'verified-inputs.json').write_bytes(enc(report));print(json.dumps(report,indent=2))
review.close();target.close()
