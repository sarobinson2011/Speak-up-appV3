"""Package independent review evidence; does not execute candidate code."""
from pathlib import Path, PurePosixPath
import hashlib, json, os, shutil, stat, zipfile

base = Path(__file__).resolve().parents[1]
workspace = base.parent
def identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
def read(name):
    return json.loads((base / name).read_bytes())

primary = read('independent-primary/RESULT.json')
recovered = read('independent-recovered/RESULT.json')
cli = read('cli-recovered/RESULT.json')
composition = read('results/composition.json')
integrity = read('results/integrity.json')
assert primary['assertions'] == 147 and recovered['assertions'] == 24
for directory, result in [('independent-primary', primary), ('independent-recovered', recovered)]:
    lines = [json.loads(line) for line in (base / directory / 'progress.jsonl').read_text().splitlines()]
    assert len(lines) == result['assertions'] and lines == result['checks']
    assert all(line['result'] in ('PASS', 'REJECTED') for line in lines)
assert cli['returncode'] == 0 and cli['stderr_bytes'] == 0 and cli['answer']['result'] == 'PASS'
assert read('results/recovery-manifest-resolution.json')['result'] == 'PASS'

archive = workspace / 'upload/I164-status-field-correspondence-1(1).zip'
raw = archive.read_bytes()
target_identity = {'bytes': 38539130, 'sha256': 'b51b313de9d03d3bc5eb8436d18e219b05f173144be46d51f090d5119b244504'}
assert identity(raw) == target_identity == integrity['identity']
assert integrity['entries'] == 489 and len(integrity['nested_archives']) == 18
preserved = []
with zipfile.ZipFile(archive) as z:
    expected = {name: z.read(name) for name in z.namelist()}
    assert len(expected) == 489
    allowed_directories = {str(parent) for name in expected for parent in PurePosixPath(name).parents if str(parent) != '.'}
    for dirname in ('sf-input', 'sf-recovered'):
        root = workspace / dirname
        assert stat.S_ISDIR(root.lstat().st_mode)
        files, directories = {}, set()
        def walk(parent):
            for entry in os.scandir(parent):
                path = Path(entry.path)
                relative = path.relative_to(root).as_posix()
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISDIR(mode):
                    directories.add(relative)
                    walk(path)
                else:
                    assert stat.S_ISREG(mode), relative
                    files[relative] = path
        walk(root)
        assert set(files) == set(expected), dirname
        assert directories == allowed_directories, dirname
        assert all(path.read_bytes() == expected[name] for name, path in files.items()), dirname
        preserved.append({'root': dirname, 'exact_unchanged_files': len(files), 'exact_parent_directories': len(directories), 'all_bytes_verified': True, 'no_special_or_symlink_entries': True})
(base / 'results/preservation-after-tests.json').write_text(json.dumps({'result': 'PASS', 'input': target_identity, 'roots': preserved}, indent=2) + '\n')

