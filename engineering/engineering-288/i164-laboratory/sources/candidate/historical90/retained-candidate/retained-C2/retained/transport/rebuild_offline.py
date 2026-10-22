"""Offline-only rebuild from packaged checksum-verified toolchain/module cache."""
import os,sys,json,hashlib,tarfile,subprocess,shutil,time,signal
from pathlib import Path
kit=Path(__file__).resolve().parents[1];work=Path(sys.argv[1]).resolve()
assert not work.exists(),'Use a fresh isolated build directory; never overwrite previous outputs'
subprocess.run([sys.executable,'-B',str(kit/'verify.py')],check=True,timeout=30)
assert shutil.disk_usage(work.parent).free>2*1024**3,'2 GiB disk planning margin required'
work.mkdir();meta=json.loads((kit/'retained/setup.json').read_text())['go_toolchain_proposed_for_offline_check'];arc=kit/'retained'/meta['filename']
assert hashlib.sha256(arc.read_bytes()).hexdigest()==meta['sha256']
with tarfile.open(arc) as t:
 ms=t.getmembers();assert sum(m.size for m in ms)<1024**3
 for m in ms:assert not Path(m.name).is_absolute() and '..' not in Path(m.name).parts and not (m.issym() or m.islnk() or m.isdev())
 t.extractall(work,filter='data')
shutil.copytree(kit/'retained/near-api-go',work/'source');shutil.copytree(kit/'retained/module-cache',work/'modules/cache/download')
env={'PATH':str(work/'go/bin')+':/usr/bin:/bin','HOME':os.environ.get('HOME','/nonexistent'),'GOENV':'off','GOTOOLCHAIN':'local','GOPATH':str(work/'gopath'),'GOCACHE':str(work/'gocache'),'GOMODCACHE':str(work/'modules'),'GOMAXPROCS':'2','GOMEMLIMIT':'512MiB','GOPROXY':'off','GOSUMDB':'off','CGO_ENABLED':'0'}
go=str(work/'go/bin/go');results=[]
commands=[('version',[go,'version'],10),('verify',[go,'-C',str(work/'source'),'mod','verify'],30),('build',[go,'-C',str(work/'source'),'build','-buildvcs=false','-mod=readonly','-p=2','-o',str(work/'compat'),'./cmd/compat'],180),('probe',[str(work/'compat')],10),('correspondence',[sys.executable,'-B',str(kit/'retained/unsigned-probe-oracle.py'),str(work/'probe.stdout')],10)]
for name,args,limit in commands:
 start=time.monotonic()
 with (work/(name+'.stdout')).open('wb') as out,(work/(name+'.stderr')).open('wb') as err:
  p=subprocess.Popen(args,env=env,stdout=out,stderr=err,start_new_session=True)
  try:p.wait(timeout=limit)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait();raise
 results.append({'stage':name,'returncode':p.returncode,'seconds':time.monotonic()-start,'limit_seconds':limit});(work/'results.json').write_text(json.dumps(results,indent=2));assert p.returncode==0,results[-1]
for n in ['go.mod','go.sum']:assert (work/'source'/n).read_bytes()==(kit/'retained/near-api-go'/n).read_bytes()
print(json.dumps({'result':'PASS-OFFLINE-REBUILD','directory':str(work),'actual_admission':False}))
