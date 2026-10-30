"""Package saved evidence only. Never imports or runs candidate validation."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, os, stat, zipfile

BASE = Path('/workspace/scratch/ace5c9b2f18b')
HERE = Path(__file__).resolve().parent
RUN = HERE / 'run'
RETAINED = BASE / 'Formal-Lab6-I164-control-callback-exception-INCOMPLETE-recovery.zip'
RETAINED_PIN = {'bytes': 122064627, 'sha256': '1821bf45816c834bceada2e14f8899f947b7b238473da60d94346e4303083895'}
TARGET_PIN = {'bytes': 124424355, 'sha256': 'ed07f4ceb638f1c967cb3936b0051f5c0c8d781c95d26838b7bdc7baba7f4c20'}
TARGET_NAME = 'I164-control-callback-exception-correspondence-1.zip'
def identity(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def enc(v): return (json.dumps(v, sort_keys=True, indent=2) + '\n').encode()
def save(n, v):
    with (HERE / n).open('xb') as f: f.write(enc(v))
def safe(n):
    p = PurePosixPath(n)
    assert n and not p.is_absolute() and p.as_posix() == n and '..' not in p.parts and '\\' not in n and ':' not in n and not n.endswith('/'), n
def checked_archive(path, expected):
    assert identity(path.read_bytes()) == expected
    with zipfile.ZipFile(path) as z:
        names = z.namelist(); assert len(names) == len(set(names))
        for i in z.infolist():
            safe(i.filename); assert stat.S_ISREG(i.external_attr >> 16) and not i.flag_bits & 1
        manifest = json.loads(z.read('MANIFEST.json'))
        assert set(names) == set(manifest) | {'MANIFEST.json'}
        for n, pin in manifest.items(): assert identity(z.read(n)) == pin, n
        return {'identity': expected, 'entries': len(names), 'manifested_hashes': len(manifest), 'CRC': 'PASS', 'safe_exact_membership': 'PASS', 'manifested_hashes_verified': 'PASS'}

# The former incomplete checkpoint remains a separate exact historical record.
retained_verification = checked_archive(RETAINED, RETAINED_PIN)
with zipfile.ZipFile(RETAINED) as z:
    assert identity(z.read('input/' + TARGET_NAME)) == TARGET_PIN
prior_inventory = json.loads((HERE / 'prior-evidence-inventory.json').read_bytes())
for n, pin in prior_inventory.items():
    p = BASE / n; assert stat.S_ISREG(p.lstat().st_mode) and identity(p.read_bytes()) == pin, n
reconciliation = json.loads((BASE / 'cc-recovery-20261030/RECONCILIATION.json').read_bytes())
assert reconciliation['result_recorded_rows'] == 520
assert reconciliation['corroborated_progress_stdout_rows'] == 517
old_checkpoint = json.loads((BASE / 'cc-recovery-20261030/CHECKPOINT.json').read_bytes())
exit_path = RUN / 'exit-status.json'
assert exit_path.is_file(), 'PROCESS-NOT-YET-FINALIZED: do not package while process is active'
exit_status = json.loads(exit_path.read_bytes())
result_path = RUN / 'RESULT.json'
result = json.loads(result_path.read_bytes()) if result_path.exists() else None
check_path = RUN / 'check-result.json'
check = json.loads(check_path.read_bytes()) if check_path.exists() else None
passed = (exit_status['returncode'] == 0 and exit_status['timed_out'] is False and result is not None and result['status'] == 'PASS')
if passed:
    assert result['checks'] == result['validator_invocations'] == 1
    assert check['result'] == 'REJECTED' and check['error'] == 'CONTROL-STALE-OR-ALTERED-RECEIPT'
    assert check['exception_type'] == 'ValueError' and check['validator_invocations'] == 1
    assert json.loads((RUN / 'final-verification.json').read_bytes()) == {'files': 3069, 'directories': 853, 'safe_exact_membership': 'PASS', 'hashes': 'PASS'}
    progress = [json.loads(s) for s in (RUN / 'progress.jsonl').read_text().splitlines()]
    stdout = [json.loads(s) for s in (RUN / 'stdout.log').read_text().splitlines()]
    assert progress == stdout
    assert [r['stage'] for r in progress] == ['started', 'unchanged-inputs-verified', 'intended-six-field-mutation-verified', 'public-validator-started', 'intended-validator-rejection-confirmed', 'finished']
    calls = json.loads((RUN / 'calls.json').read_bytes())
    assert sum(c['file'] == '/workspace/review-evidence/FL6-control-20261030/recovered/code/correspondence.py' and c['function'] == 'validate' for c in calls) == 1
    assert any(c['file'] == '/workspace/review-evidence/FL6-control-20261030/recovered/code/correspondence.py' and c['function'] == '_assemble' for c in calls)
    outcome = 'SCOPED SUPPORT WITH RETAINED ACCOUNTING QUALIFICATIONS'
    tag = 'independent-review'
elif (RUN / 'unexpected-acceptance.json').exists():
    outcome = 'NOT SUPPORTED: PUBLIC VALIDATOR ACCEPTED THE COORDINATED CLAIMS'
    tag = 'defect-review'
else:
    outcome = 'INCOMPLETE: OUTSTANDING CHECK NOT CONFIRMED'
    tag = 'INCOMPLETE-completion'

status_text = ("The one outstanding public check was executed once in a fresh isolated process on the unchanged recovered root. It rejected the exact six-field, two-context mutation with ValueError: CONTROL-STALE-OR-ALTERED-RECEIPT at the public post-derivation receipt comparison. The child exited 0 before the finite timeout. Input verification and final verification both passed for 3,069 files and 853 directories. No missing input, harness exception or timeout was counted as rejection. The actual pristine public/CLI acceptance and other completed groups were reused, not rerun."
               if passed else "The new single-check attempt did not establish the intended successful rejection. Its actual exit status, incremental records, witness, stdout and stderr are preserved. A timeout, missing input, unexpected acceptance or harness failure is not accepted as evidence of successful rejection. See CHECKPOINT.json and completion/run/ for the exact outcome; no further attempt was launched.")
qualification = """Accounting is intentionally not collapsed into one completed total. Five prior independent RESULT records contain 520 controls, while 517 rows are corroborated across progress/stdout. The coordinated group remains 106 RESULT / 103 progress / 103 stdout. Rows 104–106, the second-context submitted-output claims for owner_failure_guard_evaluated_in_model, client_handler_entered_in_model and new_explicit_cause_assignment_established_in_model, remain result-only REJECTED records; their missing logs and cause are UNESTABLISHED. Nothing in this completion recreates or retrospectively corroborates them. The other four groups reconcile exactly. Nine matching rows in the interrupted public group remain partial historical evidence; the old process/session exit and result remain unrecovered. The new public check is one separately recorded execution, not a repaired tenth historical row or a rerun of the public group.

