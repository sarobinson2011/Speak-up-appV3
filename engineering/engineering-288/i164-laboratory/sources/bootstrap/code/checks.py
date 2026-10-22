import sys,json,subprocess,tempfile,shutil,stat
from pathlib import Path
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'implementation/code'));import lab_bootstrap as b
from lock_contract import parse_lock
x=b.read(P/'provenance/local-inputs.json');c=Path(x['candidate']);d=Path(x['draft']);T=Path(tempfile.mkdtemp(prefix='i164-BR-controls-'));r=T/'runtime';out=P/'results/fresh';out.mkdir();rows=[]
def check(name,cmd,code=0,message=None):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=120);(out/(name+'.log')).write_text(p.stdout+p.stderr)
 ok=p.returncode==code and (message is None or message in p.stdout+p.stderr);rows.append({'name':name,'pass':ok,'returncode':p.returncode,'expected':code})
 assert ok,(name,p.stderr[-1000:])
def run(name,case,dest,code=0,msg=None,runtime=None,draft=None):
 check(name,[sys.executable,'-B',str(P/'code/worker.py'),case,str(c),str(draft or d),str(runtime or r),str(dest)],code,msg)
try:
 run('BR01-clean-draft-accepted','inputs',T/'unused')
 run('recover-exact-runtime','recover',r)
 assert stat.S_IMODE((r/b.NATIVE_HELPER).stat().st_mode)==0o755
 for mode in ['valid','invalid']:
  check('BR02-'+mode,[sys.executable,'-B',str(P/'code/native_probe.py'),str(r),str(P/'provenance/review/results/BR-02.json'),mode])
 run('duplicate-runtime-refused','recover',r,1,'DESTINATION-EXISTS')
 partial=T/'partial';run('copy-process-interruption','copy-interrupt',partial,77);run('partial-runtime-refused','recover',partial,1,'DESTINATION-EXISTS')
 # Added and missing declared draft members both reject; unrelated originals untouched.
 for name in ['extra','missing']:
  dd=T/name;shutil.copytree(d,dd)
  if name=='extra':(dd/'unexpected-partial').write_bytes(b'prefix')
  else:(dd/'outputs/provenance.json').unlink()
  run('draft-'+name+'-rejected','inputs',T/'unused',1,'TREE-MEMBERSHIP',draft=dd)
 run('fresh-managed-creation','create',T/'session')
 run('fresh-process-managed-reopening','reopen',T/'session')
 helper=r/b.NATIVE_HELPER;helper.chmod(0o644)
 run('nonexecutable-runtime-rejected-before-open','reopen',T/'session',1,'NATIVE-EXECUTABLE-MODE');helper.chmod(0o755)
 run('managed-after-mode-restoration','reopen',T/'session')
 run('managed-process-exit','exit',T/'interrupted',78)
 run('interrupted-reopening-refused','reopen',T/'interrupted',1,'UNCERTAIN-PRIOR-OWNER')
 # Different recovery root, same bytes and native mode, fresh process.
 rr=T/'runtime2';run('second-root-recovery','recover',rr)
 check('second-root-authenticate',[sys.executable,'-B',str(P/'code/native_probe.py'),str(rr),str(P/'provenance/review/results/BR-02.json')])
 raw=(P/'provenance/host-addendum/requirements.lock').read_text();lock=parse_lock(raw)
 assert {k:v['version'] for k,v in lock.items()}=={'cffi':'2.1.1','cryptography':'41.0.7','pycparser':'3.11'}
 assert {k:len(v['hashes']) for k,v in lock.items()}=={'cffi':100,'cryptography':23,'pycparser':2}
 rows.append({'name':'actual-host-multiline-lock-all125-hashes','pass':True})
 for name,s in [('unfinished','x==1 \\'),('missing-hash','x==1'),('wrong-algorithm','x==1 --hash=md5:'+'0'*64),('unknown-option','x==1 --index-url=bad'),('duplicate',raw+raw),('range','x>=1 --hash=sha256:'+'0'*64),('hash-truncated','x==1 --hash=sha256:00')]:
  try:parse_lock(s)
  except ValueError:rows.append({'name':'lock-'+name+'-refused','pass':True})
  else:raise AssertionError(name)
 b.inputs(c,d);b.validate_runtime(r);b.validate_runtime(rr);rows.append({'name':'all666-and-current-inputs-preserved','pass':True})
finally:
 # Retain state/failures, runtime hashes and case logs without duplicating entire candidate/draft.
 for name in ['session','interrupted']:
  if (T/name).exists():shutil.copytree(T/name,out/name)
 (out/'results.json').write_bytes(b.enc({'checks':rows,'passed':sum(v['pass'] for v in rows),'temporary_root':str(T),'environment':b.environment(),'scope':'local private mechanics; public41.0.7 remains pending host command'}))
print('PASS',len(rows))
