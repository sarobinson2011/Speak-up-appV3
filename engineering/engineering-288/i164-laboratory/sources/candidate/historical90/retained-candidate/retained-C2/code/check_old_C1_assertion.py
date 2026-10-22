import sys,json,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from fixtures import *
def prepared(b,c,u='LAB-U-1',nonce=1):
 b.retire(u,intent(c,u,nonce=nonce));b.seal_conditional(u);b.prepare(u,*envelope(b,u,nonce))
def error(fn):
 try:fn()
 except Exception as ex:return type(ex).__name__+':'+str(ex)
 raise AssertionError('expected rejection')
def result_gap_exhaustion(b,p,c,tmp):
 b.close();c['query_limit']=1
 with Bridge(tmp/'small',c,True) as x:
  prepared(x,c);sim=t.OfflineTransport();x.submit('LAB-U-1','a',sim);sim.outcome=outcome(x)
  error(lambda:x.reconcile('LAB-U-1','q',sim,'after_transport_result'))
 with Bridge(tmp/'small',c) as x:
  x.recover();x.allowances.repair_anchor();before=x.executor.states['LAB-U-1']['status']
  er=error(lambda:x.reconcile('LAB-U-1','q2',sim))
  assert before=='UNCERTAIN' and 'EXHAUSTED' in er
  return {'transport':x.transport.states['LAB-U-1']['status'],'executor':before,'retry_error':er,'no_uncharged_external_observation':True,'internal_executor_completion_unavailable':True}
with tempfile.TemporaryDirectory() as d:
 c=config();b=Bridge(Path(d)/'job',c,True)
 try:r=result_gap_exhaustion(b,Path(d)/'job',c,Path(d))
 finally:b.close()
 print(json.dumps(r))
