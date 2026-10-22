"""Bounded host probe. Uses public gates and only a new tempfile directory.
Preserves records and failures. Does not install, repair pins, reset or serve.
"""
import argparse,hashlib,importlib.metadata,json,os,re,subprocess,sys,tempfile,traceback
from pathlib import Path
def ident(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
ap=argparse.ArgumentParser();ap.add_argument('--package',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--draft',type=Path,required=True);ap.add_argument('--environment-record',type=Path);ap.add_argument('--lock',type=Path);ap.add_argument('--compatibility-record',type=Path);ap.add_argument('--worker',choices=['create','reopen']);ap.add_argument('--temporary-root',type=Path);a=ap.parse_args()
a.package=a.package.resolve();a.candidate=a.candidate.resolve();a.draft=a.draft.resolve()
assert ident(a.package/'code/lab_bootstrap.py')['sha256']=='b2ce7f0fdf9aabb578da7330a9987a34b7c76e1fe1f543f913ba759aededc2f6','UNREVIEWED-LAUNCHER'
sys.path.insert(0,str(a.package/'code'));import lab_bootstrap as b
from lock_contract import parse_lock
from dependency_check import check as check_dependencies
from derive_draft import ident as byte_ident
EXPECTED=json.loads((Path(__file__).resolve().parents[1]/'provenance/host-addendum/HOST-PROBE-RESULT.json').read_bytes())
if a.worker:
 root=a.temporary_root.resolve();assert root.name.startswith('I164-bootstrap-review-') and root.parent==Path(tempfile.gettempdir()).resolve(),'TEMPORARY-ROOT-ONLY'
 with b.session(a.candidate,a.draft,root/'runtime',root/'session',create=a.worker=='create') as g:
  state=g.state();assert state['seq']==0 and state['head']=='0'*64 and g.status()['actual_admission'] is False
  assert {n for n in dir(g) if not n.startswith('_')}=={'state','status','handle'}
  if a.worker=='reopen':
   import authority
   cfg=b.read(a.package/'laboratory-configuration.json')['config'];q={'version':authority.VERSION,'binding':state['binding'],'pilot':cfg['pilot'],'session':cfg['session'],'principal':'executor','challenge':'7'*64,'expected':state['head'],'method':'head','u':'TEMP-HOST-PROBE','body':{}}
   packet=authority.enc({'request':q,'signature':authority.sig('executor',q)})
   reply=json.loads(g.handle(packet));assert reply['response']['ok'] is True and reply['response']['data']==state and g.state()==state
 assert g.status()['phase']=='CLOSED' and not (root/'session/ACTIVE.json').exists()
 print('PASS public temporary '+a.worker+' and confirmed close');sys.exit(0)
root=Path(tempfile.mkdtemp(prefix='I164-bootstrap-review-'));result={'temporary_root':str(root),'persistent_initialization_authorized':False,'prepared_record_reconciliation':'PENDING independent comparison of original records and this captured environment','status':'INCOMPLETE'}
print('Temporary evidence:',root,flush=True)
try:
 records={}
 for name,path in [('ENVIRONMENT-RESULT.json',a.environment_record),('requirements.lock',a.lock),('COMPATIBILITY-RESULT.json',a.compatibility_record)]:
  assert path and path.is_file(),'MISSING-ORIGINAL-RECORD:'+name
  raw=path.read_bytes();(root/name).write_bytes(raw);records[name]={'path':str(path.resolve()),**ident(path)}
  if name.endswith('.json'):json.loads(raw)
 result['original_record_identities']=records
 for name,v in records.items():assert {k:v[k] for k in ['bytes','sha256']}=={k:EXPECTED['original_record_identities'][name][k] for k in ['bytes','sha256']},'ORIGINAL-RECORD-IDENTITY:'+name
 result['current_environment']=b.enforce_environment()
 for field in ['implementation','python','optimize','cryptography','sqlite','executable','executable_identity']:
  assert result['current_environment'][field]==EXPECTED['current_environment'][field],'HOST-ENVIRONMENT-BINDING:'+field
 normalize=lambda n:re.sub('[-_.]+','-',n).lower()
 parsed=parse_lock(a.lock.read_text());wanted={n:v['version'] for n,v in parsed.items()}
 result['retained_lock_hash_counts']={n:len(v['hashes']) for n,v in parsed.items()}
 current={normalize(x.metadata['Name']):x.version for x in importlib.metadata.distributions()}
 result['lock_comparison']={'expected':wanted,'installed':current};assert wanted and wanted==current,'EXACT-DISTRIBUTION-LOCK-MISMATCH'
 result['installed_requirement_checks']=check_dependencies()
 result['dependency_check_method']='stdlib installed Requires-Dist evaluation; no pip installation; unsupported syntax rejects'
 b.inputs(a.candidate,a.draft);b.recover_runtime(a.candidate,a.draft,root/'runtime')
 b.validate_runtime(root/'runtime')
 probe=subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('native_probe.py')),str(root/'runtime'),str(Path(__file__).resolve().parents[1]/'provenance/review/results/BR-02.json')],capture_output=True,text=True,timeout=15)
 (root/'native-authentication.log').write_text(probe.stdout+probe.stderr);assert probe.returncode==0,'NATIVE-PRIMITIVE-COMPATIBILITY'
 for mode in ['create','reopen']:
  cmd=[sys.executable,'-B',str(Path(__file__).resolve()),'--package',str(a.package),'--candidate',str(a.candidate),'--draft',str(a.draft),'--worker',mode,'--temporary-root',str(root)]
  p=subprocess.run(cmd,capture_output=True,text=True,timeout=120);(root/(mode+'.log')).write_text(p.stdout+p.stderr);assert p.returncode==0,'TEMPORARY-'+mode.upper()+'-FAILED'
 result['status']='PASS bounded current-host public runtime compatibility; original record bodies captured for separate reconciliation'
 result['installed_wheel_hash_authentication']='NOT-ESTABLISHED; lock bytes and installed versions checked, not installed wheel bytes'
except BaseException as e:
 result['status']='BLOCKED';result['error']=type(e).__name__+': '+str(e);result['traceback']=traceback.format_exc();raise
finally:
 (root/'HOST-PROBE-RESULT.json').write_text(json.dumps(result,indent=2));print('Preserved evidence:',root,flush=True)
