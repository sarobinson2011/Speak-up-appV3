"""Read-only reconciliation of supplied records, never executes their campaigns."""
from pathlib import Path
import json,hashlib,collections,traceback,ast
B=Path(__file__).resolve().parent;H=B/'host';R=B/'candidate';A=B/'author-results'
def read(p):return json.loads(p.read_bytes())
def jl(p):return [json.loads(x) for x in p.read_text().splitlines()]
def fid(p):return {'bytes':p.stat().st_size,'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()}
def bid(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(n,v):(B/n).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def focused():
 groups=read(A/'GROUPS.json');src=read(A/'SOURCE.json');assert {k:src[k] for k in ('bytes','sha256')}==fid(H/'inputs'/src['filename'])
 expected={'source-rows':(55,15,40),'matrix-one':(43,19,24),'matrix-two':(43,19,24),'mutations-one':(74,13,61),'mutations-two':(74,13,61)}
 allrows=[];index=[];records=[]
 for g in groups:
  name=g['batch'];d=A/name;raw=d/'raw';rows=[read(p) for p in sorted(raw.glob('[0-9][0-9][0-9][0-9].json'))];stdout=jl(d/'stdout.log');result=read(raw/'RESULT.json');ex=read(d/'exit.json');launch=read(d/'launch.json')
  assert rows==jl(raw/'progress.jsonl')==[x['row'] for x in stdout if x.get('event')=='CONTROL']
  assert [x['sequence'] for x in rows]==list(range(1,len(rows)+1));assert [x['result'] for x in stdout if x.get('event')=='RESULT']==[result]
  counts=collections.Counter(x['status'] for x in rows);assert (len(rows),counts['PASS'],counts['REJECTED'])==expected[name]
  assert result['rows']==g['rows']==len(rows) and result['counts']==g['counts']=={k:counts[k] for k in ('PASS','REJECTED','FAIL')}
  assert result['result']=='PASS' and result['guard']=={'forbidden_calls':0} and result['public_authentication']=='UNEXECUTED' and result['authenticated_constructed_path']=='UNEXECUTED' and result['full_public_negative_derivations']==0
  assert ex==g['exit'] and ex['returncode']==0 and ex['timed_out'] is False and ex['automatic_retry'] is False
  assert launch['source_manifest']==g['source_manifest']==fid(R/'MANIFEST.json') and launch['batch']==name
  chunks=sorted((d/'chunks').glob('*.json'));streams={'stdout':[],'stderr':[]}
  for ch in chunks:
   item=read(ch);p=d/item['path'];assert fid(p)=={k:item[k] for k in ('bytes','sha256')};streams[item['stream']].append(p.read_bytes())
  assert len(chunks)==ex['captured_chunks']
  for s,parts in streams.items():assert b''.join(parts)==(d/(s+'.log')).read_bytes()
  assert (d/'stderr.log').read_bytes()==b''
  for row in rows:
   index.append({k:row[k] for k in ('batch','layer','name','sequence','status')}|{'raw':f"{name}/raw/{row['sequence']:04d}.json"})
  allrows+=rows;records.append({'batch':name,'counts':dict(counts),'rows':len(rows),'exit':ex,'raw_progress_stdout_result_exact':True,'chunks':len(chunks),'layers':dict(collections.Counter(x['layer'] for x in rows))})
 assert read(A/'COMBINED-INDEX.json')==index and len(allrows)==289
 save('supplied-focused-audit.json',{'status':'PASS','source':src,'groups':records,'counts':dict(collections.Counter(x['status'] for x in allrows)),'total':289,'campaigns_replayed':0,'full_public_negative_derivations':0,'historical_groups':'separate, no new credit','author_failures':read(A/'FAILURES.json')})
def host():
 p=H/'validation/process';r=H/'validation/results';cap=read(p/'capture.json');ex=read(p/'exit.json');ix=jl(p/'chunk-index.jsonl');plan=read(H/'PLAN.json')
 for stream in ('stdout','stderr'):
  chunks=cap['chunks'][stream];assert [{k:v for k,v in x.items() if k!='stream'} for x in ix if x['stream']==stream]==chunks
  assert [x['sequence'] for x in chunks]==list(range(1,len(chunks)+1));parts=[]
  for x in chunks:assert fid(p/x['path'])==x['identity'];parts.append((p/x['path']).read_bytes())
  bb=b''.join(parts);assert bb==(p/(stream+'.log')).read_bytes()==(p/(stream+'-captured.bin')).read_bytes()
  assert bid(bb)==cap['streams'][stream]==ex['streams'][stream]
  assert {x['path'] for x in chunks}=={q.relative_to(p).as_posix() for q in (p/(stream+'-chunks')).glob('*')}
 ev=jl(r/'events.jsonl');lines=(p/'stdout.log').read_text().splitlines();assert len(ev)==286 and all(x.startswith('EVENT ') for x in lines) and ev==[json.loads(x[6:]) for x in lines]
 selection={'computation-progress','dummy-computation-phase','actual-authenticated-basis-returned','public-validator-entered','public-validator-departed','focused-case-start'}
 assert jl(p/'computation-phases.jsonl')==[e for e in ev if e['event'] in selection] and len(jl(p/'computation-phases.jsonl'))==cap['recorded_computation_events']
 progress=[e for e in ev if e['event']=='computation-progress'];snaps=sorted(r.glob('phase-counts-*.json'));assert len(progress)==len(snaps)==230
 for i,(event,snap) in enumerate(zip(progress,snaps),1):
  o=read(snap);assert event['sequence']==i and event['entered']==sum(o['entered'].values()) and event['returned']==sum(o['returned'].values()) and event['abrupt_or_None_qualified']==sum(o['abrupt_or_None_qualified'].values()) and event['active']==len(o['active'])
 assert progress[-1]['entered']==progress[-1]['returned']==17857 and progress[-1]['active']==progress[-1]['abrupt_or_None_qualified']==0
 assert not any(k.startswith('code/correspondence.py::_construct_checked') for k in read(snaps[-1])['entered'])
 capture=[e for e in ev if e['event']=='actual-authenticated-basis-returned'];assert len(capture)==1 and capture[0]['capture_count']==1
 prefix=plan['workspace']+'/candidate/';calls=read(r/'calls.json');assert all(c['function']=='validate' for c in calls)
 counts=collections.Counter(c['file'].removeprefix(prefix) for c in calls);parents=[];path=''
 for part in ('res-null','fast','decref','return','enter','lookup','r1','helper-open'):path+=('' if not path else '/')+'retained/'+part;parents.append(path)
 assert counts['code/correspondence.py']==1 and all(counts[x+'/code/correspondence.py']==0 for x in parents) and counts[parents[-1]+'/retained/write-call/code/correspondence.py']==1
 entered=[e for e in ev if e['event']=='public-validator-entered'];returned=[e for e in ev if e['event']=='public-validator-departed']
 assert len(entered)==len(returned)==26 and collections.Counter(e['source'].split('::')[0] for e in entered)==counts and collections.Counter(e['source'] for e in entered)==collections.Counter(e['source'] for e in returned)
 assert all(e['departure']=='returned-value' and e['result']=='PASS' for e in returned)
 result=read(r/'RESULT.json');public=read(r/'actual-public-result.json');prov=read(r/'actual-parent-provenance.json');cmp=read(r/'actual-receipt-comparison.json')
 assert result['result']=='PASS' and result['failure'] is None and result['public_result']==public and result['exit_decref_public_call_count']==result['full_public_positive']==1 and result['actual_returned_basis_captured'] is True
 assert result['receipt_agreements']==dict.fromkeys(('exit_decref','res_null','fast','decref','return','enter','lookup','r1','helper'),True) and result['thin_wrapper_calls']==dict.fromkeys(('res_null','fast','decref','return','enter','lookup','R1','helper'),0)
 assert result['full_public_negative_derivations']==result['focused_checks_replayed']==result['historical_checks_replayed']==result['new_authenticated_constructed_call_count']==0
 assert ex['child_exit']==0 and ex['timed_out'] is False and ex['automatic_retries']==0 and ex['kill_sent'] is False and ex['supervisor_failure'] is None and ex['termination_requested'] is None
 service=read(H/'service-exit.json');manager=read(H/'manager-exit.json');assert service['exit']==0 and manager['SERVICE_RESULT']=='success' and manager['EXIT_CODE']=='exited' and manager['EXIT_STATUS']=='0'
 expected=H/'expected/expected-exit-decref-receipt.json';actual=r/'actual-derived-receipt.json';assert expected.read_bytes()==actual.read_bytes();pin=fid(actual)
 assert pin==cmp['expected']==cmp['actual']==plan['expected_receipt']==public['receipt'] and public['contexts']==plan['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
 assert prov['thin_res_null_fast_decref_return_enter_lookup_R1_helper_validate_wrappers_called'] is False
 location=R;receipts={}
 for key,part in [('res_null','res-null'),('fast','fast'),('decref','decref'),('return','return'),('enter','enter'),('lookup','lookup'),('r1','r1')]:
  q=location/'reference'/part/'actual-receipt.json';assert fid(q)==plan[key+'_receipt']==prov[('R1' if key=='r1' else key)+'_receipt'];receipts[key]=fid(q);location=location/'retained'/part
 q=location/'reference/receipts/prepared-helper-open-attempt.json';assert fid(q)==plan['helper_receipt']==prov['helper_receipt'];receipts['helper']=fid(q)
 recon=read(H/'validation/RECONCILIATION.json');assert recon['child_exit']==ex and recon['result_identity']==fid(r/'RESULT.json') and recon['expected_receipt']==pin
 prep=read(H/'PREPARED.json');reservation=read(H/'ONE-ATTEMPT-RESERVATION.json');launch=read(H/'LAUNCH-RECEIPT.json');pl=read(p/'launch.json');process=read(p/'process.json')
 assert reservation['attempt']==reservation['authorization']==plan['attempt']==result['attempt']==launch['attempt']
 assert reservation['bundle']==prep['bundle'] and reservation['source_archive']==prep['source_archive']==plan['source_archive']==fid(H/'inputs/I164-exit-decref-attempt-1-source.zip')
 assert reservation['expected_receipt']==prep['expected_receipt']==pin and reservation['exit_decref_public_calls_authorized']==1 and reservation['automatic_retries']==0
 assert pl['command'][0]==plan['python']==prep['python'] and pl['supervisor_identity']==process['supervisor'] and process['child']['boot_id']==process['supervisor']['boot_id']
 assert int(process['child']['proc_start_ticks'])>=int(process['supervisor']['proc_start_ticks'])
 assert prep['utc']<reservation['utc']<launch['utc']<pl['started_utc']<result['finished_utc']<ex['finished_utc']<service['utc']<manager['utc']
 profile=read(H/'service-runtime-profile.json');ep=read(H/'code/expected-runtime.json');assert profile==read(H/'host-profile.stdout') and profile['matches'] is True and profile['differences']==[] and profile['prohibited_host_paths']==[]
 assert {k:v for k,v in profile['actual'].items() if k!='observation_only'}=={k:v for k,v in ep.items() if k!='observation_only'}
 for n in ('host-profile.exit.json','byte-recovery.exit.json','service-launch.exit.json'):assert read(H/n)['exit']==0 and read(H/n)['timeout'] is False
 for n in ('assembled-root.json','service-root-verification.json','validation/results/input-root.json','validation/results/final-root.json'):assert read(H/n)=={'files':4963,'directories':1264,'exact_types_membership_hashes':'PASS'}
 save('saved-host-audit.json',{'status':'PASS','attempt':plan['attempt'],'event_rows':len(ev),'snapshots':len(snaps),'chunks':{s:len(v) for s,v in cap['chunks'].items()},'stream_identities':cap['streams'],'last_computation':progress[-1],'events_not_controls':True,'public_calls':dict(counts),'actual_basis_capture':capture[0],'receipt':pin,'exact_bytes_equal':True,'receipt_provenance':prov,'child_exit':ex,'wrapper_exit':service,'manager_exit':manager,'reservation':reservation,'prepared':prep,'launch':launch,'process':process,'runtime':profile,'public_positives':1,'fresh_public_runs':0,'full_public_negative_derivations':0,'authenticated_constructed_path':'UNEXECUTED','outer_preparation_zip':'recorded identity consistent; only its91 retained preparation files verified, not omitted outer zip bytes','chronology':'preparation-only states historical'})
 current=read(actual);old=read(R/'reference/res-null/actual-receipt.json');rel='exit_decref_attempt_correspondence'
 for ctx,prior in zip(current['contexts'],old['contexts']):assert {k:v for k,v in ctx.items() if k!=rel}==prior
 assert current['prior_res_null_components']==old['extension_components'] and current['prior_res_null_receipt']==receipts['res_null']
 ignored={'format','contexts','extension_components','prior_res_null_components','prior_res_null_receipt','new_exit_decref_attempt_limits'}
 assert {k:v for k,v in current.items() if k not in ignored}=={k:v for k,v in old.items() if k not in ('format','contexts','extension_components')}
 for n,pin in current['extension_components'].items():assert fid(R/'code'/n)==pin
 for ctx in current['contexts']:
  row=ctx[rel];parent=ctx['res_null_test_correspondence'];assert row['instance_anchor']==parent['instance_anchor'] and row['scope']==parent['scope'] and row['predecessor_validation']==prov['res_null_validation'] and row['separate_observer']==parent['separate_observer']
  assert row['runtime_chain'] is None and row['observer_join'] is None and row['classification']=='UNKNOWN' and row['actual_admission'] is False
 assert current['inventory_unknown_totals']==4 and current['lifetime_unknown_totals']==14
 save('inheritance-audit.json',{'status':'PASS','all_inherited_context_and_unaffected_top_level_fields':'byte-decoded exact equality','current_format':current['format'],'new_limits':current['new_exit_decref_attempt_limits'],'eleven_obligations':'unchanged inherited inputs','unknown_totals':[4,14],'source_pins':current['extension_components']})
if __name__=='__main__':
 try:focused();host();save('saved-record-audit.exit.json',{'exit':0,'error':None});print('Supplied289 and saved public positive reconciled separately.')
 except BaseException as e:save('saved-record-audit.exit.json',{'exit':1,'error':repr(e)});raise