Engineering's 276 primary / 64 recovered-root / 7 public-process controls remain separate supplied evidence. Their reconciled saved logs were inspected previously and no campaign was rerun. Historical Engineering 308/307/303, separate 78/5, both zero-control membership failures and all partial files remain unchanged. The independent zero-control membership-level audit failure and zero-test recovery-packaging reconciliation failure are also retained outside test totals.
"""
assessment = ("Scoped assessment: the source-derived catalogue, mandatory integration, qualified independent semantic/constructed evidence, prior positive public baseline and this confirmed public rejection support this bounded control-callback exception correspondence. The three result-only rows are not necessary to infer the specific fresh public rejection and are not promoted into corroborated results. No residual implementation defect was established in this bounded review. This is support for the static/conditional saved-input contract, not operational qualification or observation of runtime cleanup."
              if passed else "Scoped assessment: no completed support verdict is issued. This attempt's actual outcome governs the remaining obstacle; passing historical groups cannot substitute for the missing rejection. Any unexpected-acceptance record and exact mutated receipt are retained as the smallest attempted witness in this slice.")
draft = (BASE / 'cc-review/REPORT.draft.txt').read_text()
assert 'VERDICT_PENDING_COMPLETED_CHECKS' in draft
report = draft.replace('VERDICT_PENDING_COMPLETED_CHECKS', 'VERDICT: ' + outcome + '\n\n' + status_text + '\n\n' + qualification + '\n' + assessment)
report += """

