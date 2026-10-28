"""Read saved archives and prepare exact compact members; no reviewed code runs."""
from pathlib import Path,PurePosixPath
import hashlib,io,json,stat,zipfile
R=Path(__file__).resolve().parent
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def unpack(raw,pin,count):
 assert ident(raw)==pin
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  infos=z.infolist();names=[i.filename for i in infos]
  assert len(infos)==len(set(names))==count and z.testzip() is None
  for i in infos:
   p=PurePosixPath(i.filename)
   assert not p.is_absolute() and '..' not in p.parts and p.as_posix()==i.filename and not i.is_dir()
   assert stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
  data={n:z.read(n) for n in names};manifest=json.loads(data['MANIFEST.json']);members=manifest.get('members',manifest)
  assert set(data)==set(members)|{'MANIFEST.json'}
  for n,v in members.items():assert ident(data[n])==v,n
 return data
reviewpin={'bytes':42069714,'sha256':'d69cd5939e0fc051adee4f270dd0148d4aecf5cfef2ecae65b3ec33cedf4f31c'}
inputpin={'bytes':42330497,'sha256':'6b486b1ca0c49da010face18132507020a07f3db84602d62a7c75af0305caa8e'}
v=unpack((R.parent/'upload/Formal-Lab6-I164-handle-return-correspondence-independent-review(1).zip').read_bytes(),reviewpin,142)
raw=v['input/I164-handle-return-correspondence-1.zip'];c=unpack(raw,inputpin,1088)
assert raw==(R.parent/'I164-handle-return-correspondence-1.zip').read_bytes()
cp=json.loads(v['CHECKPOINT.json']);assert all(cp['input'][k]==inputpin[k] for k in inputpin)
for n,p in cp['identities']['current_code'].items():assert ident(c['code/'+n])==p
assert ident(c['results/handle-correspondence.json'])==cp['identities']['new_receipt']
for family,count in [('primary',219),('recovered',133)]:
 result=json.loads(v['independent-'+family+'/RESULT.json']);assert result['result']=='PASS' and result['assertions']==len(result['checks'])==count
assert json.loads(v['cli-recovered/RESULT.json'])['returncode']==0
for family,count in [('primary',101),('relations',21),('recovered',101)]:
 result=json.loads(c['results/'+family+'/RESULT.json']);assert result['result']=='PASS' and result['checks']==len(result['rows'])==count
assert json.loads(c['results/fresh/RESULT.json'])['exit_code']==0
assert json.loads(v['failures/public-key-lookup-attempt-1/PRESERVATION.json'])['completed_before_failure']==7
assert json.loads(v['failures/interrupted-execution-attempt-2/PRESERVATION.json'])['progress_rows']=={'independent-primary':179,'independent-recovered':4}
omissions={}
for label,data in [('handle',c),('review',v)]:
 target=R/'inputs'/label;target.mkdir(parents=True,exist_ok=False)
 omitted={}
 for n,b in data.items():
  if (label=='handle' and n.startswith('retained/')) or (label=='review' and n.startswith('input/')):
   omitted[n]=ident(b);continue
  assert len(b)<2000000 and Path(n).suffix not in ('.zip','.db','.sqlite','.bin')
  if label=='handle':assert (R.parent/'handle-return'/n).read_bytes()==b,n
  p=target/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 omissions[label]={'count':len(omitted),'members':omitted,'retained_in_exact_external_review':True}
info={'review':dict(reviewpin,entries=142,manifested_hashes=141),'implementation':dict(inputpin,entries=1088,manifested_hashes=1087),'verification':'read-only CRC, safe unique regular membership, exact manifest membership and hashes; no candidate or review execution','compact_omissions_retained_in_exact_external_archive':omissions,'completed_work_rerun':False}
(R/'review-verification.json').write_bytes(enc(info))
print(json.dumps({k:v for k,v in info.items() if k!='compact_omissions_retained_in_exact_external_archive'},indent=2))
