"""Package qualified review records; never executes a candidate or test.
Original preparation-only package.py is preserved unchanged.
"""
from pathlib import Path,PurePosixPath
import sys,json,zipfile,stat,re,collections
sys.path.insert(0,str(Path(__file__).parent))
from intake import AREA,BASE,INPUT,PIN,identity,enc,js
def load(p):return js(p.read_bytes())
def reconcile(group):
 p=BASE/'results'/group;s=BASE/'processes'/group;result=load(p/'RESULT.json');ex=load(s/'exit-status.json');rows=result['rows'];progress=[js(x) for x in (p/'progress.jsonl').read_bytes().splitlines()]
 stdout=[x for x in (s/'stdout.log').read_text().splitlines() if re.match(r'^\d+ ',x)]
 assert result['checks']==len(rows) and len({x['check'] for x in rows})==len(rows)
 byname={x['check']:(i,x) for i,x in enumerate(rows,1)}
 for x in progress:assert x==byname[x['check']][1]
 indices=[byname[x['check']][0] for x in progress];assert indices==sorted(set(indices))
 for i,line in enumerate(stdout,1):assert line==f"{i} {rows[i-1]['check']} {rows[i-1]['result']}"
 missing=[i for i in range(1,len(rows)+1) if i not in indices]
 if group=='public-recovered':assert len(rows)==146 and len(progress)==145 and len(stdout)==125 and missing==[126]
 else:assert len(rows)==len(progress)==len(stdout) and not missing
 support=[{'ordinal':i,'check':x['check'],'result':x['result'],'layer':x['layer'],'records':['RESULT.json']+(['progress.jsonl'] if i in indices else [])+(['stdout.log'] if i<=len(stdout) else [])} for i,x in enumerate(rows,1)]
 return {'result':result['result'],'rows':len(rows),'kinds':dict(collections.Counter(x['result'] for x in rows)),'layers':dict(collections.Counter(x['layer'] for x in rows)),'exit':ex,'error':result['error'],'environment':result['environment'],'stdout_progress_RESULT_reconciled':not missing and len(stdout)==len(rows),'progress_rows':len(progress),'stdout_rows':len(stdout),'missing_progress_ordinals':missing,'missing_stdout_ordinals':list(range(len(stdout)+1,len(rows)+1)),'record_support_by_row':support,'discrepancy_cause':'UNKNOWN' if missing or len(stdout)!=len(rows) else None},rows
