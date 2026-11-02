"""Write closure report and self-contained verified checkpoint after completion.
No validator or producer is executed here.
"""
from pathlib import Path,PurePosixPath
import sys,json,zipfile,stat,collections,re
sys.path.insert(0,str(Path(__file__).parent))
from intake import identity,enc,js,INPUT,AREA,PIN
base=Path(__file__).resolve().parents[1];workspace=base.parent
def load(p):return js(p.read_bytes())
res=load(base/'results/public-recovered/RESULT.json');exit=load(base/'processes/public-recovered/exit-status.json');assert res['error'] is None and exit['returncode']==0 and not exit['timed_out']
rows=[js(s) for s in (base/'results/public-recovered/progress.jsonl').read_bytes().splitlines()];assert rows==res['rows'] and len(rows)==res['checks']
numbered=[s for s in (base/'processes/public-recovered/stdout.log').read_text().splitlines() if re.match(r'^\d+ ',s)];assert len(numbered)==len(rows)
for i,(row,line) in enumerate(zip(rows,numbered),1):assert line==f"{i} {row['check']} {row['result']}"
counts=dict(collections.Counter(r['result'] for r in rows));assert set(counts)<={'PASS','REJECTED'}
calls=load(base/'results/public-recovered/calls.json');root=str(AREA/'recovered');callcounts={label:dict(collections.Counter(c['function'] for c in calls if c['file']==path)) for label,path in [('current',root+'/code/correspondence.py'),('unchanged_predecessor',root+'/retained/details/code/correspondence.py')]};assert callcounts['current']['validate']==callcounts['current']['_basis']==1 and callcounts['unchanged_predecessor']['validate']==1
for n,pin in load(base/'results/public-recovered/review-check-identities.json').items():assert identity((base/'code'/n).read_bytes())==pin
intake=load(base/'results/intake.json');audit=load(base/'results/audit/AUDIT.json');summary=load(base/'results/public-recovered/closure-summary.json');assert summary['EC01'].startswith('CLOSED') and identity(INPUT.read_bytes())==PIN
layers=load(base/'results/public-recovered/validation-layers.json');recordedlayers={r['check']:r for r in layers['focused_rows']};assert set(recordedlayers)=={r['check'] for r in rows[3:]}
for r in rows[3:]:assert recordedlayers[r['check']]['result']==r['result']
layercounts=dict(collections.Counter(r['layer'] for r in layers['focused_rows']))
checkpoint={'reviewer':'Formal-Lab[6], author-independent of SU-Engineering[288D] construction','target':'I164-EC01-terminal-exception-correction-1.zip','input':PIN,'entries':57,'manifested_hashes':56,'verdict':'EC-01 CLOSED within the retained bounded conditional SOURCE-ONLY correspondence contract','residual_witness':None,'fresh_independent':{'rows':len(rows),'row_types':counts,'exit':exit,'environment':res['environment'],'stdout_progress_RESULT_reconciled':True,'layer_counts_excluding_first_three_public_positive_checks':layercounts,'actual_monitored_calls':callcounts,'full_current_public_positives':1,'actual_unchanged_predecessor_public_positives':1,'full_public_negative_derivations':0,'public_negative_calls':0},'supplied_controls_separate':audit['supplied'],'historical_independent_separate':audit['historical_independent_separate'],'historical_Engineering_separate':audit['historical_Engineering_separate'],'historical_zero_control_audit_failure_correction':audit['zero_control_audit_failure_and_correction'],'historical_NOT_ACCEPTED_verdict_preserved':audit['historical_verdict'],'new_preparation_failure':load(base/'failures/audit-syntax/RECORD.json'),'new_read_only_audit':{'exit':load(base/'processes/audit/exit-status.json'),'controls':0,'candidate_executions':0},'root_verification':intake['root'],'only_three_existing_content_files_changed':intake['existing_changed_files'],'root_manifest_change':'Replaced by exact ROOT-MANIFEST.json as declared; original manifest preserved byte-exact','prepared_receipt':intake['corrected_receipt'],'historical_receipt':intake['historical_receipt'],'receipt_only_changed_component_pins':intake['receipt_change_paths'],'preparation_is_validation':False,'retained_independent_review':intake['retained_review'],'prior_support_and_LD01':'Reused unchanged; no earlier suite replay','limits':['Constructed source correspondence, not observed cleanup/append execution','Conditional owner/local/method/list continuity; no physical identity/exclusivity proof','Initial reference states and opaque outcomes are premises, not feasible-runtime-history proof','No line172 or later cleanup expansion; no normal overall return or final rethrow established','Non-None construction and outer-cleanup gaps retained; observer unjoined','Monitoring qualifications remain limited to cooperative CPython3.12.14; cleanup failure/repeated interruption/termination/alternate interpreter/hostile replacement gaps retained','No new prepared-host or installed-wheel qualification'],'preserved':{'both_acquisitions':'SEPARATE','obligations':11,'inventory_UNKNOWN':4,'lifetime_UNKNOWN':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','admission':False},'confirmed_save_reused':'c43954ff5ee384c6fb6e7a85d83eb36bfea342d1','operations':{'implementation_changes':0,'application_runtime_changes':0,'acquisitions':0,'requests':0,'database_connections':0,'session_operations':0,'Git_saves':0,'completed_campaign_replays':0,'historical_missing_records_reconstructed':0},'unqualified_combined_total':None}
(base/'CHECKPOINT.json').write_bytes(enc(checkpoint))
report=f'''Formal-Lab[6] — independent EC-01 closure review

EC-01 CLOSED within the retained bounded conditional SOURCE-ONLY correspondence
contract. No residual witness was found in the focused checks. This closure does
not add runtime observations, expand outer cleanup or establish readiness.

Target: I164-EC01-terminal-exception-correction-1.zip.
Construction author: SU-Engineering[288D]. Independent reviewer: Formal-Lab[6].
The reviewer changed no candidate implementation, runtime source or evidence.

Integrity and exact recovery

The input is 153,799,952 bytes, 57 entries, SHA-256
ae83c5eeb7bf4ab09943f66f239bea3c7802777899f4fe6417e10e39dc9b1f71.
CRC, safe unique regular membership and all 56 manifested hashes passed. The
declared 20-member overlay reconstructs the exact ROOT-MANIFEST.json tree:
3,999 files / 1,103 directories, with 3,998 manifested content files. Its manifest
is 1,415,643 bytes, SHA-256
dd11a30a719b7058ed084ad700c27cf66abd9040d37235f2b6ad9a5152c44e53.

Exactly three existing content files changed: the one terminal-exception expression
in code/managed_coverage.py, the producer pin in code/correspondence.py, and the
omitted normal-path assertion in tests/cases.py. Exact byte substitutions and the
declared diff match. The adapter's function bodies and AST locations are unchanged.
The other 3,978 original manifested members are unchanged; 17 new ec01/ files were
added. The recovered root manifest is necessarily replaced by the declared root
manifest; its original bytes are preserved in ec01/original/MANIFEST.json.

The exact retained independent review and its embedded original candidate were
verified and recovered. The 3,771-file LD-01 predecessor retains its exact manifest
and all hashes. Original witness files, rejected verdict, receipts, failures and
records are unchanged. Prior bounded support and LD-01 closure are reused; no old
review or campaign was rerun. The correction is self-contained for byte recovery.

The historical receipt remains 13,408,039 bytes, SHA-256
f37342856f6b0f3ef9d79714a0d412e0273f09b85eb5a1adb5670a1f4accdefb.
The prepared current receipt has the same byte count and SHA-256
4b84be0804b2a0a5dd0cef421403fa2e608a703899c97196f4063b11b04df952.
Canonical comparison shows changes only within the two declared implementation
component pins. Contexts, declarations, obligations and other receipt content are
identical. Preparation was not counted as validation and did not repair any
submitted receipt.

Independent exception semantics and witness

lab_bootstrap.py:167–171 remains inside except BaseException as e. The validated
parent has completed details assignment with the selected constructor error still
pending and active. Normal selected close and append are successful suboperations;
they establish neither normal overall return nor the final rethrow. Therefore
terminal_python_exception_in_model remains exactly True. Replacement-error paths
also retain True, with the replacement as last pending and the original error
preserved separately. Process termination and unobserved frontiers retain None.
They do not manufacture a Python exception, unwind or completed cleanup.

The retained smallest EC-01 witness was submitted unchanged to corrected code and
rejected with CLEANUP-OUTPUT-CORRESPONDENCE. The retained counterpart that changes
only the terminal flag from False to True was accepted. The new accepted result
differs from the historical accepted result in that one flag only. The rejected
input remains unchanged. Source-consistent normal cases passed in both contexts
and both control prefixes. These checks used the actual returned authenticated
basis from this review's current public validation, not fixture agreement or
capture hashes alone.

Focused adjacent checks covered loop-evaluation replacement, inherited close
failure/partial outcomes, append failure, termination and missing observations.
Append failure preserves an established close return. Last acknowledged list
contents remain distinct from UNKNOWN partial effects. Wrong False/None/int/string
classifications, omitted flags, coordinated error disappearance, subclassed values,
containers and keys rejected at the recorded layers. Nested returned mutations
did not alter subsequent pristine expectations. The independent oracle comes from
the retained Formal-Lab source-derived case machinery plus the fresh source check;
Engineering's changed tests/cases.py oracle was inspected, not used by this review.
Line172 and later cleanup remain unexpanded.

Actual validation and accounting

One fresh isolated process validated ec01/receipts/prepared-cleanup-append.json on
the independently recovered root through the unchanged actual predecessor public
validator. It captured the returned basis passively; no validator, source, function
or authentication output was replaced. The exact new receipt matched authenticated
assembly. Normal post-public slot2/slot3 state was inspected; inherited interruption
and ownership campaigns were not rerun, and their qualifications remain unchanged.

The new independent group completed {len(rows)} rows: {counts.get('PASS',0)} PASS
and {counts.get('REJECTED',0)} REJECTED, with matching progress, stdout and RESULT;
exit 0, no timeout. There was exactly one current public positive and one required
unchanged predecessor public positive. No full public negative derivation or
public negative call is claimed. Negatives were authenticated-basis constructed/
output-comparison cores, exact-type gates before constructed parent validation,
or the authenticated-basis receipt-comparison core. Every focused row's layer is
recorded in validation-layers.json. Historical receipt rejection is a stale-code-pin
comparison, not a new finding against its original source version.

The process had a 3,600-second hard timeout and a 3,150-second control deadline to
reserve final-record time. Incremental logs, process identity, launch command,
stdout, stderr, calls, final integrity verification and explicit exit are retained.
Actual environment: {res['environment']['python']}; Cryptography
{res['environment']['cryptography']}, isolated Python, bytecode writes disabled,
optimization 0. This does not newly qualify another host, interpreter or wheel.

A reviewer audit syntax precheck failed before any controls or candidate code ran.
Its exact source and zero-control failure record are preserved. One unmatched
parenthesis in reviewer code was corrected, and the read-only audit then passed;
it made zero validator/projector calls. No new semantic control failed. This
preparation failure is not folded into completed control totals.

Supplied and historical records remain separate

Engineering's new 105 controls reconcile: 55 PASS, 50 REJECTED, exit 0. They were
inspected, not replayed or counted as independent. Its real public positive and
its core, exact-type and test-oracle layers retain their actual scope.

Engineering's earlier 46 completed source and 341 completed recovered-root controls
remain separate. The primary is still incomplete: 1,300 progress rows / 165 stdout
rows; stdout166–1300 is unavailable, discrepancy cause UNKNOWN. RESULT.json,
calls.json and final-verification.json remain absent. The withdrawn corroboration
claim, original failures, partial evidence and zero-replay audit are preserved.
Saved public positives do not complete that interrupted campaign.

Formal-Lab's earlier 170-row group retains four DEFECT-OBSERVED rows. Its 21-row
completion, 50-row failed source attempt, and zero-control audit failure/correction
remain separate. The earlier NOT ACCEPTED AS COMPLETE verdict remains historical
and unchanged. No missing records were reconstructed, no streams repaired and no
unqualified combined total asserted. Confirmed save
c43954ff5ee384c6fb6e7a85d83eb36bfea342d1 is reused without a Git operation.

Retained limits

These are conditional source-correspondence checks, not close/append runtime
observations. Selected-owner/local/method/list continuity remains a premise.
Initial reference states and opaque outcomes do not demonstrate feasible runtime
history. Physical identity, closure, durability and released ownership remain
unestablished. Non-None construction and other outer-cleanup gaps remain; the
observer is unjoined. CPython3.12.14 cooperative monitoring support retains cleanup
failure, repeated interruption, termination, alternate-interpreter and hostile
replacement qualifications. A free slot alone is not complete cleanup evidence.

Both acquisitions, all eleven obligations, four inventory and fourteen lifetime
UNKNOWN totals, Decision B, retention and allowances remain unchanged. SOURCE-ONLY;
cumulative-envelope unadopted; backup kernel-only; streams UNCOMPUTED; readiness/
final binding blocked; admission disabled. No implementation, application-runtime,
request, acquisition, database/session operation, completed-campaign replay, Git
save or policy change occurred.
'''
(base/'REVIEW.txt').write_text(report)
(base/'RECOVERY.txt').write_text('''Verify this checkpoint's delivery identity, ZIP CRC, unique safe regular membership
and all MANIFEST.json hashes before extraction into a new empty persistent root.
Do not overwrite existing evidence or use /tmp.

The exact input is input/I164-EC01-terminal-exception-correction-1.zip:
153799952 bytes; 57 entries; SHA-256
ae83c5eeb7bf4ab09943f66f239bea3c7802777899f4fe6417e10e39dc9b1f71.
Verify its 56 hashes and exact membership. Read its START-HERE.txt, README.txt,
RESULTS.json and RECOVERY.txt. Its retained review and embedded original candidate
are complete, exact dependencies. Apply only OVERLAY-MANIFEST.json members in byte
recovery and require the resulting exact ROOT-MANIFEST.json tree. The supplied
tools/recover.py documents that byte-only recovery; it executes no candidate code.
Preserve original partial files at their declared evidence locations, outside
strict predecessor inputs.

Active recovered adapter: code/correspondence.py. Current submitted receipt:
ec01/receipts/prepared-cleanup-append.json. Its identity is in CHECKPOINT.json and
review/results/public-recovered/submitted-receipt-identity.json. The unchanged
predecessor is retained/details with its LD01 corrected receipt. Historical root
receipts and NOT ACCEPTED verdicts retain their original source/version status.

Read REVIEW.txt, CHECKPOINT.json, intake/audit records and the new independent
process/result logs. The original witness is preserved inside the exact input;
the new corrected witness and accepted result are under review/results/public-
recovered. Check validation-layers.json before interpreting any rejection.

No validator execution is needed to recover this evidence. Included reviewer code
documents what ran; it is not authorization to rerun completed checks. Any separately
authorized future focused execution requires the retained cooperative CPython3.12.14
profile, exact current inputs, bounded process, incremental logs and explicit exit.
Never substitute a saved result, synthetic predecessor or mutable caller output
for actual public authentication. No runtime/session/database operations are allowed.

All existing obligations, UNKNOWNs, evidence limits and authority boundaries remain.
Admission remains disabled.
''')
files={'input/I164-EC01-terminal-exception-correction-1.zip':INPUT}
for n in ('REVIEW.txt','CHECKPOINT.json','RECOVERY.txt'):files[n]=base/n
for sub in ('code','results','processes','failures'):
 for p in sorted((base/sub).rglob('*')):
  assert not p.is_symlink()
  if p.is_file():files['review/'+p.relative_to(base).as_posix()]=p
manifest={n:identity(p.read_bytes()) for n,p in files.items()};dest=workspace/'Formal-Lab6-I164-EC01-independent-closure.zip'
with zipfile.ZipFile(dest,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in files.items():
  assert n==str(PurePosixPath(n)) and not PurePosixPath(n).is_absolute() and all(x not in ('','.','..') for x in n.split('/'));info=zipfile.ZipInfo(n);info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_STORED if n.startswith('input/') else zipfile.ZIP_DEFLATED;z.writestr(info,p.read_bytes())
 info=zipfile.ZipInfo('MANIFEST.json');info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,enc(manifest))
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None and len(z.namelist())==len(manifest)+1 and set(z.namelist())==set(manifest)|{'MANIFEST.json'}
 for n,pin in manifest.items():assert identity(z.read(n))==pin,n
pin={'filename':dest.name,**identity(dest.read_bytes()),'entries':len(manifest)+1,'manifested_hashes':len(manifest),'CRC':'PASS','safe_exact_membership_hashes':'PASS'};(workspace/'Formal-Lab6-I164-EC01-closure-identity.json').write_bytes(enc(pin));print(json.dumps(pin),flush=True)
