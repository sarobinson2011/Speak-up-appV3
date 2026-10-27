"""New SOC correction controls; old supplied/independent suites are not invoked."""
import argparse,copy,json,os,subprocess,sys,types
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def guard(e,a):
 if e in ('sqlite3.connect','socket.connect','socket.bind'):raise AssertionError('FORBIDDEN:'+e)
 if e=='open' and isinstance(a[0],(str,bytes)) and os.fsdecode(a[0]).startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
sys.addaudithook(guard)
def profile(f,event,arg):
 if event=='call' and f.f_code.co_filename.rsplit('/',1)[-1] in ('live_connection.py','authority.py','lab_bootstrap.py','worker.py'):raise AssertionError('RUNTIME-EXECUTION')
sys.setprofile(profile)
def load(root):
 p=root/'code/smoke_occurrences.py';m=types.ModuleType('corrected');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=R/'corrected');p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=False)
 source_before=(a.root/'code/smoke_occurrences.py').read_bytes()
 m=load(a.root);ctx=m.load(a.root);raw=(a.root/'results/occurrence-connection.json').read_bytes();records=[]
 def good(label,fn):fn();records.append({'check':label,'result':'PASS'})
 def reject(fn):
  try:fn()
  except (ValueError,TypeError,KeyError) as e:return {'type':type(e).__name__,'message':str(e)}
  raise AssertionError('mutation accepted')
 def invariant():assert m.enc(m.derive(ctx))==raw and m.validate(a.root,raw)['result']=='PASS'
 try:
  good('pristine derivation and public acceptance',invariant)
  for label,fn in [('clear',lambda x:x.clear()),('pop',lambda x:x.pop()),('reverse',lambda x:x.reverse()),('duplicate',lambda x:x.__setitem__(1,x[0]))]:
   answer=m.validate(a.root,raw);fn(answer['contexts']);w=(R/'review/independent-primary'/('SOC-01-'+label)/'accepted-receipt.json').read_bytes()
   good('SOC-01 rejected '+label,lambda w=w:reject(lambda:m.validate(a.root,w)))
   good('pristine unaffected after '+label,invariant)
  for label,fn in [
   ('returned receipt identity',lambda d:d['receipt'].update(bytes=0,sha256='0'*64)),
   ('returned result fields',lambda d:d.update(actual_admission=True,result='anything')),
   ('returned nested contexts',lambda d:d['contexts'].__setitem__(0,{'nested':['SYMBOLIC-U-TWO']}))]:
   answer=m.validate(a.root,raw);fn(answer);good(label+' detached',invariant)
  for label,fn in [
   ('occurrence source',lambda d:d['contexts'][0]['occurrences'][0]['source'].update(sha256='0'*64)),
   ('nested declaration',lambda d:d['contexts'][0]['declarations'][0].update(type='anything')),
   ('nested duty',lambda d:d['contexts'][0]['joins']['managed:normal']['duty']['obligations'].clear()),
   ('nested producer',lambda d:d['contexts'][1]['joins']['managed:entry']['producer'].clear()),
   ('limits',lambda d:d['limits'].update(actual_admission=True)),
   ('instance',lambda d:d['contexts'][1]['instance'].clear()),
   ('record declaration',lambda d:d['contexts'][0]['record_declaration_joins'][0]['declaration'].clear()),
   ('whole contexts',lambda d:d['contexts'].clear())]:
   d=m.derive(ctx);fn(d);good('derived '+label+' receipt rejects',lambda d=d:reject(lambda:m.validate(a.root,m.enc(d))));good('derived '+label+' leaves pristine',invariant)
  trace='evidence/execution-trace.json'
  for label in ['constructor-epoch','unwatched-old-main','main-return-bool','main-invented-self-state','resume-nonboolean']:
   altered=dict(ctx['e']);altered[trace]=(R/'review/independent-primary'/('SOC-02-'+label)/'altered-trace.json').read_bytes()
   good('SOC-02 semantic '+label,lambda alt=altered:reject(lambda:m.semantic(ctx,alt)))
   sub=dict(ctx);sub['e']=altered;good('SOC-02 derive '+label,lambda sub=sub:reject(lambda:m.derive(sub)))
   w=(R/'review/independent-primary'/('SOC-02-'+label)/'derived-receipt.json').read_bytes();good('SOC-02 public '+label,lambda w=w:reject(lambda:m.validate(a.root,w)))
  def coordinated(t):
   for i in (11,12):t['events'][i]['state']['_epoch']=7
  def coherent_offset(t):
   for v in t['events']:
    if v['state'] and '_epoch' in v['state']:v['state']['_epoch']+=4
    if v['function']=='ManagedAuthority.status' and 'value' in v:v['value']['connection_epoch']+=4
    if v['function']=='ManagedAuthority.recover' and 'value' in v:v['value']['status']['connection_epoch']+=4
  mutations=[('constructor adjacent epoch',lambda t:t['events'][11]['state'].update(_epoch=1)),('constructor negative epoch',lambda t:t['events'][11]['state'].update(_epoch=-1)),('constructor bool epoch',lambda t:t['events'][11]['state'].update(_epoch=False)),('constructor phase',lambda t:t['events'][11]['state'].update(_phase='READY')),('constructor reason',lambda t:t['events'][11]['state'].update(_reason='other')),('constructor extra attr',lambda t:t['events'][11]['state'].update(binding='x')),('constructor call state',lambda t:t['events'][10]['state'].update(_epoch=0)),('coordinated constructor and recovery',coordinated),('coordinated all epoch values',coherent_offset),('main float zero',lambda t:t['events'][39].update(value=0.0)),('main none return',lambda t:t['events'][39].update(value=None)),('free function empty snapshot',lambda t:t['events'][0].update(state={})),('wrapper invented self snapshot',lambda t:t['events'][24].update(state={'_epoch':1})),('client invented attr',lambda t:t['events'][26]['state'].update(_phase='READY')),('authority missing attr',lambda t:t['events'][14]['state'].pop('ownership_binding')),('authority call invented attr',lambda t:t['events'][13]['state'].update(binding='x')),('status missing phase',lambda t:t['events'][17]['state'].pop('_phase')),('validation wrong reason',lambda t:t['events'][16]['state'].update(_reason='other')),('close call epoch',lambda t:t['events'][31]['state'].update(_epoch=2)),('integer false resume',lambda t:t['events'][0].update(resumed_generator=0)),('string resume',lambda t:t['events'][29].update(resumed_generator='true')),('integer normal flag',lambda t:t['events'][34].update(normal_return=1)),('boolean parent',lambda t:t['events'][1].update(parent=True)),('boolean frame',lambda t:t['events'][0].update(frame=True)),('boolean line',lambda t:t['events'][0].update(line=True)),('wrong supported caller',lambda t:t['events'][27].update(parent=1))]
  for label,fn in mutations:
   t=json.loads(ctx['e'][trace]);fn(t);alt=dict(ctx['e']);alt[trace]=m.enc(t);good('adjacent semantic '+label,lambda alt=alt:reject(lambda:m.semantic(ctx,alt)))
  # Fully coordinated path substitution including source-compatible lines still
  # fails the observer watch predicate, before relying on archive identity.
  alt=dict(ctx['e']);t=json.loads(alt[trace]);path=m.WORK+'/reviewed-boundary/retained/launcher/code/lab_bootstrap.py'
  for v in (t['events'][0],t['events'][-1]):v['path']=path
  t['events'][0]['line']=188;t['events'][-1]['line']=194;t['events'][-1]['value']=None;alt[trace]=m.enc(t)
  good('coordinated historical main semantic',lambda:reject(lambda:m.semantic(ctx,alt)))
  alt=dict(ctx['e']);t=json.loads(alt[trace])
  for v in t['events']:
   v['frame']+=20
   if v['parent'] is not None:v['parent']+=20
  alt[trace]=m.enc(t);closed=json.loads(alt['evidence/confirmed-close.json']);closed['normal_close_event']=t['events'][34];alt['evidence/confirmed-close.json']=m.enc(closed)
  good('coordinated frame renumbering',lambda:reject(lambda:m.semantic(ctx,alt)))
  # Distinct context and observer identity constraints continue independently.
  for index in (0,1):
   d=json.loads(raw);d['contexts'].pop(index);good('each context independently required '+str(index),lambda d=d:reject(lambda:m.validate(a.root,m.enc(d))))
   d=json.loads(raw);d['contexts'][index]['occurrences'][-1]['frame']=16;good('observer no invented frame '+str(index),lambda d=d:reject(lambda:m.validate(a.root,m.enc(d))))
  good('final pristine after all mutations',invariant)
 finally:
  source_after=(a.root/'code/smoke_occurrences.py').read_bytes()
  (out/'RESULT.json').write_text(json.dumps({'passed':len(records),'checks':records,'source_before':m.identity(source_before),'source_after':m.identity(source_after),'source_stable':source_before==source_after,'scope':'New SOC correction controls only','database_connections':0,'host_execution':False,'completed_review_reruns':0},indent=2)+'\n')
  assert source_before==source_after,'source changed during controls'
 print('PASS',len(records),'SOC controls')
if __name__=='__main__':main()
