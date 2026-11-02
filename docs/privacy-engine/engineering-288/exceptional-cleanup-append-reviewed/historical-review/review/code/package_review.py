"""Package verified, immutable review evidence after all processes have exited.
This does not execute a validator, producer, session or earlier review.
"""
from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,stat,collections,re,sys
sys.path.insert(0,str(Path(__file__).parent))
from integrity import identity,enc,js,INPUT
base=Path(__file__).resolve().parents[1];work=base.parent;output=work/'Formal-Lab6-I164-exceptional-cleanup-append-independent-review.zip'
def reconcile(name):
 p=base/'results'/name;result=js((p/'RESULT.json').read_bytes());progress=[js(s) for s in (p/'progress.jsonl').read_bytes().splitlines()];stdout=(base/'processes'/name/'stdout.log').read_text().splitlines();numbered=[s for s in stdout if re.match(r'^\d+ ',s)]
 assert result['rows']==progress and result['checks']==len(progress)==len(numbered)
 for i,(row,line) in enumerate(zip(progress,numbered),1):assert line==f"{i} {row['check']} {row['result']}"
 exit=js((base/'processes'/name/'exit-status.json').read_bytes());return {'result':result['result'],'rows':len(progress),'row_types':dict(collections.Counter(x['result'] for x in progress)),'exit':exit,'completed_group':result['error'] is None,'environment':result['environment']}
groups={n:reconcile(n) for n in ('source-slot3','source-completion','public-recovered')};main=groups['public-recovered'];assert main['completed_group'] and main['exit']['returncode']==0 and not main['exit']['timed_out'];assert main['row_types'].get('DEFECT-OBSERVED')==4
summary=js((base/'results/public-recovered/final-focused-summary.json').read_bytes());assert summary['candidate_false_flag_accepted'] is True
for label in ('audit','audit-completion'):
 exit=js((base/'processes'/label/'exit-status.json').read_bytes());groups[label]={'rows':0,'validator_projector_calls':0,'exit':exit,'completed_group':exit['returncode']==0}
supplied=js((base/'results/audit-completion/AUDIT.json').read_bytes());integrity=js((base/'results/integrity.json').read_bytes());assert identity(INPUT.read_bytes())==integrity['input']
calls=js((base/'results/public-recovered/calls.json').read_bytes());root='/workspace/review-evidence/FL6-cleanup-append-20261101/recovered';current=root+'/code/correspondence.py';previous=root+'/retained/details/code/correspondence.py';counts={label:dict(collections.Counter(c['function'] for c in calls if c['file']==path)) for label,path in [('current',current),('unchanged_predecessor',previous)]}
assert counts['current']['_basis']==1 and counts['current']['validate']==3 and counts['unchanged_predecessor']['validate']>=1
checkpoint={'reviewer':'Formal-Lab[6], author-independent reviewer; not construction author','construction_author':'SU-Engineering[288D]','target':'I164-exceptional-cleanup-append-correspondence-1.zip','target_identity':integrity['input'],'target_entries':3982,'target_manifested_hashes':3981,'verdict':'NOT ACCEPTED AS COMPLETE: EC-01 normal-append terminal-exception classification is inconsistent with the retained pending constructor error','finding':{'id':'EC-01','candidate_source':'code/managed_coverage.py:2952','validated_core':'code/correspondence.py:_construct_checked','scope':'Conditional constructed projection/output comparison; no runtime loss, false admission, or altered saved public receipt asserted','smallest_witness':'review/results/public-recovered/EC01-smallest-case.json','actual_accepted_result':'review/results/public-recovered/EC01-accepted-result.json','single_field_counterpart':'review/results/public-recovered/EC01-source-consistent-one-field-output.json','accepted_value':False,'source_consistent_terminal_exception_value':True,'pending_original_preserved_in_other_fields':True,'contexts':2,'control_prefixes':2,'full_public_negative_derivation':False},'fresh_independent_groups_separate':groups,'engineering_separate':{k:supplied[k] for k in ('source-1','recovered','primary')},'validation_layers':js((base/'results/public-recovered/validation-layers.json').read_bytes()),'actual_monitored_call_counts':counts,'prior_LD01_closure_reused':True,'previous_bounded_source_support_carried_forward_unchanged':True,'unqualified_combined_control_total':None,'preservation':{'candidate_implementation':'UNCHANGED','both_acquisitions':'SEPARATE','obligations':11,'inventory_UNKNOWN':4,'lifetime_UNKNOWN':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','admission':False},'limits':['Saved inputs only; no actual close/append or selected runtime chain observation','Conditional owner/local/method/list continuity, no physical identity/exclusivity proof','Initial reference states and opaque outcomes are constructed premises, not demonstrated feasible history','No line172 error append or later outer cleanup expansion','Non-None constructor route remains open','Observer remains unjoined','Monitoring support only within retained cooperative CPython3.12.14 profile','Cleanup failure, repeated interruption, termination, alternate interpreters and hostile replacement qualifications retained','Cryptography50.0.2 test environment does not newly qualify any prepared host or installed wheel'], 'operations':{'implementation_changes':0,'application_runtime_operations':0,'requests':0,'acquisitions':0,'database_connections':0,'session_operations':0,'Git_saves':0,'policy_changes':0,'completed_campaign_replays':0},'confirmed_save_reused':'c43954ff5ee384c6fb6e7a85d83eb36bfea342d1'}
(base/'CHECKPOINT.json').write_bytes(enc(checkpoint))
report=(base/'REVIEW.txt').read_text();assert 'EC-01' in report and 'NOT ACCEPTED AS COMPLETE' in report and '1,300' in report and '165' in report
files={'input/I164-exceptional-cleanup-append-correspondence-1.zip':INPUT}
for n in ('REVIEW.txt','RECOVERY.txt','CHECKPOINT.json'):files[n]=base/n
for sub in ('code','results','processes'):
 for p in sorted((base/sub).rglob('*')):
  assert not p.is_symlink()
  if p.is_file():files['review/'+p.relative_to(base).as_posix()]=p
manifest={n:identity(p.read_bytes()) for n,p in files.items()};assert len(files)==len(set(files))
with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in files.items():
  pp=PurePosixPath(n);assert not pp.is_absolute() and all(x not in ('','.','..') for x in n.split('/'))
  info=zipfile.ZipInfo(n);info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_STORED if n.startswith('input/') else zipfile.ZIP_DEFLATED;z.writestr(info,p.read_bytes())
 info=zipfile.ZipInfo('MANIFEST.json');info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,enc(manifest))
with zipfile.ZipFile(output) as z:
 assert z.testzip() is None;assert set(z.namelist())==set(manifest)|{'MANIFEST.json'} and len(z.namelist())==len(manifest)+1
 for n,p in manifest.items():assert identity(z.read(n))==p,n
pin={'filename':output.name,**identity(output.read_bytes()),'entries':len(manifest)+1,'manifested_hashes':len(manifest),'CRC':'PASS','safe_exact_membership_hashes':'PASS','input_archive_preserved_exact':True};(work/'Formal-Lab6-I164-exceptional-cleanup-append-checkpoint-identity.json').write_bytes(enc(pin));print(json.dumps(pin,sort_keys=True),flush=True)
