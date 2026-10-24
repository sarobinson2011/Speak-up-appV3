"""Add the exact reviewed finite checkpoint; preserve unrelated work; no application execution."""
import hashlib,json,os,re,stat,subprocess,sys,traceback,uuid
from pathlib import Path
TARGET='engineering/engineering-288/i164-finite-pipeline'
PREVIOUS='engineering/engineering-288/i164-laboratory'
BASE=Path('/home/steve/dev/Engineering-288-execution')
REPO=Path('/home/steve/dev/Speak-up-appV3')
HOST=BASE/'I164-finite-pipeline-643cef71dff9'
PATTERNS=[('private key',rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),('GitHub token',rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b'),('AWS key',rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),('Slack token',rb'\bxox[baprs]-[A-Za-z0-9-]{20,}\b'),('credential URL',rb'https?://[^\s/"\x27:@]+:[^\s/"\x27@]+@'),('literal secret',rb'(?im)^\s*["\x27]?(?:password|api[_-]?key|access[_-]?token|client[_-]?secret)["\x27]?\s*[:=]\s*["\x27][A-Za-z0-9+/=_-]{16,}["\x27]')]
def need(x,s):
 if not x:raise RuntimeError(s)
def enc(x):return (json.dumps(x,sort_keys=True,indent=2)+'\n').encode()
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p):
 p=Path(p);need(stat.S_ISREG(p.lstat().st_mode),'Nonregular: '+str(p));return p.read_bytes()
def write(p,b):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
def scan(n,b):
 for kind,p in PATTERNS:need(re.search(p,b) is None,'Secret scan stopped: '+kind+' in '+n)
def tree(root,m):
 dirs={str(p) for n in m for p in Path(n).parents if str(p)!='.'};seen=set()
 for d,ds,fs in os.walk(root,followlinks=False):
  for n in ds:
   p=Path(d,n);need(not p.is_symlink() and p.relative_to(root).as_posix() in dirs,'Unexpected directory '+str(p))
  for n in fs:
   p=Path(d,n);k=p.relative_to(root).as_posix();need(k in m and ident(read(p))==m[k],'File identity '+str(p));seen.add(k)
 need(seen==set(m),'Missing tree members')
def verify_host(payload,host):
 report=read(host/'RESULT.json');need(report==payload['provenance/host/finite-pipeline.json'],'Host report changed/missing')
 r=json.loads(report);need(r['status'].startswith('PASS') and r['returncode']==0,'Host status')
 receipt=read(host/'pipeline/receipt.json');need(ident(receipt)==r['receipt'],'Saved receipt identity')
 v=json.loads(receipt)
 for role,rel in [('model','02-consumer/native.json'),('ledger','04-ledger/ledger.json')]:
  need(ident(read(host/'pipeline'/rel))==v['outputs']['artifacts'][role],'Saved '+role+' identity')
 for name in ['01-inputs','02-consumer','03-verification','04-ledger']:
  x=json.loads(read(host/'pipeline'/(name+'-execution.json')));need(x['returncode']==0,'Recorded stage failed')
 cfg=json.loads(read(host/'recovered/config.json'))
 for role in ('candidate','draft'):
  m=json.loads(payload['provenance/'+role+'-members.json']);tree(Path(cfg[role]),m)
 for role,label in [('inputs','finite-inputs'),('consumer','finite-consumer'),('ledger','finite-ledger'),('counts','evidence-count')]:
  rows=json.loads(payload['provenance/source-membership.json'])[label]['members']
  tree(Path(cfg[role+'_root']),{n:{k:row[k] for k in ('bytes','sha256')} for n,row in rows.items()})
 tree(host/'runtime',r['runtime_members'])
 return {'report':ident(report),'receipt':ident(receipt),'scope':'saved identities inspected; host execution remains report-supported; no validator rerun'}

def run(repo=REPO,base=BASE,host=HOST,host_check=verify_host):
 os.umask(0o077);evidence=base/('I164-git-finite-'+uuid.uuid4().hex[:12]);evidence.mkdir(parents=True,exist_ok=False)
 report={'status':'STOP — checkpoint incomplete','evidence':str(evidence),'assessment':'SOURCE-ONLY','readiness':'BLOCKED','final_binding':'BLOCKED','streams':'UNCOMPUTED','actual_admission':False}
 env=dict(os.environ,GIT_TERMINAL_PROMPT='0',GIT_OPTIONAL_LOCKS='0')
 def git(*args):
  p=subprocess.run(['git','-C',str(repo),*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
  with (evidence/'git.log').open('ab') as f:f.write(('git '+' '.join(args)+'\nexit='+str(p.returncode)+'\n').encode())
  need(p.returncode==0,'git '+args[0]+' failed (exit '+str(p.returncode)+'); no reset/force/retry')
  return p.stdout
 def text(*a):return git(*a).decode().strip()
 def status():return git('status','--porcelain=v1','-z','--untracked-files=all','--','.',':(exclude)'+TARGET)
 def tracked():return git('diff','--binary','--','.',':(exclude)'+TARGET)
 try:
  print('PERSISTENT GIT EVIDENCE:',evidence,flush=True);print('Estimate: 2–5 minutes; no pipeline execution.',flush=True)
  print('1/5 Inspect repository instructions/status and main/origin/main',flush=True)
  need(text('rev-parse','--show-toplevel')==str(repo.resolve()),'Repository root')
  need(text('symbolic-ref','--short','HEAD')=='main','Expected main branch')
  need(text('rev-parse','--abbrev-ref','--symbolic-full-name','@{upstream}')=='origin/main','Expected upstream origin/main')
  instructions={}
  for p in [repo,*repo.parents,repo/'engineering',repo/'engineering/engineering-288']:
   q=p/'AGENTS.md'
   if q.exists():
    b=read(q);write(evidence/('instructions-'+str(len(instructions))+'.txt'),b);instructions[str(q)]=ident(b)
  report['instructions']=instructions
  need(not instructions,'Applicable AGENTS.md found; saved for interpretation before changes')
  for name in ('STATE.md','README.md','CONTRIBUTING.md'):
   if (repo/name).is_file():
    b=read(repo/name);report.setdefault('repository_context',{})[name]=ident(b)
  need(not git('diff','--cached','--name-only'),'Existing staged work; preserved, no commit')
  before=status();diff=tracked();parent=text('rev-parse','HEAD');oldtree=text('rev-parse','HEAD:'+PREVIOUS)
  report['parent']=parent;report['previous_checkpoint_tree']=oldtree
  remote=text('ls-remote','--exit-code','origin','refs/heads/main').split()
  need(remote==[parent,'refs/heads/main'],'Remote differs; no merge/reset attempted')
  dest=repo/TARGET;need(not os.path.lexists(dest),'Checkpoint destination already exists; no overwrite')
  print('2/5 Verify selected source package and saved host output identities',flush=True)
  package=Path(__file__).resolve().parent;pm=json.loads(read(package/'PACKAGE-MANIFEST.json'));tree(package,{**pm,'PACKAGE-MANIFEST.json':ident(read(package/'PACKAGE-MANIFEST.json'))})
  payload={n[len('payload/'):]:read(package/n) for n in pm if n.startswith('payload/')}
  need(bool(payload),'Empty payload')
  report['host_evidence']=host_check(payload,host)
  # Verify all historical candidate/draft bytes already committed in predecessor.
  for role in ('candidate','draft'):
   m=json.loads(payload['provenance/'+role+'-members.json']);prefix=PREVIOUS+'/sources/'+role+'/'
   names=git('ls-tree','-r','--name-only','-z','HEAD','--',prefix).decode().split('\0')
   need(any(names),'Previous tracked '+role+' source selection missing')
   for n in filter(None,names):
    rel=n[len(prefix):];need(rel in m and ident(git('show','HEAD:'+n))==m[rel],'Historical tracked source mismatch: '+n)
  payload['tools/commit_checkpoint.py']=read(Path(__file__).resolve())
  for n,b in payload.items():
   need(len(b)<500000 and Path(n).suffix not in ('.zip','.db','.sqlite','.so','.pem','.key'),'Disallowed Git payload '+n);scan(n,b)
  manifest={n:ident(b) for n,b in payload.items()};payload['MANIFEST.json']=enc(manifest)
  report['selection']={'files':len(payload),'bytes':sum(map(len,payload.values())),'manifest':ident(payload['MANIFEST.json'])}
  need(status()==before and tracked()==diff and not git('diff','--cached','--name-only'),'Repository changed during preparation')
  print('3/5 Add exact selected sources/provenance; scan staged bytes',flush=True)
  dest.mkdir(parents=True)
  for n,b in payload.items():write(dest/n,b)
  git('add','--',TARGET)
  expected={TARGET+'/'+n for n in payload}
  staged=set(filter(None,git('diff','--cached','--name-only','-z').decode().split('\0')));need(staged==expected,'Unexpected staged paths')
  for n in sorted(staged):
   b=git('show',':'+n);need(b==payload[n[len(TARGET)+1:]],'Staged bytes changed');scan(n,b)
  need(status()==before and tracked()==diff,'Unrelated work changed')
  report['secret_scan']='PASS heuristic staged-content scan; deterministic public laboratory source identities retained; not a proof of absence'
  write(evidence/'PRECOMMIT.json',enc(report))
  print('4/5 Commit bounded finite pipeline and mechanical ledger complete',flush=True)
  git('commit','-m','Engineering 288: bounded finite pipeline and mechanical ledger complete','-m','Finite saved-acquisition scope only. Reviewed CF-01 correction, prospective 50.0.2 profile, contract mappings and report-supported host compatibility. SOURCE-ONLY; UNKNOWN and all eleven obligations preserved. Readiness/final binding blocked; streams UNCOMPUTED; admission disabled. No canonical rebinding or qualification.')
  commit=text('rev-parse','HEAD');report.update(commit=commit,tree=text('rev-parse','HEAD^{tree}'),commit_created=True)
  need(text('rev-parse','HEAD^')==parent,'Commit parent changed')
  changed=set(filter(None,git('diff-tree','--no-commit-id','--name-only','-r','-z','HEAD').decode().split('\0')));need(changed==expected,'Commit contains unrelated paths')
  for n,b in payload.items():need(git('show','HEAD:'+TARGET+'/'+n)==b,'Committed bytes mismatch')
  need(text('rev-parse','HEAD:'+PREVIOUS)==oldtree,'Previous checkpoint changed')
  need(status()==before and tracked()==diff and not git('diff','--cached','--name-only'),'Unrelated post-commit changes')
  print('5/5 Push without force and verify remote tip',flush=True)
  git('push','origin','HEAD:refs/heads/main')
  remote=text('ls-remote','--exit-code','origin','refs/heads/main').split();need(remote==[commit,'refs/heads/main'],'Remote tip unconfirmed')
  report.update(status='PASS — committed and pushed bounded finite checkpoint',remote_tip=commit,unrelated_work_preserved=True)
 except BaseException as exc:
  report['error']=str(exc);write(evidence/'failure.txt',traceback.format_exc().encode())
 finally:
  write(evidence/'GIT-RESULT.json',enc(report));downloads=Path('/home/steve/Downloads') if repo==REPO else base/'downloads';downloads.mkdir(parents=True,exist_ok=True)
  target=downloads/'SEND-TO-ANCHOR-git-finite.json'
  if target.exists():target.rename(downloads/('SEND-TO-ANCHOR-git-finite.previous-'+uuid.uuid4().hex[:8]+'.json'))
  write(target,enc(report));print(report['status']);print('COMMIT:',report.get('commit','NOT CREATED'));print('TREE:',report.get('tree','NOT ESTABLISHED'));print('REMOTE:',report.get('remote_tip','NOT CONFIRMED'));print('REPORT:',target)
  if 'error' in report:print('STOP REASON:',report['error'])
 return report
if __name__=='__main__':sys.exit(0 if run()['status'].startswith('PASS') else 1)
