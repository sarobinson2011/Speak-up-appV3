"""Bounded host probe. Uses public gates and only a new tempfile directory.
Preserves records and failures. Does not install, repair pins, reset or serve.
"""
import argparse,hashlib,importlib.metadata,json,os,re,subprocess,sys,tempfile,traceback
from pathlib import Path
def ident(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
ap=argparse.ArgumentParser();ap.add_argument('--package',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--draft',type=Path,required=True);ap.add_argument('--environment-record',type=Path);ap.add_argument('--lock',type=Path);ap.add_argument('--compatibility-record',type=Path);ap.add_argument('--worker',choices=['create','reopen']);ap.add_argument('--temporary-root',type=Path);a=ap.parse_args()
a.package=a.package.resolve();a.candidate=a.candidate.resolve();a.draft=a.draft.resolve()
assert ident(a.package/'code/lab_bootstrap.py')['sha256']=='ff78ac4e8b70997b20a5d1e732ace1755237d81b4a22bd5ff87ae1cf49da36b9','UNREVIEWED-LAUNCHER'
sys.path.insert(0,str(a.package/'code'));import lab_bootstrap as b
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
 result['original_record_identities']=records;result['current_environment']=b.enforce_environment()
 normalize=lambda n:re.sub('[-_.]+','-',n).lower()
 wanted={}
 for line in a.lock.read_text().splitlines():
  line=line.strip()
  if not line or line.startswith('#'):continue
  m=re.fullmatch(r'([A-Za-z0-9_.-]+)==([^\s;]+)',line)
  assert m,'UNSUPPORTED-LOCK-LINE; preserve for review, do not install or reinterpret'
  name=normalize(m[1]);assert name not in wanted,'DUPLICATE-LOCK-NAME';wanted[name]=m[2]
 current={normalize(x.metadata['Name']):x.version for x in importlib.metadata.distributions()}
 result['lock_comparison']={'expected':wanted,'installed':current};assert wanted and wanted==current,'EXACT-DISTRIBUTION-LOCK-MISMATCH'
 p=subprocess.run([sys.executable,'-B','-m','pip','check'],capture_output=True,text=True);(root/'pip-check.log').write_text(p.stdout+p.stderr);assert p.returncode==0,'DEPENDENCY-CHECK'
 # As delivered this stops on BR-01 for a clean reviewed draft. No partial is fabricated.
 b.inputs(a.candidate,a.draft);b.recover_runtime(a.candidate,a.draft,root/'runtime')
 assert os.access(root/'runtime/retained-candidate/native/bin/pe-rfc8032-stream',os.X_OK),'BR-02:RECOVERED-NATIVE-HELPER-NOT-EXECUTABLE'
 for mode in ['create','reopen']:
  cmd=[sys.executable,'-B',str(Path(__file__).resolve()),'--package',str(a.package),'--candidate',str(a.candidate),'--draft',str(a.draft),'--worker',mode,'--temporary-root',str(root)]
  p=subprocess.run(cmd,capture_output=True,text=True,timeout=120);(root/(mode+'.log')).write_text(p.stdout+p.stderr);assert p.returncode==0,'TEMPORARY-'+mode.upper()+'-FAILED'
 result['status']='PASS bounded current-host public checks; original record reconciliation still required'
except BaseException as e:
 result['status']='BLOCKED';result['error']=type(e).__name__+': '+str(e);result['traceback']=traceback.format_exc();raise
finally:
 (root/'HOST-PROBE-RESULT.json').write_text(json.dumps(result,indent=2));print('Preserved evidence:',root,flush=True)
