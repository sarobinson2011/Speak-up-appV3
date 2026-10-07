import signal
signal.alarm(55) # OS default termination; native descendants use parent-death SIGKILL.
import resource,tempfile,time
from worker import *
def main():
 t=Path(sys.argv[1]);m=core.load_json(sys.argv[2]);records=[];started=time.monotonic();cap=64*1048576
 with tempfile.TemporaryDirectory(prefix='attempt-',dir=t) as tmp:
  d=Path(tmp);core.keygen(d/'key');a=time.monotonic();core.initialize(d/'data',d/'key',m,cap);init=time.monotonic()-a
  with core.Job(d/'data',d/'key') as j:
   a=time.monotonic();j.services('emit');j.services('validate');index_start=time.monotonic()-a;ready=j.ready.copy()
   old=j.produce
   def produce(c,o):
    a=time.monotonic();v=old(c,o);records.append({'stage':'generation_with_spool_fsync_and_exact_check','bytes':v['bytes'],'seconds':time.monotonic()-a,'worker_seconds':v['seconds']});return v
   j.produce=produce;oldask=j.validator.ask
   def ask(q):
    a=time.monotonic();v=oldask(q);records.append({'stage':'independent_validation_including_spool_hash','seconds':time.monotonic()-a,'worker_seconds':v['seconds'],'offset':v['offset'],'rss_kib':v['rss_kib']});return v
   j.validator.ask=ask;a=time.monotonic();r=j.step();steady=time.monotonic()-a
   need(not r['complete'],'probe must not finish retained stream');first=r.copy()
   if m['model']['sha256']==core.MODEL:need(r['consumed_sha256']=='b48c77645a5d6826203730fca8262b20c3eb969c4a011293b2c70c9cad64a41e','first 64 MiB correspondence with recorded 4V bounded prefix')
   j.step(17,7);interrupted=j.state['offset'];peak=j.peak_disk
  (d/'data/spool.bin').unlink();a=time.monotonic()
  with core.Job(d/'data',d/'key') as j:
   # Missing active spool exercises exact cursor regeneration and parser continuation.
   resumed=j.step();recovery=time.monotonic()-a;need(j.state['metrics']['spool_regenerations']==1 and j.state['offset']>interrupted,'recovery progress');metrics=j.state['metrics'];peak=max(peak,j.peak_disk)
  return {'result':'PASS-BOUNDED-GENERATION-AND-INDEPENDENT-VALIDATION-PROBE','wall_seconds':time.monotonic()-started,'initialization_seconds':init,'persistent_index_startup_seconds':index_start,'ready':ready,'records':records,'first_complete_spool_step_seconds':steady,'first_prefix':first,'recovery_seconds_including_input_rehash_index_reload_and_spool_regeneration':recovery,'recovery_result':resumed,'metrics':metrics,'peak_job_file_bytes':peak,'parent_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'measurement_only':True,'full_retained_validation':False,'actual_admission':False}
if __name__=='__main__':
 try:print(json.dumps(main(),separators=(',',':')))
 except BaseException as e:print(json.dumps({'result':'PROBE-FAILED','detail':str(e),'actual_admission':False}));sys.exit(2)