Completion evidence and recovery

This checkpoint contains the unchanged, previously issued INCOMPLETE recovery ZIP as an exact dependency. That dependency contains the exact target archive, original review files, failures, partial public logs and reconciliation records. Its original INCOMPLETE status is preserved as history; the present REPORT.txt and CHECKPOINT.json state the current assessment. The old draft and unexecuted supported-verdict packager are not retroactively made final. The new supervisor has a 1,800-second limit, a five-second termination grace, one launch and zero retries. Incremental worker/supervisor records, complete stdout/stderr, actual exit status, isolated environment, exact six-field witness, rejection traceback and before/after byte verification are retained where produced. Proc activity inspection returned PermissionError; that limitation is recorded without bypass and was not used to infer validator success. Subprocess exit/result evidence provides the outcome.

The six-field mutation retains both contexts and changes only exception_chain_observation to {existing_cause: null}, client_handler_applicable to true, and declaration.source.new_explicit_cause_assignment to true in each. This is the previously unfinished coordinated public check, not a new campaign. The original positive receipt bytes remain 7,426,382 / b2344acaa2370d94a03f59c7f505df84c423f41dc4937ec81d6f939a01240eb5. The mutation is 7,426,416 / 6bd6924dc819574dd2587b108ce1747ef7aaca7481ec0af4430d6f146f56c66d. The mandatory validator still consumes its actual predecessor validators as part of this one call; no completed test suite, pipeline or application was run separately.

All 69 existing review/recovery files recorded at continuation start are byte-unchanged. The retained checkpoint identity, CRC, safe exact membership, 70 manifested hashes and exact embedded target identity are verified during packaging. Original target CRC/composition, declared changes and preservation findings are reused from the completed integrity work; no original host or intermediate-cut outer archive qualification is invented. The final package is also verified for CRC, safe exact membership and all manifested hashes before delivery.
"""
(HERE / 'REPORT.txt').write_text(report)
checkpoint = {
    'checkpoint': 'Formal-Lab6-I164-control-callback-exception-' + tag,
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'verdict': outcome, 'scoped_support': passed,
    'reviewer': 'Formal-Lab[6]', 'construction_author': 'SU-Engineering[288D]', 'author_independent': True,
    'target_name': TARGET_NAME, 'target': TARGET_PIN, 'target_entries': 3069, 'target_manifested_hashes': 3068,
    'original_integrity_basis': 'retained/INCOMPLETE-recovery.zip/review-files/results/integrity.json and recovered-integrity.json',
    'retained_checkpoint': retained_verification, 'prior_evidence_files_preserved': len(prior_inventory),
    'prior_accounting': reconciliation, 'interrupted_public_rows': 9,
    'old_public_exit_status': None, 'old_public_result': 'UNRECOVERED; not inferred from new process',
    'new_execution': {'result': result, 'check': check, 'exit_status': exit_status, 'count_combined_with_prior': False},
    'supplied_controls_separate': {'primary': 276, 'recovered_root': 64, 'public_process': 7},
    'limitations': {k: v for k, v in old_checkpoint['limitations'].items() if k != 'no_final_public_rejection_inferred_from_other_passes'},
    'boundaries': old_checkpoint['boundaries'],
    'residual_implementation_defect_demonstrated': bool((RUN / 'unexpected-acceptance.json').exists()),
    'no_implementation_changes': True, 'no_completed_campaign_reruns': True,
    'reused_pristine_baselines': True, 'original_records_repaired': False,
    'runtime_operations': 0, 'database_connections': 0, 'session_operations': 0, 'acquisitions': 0,
}
save('CHECKPOINT.json', checkpoint)
save('PRESERVATION.json', {'unchanged_prior_files': prior_inventory, 'retained_verification': retained_verification})
(HERE / 'RECOVERY.txt').write_text("""Recovery plan (saved inputs only; no automatic execution)

