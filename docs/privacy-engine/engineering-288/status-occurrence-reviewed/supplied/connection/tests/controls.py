"""New offline connection controls only. No prior control suite is invoked."""
import copy, importlib.util, json, os, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def audit(event,args):
 if event in ('sqlite3.connect','socket.connect','socket.bind'):raise AssertionError('FORBIDDEN-OPERATION:'+event)
 if event=='open' and isinstance(args[0],str) and args[0].startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
sys.addaudithook(audit)
spec=importlib.util.spec_from_file_location('connection',ROOT/'code/smoke_occurrences.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False);results=[]
def check(name,f):
 f();results.append({'name':name,'result':'PASS'})
def rejected(f):
 try:f()
 except (ValueError,KeyError,TypeError,FileNotFoundError):return
 raise AssertionError('mutation accepted')
ctx=m.load(ROOT);e=ctx['e'];receipt=(ROOT/'results/occurrence-connection.json').read_bytes()
def mutate(member,fn):
 altered=dict(e);v=json.loads(e[member]);fn(v);altered[member]=m.enc(v);return altered
def neg(name,member,fn):check(name,lambda:rejected(lambda:m.semantic(ctx,mutate(member,fn))))
try:
 check('legitimate saved connection exact serialization',lambda:m.validate(ROOT,receipt))
 t='evidence/execution-trace.json'
 for name,fn in [
 ('completion normal flag',lambda d:d['events'][34].update(normal_return=False)),
 ('yield mislabeled normal',lambda d:d['events'][23].update(normal_return=True)),
 ('return opcode',lambda d:d['events'][34].update(opcode='RAISE_VARARGS')),
 ('return source line',lambda d:d['events'][34].update(line=999)),
 ('caller parent',lambda d:d['events'][27].update(parent=1)),
 ('caller substitution',lambda d:d['events'][27].update(function='run_controlled')),
 ('historical source path',lambda d:d['events'][0].update(path='/home/steve/old/entry.py')),
 ('missing close',lambda d:d['events'].pop(34)),
 ('duplicate occurrence',lambda d:d['events'].append(copy.deepcopy(d['events'][-1]))),
 ('incomplete final return',lambda d:d['events'].pop()),
 ('invented generator resume',lambda d:d['events'][29].update(resumed_generator=False)),
 ('epoch substitution',lambda d:d['events'][18]['value'].update(connection_epoch=2)),
 ('reason substitution',lambda d:d['events'][18]['value'].update(reason='changed')),
 ('recovery renewal',lambda d:d['events'][19]['value'].update(new_attempt_authorized=True)),
 ('close phase',lambda d:d['events'][34]['state'].update(_phase='READY')),
 ('raw authority ownership swap',lambda d:d['events'][6]['state'].update(ownership_binding='0'*64)),
 ('invented offset',lambda d:d['events'][18].update(offset=0)),
 ('main failed exit',lambda d:d['events'][39].update(value=1))]:neg(name,t,fn)
 for name,member,fn in [
 ('state frame invented','evidence/client-handoff.json',lambda d:d[0].update(frame=16)),
 ('state caller changed','evidence/client-handoff.json',lambda d:d[0].update(observer_call_site='launcher')),
 ('capability exposure','evidence/client-handoff.json',lambda d:d[0]['public_methods'].append('status')),
 ('state differs','evidence/client-handoff.json',lambda d:d[0]['state'].update(seq=1)),
 ('handoff interval','evidence/client-handoff.json',lambda d:d[0].update(observed_before='2026-01-01')),
 ('altered completion','evidence/session-records/BOOTSTRAP-COMPLETE.json',lambda d:d['status'].update(phase='CLOSED')),
 ('close summary changed','evidence/confirmed-close.json',lambda d:d.update(active_marker_absent=False)),
 ('removed retained evidence','evidence/confirmed-close.json',lambda d:(d['before'].clear(),d['after'].clear())),
 ('changed database identity','evidence/confirmed-close.json',lambda d:d['after']['state/session.sqlite'].update(sha256='0'*64)),
 ('mixed session workspace','evidence/session-records/binding.json',lambda d:d.update(candidate='/home/steve/old/candidate')),
 ('stale entry','evidence/SMOKE-ABOUT-TO-START.json',lambda d:d['entry'].update(sha256='0'*64)),
 ('stale worker','preparation/preparation-identity.json',lambda d:d['worker'].update(sha256='0'*64)),
 ('mixed ownership incarnation','evidence/recovery-export-0.json',lambda d:d.update(ownership_meta=m.enc({'incarnation':'old'}).hex())),
 ('unexpected journal','evidence/recovery-export-0.json',lambda d:d['journal'].append(['fabricated'])),
 ('process failure','evidence/smoke-process-result.json',lambda d:d.update(returncode=1)),
 ('summary output substitution','evidence/output-check.json',lambda d:d.update(exact_fixed_stdout=False)),
 ('result admission','evidence/smoke-result.json',lambda d:d.update(actual_admission=True))]:neg(name,member,fn)
 for name,member,raw in [('stdout diagnostic','evidence/smoke.stdout',b'{"phase":"READY"}\n'),('stderr traceback','evidence/smoke.stderr',b'Traceback\n'),('summary instead of trace',t,b'{"result":"PASS"}')]:
  altered=dict(e);altered[member]=raw;check(name,lambda a=altered:rejected(lambda:m.semantic(ctx,a)))
 # Output consumers recompute; they cannot accept a detached summary or mutated context.
 for name,fn in [
 ('missing context',lambda d:d['contexts'].pop()),
 ('mixed contexts',lambda d:d['contexts'][0].update(context='SYMBOLIC-U-TWO')),
 ('merged invocations',lambda d:d['contexts'][0]['occurrences'].pop()),
 ('invented observer frame',lambda d:d['contexts'][0]['occurrences'][-1].update(frame=16)),
 ('changed occurrence acquisition',lambda d:d['contexts'][0]['occurrences'][0]['call'].update(acquisition='legacy')),
 ('changed instance',lambda d:d['contexts'][0]['instance'].update(ownership_incarnation='legacy')),
 ('duty discharge',lambda d:d['contexts'][0]['joins']['managed:normal']['duty'].update(disposition='ESTABLISHED')),
 ('inventory total resolved',lambda d:d.update(inventory_unknown_totals=0)),
 ('stale status binding',lambda d:d['status_binding'].update(sha256='0'*64))]:
  obj=json.loads(receipt);fn(obj);check(name,lambda v=m.enc(obj):rejected(lambda:m.validate(ROOT,v)))
 check('alternate serialization',lambda:rejected(lambda:m.validate(ROOT,json.dumps(json.loads(receipt),indent=2).encode())))
 def process(root,label):
  p=subprocess.run([sys.executable,'-I','-B',str(root/'code/smoke_occurrences.py'),'check',str(root/'results/occurrence-connection.json'),'--root',str(root)],capture_output=True)
  (out/(label+'.stdout')).write_bytes(p.stdout);(out/(label+'.stderr')).write_bytes(p.stderr);assert p.returncode==0,p.stderr.decode()
 check('fresh-process legitimate',lambda:process(ROOT,'fresh'))
 recovered=out/'recovered-root';recovered.mkdir()
 for name in ('code','inputs','retained'):shutil.copytree(ROOT/name,recovered/name)
 (recovered/'results').mkdir();(recovered/'results/occurrence-connection.json').write_bytes(receipt)
 check('recovered-root fresh-process legitimate',lambda:process(recovered,'recovered'))
 rr=recovered/'retained/correction'
 for name,make,remove in [
 ('undeclared empty directory',lambda p:p.mkdir(),lambda p:p.rmdir()),
 ('undeclared FIFO',lambda p:os.mkfifo(p),lambda p:p.unlink()),
 ('undeclared symlink',lambda p:p.symlink_to('code'),lambda p:p.unlink())]:
  p=rr/'unexpected';make(p)
  try:check(name,lambda:rejected(lambda:m.load(recovered)))
  finally:remove(p)
 for name in ('code/prospective_entry.py','contract/DECISION.json','basis/candidate/managed-route/model.json'):
  p=rr/name;b=p.read_bytes();p.write_bytes(b+b' ')
  try:check('stale recovered '+name,lambda:rejected(lambda:m.load(recovered)))
  finally:p.write_bytes(b)
 p=recovered/'inputs/smoke.zip';b=p.read_bytes();p.write_bytes(b+b'x')
 try:check('altered acquisition archive',lambda:rejected(lambda:m.load(recovered)))
 finally:p.write_bytes(b)
 check('saved result remains unchanged',lambda:m.need((ROOT/'results/occurrence-connection.json').read_bytes()==receipt,'MUTATED-RESULT'))
finally:
 (out/'RESULT.json').write_bytes(m.enc({'passed':len(results),'checks':results,'scope':'New offline connection only; no prior reviews, smoke, pipelines or sessions rerun','database_connections':0,'host_execution':False}))
print('PASS',len(results),'new connection controls')
