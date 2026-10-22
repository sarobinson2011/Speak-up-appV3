"""Evaluate one pinned saved acquisition. Never connects to a database."""
import argparse
import contextlib
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import stat
import sys
import tempfile
import traceback
import zipfile

ARCHIVE_ID = {"bytes": 70665, "sha256": "554d27a0c5eb5d97c762eb082001930be9317c8f317ea62759557d01727177a4"}
BASE = Path('/home/steve/dev/Engineering-288-execution')
ACQUISITION = 'I164-snapshot-acquisition-egpf25d9'

def require(value, message):
    if not value:
        raise RuntimeError(message)

def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def same_json(a, b, message):
    require(encode(a) == encode(b), message)

def byte_identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def identity(path):
    path = Path(path)
    require(stat.S_ISREG(path.lstat().st_mode), 'NONREGULAR: ' + str(path))
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode), 'OPENED NONREGULAR FILE')
        h = hashlib.sha256()
        count = 0
        while True:
            data = os.read(fd, 1024 * 1024)
            if not data:
                break
            h.update(data)
            count += len(data)
        after = os.fstat(fd)
        fields = ('st_dev', 'st_ino', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
        require(all(getattr(before, k) == getattr(after, k) == getattr(path.lstat(), k)
                    for k in fields), 'FILE CHANGED: ' + str(path))
        return {'bytes': count, 'sha256': h.hexdigest()}
    finally:
        os.close(fd)

def read_json(path):
    identity(path)
    return json.loads(Path(path).read_bytes())

def verify_tree(root, pins):
    require(stat.S_ISDIR(root.lstat().st_mode), 'ROOT TYPE: ' + str(root))
    allowed_dirs = {str(p) for n in pins for p in Path(n).parents if str(p) != '.'}
    files, dirs = set(), set()
    def walk(parent):
        for child in parent.iterdir():
            name = str(child.relative_to(root))
            mode = child.lstat().st_mode
            if stat.S_ISDIR(mode):
                require(name in allowed_dirs, 'UNDECLARED DIRECTORY: ' + name)
                dirs.add(name)
                walk(child)
            else:
                require(stat.S_ISREG(mode) and name in pins, 'UNSUPPORTED ENTRY: ' + name)
                files.add(name)
    walk(root)
    require(files == set(pins) and dirs == allowed_dirs, 'TREE MEMBERSHIP: ' + str(root))
    for name, expected in pins.items():
        same_json(identity(root / name), expected, 'TREE HASH: ' + name)

def read_archive(path):
    same_json(identity(path), ARCHIVE_ID, 'ACQUISITION ARCHIVE IDENTITY')
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), 'DUPLICATE ZIP MEMBERS')
        for item in z.infolist():
            p = Path(item.filename)
            require(not item.is_dir() and not p.is_absolute() and '..' not in p.parts
                    and not stat.S_ISLNK(item.external_attr >> 16), 'UNSAFE ZIP MEMBER')
        require(z.testzip() is None, 'ACQUISITION CRC')
        manifest = json.loads(z.read('PACKAGE-MANIFEST.json'))
        require(set(names) == set(manifest) | {'PACKAGE-MANIFEST.json'}, 'ACQUISITION MEMBERSHIP')
        contents = {n: z.read(n) for n in names}
        for name, expected in manifest.items():
            same_json(byte_identity(contents[name]), expected, 'ACQUISITION MEMBER: ' + name)
    return contents, manifest

def check_environment(captured, mode):
    import sqlite3
    observed = {
        'implementation': platform.python_implementation(), 'python': platform.python_version(),
        'optimize': sys.flags.optimize, 'cryptography': importlib.metadata.version('cryptography'),
        'sqlite': sqlite3.sqlite_version, 'executable': str(Path(sys.executable).resolve()),
        'executable_identity': identity(Path(sys.executable).resolve()),
        'distributions': {d.metadata['Name']: d.version for d in importlib.metadata.distributions()}
    }
    require(observed['implementation'] == 'CPython' and observed['python'] == '3.12.14'
            and observed['optimize'] == 0, 'CPYTHON 3.12.14 UNOPTIMIZED REQUIRED')
    if mode == 'prepared-host':
        same_json(observed, captured, 'PREPARED HOST ENVIRONMENT MISMATCH')
        require(observed['cryptography'] == '41.0.7', 'CRYPTOGRAPHY PIN')
    return {'mode': mode, 'observed': observed, 'captured_host': captured,
            'host_equivalence_established': mode == 'prepared-host'}

