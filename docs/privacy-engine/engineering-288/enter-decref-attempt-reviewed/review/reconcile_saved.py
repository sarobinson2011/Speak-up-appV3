"""Read-only record reconciliation. No candidate imports, validation or old campaign replay."""
from bytes_only import B,read,save,fid,ident,safe
import json,collections
H=B/'host';F=B/'focused';R=B/'candidate'
def lines(p):return [json.loads(x) for x in p.read_text().splitlines()]
def main():
 src=fid(H/'inputs/I164-enter-decref-attempt-1-source.zip');s=read(F/'SOURCE-CHECKPOINT.json');assert src=={k:s[k] for k in ('bytes','sha256')} and s['entries']==49 and s['manifested_hashes']==48
 f=F/'attempt-1';raw=f/'raw';res=read(raw/'RESULT.json');rows=lines(raw/'progress.jsonl');out=lines(f/'stdout.log')
 assert out[:-1]==rows==[read(p) for p in sorted(raw.glob('[0-9][0-9][0-9][0-9].json'))]
 assert out[-1]=={'event':'RESULT','result':res} and [r['sequence'] for r in rows]==list(range(1,751))
 counts=dict(collections.Counter(x['status'] for x in rows));assert counts=={'PASS':213,'REJECTED':537} and res['counts']==dict(counts,FAIL=0) and res['rows']==750 and res['result']=='PASS'
 chunks=[read(p) for p in sorted((f/'chunks').glob('*.json'))];assert len(chunks)==786
 for stream in ('stdout','stderr'):
  parts=[]
  for c in chunks:
   safe(c['path']);rawbytes=(f/c['path']).read_bytes();assert ident(rawbytes)=={k:c[k] for k in ('bytes','sha256')}
   if c['stream']==stream:parts.append(rawbytes)
  assert b''.join(parts)==(f/(stream+'.log')).read_bytes()
 assert {c['path'] for c in chunks}=={p.relative_to(f).as_posix() for p in (f/'chunks').glob('*.bin')}
 ex=read(f/'exit.json');assert ex['returncode']==0 and ex['timed_out'] is False and ex['automatic_retry'] is False and read(f/'launch.json')['source_sha256']==src['sha256']
 supplied=read(F/'RECONCILIATION.json');layers={}
 for x in rows:layers.setdefault(x['layer'],collections.Counter())[x['status']]+=1
 assert layers==supplied['layer_counts'] and supplied['counts']==counts and supplied['individual_rows']==supplied['progress_rows']==supplied['stdout_rows']==750 and supplied['explicit_exit']==ex
 save(B/'focused-record-audit.json',{'status':'PASS','rows':750,'counts':counts,'layers':layers,'source':src,'exact_individual_progress_stdout_RESULT_agreement':True,'chunks':786,'streams':{s:fid(f/(s+'.log')) for s in ('stdout','stderr')},'exit':ex,'qualifications':res['qualifications'],'replayed':False})
 print('750 supplied rows reconciled without replay',flush=True)
 p=H/'validation/process';r=H/'validation/results';cap=read(p/'capture.json');ex=read(p/'exit.json');ix=lines(p/'chunk-index.jsonl')
 for stream in ('stdout','stderr'):
  cc=cap['chunks'][stream];assert [{k:v for k,v in x.items() if k!='stream'} for x in ix if x['stream']==stream]==cc
  assert [x['sequence'] for x in cc]==list(range(1,len(cc)+1));parts=[]
  for x in cc:safe(x['path']);bb=(p/x['path']).read_bytes();assert ident(bb)==x['identity'];parts.append(bb)
  bb=b''.join(parts);assert bb==(p/(stream+'.log')).read_bytes()==(p/(stream+'-captured.bin')).read_bytes()
  assert ident(bb)==cap['streams'][stream]==ex['streams'][stream]
  assert {x['path'] for x in cc}=={q.relative_to(p).as_posix() for q in (p/(stream+'-chunks')).glob('*')}
 assert len(cap['chunks']['stdout'])==275 and len(cap['chunks']['stderr'])==0
 ev=lines(r/'events.jsonl');stdout=(p/'stdout.log').read_text().splitlines();assert len(ev)==276 and all(x.startswith('EVENT ') for x in stdout) and ev==[json.loads(x[6:]) for x in stdout]
 select={'computation-progress','dummy-computation-phase','actual-authenticated-basis-returned','public-validator-entered','public-validator-departed','focused-case-start'}
 phases=lines(p/'computation-phases.jsonl');assert phases==[e for e in ev if e['event'] in select] and len(phases)==cap['recorded_computation_events']
 progress=[e for e in ev if e['event']=='computation-progress'];snapshots=sorted(r.glob('phase-counts-*.json'));assert len(progress)==len(snapshots)==220
 for i,(event,snapshot) in enumerate(zip(progress,snapshots),1):
  snap=read(snapshot);assert event['sequence']==i and event['entered']==sum(snap['entered'].values()) and event['returned']==sum(snap['returned'].values()) and event['abrupt_or_None_qualified']==sum(snap['abrupt_or_None_qualified'].values()) and event['active']==len(snap['active'])
 assert progress[-1]['entered']==progress[-1]['returned']==17827 and progress[-1]['abrupt_or_None_qualified']==progress[-1]['active']==0
 assert not any(k.startswith('code/correspondence.py::_construct_checked') for k in read(snapshots[-1])['entered'])
 captures=[e for e in ev if e['event']=='actual-authenticated-basis-returned'];assert len(captures)==1 and captures[0]['capture_count']==1
 plan=read(H/'PLAN.json');prefix=plan['workspace']+'/candidate/';calls=read(r/'calls.json');assert all(c['function']=='validate' for c in calls)
 counts=collections.Counter(c['file'].removeprefix(prefix) for c in calls)
 parents=['retained/return','retained/return/retained/enter','retained/return/retained/enter/retained/lookup','retained/return/retained/enter/retained/lookup/retained/r1','retained/return/retained/enter/retained/lookup/retained/r1/retained/helper-open']
 assert counts['code/correspondence.py']==1 and all(counts[x+'/code/correspondence.py']==0 for x in parents) and counts[parents[-1]+'/retained/write-call/code/correspondence.py']==1
 entries=[e for e in ev if e['event']=='public-validator-entered'];departures=[e for e in ev if e['event']=='public-validator-departed']
 assert collections.Counter(e['source'].split('::')[0] for e in entries)==counts and collections.Counter(e['source'] for e in entries)==collections.Counter(e['source'] for e in departures)
 assert all(e['departure']=='returned-value' and e['result']=='PASS' for e in departures)
 res=read(r/'RESULT.json');public=read(r/'actual-public-result.json');prov=read(r/'actual-parent-provenance.json')
 assert res['result']=='PASS' and res['failure'] is None and res['public_result']==public and res['enter_decref_public_call_count']==res['full_public_positive']==1 and res['actual_returned_basis_captured'] is True
 assert res['receipt_agreements']==dict.fromkeys(('enter','enter_decref','helper','lookup','r1','return'),True) and res['thin_wrapper_calls']==dict.fromkeys(('return','enter','lookup','R1','helper'),0)
 assert res['full_public_negative_derivations']==res['focused_checks_replayed']==res['historical_checks_replayed']==0
 assert ex['child_exit']==0 and ex['timed_out'] is False and ex['automatic_retries']==0 and ex['kill_sent'] is False and ex['termination_requested'] is None and ex['supervisor_failure'] is None
 service=read(H/'service-exit.json');manager=read(H/'manager-exit.json');assert service['exit']==0 and manager['SERVICE_RESULT']=='success' and manager['EXIT_CODE']=='exited' and manager['EXIT_STATUS']=='0'
 expected=H/'expected/expected-enter-decref-receipt.json';actual=r/'actual-derived-receipt.json';assert expected.read_bytes()==actual.read_bytes();pin=fid(actual)
 compare=read(r/'actual-receipt-comparison.json');assert pin==compare['expected']==compare['actual']==plan['expected_receipt']==public['receipt'] and public['contexts']==plan['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and public['actual_admission'] is False
 assert prov['thin_return_enter_lookup_R1_helper_validate_wrappers_called'] is False
 pairs=[('return',R/'reference/return/actual-receipt.json'),('enter',R/parents[0]/'reference/enter/actual-receipt.json'),('lookup',R/parents[1]/'reference/lookup/actual-receipt.json'),('r1',R/parents[2]/'reference/r1/actual-receipt.json'),('helper',R/parents[3]/'reference/receipts/prepared-helper-open-attempt.json')]
 for key,path in pairs:assert fid(path)==plan[key+'_receipt']==prov[('R1' if key=='r1' else key)+'_receipt']
 recon=read(H/'validation/RECONCILIATION.json');assert recon['child_exit']==ex and recon['result_identity']==fid(r/'RESULT.json') and recon['expected_receipt']==pin
 save(B/'host-record-audit.json',{'status':'PASS','event_records':276,'snapshots':220,'chunks':{s:len(c) for s,c in cap['chunks'].items()},'streams':cap['streams'],'event_counts':dict(collections.Counter(e['event'] for e in ev)),'public_calls':dict(counts),'actual_basis_capture':captures[0],'provenance':prov,'receipt':pin,'receipt_bytes_equal':True,'last_computation':progress[-1],'child_exit':ex,'service_exit':service,'manager_exit':manager,'public_positives':1,'fresh_public_runs':0,'full_public_negative_derivations':0,'constructed_path_execution':'UNEXECUTED','events_add_controls':False})
 print('276 events / 220 snapshots / 275 chunks / one actual basis and public positive reconciled',flush=True)
 prepared=read(H/'PREPARED.json');reservation=read(H/'ONE-ATTEMPT-RESERVATION.json');launch=read(H/'LAUNCH-RECEIPT.json');process=read(p/'process.json');pl=read(p/'launch.json')
 assert reservation['attempt']==reservation['authorization']==plan['attempt']==res['attempt']==launch['attempt']
 assert reservation['bundle']==prepared['bundle'] and reservation['source_archive']==prepared['source_archive']==plan['source_archive']==src
 assert reservation['expected_receipt']==prepared['expected_receipt']==pin and reservation['enter_decref_public_calls_authorized']==1 and reservation['automatic_retries']==0
 assert pl['command'][0]==plan['python']==prepared['python'] and pl['supervisor_identity']==process['supervisor']
 assert process['child']['boot_id']==process['supervisor']['boot_id'] and int(process['child']['proc_start_ticks'])>=int(process['supervisor']['proc_start_ticks'])
 assert prepared['utc']<reservation['utc']<launch['utc']<pl['started_utc']<res['finished_utc']<ex['finished_utc']<service['utc']<manager['utc']
 profile=read(H/'service-runtime-profile.json');ep=read(H/'code/expected-runtime.json');assert profile==read(H/'host-profile.stdout') and profile['matches'] is True and profile['differences']==[] and profile['prohibited_host_paths']==[]
 assert {k:v for k,v in profile['actual'].items() if k!='observation_only'}=={k:v for k,v in ep.items() if k!='observation_only'} and profile['actual']['observation_only']['executable']==plan['python']
 for n in ('host-profile.exit.json','byte-recovery.exit.json','service-launch.exit.json'):assert read(H/n)['exit']==0 and read(H/n)['timeout'] is False
 for n in ('assembled-root.json','service-root-verification.json','validation/results/input-root.json','validation/results/final-root.json'):assert read(H/n)=={'files':4271,'directories':1197,'exact_types_membership_hashes':'PASS'}
 for n,k in [('RETURN-ROOT-MANIFEST.json','return_root_manifest'),('ASSEMBLED-ROOT-MANIFEST.json','assembled_root_manifest'),('ENTER-ROOT-MANIFEST.json','enter_root_manifest'),('LOOKUP-ROOT-MANIFEST.json','lookup_root_manifest'),('R1-ROOT-MANIFEST.json','r1_root_manifest')]:assert fid(H/'expected'/n)==plan[k]
 save(B/'host-identity-audit.json',{'status':'PASS','reservation':reservation,'prepared':prepared,'launch':launch,'process_launch':pl,'process':process,'runtime':profile,'preparation_pins':len(read(H/'MANIFEST.json')),'omitted_preparation_zip':'recorded consistently; its pinned members verified, no separate outer ZIP verification claimed','chronology':'current attempt reservation/start/finish on 10 November 2026; inherited enter-return event names retained; prepared-only states historical','fresh_host_probe':False})
 receipt=read(actual);old=read(R/'reference/return/actual-receipt.json');rel='enter_decref_attempt_correspondence'
 assert receipt['format']=='I164-ENTER-DECREF-ATTEMPT-1' and len(receipt['contexts'])==len(old['contexts'])==2
 for ctx,prior in zip(receipt['contexts'],old['contexts']):assert {k:v for k,v in ctx.items() if k!=rel}==prior
 assert receipt['prior_enter_return_components']==old['extension_components'] and receipt['prior_enter_return_receipt']==fid(R/'reference/return/actual-receipt.json')
 ignored={'format','contexts','extension_components','prior_enter_return_components','prior_enter_return_receipt','new_enter_decref_attempt_limits'}
 assert {k:v for k,v in receipt.items() if k not in ignored}=={k:v for k,v in old.items() if k not in ('format','contexts','extension_components')}
 for n,pin in receipt['extension_components'].items():assert fid(R/'code'/n)==pin
 for ctx in receipt['contexts']:
  row=ctx[rel];parent=ctx['enter_return_res_correspondence'];assert row['instance_anchor']==parent['instance_anchor'] and row['scope']==parent['scope']
  assert row['predecessor_validation']==prov['return_validation'] and row['separate_observer']==parent['separate_observer']
  assert row['runtime_chain'] is None and row['observer_join'] is None and row['classification']=='UNKNOWN' and row['actual_admission'] is False
 assert receipt['inventory_unknown_totals']==4 and receipt['lifetime_unknown_totals']==14
 save(B/'inheritance-audit.json',{'status':'PASS','all_prior_context_fields':'exact equality in both contexts','all_unaffected_top_level_fields':'exact equality','new_relation':rel,'new_limits':receipt['new_enter_decref_attempt_limits'],'eleven_obligations':'inherited values unchanged','unknown_totals':[4,14],'component_pins':'actual corrected code bytes','deeper_receipt_bindings':prov})
 print('reservation/runtime/root identity, chronology and receipt inheritance reconciled',flush=True)
if __name__=='__main__':
 try:main();save(B/'record-audit.exit.json',{'exit':0,'failure':None})
 except BaseException as e:save(B/'record-audit.exit.json',{'exit':1,'failure':repr(e)});raise