target = base / 'input/I164-status-field-correspondence-1.zip'
target.parent.mkdir(parents=True, exist_ok=True)
assert not target.exists()
shutil.copyfile(archive, target)
cp = {
    'checkpoint': 'Formal-Lab6-I164-status-field-correspondence-independent-review',
    'review_target': 'I164-status-field-correspondence-1.zip',
    'target': {**target_identity, 'entries': 489},
    'review_author': 'Formal-Lab[6]', 'construction_author': 'SU-Engineering[288D]',
    'author_independent': True, 'canonical': False,
    'verdict': 'SUPPORTED for bounded six-field static correspondence and connection to exact retained successful observations',
    'residual_witness': 'None found within tested bounded contract',
    'preserved_closures': ['SOC-01', 'Original SOC-02 corrections', 'SOC-02-R1', 'Status boundary'],
    'completed_review_reruns': False,
    'independent_checks': {'primary_assertions': 147, 'source_legitimate_preservation': 20, 'catalogue_negatives': 62, 'constructed_expression_controls': 32, 'altered_evidence_controls': 26, 'public_receipt_negatives': 7, 'fresh_process_recovered_assertions': 24, 'actual_offline_CLI_processes': 1, 'overlap_is_not_extra_semantic_coverage': True},
    'supplied_controls': {'primary': 156, 'recovered_repetition': 156, 'inspected_not_executed': True, 'author_repetition_root': 'Documented pre-documentary-package root; not a newly verified complete historical ZIP'},
    'independent_source_audit': primary['source_audit_counts'],
    'source': primary['source'], 'new_receipt': primary['receipt'],
    'unchanged_pristine_occurrence_receipt': composition['prior_receipt'],
    'unchanged_SOC_adapter': composition['SOC_closed_adapter'],
    'observations': {'contexts': ['SYMBOLIC-U-ONE', 'SYMBOLIC-U-TWO'], 'traced_invocations': 18, 'separate_observer_Client_state_calls': 1, 'saved_status_returns': 2, 'fields_per_status_return': 6, 'recovery_field_links_per_context': 6, 'no_invented_observer_frame_or_parent': True, 'context_views_are_not_extra_executions': True, 'no_new_status_observations': True, 'complete_runtime_coverage': False},
    'environment': primary['environment'],
    'preservation': {'input_members': 489, 'SOC_closed_root_members': 467, 'retained_boundary_members': 463, 'candidate_identity_map': 666, 'draft_identity_map': 163, 'maps_are_continuity_not_fresh_full_member_review': True, 'obligations': 11, 'inventory_unknown_totals': 4, 'lifetime_unknown_totals': 14, 'SOURCE_ONLY': 'UNCHANGED', 'Decision_B': 'UNCHANGED', 'cumulative_envelope': 'UNADOPTED', 'readiness': 'BLOCKED', 'final_binding': 'BLOCKED', 'admission': False, 'backup': 'KERNEL-ONLY', 'streams': 'UNCOMPUTED', 'historical_launcher_frames': 'UNAVAILABLE', 'implementation_modified': False},
    'limits': ['Trusted pinned sources/observer and stable filesystem', 'Sparse saved trace lacks full assignment/line/exception histories, offsets, call arguments and live/retired snapshots', 'No saved initial/failure/quarantine/cleanup status returns, exact exception-derived returned text, extra recoveries or additional epochs', 'Static source guards and continuations are not feasible-path or complete repetition/history proof', 'Pure expression helper controls are constructed and never producer execution', 'No arbitrary callback, foreign mutation, introspection or forged-observer resistance claim', 'No finite reason/lifetime domain, canonical field allocation, privacy classification, native serializer or new qualification', 'No operational ownership, durability, authoritative model/final-binding evidence or prepared-host 41.0.7 compatibility established'],
    'prohibited_operations': {'runtime_or_session_operations': False, 'database_connections': 0, 'completed_review_reruns': False, 'host_smoke_rerun': False, 'pipeline_rerun': False, 'lifecycle_rerun': False, 'policy_adoption': False},
    'handoff': 'Return scoped support to Engineering-Anchor[2]; all obligations, UNKNOWN totals and substantive blockers remain.'
}
(base / 'CHECKPOINT.json').write_text(json.dumps(cp, indent=2) + '\n')
members = {}
for path in sorted(base.rglob('*')):
    if path.is_file() and path.name != 'MANIFEST.json' and '__pycache__' not in path.parts:
        assert stat.S_ISREG(path.lstat().st_mode)
        members[path.relative_to(base).as_posix()] = identity(path.read_bytes())
(base / 'MANIFEST.json').write_text(json.dumps({'format': 'Formal-Lab6-status-field-correspondence-independent-review-1', 'members': members}, indent=2) + '\n')
destination = workspace / 'Formal-Lab6-I164-status-field-correspondence-independent-review.zip'
assert not destination.exists()
with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for name in sorted([*members, 'MANIFEST.json']):
        info = zipfile.ZipInfo(name, date_time=(2026, 10, 27, 0, 0, 0))
        info.external_attr = (stat.S_IFREG | 0o644) << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, (base / name).read_bytes())
print(destination)