def evaluate(args, out, save):
    contents, manifest = read_archive(args.archive)
    j = lambda name: json.loads(contents[name])
    require(j('RESULT.json').get('error') == 'RuntimeError: DRAFT MODEL PROCEDURE',
            'UNEXPECTED PREDECESSOR FAILURE')
    # Raw bytes are compared as bytes, never sent through JSON serialization.
    require(encode(json.loads(contents['PACKAGE-MANIFEST.json'])) == encode(manifest),
            'MANIFEST CONTENT')
    if args.acquisition_directory is not None:
        verify_tree(args.acquisition_directory, {
            **manifest, 'PACKAGE-MANIFEST.json': byte_identity(contents['PACKAGE-MANIFEST.json'])})
    save('predecessor.json', {'acquisition_id': ACQUISITION, 'archive': str(args.archive),
         'identity': ARCHIVE_ID, 'saved_failure': contents['failure.txt'].decode(),
         'saved_result': j('RESULT.json'), 'manifest': manifest})
    env = check_environment(j('environment.json'), args.environment_mode)
    save('environment.json', env)
    # Copies of original evidence only. No acquisition and no database extraction/opening.
    for name in ('export.json', 'saved-head/request.bin', 'saved-head/response.bin',
                 'saved-head/EVIDENCE-MANIFEST.json', 'locked-copy.json'):
        p = out / 'preserved' / name
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('xb') as f:
            f.write(contents[name])
    cpins = j('inputs/launcher/provenance/candidate-members.json')
    dpins = j('inputs/launcher/provenance/draft-members.json')
    verify_tree(args.candidate, cpins)
    verify_tree(args.draft, dpins)
    def audit(event, event_args):
        if event == 'sqlite3.connect':
            raise RuntimeError('DATABASE CONNECTION PROHIBITED')
    sys.addaudithook(audit)
    sys.path[:0] = [str(args.candidate / 'support/code'), str(args.candidate / 'compiler'),
                   str(args.candidate / 'integration'), str(args.draft / 'code')]
    import common, ingest, semantic, layout_consumers, prospective_procedure, construction_inputs
    imported = {}
    def check_imports():
        for module in list(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if not filename:
                continue
            path = Path(filename).resolve()
            for root, pins in ((args.candidate, cpins), (args.draft, dpins)):
                if path.is_relative_to(root):
                    rel = str(path.relative_to(root))
                    require(rel in pins, 'UNDECLARED IMPORT: ' + str(path))
                    same_json(identity(path), pins[rel], 'IMPORTED SOURCE: ' + str(path))
                    imported[str(path)] = pins[rel]
    check_imports()
    export = common.parse(contents['export.json'], 200000000)
    validated = ingest.validate_export(export)
    same_json(validated, j('authenticated-export-validation.json'), 'SAVED VALIDATION')
    packet, response_bytes = contents['saved-head/request.bin'], contents['saved-head/response.bin']
    q = common.parse(packet)['request']
    response = common.parse(response_bytes)['response']
    challenge = contents['saved-head/challenge.txt'].decode().strip()
    same_json([r for r in export['journal'] if r[0] == challenge],
              [[challenge, packet.hex(), response_bytes.hex()]], 'EXACT AUTHENTICATED JOURNAL ROW')
    require(q['method'] == 'head' and q['challenge'] == challenge and response['ok'] is True,
            'AUTHENTICATED HEAD REQUEST/RESPONSE')
    same_json(export['config'], j('inputs/launcher/laboratory-configuration.json')['config'],
              'EXACT CONFIGURATION')
    head = common.parse(bytes.fromhex(export['head']))
    for other in (response['data'], j('saved-head/before-state.json'), j('saved-head/after-state.json')):
        same_json(head, other, 'AUTHENTICATED HEAD CORRESPONDENCE')
    require(head['seq'] == 0 and head['head'] == '0' * 64, 'HEAD FRONTIER')
    candidate = semantic.setup(args.candidate)
    current = {k: read_json(args.candidate / p) for k, p in layout_consumers.PATHS.items()}
    # Reuse completed static validation after verifying all exact source/input bytes.
    same_json(j('current-input-validation.json')['current_candidate_binding'], candidate.binding,
              'SAVED CURRENT VALIDATION BINDING')
    bundle = construction_inputs.read_bundle(args.draft / 'outputs')
    model, ledger = bundle['model-input.json'], bundle['ledger-input.json']
    same_json(model['directory_program'], current['directory'], 'DRAFT DIRECTORY')
    same_json(model['semantic_rule_program'], current['rules'], 'DRAFT RULES')
    pp = layout_consumers.PATHS['procedure']
    same_json(model['procedure_input'], {'path': pp, **identity(args.candidate / pp)},
              'DRAFT MODEL PROCEDURE REFERENCE')
    same_json(ledger['procedure_input'], current['procedure'], 'DRAFT LEDGER PROCEDURE VALUE')
    same_json(model['binding']['candidate_binding'], candidate.binding, 'DRAFT CANDIDATE')
    same_json(ledger['binding'], model['binding'], 'MODEL/LEDGER BINDING')
    construction_inputs.consume_draft(args.candidate, bundle)
    contexts = layout_consumers.current_contexts(args.candidate)
    same_json(contexts, ['SYMBOLIC-U-ONE', 'SYMBOLIC-U-TWO'], 'CONTEXT ORDER')
    lineage = {'acquisition_id': ACQUISITION, 'evaluation_id': out.name,
               'export_identity': byte_identity(contents['export.json']),
               'database_identities': j('database-identities-before.json'),
               'occurrence_key': ['acquisition_id', 'context', 'pinned_local_occurrence_id'],
               'source_row_key': ['acquisition_id', 'table', 'stored_key', 'export_row_position'],
               'equal_contents_merged': False, 'cross_acquisition_joins': False,
               'historical_execution_slot': None}
    save('lineage.json', lineage)
    save('obligations.json', {'model': model['obligations'], 'ledger': ledger['obligations'],
         'source_only': bundle['source-only-result.json']['obligations'],
         'model_status': model['status'], 'ledger_status': ledger['status']})
    counts = {}
    for context in contexts:
        print('Evaluating', context, flush=True)
        occurrence = candidate.ingest(export, context, candidate.binding)
        result = prospective_procedure.consume(current['procedure'], current['directory'],
                                               current['rules'], occurrence, export)
        require(result['full_expansion_ready'] is False and result['actual_admission'] is False
                and result['final_binding'] == 'BLOCKED', 'STATUS ESCALATION')
        save(context + '/occurrences.json', occurrence)
        save(context + '/procedure-result.json', result)
        save(context + '/lineage.json', {**lineage, 'context': context})
        counts[context] = {k: result[k] for k in ('finite_tokens', 'finite_structural_pairs',
            'finite_semantic_pairs', 'production_token_count', 'production_pair_count', 'unresolved')}
    check_imports()
    save('consumed-inputs.json', {'imported_sources': imported,
         'candidate_manifest': byte_identity(contents['inputs/launcher/provenance/candidate-members.json']),
         'draft_manifest': byte_identity(contents['inputs/launcher/provenance/draft-members.json']),
         'current_inputs': {p: identity(args.candidate / p) for p in layout_consumers.PATHS.values()},
         'draft_inputs': {n: identity(args.draft / 'outputs' / n) for n in construction_inputs.FILES}})
    verify_tree(args.candidate, cpins)
    verify_tree(args.draft, dpins)
    same_json(identity(args.archive), ARCHIVE_ID, 'ACQUISITION ARCHIVE CHANGED')
    if args.acquisition_directory is not None:
        verify_tree(args.acquisition_directory, {
            **manifest, 'PACKAGE-MANIFEST.json': byte_identity(contents['PACKAGE-MANIFEST.json'])})
    return {'status': 'PASS — bounded saved-snapshot correspondence' if args.environment_mode == 'prepared-host'
            else 'PASS — local continuation test; prepared-host compatibility not claimed',
            'head': head['head'], 'sequence': head['seq'], 'finite_counts_by_context': counts,
            'stored_row_counts': {k: len(export[k]) for k in ('events', 'blobs', 'journal', 'owners')},
            'remaining_gaps': j('RESULT.json')['gaps'], 'environment_mode': args.environment_mode}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive', type=Path, default=Path('/home/steve/Downloads') / (ACQUISITION + '.zip'))
    ap.add_argument('--candidate', type=Path, default=BASE / 'I164-reviewed-recovery-0s8zad3j/current-candidate')
    ap.add_argument('--draft', type=Path, default=BASE / 'I164-reviewed-recovery-0s8zad3j/draft-connection')
    ap.add_argument('--output-parent', type=Path, default=BASE)
    ap.add_argument('--downloads', type=Path, default=Path('/home/steve/Downloads'))
    ap.add_argument('--acquisition-directory', type=Path)
    ap.add_argument('--environment-mode', choices=('prepared-host', 'local-test'), default='prepared-host')
    args = ap.parse_args()
    for key in ('archive', 'candidate', 'draft', 'output_parent', 'downloads'):
        setattr(args, key, getattr(args, key).absolute())
    require(args.output_parent.is_dir() and args.downloads.is_dir(), 'PERSISTENT OUTPUT DIRECTORIES MISSING')
    require(not args.output_parent.resolve().is_relative_to('/tmp') and
            not args.downloads.resolve().is_relative_to('/tmp'), 'NO TMP OUTPUT')
    out = Path(tempfile.mkdtemp(prefix='I164-snapshot-evaluation-v3-', dir=args.output_parent))
    print('PERSISTENT OUTPUT:', out, flush=True)
    def save(name, value):
        p = out / name
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('xb') as f:
            f.write(json.dumps(value, sort_keys=True, indent=2, allow_nan=False).encode() + b'\n')
    report = {'status': 'INCOMPLETE', 'assessment': 'SOURCE-ONLY', 'acquisition_id': ACQUISITION,
              'evaluation_id': out.name, 'readiness': 'BLOCKED', 'final_binding': 'BLOCKED',
              'streams': 'UNCOMPUTED', 'actual_admission': False, 'database_connections': 0,
              'managed_requests': 0, 'new_acquisition': False, 'native_expansion': False,
              'ledger_construction': False, 'script': identity(__file__)}
    with (out / 'execution.log').open('x') as log:
        try:
            with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                report.update(evaluate(args, out, save))
        except BaseException as exc:
            report['status'] = 'STOP — saved-snapshot evaluation not established'
            report['error'] = type(exc).__name__ + ': ' + str(exc)
            with (out / 'failure.txt').open('x') as f:
                traceback.print_exc(file=f)
    save('RESULT.json', report)
    members = {str(p.relative_to(out)): identity(p) for p in sorted(out.rglob('*')) if p.is_file()}
    save('PACKAGE-MANIFEST.json', members)
    package = args.downloads / (out.name + '.zip')
    with zipfile.ZipFile(package, 'x', zipfile.ZIP_DEFLATED) as z:
        for n in sorted(set(members) | {'PACKAGE-MANIFEST.json'}):
            z.write(out / n, n)
    with zipfile.ZipFile(package) as z:
        require(z.testzip() is None and len(z.namelist()) == len(set(z.namelist())), 'OUTPUT CRC/DUPLICATES')
        require(set(z.namelist()) == set(members) | {'PACKAGE-MANIFEST.json'}, 'OUTPUT MEMBERSHIP')
        same_json(json.loads(z.read('PACKAGE-MANIFEST.json')), members, 'OUTPUT MANIFEST')
        for n, expected in members.items():
            same_json(byte_identity(z.read(n)), expected, 'OUTPUT HASH: ' + n)
    with (args.downloads / (out.name + '-result.json')).open('xb') as f:
        f.write((out / 'RESULT.json').read_bytes())
    print('VERDICT:', report['status'])
    if 'error' in report:
        print('REASON:', report['error'])
    print('ATTACH:', package)
    print('BYTES:', identity(package)['bytes'])
    print('SHA-256:', identity(package)['sha256'])
    print('No database connections, requests or new acquisition. Original evidence preserved.')
    print('SOURCE-ONLY; readiness/final binding BLOCKED; streams UNCOMPUTED; admission disabled.')
    return 1 if 'error' in report else 0

if __name__ == '__main__':
    sys.exit(main())
