"""New SOC-02-R1 controls only; preserve SOC-01 closure and reuse prior suites."""
import argparse,copy,json,os,sys,types
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def audit(e,a):
 if e in ('sqlite3.connect','socket.connect','socket.bind'):raise AssertionError(e)
 if e=='open' and isinstance(a[0],(str,bytes)) and os.fsdecode(a[0]).startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
sys.addaudithook(audit)
def profile(f,event,arg):
 if event=='call' and f.f_code.co_filename.rsplit('/',1)[-1] in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('APPLICATION-EXECUTION')
sys.setprofile(profile)
def module(p):
 m=types.ModuleType('consumer');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=R/'corrected');p.add_argument('--output',type=Path,required=True);p.add_argument('--reproduce',action='store_true');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 before=(a.root/'code/smoke_occurrences.py').read_bytes();m=module(a.root/'code/smoke_occurrences.py');ctx=m.load(a.root);raw=(a.root/'results/occurrence-connection.json').read_bytes();trace='evidence/execution-trace.json';rows=[]
 def check(label,fn):fn();rows.append({'check':label,'result':'PASS'})
 def reject(fn):
  try:fn()
  except (ValueError,TypeError,KeyError) as e:return str(e)
  raise AssertionError('unexpected acceptance')
 def pristine():assert m.enc(m.derive(ctx))==raw and m.validate(a.root,raw)['result']=='PASS'
 def original(label):return R/'review/independent-primary/residuals'/label
 try:
  check('legitimate original receipt',pristine)
  for label in ('managed-close-binding-one-byte','raw-close-ownership-one-byte','coordinated-close-bindings'):
   altered=dict(ctx['e']);altered[trace]=(original(label)/'altered-trace.json').read_bytes()
   if a.reproduce:
    old=module(R/'original/code/smoke_occurrences.py');oldctx=old.load(a.root);oldctx['e']=altered
    assert len(old.semantic(oldctx,altered)['frames'])==18
    oldraw=old.enc(old.derive(oldctx));assert oldraw==(original(label)/'derived-receipt.json').read_bytes()
    (a.output/(label+'-reproduction.json')).write_text(json.dumps({'original_semantic':'ACCEPTED','original_derived_matches_review':True,'trace':m.identity(altered[trace]),'receipt':m.identity(oldraw),'old_public_rejection':reject(lambda:old.validate(a.root,oldraw))},indent=2)+'\n')
   check('residual semantic '+label,lambda alt=altered:reject(lambda:m.semantic(ctx,alt)))
   sub=dict(ctx);sub['e']=altered;check('residual derive '+label,lambda sub=sub:reject(lambda:m.derive(sub)))
   changed=(original(label)/'derived-receipt.json').read_bytes();check('residual public '+label,lambda v=changed:reject(lambda:m.validate(a.root,v)))
  def mutate(label,fn):
   alt=dict(ctx['e']);t=json.loads(alt[trace]);fn(t);alt[trace]=m.enc(t)
   check(label,lambda:reject(lambda:m.semantic(ctx,alt)))
  def change(t,i,k):
   old=t['events'][i]['state'][k];t['events'][i]['state'][k]=('1' if old[0]!='1' else '2')+old[1:]
  for i in (7,8,32,33):
   for k in ('binding','ownership_binding'):mutate('close identity '+str(i)+' '+k,lambda t,i=i,k=k:change(t,i,k))
  for i in (7,32):
   for k in ('binding','ownership_binding'):
    mutate('coordinated entry-return '+str(i)+' '+k,lambda t,i=i,k=k:(change(t,i,k),change(t,i+1,k)))
  mutate('both raw and managed entry identities',lambda t:[change(t,i,k) for i in (7,32) for k in ('binding','ownership_binding')])
  mutate('all close identities coordinated',lambda t:[change(t,i,k) for i in (7,8,32,33) for k in ('binding','ownership_binding')])
  mutate('all constructor and close identities coordinated',lambda t:[change(t,i,k) for i in (6,7,8,14,32,33) for k in ('binding','ownership_binding')])
  mutate('swapped binding fields',lambda t:t['events'][32]['state'].update(binding=t['events'][32]['state']['ownership_binding'],ownership_binding=t['events'][32]['state']['binding']))
  mutate('missing entry identity',lambda t:t['events'][32]['state'].pop('binding'))
  mutate('invented entry identity',lambda t:t['events'][32]['state'].update(other='x'))
  mutate('nonstring entry identity',lambda t:t['events'][32]['state'].update(binding=0))
  # Same-context receipt mutation must not leak into future expectations.
  answer=m.validate(a.root,raw);answer['contexts'].clear();answer['receipt'].clear();check('SOC-01 returned mutations remain detached',pristine)
  d=m.derive(ctx);d['contexts'][0]['occurrences'][0]['source'].clear();d['contexts'][1]['joins'].clear();check('nested mutations remain detached',pristine)
  for i in (0,1):
   d=json.loads(raw);d['contexts'].pop(i);check('context still required '+str(i),lambda d=d:reject(lambda:m.validate(a.root,m.enc(d))))
  d=json.loads(raw)
  for v in d['contexts']:
   assert len([o for o in v['occurrences'] if o['kind']=='traced-invocation'])==18
   observer=[o for o in v['occurrences'] if o['kind']=='explicit-observer-call'];assert len(observer)==1 and observer[0]['frame'] is None and observer[0]['parent_frame'] is None
  check('18 traced plus separate observer preserved',lambda:None)
  check('final pristine',pristine)
 finally:
  after=(a.root/'code/smoke_occurrences.py').read_bytes()
  (a.output/'RESULT.json').write_text(json.dumps({'passed':len(rows),'checks':rows,'source_before':m.identity(before),'source_after':m.identity(after),'source_stable':before==after,'residuals_reproduced':3 if a.reproduce else 0,'scope':'New bounded close identity correction checks','database_connections':0,'host_session_execution':False,'completed_review_suites_rerun':False},indent=2)+'\n')
  assert before==after
 print('PASS',len(rows),'new close-identity controls')
if __name__=='__main__':main()
