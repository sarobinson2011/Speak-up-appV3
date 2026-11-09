"""Independent read-only reconciliation; no candidate imports or validation calls.
Uses the review's exact byte helpers. Prior review's stream-reconciliation pattern is reused.
"""
from review_bytes import HERE,ident,fid,read,save,safe
import collections,json
H=HERE/'host';F=HERE/'focused';R=HERE/'candidate'
def lines(p):return [json.loads(x) for x in p.read_text().splitlines()]
def main():
 src=fid(H/'inputs/I164-enter-call-attempt-1-source.zip')
 p=H/'validation/process';r=H/'validation/results';cap=read(p/'capture.json');ex=read(p/'exit.json');ix=lines(p/'chunk-index.jsonl')
 for s in ('stdout','stderr'):
  cc=cap['chunks'][s];assert [{k:v for k,v in c.items() if k!='stream'} for c in ix if c['stream']==s]==cc
  assert [c['sequence'] for c in cc]==list(range(1,len(cc)+1));parts=[]
  for c in cc:
   safe(c['path']);b=(p/c['path']).read_bytes();assert ident(b)==c['identity'];parts.append(b)
  b=b''.join(parts);assert b==(p/(s+'.log')).read_bytes()==(p/(s+'-captured.bin')).read_bytes()
  assert ident(b)==cap['streams'][s]==ex['streams'][s]
  assert {c['path'] for c in cc}=={q.relative_to(p).as_posix() for q in (p/(s+'-chunks')).glob('*')}
 ev=lines(r/'events.jsonl');out=(p/'stdout.log').read_text().splitlines()
 assert len(ev)==272 and all(x.startswith('EVENT ') for x in out) and ev==[json.loads(x[6:]) for x in out]
 selected={'computation-progress','dummy-computation-phase','actual-authenticated-basis-returned','public-validator-entered','public-validator-departed','focused-case-start'}
 phases=lines(p/'computation-phases.jsonl');assert phases==[e for e in ev if e['event'] in selected] and len(phases)==cap['recorded_computation_events']
 progress=[e for e in ev if e['event']=='computation-progress'];snaps=sorted(r.glob('phase-counts-*.json'));assert len(progress)==len(snaps)==216
 for i,(e,q) in enumerate(zip(progress,snaps),1):
  v=read(q);assert e['sequence']==i and e['entered']==sum(v['entered'].values()) and e['returned']==sum(v['returned'].values()) and e['abrupt_or_None_qualified']==sum(v['abrupt_or_None_qualified'].values()) and e['active']==len(v['active'])
 assert progress[-1]['entered']==progress[-1]['returned']==17812 and progress[-1]['active']==progress[-1]['abrupt_or_None_qualified']==0
 captures=[e for e in ev if e['event']=='actual-authenticated-basis-returned'];assert len(captures)==1 and captures[0]['capture_count']==1
 plan=read(H/'PLAN.json');prefix=plan['workspace']+'/candidate/';calls=read(r/'calls.json');callcounts=collections.Counter(c['file'].removeprefix(prefix) for c in calls)
 assert all(c['function']=='validate' for c in calls)
 assert callcounts['code/correspondence.py']==1
 parents=['retained/lookup','retained/lookup/retained/r1','retained/lookup/retained/r1/retained/helper-open']
 assert all(callcounts[x+'/code/correspondence.py']==0 for x in parents)
 assert callcounts[parents[-1]+'/retained/write-call/code/correspondence.py']==1
 entries=[e for e in ev if e['event']=='public-validator-entered'];departures=[e for e in ev if e['event']=='public-validator-departed']
 assert collections.Counter(e['source'].split('::')[0] for e in entries)==callcounts
 assert collections.Counter(e['source'] for e in entries)==collections.Counter(e['source'] for e in departures)
 assert all(e['departure']=='returned-value' and e['result']=='PASS' for e in departures)
 result=read(r/'RESULT.json');pub=read(r/'actual-public-result.json');prov=read(r/'actual-parent-provenance.json')
 assert result['result']=='PASS' and result['failure'] is None and result['public_result']==pub and result['enter_public_call_count']==result['full_public_positive']==1
 assert result['actual_returned_basis_captured'] is True and result['receipt_agreements']==dict.fromkeys(('enter','lookup','r1','helper'),True)
 assert result['thin_wrapper_calls']==dict.fromkeys(('lookup','R1','helper'),0)
 assert result['focused_checks_replayed']==result['historical_checks_replayed']==result['full_public_negative_derivations']==0
 assert ex['child_exit']==0 and ex['timed_out'] is False and ex['automatic_retries']==0 and ex['kill_sent'] is False and ex['termination_requested'] is None and ex['supervisor_failure'] is None
 service=read(H/'service-exit.json');manager=read(H/'manager-exit.json');assert service['exit']==0 and manager['SERVICE_RESULT']=='success' and manager['EXIT_CODE']=='exited' and manager['EXIT_STATUS']=='0'
 actual=r/'actual-derived-receipt.json';expected=H/'expected/expected-enter-receipt.json';assert actual.read_bytes()==expected.read_bytes()
 receiptid=fid(actual);comp=read(r/'actual-receipt-comparison.json');assert receiptid==comp['actual']==comp['expected']==plan['expected_receipt']==pub['receipt']
 assert pub['contexts']==plan['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and pub['actual_admission'] is False
 assert prov['thin_lookup_R1_helper_validate_wrappers_called'] is False
 assert prov['lookup_receipt']==fid(R/'reference/lookup/actual-receipt.json')==plan['lookup_receipt']
 assert prov['R1_receipt']==fid(R/'retained/lookup/reference/r1/actual-receipt.json')==plan['r1_receipt']
 assert prov['helper_receipt']==fid(R/'retained/lookup/retained/r1/reference/receipts/prepared-helper-open-attempt.json')==plan['helper_receipt']
 recon=read(H/'validation/RECONCILIATION.json');assert recon['child_exit']==ex and recon['result_identity']==fid(r/'RESULT.json') and recon['expected_receipt']==receiptid
 save(HERE/'host-record-audit.json',{'status':'PASS','events':dict(collections.Counter(e['event'] for e in ev)),'event_records':len(ev),'snapshots':len(snaps),'streams':cap['streams'],'chunks':{s:len(c) for s,c in cap['chunks'].items()},'public_calls':dict(callcounts),'actual_basis_capture':captures[0],'provenance':prov,'last_computation':progress[-1],'receipt':receiptid,'receipt_bytes_equal':True,'child_exit':ex,'service_exit':service,'manager_exit':manager,'public_positives':1,'full_public_negative_derivations':0,'fresh_launches':0,'events_are_controls':False})
 print('272 events / 216 snapshots / one positive and capture / exits reconciled',flush=True)
 reservation=read(H/'ONE-ATTEMPT-RESERVATION.json');prepared=read(H/'PREPARED.json');launch=read(H/'LAUNCH-RECEIPT.json');process=read(p/'process.json');pl=read(p/'launch.json')
 assert reservation['attempt']==reservation['authorization']==plan['attempt']==launch['attempt']==result['attempt']
 assert reservation['bundle']==prepared['bundle'] and reservation['source_archive']==prepared['source_archive']==src==plan['source_archive']
 assert reservation['expected_receipt']==prepared['expected_receipt']==receiptid and reservation['enter_public_calls_authorized']==1 and reservation['automatic_retries']==0
 assert pl['command'][0]==plan['python']==prepared['python'] and pl['supervisor_identity']==process['supervisor']
 assert process['child']['boot_id']==process['supervisor']['boot_id'] and int(process['child']['proc_start_ticks'])>int(process['supervisor']['proc_start_ticks'])
 assert prepared['utc']<reservation['utc']<launch['utc']<pl['started_utc']<result['finished_utc']<ex['finished_utc']<service['utc']<manager['utc']
 profile=read(H/'service-runtime-profile.json');pre=read(H/'host-profile.stdout');ep=read(H/'code/expected-runtime.json')
 assert profile==pre and profile['matches'] is True and profile['differences']==[] and profile['prohibited_host_paths']==[]
 assert {k:v for k,v in profile['actual'].items() if k!='observation_only'}=={k:v for k,v in ep.items() if k!='observation_only'}
 assert profile['actual']['observation_only']['executable']==plan['python']
 for n in ('host-profile.exit.json','byte-recovery.exit.json','service-launch.exit.json'):assert read(H/n)['exit']==0 and read(H/n)['timeout'] is False
 for n in ('assembled-root.json','service-root-verification.json','validation/results/input-root.json','validation/results/final-root.json'):assert read(H/n)=={'files':4169,'directories':1169,'exact_types_membership_hashes':'PASS'}
 for n,k in [('ASSEMBLED-ROOT-MANIFEST.json','assembled_root_manifest'),('LOOKUP-ROOT-MANIFEST.json','lookup_root_manifest'),('R1-ROOT-MANIFEST.json','r1_root_manifest')]:assert fid(H/'expected'/n)==plan[k]
 save(HERE/'host-identity-audit.json',{'status':'PASS','reservation':reservation,'prepared':prepared,'launch':launch,'process_launch':pl,'process':process,'runtime':profile,'preparation_manifest_members':len(read(H/'MANIFEST.json')),'preparation_zip_outer_digest':'recorded consistently, omitted archive not reconstructed; preparation members authenticated by export and member manifest','chronology':'preparation-only states remain historical; later result and explicit exits establish saved completion','fresh_host_probe':False})
 receipt=read(actual);old=read(R/'reference/lookup/actual-receipt.json');relation='enter_call_attempt_correspondence'
 assert receipt['format']=='I164-ENTER-CALL-ATTEMPT-1'
 for ctx,prior in zip(receipt['contexts'],old['contexts']):assert {k:v for k,v in ctx.items() if k!=relation}==prior
 assert receipt['prior_lookup_components']==old['extension_components'] and receipt['prior_lookup_receipt']==fid(R/'reference/lookup/actual-receipt.json')
 ignored={'format','contexts','extension_components','prior_lookup_components','prior_lookup_receipt','new_enter_call_limits'}
 assert {k:v for k,v in receipt.items() if k not in ignored}=={k:v for k,v in old.items() if k not in {'format','contexts','extension_components'}}
 for n,pin in receipt['extension_components'].items():assert fid(R/'code'/n)==pin
 for ctx in receipt['contexts']:
  row=ctx[relation];parent=ctx['context_special_lookup_correspondence'];assert row['instance_anchor']==parent['instance_anchor'] and row['scope']==parent['scope']
  assert row['predecessor_validation']==prov['lookup_validation'] and row['separate_observer']==parent['separate_observer']
  assert row['runtime_chain'] is None and row['observer_join'] is None and row['classification']=='UNKNOWN' and row['actual_admission'] is False
 assert receipt['inventory_unknown_totals']==4 and receipt['lifetime_unknown_totals']==14
 save(HERE/'inheritance-audit.json',{'status':'PASS','all_prior_context_fields':'exact equality both contexts','all_unaffected_top_level_fields':'exact equality','new_relation':relation,'receipt':receiptid,'eleven_obligations':'exact preserved inherited values','unknown_totals':[4,14],'new_limits':receipt['new_enter_call_limits'],'no_public_rerun':True})
 print('host identity chronology, runtime profile and receipt inheritance reconciled',flush=True)
if __name__=='__main__':
 try:main();save(HERE/'record-audit-continuation.exit.json',{'exit':0,'failure':None})
 except BaseException as e:save(HERE/'record-audit-continuation.exit.json',{'exit':1,'failure':repr(e)});raise