def main():
 group,rows=reconcile('public-recovered');monitor,mrows=reconcile('slot4');assert group['error'] is None and group['exit']['returncode']==0 and not group['exit']['timed_out']
 assert monitor['rows']==13 and monitor['kinds']=={'PASS':12,'QUALIFIED':1} and monitor['exit']['returncode']==1 and 'tool 4 is not in use' in monitor['error']
 scope=load(BASE/'results/public-recovered/scope-result.json');assert scope['focused_checks_completed'] and scope['full_public_negative_derivations']==0
 for name,pin in load(BASE/'results/public-recovered/executed-review-code-identities.json').items():assert identity((BASE/'code'/name).read_bytes())==pin,name
 calls=load(BASE/'results/public-recovered/calls.json');root=AREA/'recovered';callcounts={label:dict(collections.Counter(x['function'] for x in calls if x['file']==str(path))) for label,path in [('current',root/'code/correspondence.py'),('unchanged_predecessor',root/'retained/cleanup/code/correspondence.py')]}
 assert callcounts['current']['validate']==callcounts['current']['_basis']==1 and callcounts['unchanged_predecessor']['validate']==1
 intake=load(BASE/'results/intake.json');audit=load(BASE/'results/audit/AUDIT.json');failure=load(BASE/'failures/slot4-finalization/RECORD.json');assert identity(INPUT.read_bytes())==PIN
 assert load(BASE/'results/public-recovered/final-verification.json')==intake['recovered_root']
 rpin=load(BASE/'results/public-recovered/submitted-receipt-identity.json');assert rpin==audit['prepared_receipt']
 verdict='SUPPORTED within the bounded conditional SOURCE-ONLY line172 correspondence contract, with explicit execution-record qualifications; no candidate defect demonstrated'
 checkpoint={'reviewer':'Formal-Lab[6], independent of the SU-Engineering[288D] construction author','target':'I164-cleanup-error-report-correspondence-1.zip','input':PIN,'input_entries':83,'input_manifested_hashes':82,'verdict':verdict,'smallest_residual_witness':None,'integrity_and_recovery':intake,'current_receipt':rpin,'fresh_independent_public_core_group_with_record_qualification':group,'new_record_availability_qualification':load(BASE/'failures/public-log-reconciliation/RECORD.json'),'actual_monitored_call_counts':callcounts,'fresh_slot4_failed_attempt_separate':monitor,'fresh_slot4_finalization_failure':failure,'fresh_slot4_qualified_observation':load(BASE/'results/slot4/qualified-cleanup-interruption.json'),'supplied_accounting_separate':audit['supplied'],'supplied_failures_separate':audit['new_supplied_failures'],'prior_accounting_and_closures_reused':audit['historical'],'no_unqualified_combined_total':True,'validation_layers':'Every independent row retains its actual layer. Exactly one current and unchanged predecessor public positive; no public negative call or full public negative derivation. Other negatives use actual-authenticated cores, source rederivation, or exact-type/shape gates.','limits':['Source/constructed correspondence only; no new application runtime catch/evaluation/append observations','Original, selected and replacement error roles are modeled source-qualified records, not observed exception object identities','Last acknowledged active caught error is not a terminal interpreter-state observation; active_at_terminal_observed remains None','Conditional selected-error/owner/local/name/details/list/method continuity remains a premise','Generated names/messages/formatted bytes remain unavailable','Prior UNKNOWN append effects remain UNKNOWN after acknowledged reporting; complete list contents and physical effects unestablished','Stop after selected append or first nonnormal frontier; no handler exit/later iteration/loop completion/failure writing/final rethrow/owner finalization','Non-None construction and remaining outer cleanup gaps remain open; observer unjoined','Cooperative CPython3.12.14 only; cleanup failure, repeated interruption, termination, alternate interpreters and hostile replacement remain qualified','No new prepared-host or installed-wheel qualification'],'preserved':audit['historical']['preserved'],'confirmed_save_reused':'c2fb30a1a427db2a1066df4d40e17574fa51bcbf','operations':{'candidate_implementation_changes':0,'acquisitions':0,'requests':0,'database_connections':0,'session_operations':0,'Git_saves':0,'completed_campaign_replays':0,'missing_historical_rows_reconstructed':0},'read_only_audit':{'controls':0,'candidate_executions':0,'exit':load(BASE/'processes/audit/exit-status.json')}}
 (BASE/'CHECKPOINT.json').write_bytes(enc(checkpoint))
 report=f'''Formal-Lab[6] — author-independent line172 cleanup error-report review

Verdict: SUPPORTED within the retained bounded conditional SOURCE-ONLY contract,
with explicit execution-record qualifications.
No residual defect was demonstrated in the focused review. This is not runtime
coverage, complete cleanup, qualification, readiness or admission.

Target: I164-cleanup-error-report-correspondence-1.zip.
Construction author: SU-Engineering[288D]. Independent reviewer: Formal-Lab[6].
No candidate implementation, source, original receipt or evidence was modified.

Integrity and preservation

The input is exactly 159,370,715 bytes / 83 entries, SHA-256
2b6d61b3f9dc756740a0c66f4bdf70a729cfb77d43beb495424965331aa72bd1.
CRC, safe unique regular membership and all 82 manifested hashes passed. The
exact retained EC01 closure, correction, earlier review and original candidate
archives were verified, including their CRCs, membership and hashes. Byte-only
independent recovery produced 4,015 files / 1,110 directories. ROOT-MANIFEST.json
is 1,485,862 bytes, SHA-256
5136aad4ca70ebb9adfef7c262ead6644f1ae2f163aa3cb789a7abc44d1b183d.
The root's exact membership, types and hashes passed before and after execution.

All 3,999 EC01 predecessor files are unchanged. The active producer is exactly
the reviewed 342,189-byte prefix plus the declared 16,906-byte addition; the six
new function names do not override inherited definitions. The actual predecessor
public validator and all runtime source bytes are unchanged. The new adapter and
declared active counterpart identities match the delivery record. All historical
candidate/evidence members, relationships and ordinals within this retained tree
are preserved by exact bytes; completed component reviews were reused, not rerun.
LD01 and EC01 support carry forward within their existing scopes.

The current prepared receipt is {rpin['bytes']:,} bytes, SHA-256
{rpin['sha256']}.
Preparation remains distinct from validation. Historical receipts and historical
NOT ACCEPTED findings retain their original versions and status. Undeclared partial
files are retained as exact failure-evidence copies outside the strict input root.
Their origins remain UNKNOWN; none was silently admitted, deleted or repaired.

Source-derived findings

lab_bootstrap.py:171 contains one try protecting obj.close() and the subsequent
normal-message append. Line172 catches BaseException as close_error and evaluates
details['cleanup'].append([name,type(close_error).__name__,str(close_error)]).
Independent AST traversal verifies the shared protection, non-None guard, exact
source positions and 23 semantic boundaries. It confirms callable-before-argument
evaluation and left-to-right list elements, including the inner type and str
callables/arguments/call boundaries. The generated catalogue and Engineering's
oracle were not used to derive those expected positions and ordering.

The selected parent must be a validated modeled raise at its exact protected
source occurrence, context, instance and invocation. Its pending selected error,
owner/token/name/details/list roles and original constructor provenance are bound
through that predecessor result. Outside-try failures reject before acquiring this
handler. Eligibility, type evaluation, matching, selection, entry and caught-name
binding remain separate acknowledgements. Source anchors are not runtime delivery.

Close and subsequent normal-append failure origins remain distinct. Later append
failure retains an established close return; the name close_error does not establish
that close itself failed. An acknowledged reporting append preserves earlier UNKNOWN
append effects and records a symbolic append separately from complete list contents.
Earlier acknowledged details, dynamic origins and exact False fields are retained.
Concrete generated names, messages, bytes and runtime object identities remain unknown.

Original constructor, selected cleanup and replacement error roles remain distinct.
Normal reporting retains True for the modeled pending-exception classification;
it proves neither normal overall return nor final rethrow. Replacement raises retain
True with their correct pending role; termination/unobserved frontiers retain None.
The last acknowledged active caught error is tracked separately from pending errors
and unavailable terminal-state observations. Existing cause/context/suppression
qualifications remain; no new explicit-cause relation is invented.

The slice stops after the selected append or first nonnormal frontier. Handler exit,
later iterations, loop completion, failure-file writing, final rethrow and owner
finalization remain unestablished. Conditional initial reference/outcome premises
are not evidence of feasible or observed runtime histories.

Fresh independent execution and precise layers

One fresh isolated process validated the exact current receipt on the independently
recovered root through the actual unchanged predecessor. Its returned authenticated
basis was captured passively, with no source/function/output replacement. All focused
core negatives used this live basis. No saved fixture, prepared receipt or synthetic
predecessor substituted for public authentication.

The public/core process exited0 without timeout and saved146 RESULT rows:
39 PASS /107 expected REJECTED. Only rows1-125 have matching RESULT, progress
and stdout (33 PASS/92 REJECTED). Progress has145 rows:1-125 and127-146
(39 PASS/106 REJECTED). Stdout rows126-146 are unavailable. Row126, literal-key
subclass rejection at REPORT-CONSTRUCTED-INPUT:KEY-TYPE, is supported only by
RESULT; its progress record is also unavailable. Rows127-146 have matching RESULT
and progress, but no stdout. The cause remains UNKNOWN. Exact streams, final
records and identities are frozen; nothing was reconstructed or replayed. There
is no unqualified146-control completion claim. The actual public positive and
source/origin/frontier/wrong-binding controls are in the fully corroborated prefix;
additional row-specific qualifications appear in CHECKPOINT.json. The scoped
verdict rests on source analysis and the precisely identified available records,
not an inference that missing records must have passed. Both contexts and prefixes were
checked with close and normal-append origins. Adjacent frontiers, omitted/reordered
stages, wrong lineage, outside-try failures, coordinated reports, lost partial effects,
invented completion, exact types, UNKNOWN-to-zero claims and nested result mutations
were challenged. Pristine receipts and legitimate constructed cases remain accepted.

Every row records its actual validation layer: selected-parent-revalidated
constructed core; output comparison; source rederivation; authenticated semantic
catalogue/claims or evidence comparison; exact-type pre-parent gate; receipt shape
gate; or authenticated receipt comparison. There is no full public negative
derivation or public negative invocation. Public positives and constructed controls
are not runtime application observations.

New slot4 monitoring review, separately qualified

Source comparison confirms the new helper has the retained slot3 helper's AST
structure after only slot, error-label and lease-marker normalization. Reservation
is inside the protected try; release uses live marker identity, not string equality,
and nested finally blocks attempt local-event, callback and reservation cleanup.
Slots2/3 implementation/support are unchanged; their campaigns were not replayed.

A separate fresh process using real CPython monitoring APIs and explicitly synthetic
predecessors recorded 12 PASS rows and one QUALIFIED observation. Normal, nested,
missing/extra-return, bad-assembly and predecessor-failure paths were checked, as
were C-return interruptions after acquisition/registration/event setup, foreign
ownership and different/equal-valued-distinct acquisition races. These observations
do not authenticate a receipt or substitute for the actual public positive.

The qualified observation showed that interruption of local-event reset can leave
local event bits even though nested cleanup removes the callback and frees the slot.
A free slot is therefore not proof of complete monitoring cleanup. This is within
the retained cleanup-interruption qualification. My harness then tried to reset
those bits without re-reserving the already freed slot and raised ValueError:
tool 4 is not in use. Its exact source, all 13 rows, stdout, stderr and exit1 are
preserved as a FAILED ATTEMPT, outside completed group totals. No rows were rerun.
The process ended; no successful reviewer cleanup or same-process authenticated
reuse is claimed for that qualified case. The separate actual public process was
unaffected. Its normal slot2/3/4 cleanup observations are recorded PASS in RESULT
and progress, with stdout unavailable as explicitly qualified above.

Actual environment: {group['environment']['python']}; Cryptography
{group['environment']['cryptography']}; isolated Python, bytecode writes disabled,
optimization 0. The public process had a 4,500-second hard limit and a 3,900-second
control deadline, reserving finalization time. Incremental logs, commands, process
identity, explicit exits and final integrity records are retained. This supplies
no new host or installed-wheel qualification.

Supplied and historical accounting

Engineering's supplied group remains exactly 392 matching RESULT/stdout rows:
130 PASS / 262 REJECTED, exit0. Progress has only rows1–391:129 PASS /262 REJECTED.
Row392 is the returned-context mutation-isolation check. Its progress row is
unavailable and the discrepancy cause remains UNKNOWN. No row was reconstructed
or replayed. Its actual public positives, pre-derivation gates and authenticated
core negatives retain their original layers; no full public negative derivation
is claimed. The zero-control byte-recovery and packaging failures remain separate.

EC01's independent93 and Engineering105 stay separate. Earlier Engineering46
source and341 recovered-root controls remain completed and separate. Its primary
remains incomplete:1,300 progress /165 stdout, missing stdout166–1300 and three
final records, UNKNOWN discrepancy cause and withdrawn corroboration claim.
Formal-Lab's170 group retains four DEFECT-OBSERVED rows; its21-row completion,
failed50-row attempt and zero-control audit failure/correction remain separate.
All earlier failures, partial evidence and qualifications remain unchanged. No
unqualified aggregate total is asserted. Read-only current reconciliation ran
zero controls/candidate calls and exited0.

Confirmed save c2fb30a1a427db2a1066df4d40e17574fa51bcbf is reused. No Git operation,
request, acquisition, database connection, session operation, implementation edit,
policy adoption or completed-campaign replay occurred.

Retained boundaries

Both acquisitions, eleven obligations, four inventory and fourteen lifetime UNKNOWN
totals, Decision B, retention and allowances remain. Conditional owner/local/error
continuity, unavailable runtime observations, non-None construction and remaining
outer-cleanup gaps remain; the observer is unjoined. Monitoring support remains
limited to the cooperative CPython3.12.14 profile, with cleanup failures, repeated
interruption, termination, alternate interpreters and hostile replacement qualified.
SOURCE-ONLY; cumulative-envelope unadopted; backup kernel-only; streams UNCOMPUTED;
readiness/final binding blocked; admission disabled.
'''
 (BASE/'REVIEW.txt').write_text(report)
 (BASE/'RECOVERY.txt').write_text('''Verify the delivered review ZIP's identity, CRC, safe unique regular membership
and every MANIFEST.json member hash before extraction into a new empty persistent
directory. Do not overwrite evidence or use /tmp.

The exact supplied input is input/I164-cleanup-error-report-correspondence-1.zip:
159370715 bytes;83 entries;SHA-256
2b6d61b3f9dc756740a0c66f4bdf70a729cfb77d43beb495424965331aa72bd1.
Verify its82 manifested hashes and read START-HERE.txt, README.txt, RESULTS.json,
RECOVERY.txt. The input contains the exact EC01 closure and all nested recovery
dependencies. Its tools/recover.py performs byte-only recovery into a NEW empty
persistent root; it verifies ROOT-MANIFEST.json and executes no candidate code.
Alternatively review/code/intake.py records this review's independent recovery;
its path constants identify the original execution locations and are not a command
to overwrite or rerun them.

The active adapter is code/correspondence.py and receipt is
receipts/prepared-error-report.json. The unchanged predecessor is retained/cleanup;
its current receipt remains ec01/receipts/prepared-cleanup-append.json. Historical
receipts/findings/failures retain their original identities and status. Undeclared
partial bytes remain outside the strict recovered input root, in the input's
new/failures/byte-recovery evidence. Do not import them into strict membership.

Read REVIEW.txt/CHECKPOINT.json, review/results/intake.json, the read-only audit,
public-recovered results/progress/stdout/stderr/calls/exit and row-specific layers.
The public/core group is qualified:146 RESULT rows,145 progress rows and125
stdout rows. Row126 is RESULT-only;rows127-146 are RESULT+progress only. Cause
UNKNOWN. Exact frozen copies are under failures/public-log-reconciliation; never
reconstruct missing rows or replay controls to fill them. The separate slot4
attempt has12 PASS and1 QUALIFIED row followed by a reviewer
finalization failure; it is not a completed group. Its failure source/record and
qualified monitoring observation are preserved. Supplied row392 lacks progress;
no record has been reconstructed. No validator execution is needed to recover
or inspect these records.

Included reviewer code documents actual work and does not authorize replaying a
completed campaign. Any separately authorized fresh validation requires the exact
inputs and cooperative CPython3.12.14 profile, bounded processes, incremental logs
and explicit exits. A prepared receipt or synthetic predecessor never substitutes
for actual public authentication. All original authority/evidence limits remain;
admission disabled. No runtime/session/database/Git operations are authorized.
''')
 files={'input/I164-cleanup-error-report-correspondence-1.zip':INPUT}
 for n in ('CHECKPOINT.json','REVIEW.txt','RECOVERY.txt'):files[n]=BASE/n
 for sub in ('code','retained-review-code','results','processes','failures'):
  for p in sorted((BASE/sub).rglob('*')):
   assert not p.is_symlink()
   if p.is_file():files['review/'+p.relative_to(BASE).as_posix()]=p
 for n in ('intake.stdout','intake.stderr'):files['review/'+n]=BASE/n
 manifest={n:identity(p.read_bytes()) for n,p in files.items()};dest=BASE.parent/'Formal-Lab6-I164-cleanup-error-report-independent-review.zip'
 with zipfile.ZipFile(dest,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n,p in files.items():
   assert n==str(PurePosixPath(n)) and not PurePosixPath(n).is_absolute() and all(x not in ('','.','..') for x in n.split('/'))
   i=zipfile.ZipInfo(n);i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=zipfile.ZIP_STORED if n.startswith('input/') else zipfile.ZIP_DEFLATED;z.writestr(i,p.read_bytes())
  i=zipfile.ZipInfo('MANIFEST.json');i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,enc(manifest))
 with zipfile.ZipFile(dest) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)+1 and set(z.namelist())==set(manifest)|{'MANIFEST.json'}
  for n,p in manifest.items():assert identity(z.read(n))==p,n
 pin={'filename':dest.name,**identity(dest.read_bytes()),'entries':len(manifest)+1,'manifested_hashes':len(manifest),'CRC':'PASS','safe_exact_membership_hashes':'PASS'};(BASE.parent/'Formal-Lab6-I164-cleanup-error-report-review-identity.json').write_bytes(enc(pin));print(json.dumps(pin),flush=True)
if __name__=='__main__':main()