1. Verify this archive identity against the delivered size/SHA-256, then verify safe unique regular-file membership, CRC and every MANIFEST.json entry. The archive has no undeclared directory entries.
2. retained/INCOMPLETE-recovery.zip must be exactly 122,064,627 bytes / SHA-256 1821bf45816c834bceada2e14f8899f947b7b238473da60d94346e4303083895; it has 71 entries and 70 manifested hashes. Preserve it unchanged. Its incomplete verdict describes the old interrupted attempt.
3. Verify that archive's manifest and CRC. Its input/I164-control-callback-exception-correspondence-1.zip is the exact 124,424,355-byte / 3,069-entry target, SHA-256 ed07f4ceb638f1c967cb3936b0051f5c0c8d781c95d26838b7bdc7baba7f4c20. Follow the retained exact composition/recovery records for fresh-root inspection. Do not put completion witnesses or partial forensic files inside strict predecessor roots.
4. This checkpoint's completion/run records are the new single-check execution. The retained review-files results are prior evidence; neither the 520/517 qualification nor 106/103/103 discrepancy is repaired. Nine old public rows remain partial. Old process/session exit remains unrecoverable. No rerun is needed to inspect this checkpoint.
5. No application/session/database/acquisition operation is authorized. Source-only boundaries, eleven obligations, four inventory and fourteen lifetime UNKNOWN totals, Decision B, retention, allowances and admission-disabled status remain unchanged.
""")
(HERE / 'START-HERE.txt').write_text('Read REPORT.txt, CHECKPOINT.json and RECOVERY.txt. The retained incomplete checkpoint is historical evidence; current verdict: ' + outcome + '.\n')

members = {'retained/INCOMPLETE-recovery.zip': RETAINED}
for p in sorted(HERE.rglob('*')):
    if p.is_dir(): continue
    assert stat.S_ISREG(p.lstat().st_mode), p
    name = p.relative_to(HERE).as_posix()
    arc = name if name in ('REPORT.txt', 'CHECKPOINT.json', 'RECOVERY.txt', 'START-HERE.txt', 'PRESERVATION.json') else 'completion/' + name
    assert arc not in members; members[arc] = p
manifest = {n: identity(p.read_bytes()) for n, p in members.items()}
for n in members: safe(n)
archive = BASE / ('Formal-Lab6-I164-control-callback-exception-' + tag + '.zip')
with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for n, p in members.items():
        i = zipfile.ZipInfo(n); i.create_system = 3; i.external_attr = 0o100644 << 16
        i.compress_type = zipfile.ZIP_STORED if n.endswith('.zip') else zipfile.ZIP_DEFLATED
        z.writestr(i, p.read_bytes())
    i = zipfile.ZipInfo('MANIFEST.json'); i.create_system = 3; i.external_attr = 0o100644 << 16; i.compress_type = zipfile.ZIP_DEFLATED
    z.writestr(i, enc(manifest))
verification = checked_archive(archive, identity(archive.read_bytes()))
assert verification['entries'] == len(members) + 1
for n, pin in prior_inventory.items(): assert identity((BASE / n).read_bytes()) == pin, n
summary = {'path': str(archive), 'verdict': outcome, **verification, 'preserved_prior_files': len(prior_inventory)}
with (BASE / 'cc-completion-package.json').open('x') as f: json.dump(summary, f, sort_keys=True, indent=2); f.write('\n')
print(json.dumps(summary, sort_keys=True), flush=True)
