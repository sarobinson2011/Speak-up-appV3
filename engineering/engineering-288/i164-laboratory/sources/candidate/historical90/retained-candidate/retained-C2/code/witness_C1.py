"""Adapted supplied C1 cut; isolated observations by the test harness only."""
from fixtures import *
import shutil,json
R=Path(__file__).resolve().parents[1];out=R/'results/C1-final';out.mkdir(exist_ok=False);job=out/'job';c=config();c['query_limit']=1
with Bridge(job,c,True) as b:
 b.retire('LAB-U-1',intent(c));b.seal_conditional('LAB-U-1');b.prepare('LAB-U-1',*envelope(b));sim=t.OfflineTransport();b.submit('LAB-U-1','a',sim);sim.outcome=outcome(b)
 try:b.reconcile('LAB-U-1','q',sim,'after_transport_result')
 except RuntimeError:pass
 else:raise AssertionError('missing interruption')
 before={'head':b.transport.head,'counts':dict(b.transport.counts),'partitions':dict(b.transport.staging),'executor':b.executor.states['LAB-U-1']['status'],'send_calls':sim.calls}
for n in ['executor.db','transport.db','independent-anchor.db']:
 d=out/'before';d.mkdir(exist_ok=True);shutil.copyfile(job/n,d/n)
with Bridge(job,c) as b:
 result=b.allowances.repair_anchor();assert result is None;b.allowances.repair_anchor()
 after={'head':b.transport.head,'counts':dict(b.transport.counts),'partitions':dict(b.transport.staging),'executor':b.executor.states['LAB-U-1']['status'],'send_calls':sim.calls}
 assert before['executor']=='UNCERTAIN' and after['executor']=='SUCCESS'
 assert all(before[k]==after[k] for k in ['head','counts','partitions','send_calls'])
 try:b.status('extra')
 except ValueError as ex:assert 'EXHAUSTED' in str(ex)
 else:raise AssertionError('uncharged observation')
 try:b.submit('LAB-U-1','retry',sim)
 except ValueError:pass
 else:raise AssertionError('second authorization')
for n in ['executor.db','transport.db','independent-anchor.db']:
 d=out/'after';d.mkdir(exist_ok=True);shutil.copyfile(job/n,d/n)
(out/'result.json').write_text(json.dumps({'before':before,'after':after,'internal_return':None,'no_new_transport_event':True,'no_new_submission':True,'actual_admission':False},indent=2))
print('PASS C1 saved-evidence convergence and accounting conservation')
