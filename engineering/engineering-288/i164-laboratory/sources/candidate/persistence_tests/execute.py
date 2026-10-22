"""Lab-only SQLite boundary proxy. Exact runtime bytes unchanged; no network."""
import sys,json,hashlib,sqlite3,shutil,tempfile,subprocess,dis
from pathlib import Path
from hydration import hydrate,export
R=Path(sys.argv[1]).resolve();P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'compiler'));from boundary_events import identity
AUTH='support/reference/runtime/authority.py'
def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def sha(x):return hashlib.sha256(x).hexdigest()
CASES=[(f'{target}-{mode}', 'ord-created',target,mode) for target in ['admission','claim','signed','response'] for mode in ['deny','ack']]+[(f'rollback-{mode}','ord-created','rollback',mode) for mode in ['deny','ack']]+[('signed-double-deny','ord-created','signed','double-deny'),('zk-signed-ack','zk-created','signed','ack'),('zk-response-deny','zk-created','response','deny'),('plain-control','ord-created','none','none')]
def error(e):return {'type':type(e).__name__,'message':str(e),'context':error(e.__context__) if e.__context__ else None}
if len(sys.argv)==2:
 rows=[]
 for name,fixture,target,mode in CASES:
  with tempfile.TemporaryDirectory() as td:
   t=Path(td);shutil.copytree(R/'historical90/retained-candidate',t/'retained-candidate');shutil.copytree(R/'support/reference/runtime',t/'prospective')
   run=subprocess.run([sys.executable,'-B',__file__,str(R),name,str(t)],capture_output=True,text=True)
   (P/'results/execution'/f'{name}.log').write_text(run.stdout+run.stderr);assert run.returncode==0,(name,run.stderr)
   x=json.loads((t/'result.json').read_bytes());rr=subprocess.run([sys.executable,'-B',__file__,str(R),name,str(t),'reopen'],capture_output=True,text=True,check=True)
   x['reopened']=json.loads(rr.stdout);x['process_code']=run.returncode
   (P/'results/execution'/f'{name}.json').write_bytes(enc(x));rows.append({'name':name,'fixture':fixture,'target':target,'mode':mode,'operations':len(x['operations']),'fresh_process_reopen':True})
 (P/'results/execution/INDEX.json').write_text(json.dumps(rows,indent=2));print('PASS',len(rows),'request executions and fresh-process reopenings');sys.exit()
name,t=sys.argv[2:4];t=Path(t);_,fixture,target,mode=next(c for c in CASES if c[0]==name)
sys.path.insert(0,str(t/'prospective'));import authority as a
assert (t/'prospective/authority.py').read_bytes()==(R/AUTH).read_bytes()
x=json.loads((R/'signing_observation_outputs/execution'/f'{fixture}-observed.json').read_bytes())['input']
if len(sys.argv)>4:
 auth=a.Authority(t/'lab.db',x['config'],ownership_path=t/'lab.owners');out=export(auth,x);auth.close();print(json.dumps(out));sys.exit()
own=hydrate(x,t/'lab.db');auth=a.Authority(t/'lab.db',x['config'],ownership_path=own)
q=a.Scheduler(auth).packet('sign',auth.state()['active'],{'action':auth.state()['u'][auth.state()['active']]['stage']['pending']['action']},challenge=sha(('persistence-'+name).encode()))
ops=[];db=auth.db;commits=0;denial=False
# Actual SQLite authorizer denial. No syscall/power-loss behavior is claimed.
def authorizer(op,one,two,db_name,trigger):
 if denial and op==sqlite3.SQLITE_TRANSACTION and one in ('COMMIT','ROLLBACK'):return sqlite3.SQLITE_DENY
 return sqlite3.SQLITE_OK
db.set_authorizer(authorizer)
def frames():
 out=[];f=sys._getframe(2)
 while f:
  if f.f_code.co_filename==str(t/'prospective/authority.py'):
   instr=next(i for i in dis.get_instructions(f.f_code,show_caches=True) if i.offset==f.f_lasti)
   # f_lasti at CALL inline cache is a valid runtime coordinate; retain exact offset.
   out.append({'function':f.f_code.co_qualname,'code':identity(f.f_code),'offset':f.f_lasti,'opname':instr.opname,'position':list(instr.positions),'request':f.f_locals.get('r')})
  f=f.f_back
 return out
class Proxy:
 def __getattr__(self,n):return getattr(db,n)
 def execute(self,sql,args=()):
  global commits,denial
  tracked=sql in ('BEGIN IMMEDIATE','COMMIT','ROLLBACK') or sql.startswith('UPDATE journal SET response')
  if not tracked:return db.execute(sql,args)
  if sql=='COMMIT':commits+=1
  wanted={'admission':1,'claim':2,'signed':3,'response':4}.get(target)
  hit=(sql=='COMMIT' and commits==wanted) or (sql=='ROLLBACK' and (target=='rollback' or mode=='double-deny'))
  row={'sql':sql,'params':[v.hex() if type(v) is bytes else v for v in args],'frames':frames(),'in_transaction_before':db.in_transaction,'injected':mode if hit else None,'sqlite_completed':False,'exception':None}
  ops.append(row)
  try:
   denial=hit and mode in ('deny','double-deny')
   db.set_authorizer(authorizer) # invalidate cached prepared statements before policy change
   result=db.execute(sql,args);row['sqlite_completed']=True
   if hit and mode=='ack':raise OSError('SIMULATED-ACK-LOSS-'+sql)
   return result
  except BaseException as e:row['exception']=error(e);raise
  finally:denial=False;row['in_transaction_after']=db.in_transaction
 def close(self):db.close()
auth.db=Proxy();inject='before_signature_commit' if target=='rollback' else None
returned=None;escaped=None
try:returned=auth.handle(q,inject).hex()
except BaseException as e:escaped=error(e)
# Captured before cleanup: a failed ROLLBACK may leave uncommitted rows visible.
preclose=export(auth,x);active=db.in_transaction;auth.close()
result={'format':'I164-PERSISTENCE-LAB-1','name':name,'input':x,'request_hex':q.hex(),'target':target,'mode':mode,'inject':inject,'operations':ops,'returned':returned,'escaped':escaped,'preclose':preclose,'preclose_in_transaction':active,'cleanup':'explicit sqlite connection close before fresh-process reopen','source_sha256':sha((R/AUTH).read_bytes()),'harness_sha256':sha(Path(__file__).read_bytes()),'interpreter':list(sys.version_info[:3]),'sqlite_version':sqlite3.sqlite_version,'evidence_kind':'actual isolated request with declared simulated/authorizer fault injection'}
(t/'result.json').write_bytes(enc(result))
