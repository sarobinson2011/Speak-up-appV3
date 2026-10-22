"""New isolated offline executions, no lifecycle. Lab keys from retained source.
Private diagnostics/fault proxy are test-owned; production serving is managed."""
import sys,json,shutil,tempfile,sqlite3,hashlib
from pathlib import Path
from hydration import hydrate,export
R=Path(sys.argv[1]).resolve();RUN=Path(sys.argv[2]).resolve();P=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(P/'code'),str(RUN/'compiler'),str(R/'compiler')]
import managed_observations as mo,managed_coverage as mc
from live_connection import open_session,ManagedAuthority
class FaultDB:
 def __init__(self,db,kind,operations):self.db=db;self.kind=kind;self.operations=operations
 def __getattr__(self,k):return getattr(self.db,k)
 def execute(self,sql,args=()):
  if self.kind=='rollback-denied':self.db.set_authorizer(lambda op,a,b,c,d:sqlite3.SQLITE_DENY if sql=='ROLLBACK' and op==sqlite3.SQLITE_TRANSACTION and a=='ROLLBACK' else sqlite3.SQLITE_OK)
  try:r=self.db.execute(sql,args);self.operations.append({'sql':sql,'params':mo.value(args),'result':'returned'});return r
  except BaseException as e:self.operations.append({'sql':sql,'params':mo.value(args),'exception':type(e).__name__+':'+str(e)});raise
 def close(self):
  k=self.kind;self.kind=None
  if k=='before':self.operations.append({'close':'failure before underlying close'});raise OSError('INJECTED-close-before')
  self.db.close();self.operations.append({'close':'underlying close returned'})
  if k=='after':raise OSError('INJECTED-close-ack-loss')
  if k=='interrupt':raise KeyboardInterrupt('INJECTED-close-interruption-after-return')

def run(name,tracing=True):
 with tempfile.TemporaryDirectory() as td:
  t=Path(td)
  for m in ('authority','ownership','accounting'):sys.modules.pop(m,None)
  shutil.copytree(R/'historical90/retained-candidate',t/'retained-candidate');shutil.copytree(R/'support/reference/runtime',t/'prospective');sys.path.insert(0,str(t/'prospective'));import authority
  fixture='zk-created' if name=='sign-zk' else 'ord-created';x=json.loads((R/'signing_observation_outputs/execution'/f'{fixture}-observed.json').read_bytes())['input'];db=t/'test.db';own=hydrate(x,db)
  trace=mo.Recorder(R);operations=[];steps=[];attempted=[]
  def step(label,f):
   try:r=f();steps.append({'label':label,'returned':mo.value(r)});return r
   except BaseException as e:steps.append({'label':label,'exception':{'type':type(e).__name__,'message':str(e)}});return None
  if tracing:sys.settrace(trace)
  try:
   g,sc=open_session(RUN,db,x['config'],ownership_path=own)
   u=g.state()['active'];act=g.state()['u'][u]['stage']['pending']['action']
   packet=sc.packet('sign' if name.startswith('sign-') else 'head',u,{'action':act} if name.startswith('sign-') else {},challenge=hashlib.sha256(('managed-observe-'+name).encode()).hexdigest())
   def send(q,inject=None):attempted.append(q.hex());return g.handle(q,inject)
   if name.startswith('sign-'):
    g._live.db=FaultDB(g._live.db,'rollback-denied',operations)
    step('managed-sign-rollback-denial',lambda:send(packet,'before_signature_commit'))
    step('quarantined-status',g.status)
    step('subsequent-request',lambda:send(packet))
    step('validated-recovery',g.recover)
   elif name in ('before','after','interrupt'):
    g._live.db=FaultDB(g._live.db,name,operations)
    step('explicit-close-with-injection',g.close);step('uncertain-status',g.status)
    step('subsequent-request',lambda:send(packet));step('confirmed-cleanup-and-reopen',g.recover)
   elif name=='missing':
    step('close',g.close);db.rename(t/'saved.db');step('missing-file-recover',g.recover);step('blocked-state',g.state);(t/'saved.db').rename(db);step('existing-file-recovery',g.recover)
   elif name=='rejected':
    step('close',g.close);d=sqlite3.connect(db);raw=d.execute('SELECT raw FROM head').fetchone()[0];bad=json.loads(raw);bad['counts']['attempt']=0;d.execute('UPDATE head SET raw=?',(authority.enc(bad),));d.commit();d.close()
    step('corrupt-head-recover',g.recover);step('blocked-state',g.state)
    # Restore exact original fixture only in test setup; not a runtime repair.
    d=sqlite3.connect(db);d.execute('UPDATE head SET raw=?',(raw,));d.commit();d.close();step('exact-fixture-restored-recover',g.recover)
   else:step('normal-head-request',lambda:send(packet))
   after=export(g._live,x);status=g.status();step('confirmed-final-close',g.close)
  finally:sys.settrace(None)
  requests=[e['arguments']['packet']['bytes_hex'] for e in trace.events if e['event']=='call' and e['source']=='authority' and e['function']=='Authority.handle']
  out={'format':'I164-MANAGED-OCCURRENCE-1','case':name,'context':'SYMBOLIC-U-TWO' if name in ('sign-zk','after','rejected') else 'SYMBOLIC-U-ONE','runtime_layout':'exact 651-member predecessor projection; integration artifacts consumed separately','evidence_class':'ACTUAL-OFFLINE-MANAGED-EXECUTION','sources':{k:mc.identity(R,v) for k,v in mo.SOURCES.items()},'inputs':{k:mc.identity(R,v) for k,v in mc.FILES.items()},'interpreter':{'version':sys.version,'optimize':sys.flags.optimize},'boundary':mc.BOUNDARY,'limits':mc.LIMITS,'obligations':mc.OBLIGATIONS,'before':x,'after':after,'requests':requests,'attempted_packets':attempted,'events':trace.events,'steps':steps,'fault_operations':operations,'status_before_final_close':status,'fault_scope':'Explicit laboratory proxy/SQLite authorizer failures; not storage durability. Corrupt-head restoration is test setup only. No new allowance.'}
  return out
if __name__=='__main__':
 names=sys.argv[3:] or ['normal','sign-ord','sign-zk','before','after','interrupt','missing','rejected']
 for name in names:
  r=run(name);(P/'evidence'/f'{name}.json').write_bytes(mo.enc(r));print('CAPTURED',name,len(r['events']),flush=True)
  if name in ('normal','sign-ord'):
   plain=run(name,False)
   for key in ('before','after','attempted_packets','steps','fault_operations','status_before_final_close'):mo.same(r[key],plain[key],'INSTRUMENTATION-BEHAVIOR:'+key)
   (P/'results'/f'{name}-instrumentation.json').write_bytes(mo.enc({'status':'PASS','compared':['before','after','attempted_packets','steps','fault_operations','status_before_final_close'],'untraced_run':plain,'scope':'representative equivalence only; no timing/thread/operational attestation'}));print('INSTRUMENTATION PASS',name,flush=True)
