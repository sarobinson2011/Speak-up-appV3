"""Evidence-bound input to the retained supplied-acquisition count path.

Finite selected acquisition only. No database connection, serving, model expansion,
qualified classification, cross-acquisition join or lifetime bound is authorized.
Predecessor candidate/draft files remain byte-for-byte unchanged.
"""
import argparse
import copy
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import sys
import zipfile

PACKAGE = Path(__file__).resolve().parents[1]
BASIS_SHA = '6b6e614fa4521f8aafc942db77cfd72cb1a252878bfbc572dddb70fe8cea91bb'
CONTEXTS = ('SYMBOLIC-U-ONE', 'SYMBOLIC-U-TWO')
FORMAT = 'I164-EVIDENCE-COUNT-RECEIPT-1'

class Rejected(ValueError):
    pass

def need(value, why):
    if not value:
        raise Rejected(why)

def enc(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                      allow_nan=False).encode()

def same(a, b, why):
    need(enc(a) == enc(b), why)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def ident(raw):
    return {'bytes': len(raw), 'sha256': sha(raw)}

def read(path):
    path = Path(path)
    need(stat.S_ISREG(path.lstat().st_mode), 'NONREGULAR:' + str(path))
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as f:
        return f.read()

def parse(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'DUPLICATE-JSON-KEY:' + key)
            result[key] = value
        return result
    def constant(value):
        raise Rejected('NONFINITE-JSON:' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)

def load(path):
    return parse(read(path))

def safe(name):
    p = Path(name)
    need(not p.is_absolute() and '..' not in p.parts, 'UNSAFE-MEMBER')
    return p

def tree(root, pins):
    root = Path(root).absolute()
    need(stat.S_ISDIR(root.lstat().st_mode), 'ROOT-TYPE')
    files, dirs = set(), set()
    allowed = {str(p) for n in pins for p in safe(n).parents if str(p) != '.'}
    def walk(parent):
        for child in parent.iterdir():
            name = str(child.relative_to(root))
            mode = child.lstat().st_mode
            if stat.S_ISDIR(mode):
                need(name in allowed, 'EXTRA-DIRECTORY:' + name)
                dirs.add(name)
                walk(child)
            else:
                need(stat.S_ISREG(mode) and name in pins, 'UNSUPPORTED-ENTRY:' + name)
                files.add(name)
    walk(root)
    need(files == set(pins) and dirs == allowed, 'EXACT-TREE-MEMBERSHIP')
    for name, value in pins.items():
        same(ident(read(root / name)), value, 'SOURCE-IDENTITY:' + name)
    return root

def archive(path, expected):
    raw = read(path)
    same(ident(raw), {k: expected[k] for k in ('bytes', 'sha256')}, 'ARCHIVE-IDENTITY')
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        need(len(names) == len(set(names)), 'DUPLICATE-ZIP-MEMBER')
        for i in z.infolist():
            safe(i.filename)
            need(not i.is_dir() and not stat.S_ISLNK(i.external_attr >> 16), 'ZIP-ENTRY-TYPE')
        need(z.testzip() is None, 'ZIP-CRC')
        manifest = parse(z.read('PACKAGE-MANIFEST.json'))
        need(set(names) == set(manifest) | {'PACKAGE-MANIFEST.json'}, 'ZIP-MEMBERSHIP')
        data = {name: z.read(name) for name in names}
        for name, value in manifest.items():
            same(ident(data[name]), value, 'ZIP-MEMBER-IDENTITY')
    return data

def _prepare(root, draft):
    """Fresh disk identities and detached evidence on every public operation."""
    basis_raw = read(PACKAGE / 'provenance/BASIS.json')
    need(sha(basis_raw) == BASIS_SHA, 'BASIS-PIN')
    basis = parse(basis_raw)
    pins = {}
    for name in ('candidate', 'draft'):
        row = basis[name + '_manifest']
        raw = read(PACKAGE / safe(row['path']))
        same(ident(raw), {k: row[k] for k in ('bytes', 'sha256')}, 'MEMBERSHIP-PIN')
        pins[name] = parse(raw)
    root, draft = tree(root, pins['candidate']), tree(draft, pins['draft'])
    data = {label: archive(PACKAGE / safe(ref['path']), ref)
            for label, ref in basis['archives'].items()}
    a, e = data['acquisition'], data['evaluation']
    for name in ('export.json', 'locked-copy.json', 'saved-head/EVIDENCE-MANIFEST.json',
                 'saved-head/request.bin', 'saved-head/response.bin'):
        need(e['preserved/' + name] == a[name], 'EXACT-ACQUISITION-LINEAGE')
    same(parse(e['predecessor.json'])['manifest'], parse(a['PACKAGE-MANIFEST.json']), 'PREDECESSOR-LINEAGE')
    # Source modules are reused in place. A module from a different recovered root rejects.
    locations = {
        'common': root / 'support/code/common.py',
        'ingest': root / 'support/code/ingest.py',
        'compiler': root / 'compiler/compiler.py',
        'semantic': root / 'compiler/semantic.py',
        'prospective_procedure': root / 'compiler/prospective_procedure.py',
        'universe': draft / 'source-only/universe/code/universe.py',
        'cardinality': draft / 'source-only/universe/code/cardinality.py'
    }
    sys.path[:0] = [str(root / 'support/code'), str(root / 'compiler'),
                   str(root / 'integration'), str(draft / 'source-only/universe/code')]
    for name, path in locations.items():
        module = importlib.import_module(name)
        need(Path(module.__file__).resolve() == path.resolve(), 'MIXED-IMPORTED-MODULE:' + name)
    import semantic, prospective_procedure, universe
    semantic.setup(root)
    def source_json(path):
        return load(root / path)
    directory = source_json('layout_outputs/directory.json')
    rules = source_json('layout_outputs/rules.json')
    procedure = source_json('layout_outputs/procedure.json')
    u = load(draft / 'source-only/universe/outputs/universe.json')
    # The exact saved draft links are checked against actual current artifact bytes.
    saved = parse(e['consumed-inputs.json'])
    for name in ('layout_outputs/directory.json', 'layout_outputs/rules.json', 'layout_outputs/procedure.json'):
        same(ident(read(root / name)), saved['current_inputs'][name], 'CURRENT-INPUT-BINDING')
    obligations = parse(e['obligations.json'])
    for kind, filename in [('model', 'model-input.json'), ('ledger', 'ledger-input.json'),
                           ('source_only', 'source-only-result.json')]:
        same(ident(read(draft / 'outputs' / filename)), saved['draft_inputs'][filename], 'DRAFT-INPUT-BINDING')
    same([x['id'] for x in obligations['source_only']], ['O%02d' % i for i in range(1, 12)], 'ELEVEN-OBLIGATIONS')
    context_rows = source_json('candidate/contexts.json')['associations']
    same([x['context'] for x in context_rows], list(CONTEXTS), 'CONTEXT-ORDER')
    return {'root': root, 'draft': draft, 'pins': pins, 'basis': basis, 'archives': data,
            'directory': directory, 'rules': rules, 'procedure': procedure, 'universe': u,
            'obligations': obligations}

def _claims(inputs):
    """Compute candidate claims from saved observations, not submitted counts.
    Claims become evidence-backed only after _validate_semantics completes.
    """
    import compiler as m
    a, e = inputs['archives']['acquisition'], inputs['archives']['evaluation']
    directory, u = inputs['directory'], inputs['universe']
    links = {r['directory']: r for r in u['directory_links']}
    need(len(links) == len(u['directory_links']), 'DUPLICATE-DIRECTORY')
    expected_dirs = {d['context'] + '|' + d['class']: d for d in directory['directories']}
    need(len(expected_dirs) == len(directory['directories']), 'DUPLICATE-CLASS-CONTEXT')
    same(sorted(links), sorted(expected_dirs), 'COMPLETE-DIRECTORY-COVERAGE')
    export_id = ident(a['export.json'])
    evidence = {k: {f: v[f] for f in ('path', 'bytes', 'sha256')}
                for k, v in inputs['basis']['archives'].items()}
    contexts = []
    records = []
    for context in CONTEXTS:
        occ = parse(e[context + '/occurrences.json'])
        duty = parse(e[context + '/procedure-result.json'])
        same(occ['context'], context, 'OCCURRENCE-CONTEXT')
        same(duty['context'], context, 'DUTY-CONTEXT')
        same(occ['saved_export_sha256'], export_id['sha256'], 'OCCURRENCE-EXPORT')
        same(duty['saved_export_sha256'], export_id['sha256'], 'DUTY-EXPORT')
        # Existing row adapter includes actual occurrences, framing and array-index records.
        rows = m._instance_rows(directory, occ)
        ranges = {r['class']: r for r in duty['node_ranges']}
        need(len(ranges) == len(duty['node_ranges']), 'DUPLICATE-RANGE')
        classes = {d['class'] for d in directory['directories'] if d['context'] == context}
        same(sorted(ranges), sorted(classes), 'RANGE-COVERAGE')
        counts = {}
        memberships = []
        position = 0
        all_ids = []
        for d in directory['directories']:
            if d['context'] != context:
                continue
            key = context + '|' + d['class']
            ids = sorted(r['id'] for r in rows.get(d['class'], []))
            need(len(ids) == len(set(ids)), 'DUPLICATE-OCCURRENCE-ID')
            recorded = ranges[d['class']]
            same(recorded['context'], context, 'RANGE-CONTEXT')
            same(recorded['members'], ids, 'EXACT-RANGE-MEMBERSHIP')
            same(recorded['range'], [position, position + len(ids)], 'CONTIGUOUS-RANGE')
            same(recorded['qualification'], 'UNAVAILABLE', 'RANGE-QUALIFICATION')
            same(recorded['disposition'], 'NOT-ESTABLISHED', 'RANGE-DISPOSITION')
            position += len(ids)
            counts[key] = len(ids)
            all_ids.extend(ids)
            memberships.append({'directory': key, 'members': ids})
        need(len(all_ids) == len(set(all_ids)), 'SHARED-OCCURRENCE-ID')
        same(position, duty['finite_tokens'], 'TOKEN-CONSERVATION')
        need(duty['production_token_count'] is None and duty['production_pair_count'] is None,
             'PRODUCTION-UNKNOWN')
        contexts.append({'context': context, 'counts': counts, 'membership_sha256': sha(enc(memberships)),
            'occurrence_identity': ident(e[context + '/occurrences.json']),
            'procedure_result_identity': ident(e[context + '/procedure-result.json']),
            'finite_tokens': duty['finite_tokens'], 'finite_structural_pairs': duty['finite_structural_pairs'],
            'finite_semantic_pairs': duty['finite_semantic_pairs'], 'unresolved': duty['unresolved']})
        records.append({'acquisition_id': inputs['basis']['acquisition_id'], 'context': context,
                        'export_sha256': export_id['sha256'], 'counts': counts})
    receipt = {'format': FORMAT, 'scope': 'FINITE-SELECTED-ACQUISITION-ONLY',
        'parent_git_commit': inputs['basis']['parent_git_commit'],
        'acquisition_id': inputs['basis']['acquisition_id'],
        'evaluation_id': inputs['basis']['evaluation_id'],
        'basis_sha256': BASIS_SHA, 'implementation_identity': ident(read(__file__)),
        'evidence': evidence, 'export_identity': export_id,
        'bindings': {name: ident(read(inputs['root'] / name)) for name in (
            'candidate/identity.json', 'candidate/profile-binding.json', 'candidate/contexts.json',
            'layout_outputs/directory.json', 'layout_outputs/rules.json', 'layout_outputs/procedure.json')},
        'contexts': contexts, 'obligations': inputs['obligations'],
        'source_row_key': ['acquisition_id', 'table', 'stored_key', 'export_row_position'],
        'occurrence_key': ['acquisition_id', 'context', 'pinned_local_occurrence_id'],
        'zero_scope': 'complete count vector for this validated export only; not zero production multiplicity',
        'production_cardinalities': None, 'global_lifetime_bound': None, 'global_storage_byte_bound': None,
        'classification': 'UNKNOWN', 'qualification': 'UNAVAILABLE', 'assessment': 'SOURCE-ONLY',
        'cross_acquisition_joins': False, 'operational_assurance': False, 'canonical_registration': False,
        'full_expansion_ready': False, 'final_binding': 'BLOCKED', 'stream_identities': 'UNCOMPUTED',
        'actual_admission': False, 'backup': 'KERNEL-ONLY'}
    return receipt, records

def _validate_semantics(inputs):
    """Reexecute existing validators, never accept an archive digest as semantics."""
    import common, ingest, prospective_procedure, semantic
    a, e = inputs['archives']['acquisition'], inputs['archives']['evaluation']
    export = common.parse(a['export.json'], 200000000)
    checked = ingest.validate_export(export)  # exact signatures, history, accounting, nonce ownership
    same(checked, parse(a['authenticated-export-validation.json']), 'AUTHENTICATED-FOLD')
    packet, raw_response = a['saved-head/request.bin'], a['saved-head/response.bin']
    q, response = common.parse(packet)['request'], common.parse(raw_response)['response']
    need(q['method'] == 'head' and response['ok'] is True, 'SAVED-HEAD-REQUEST')
    same([r for r in export['journal'] if r[0] == q['challenge']],
         [[q['challenge'], packet.hex(), raw_response.hex()]], 'AUTHENTICATED-REQUEST-RESPONSE-BYTES')
    same(response['data'], common.parse(bytes.fromhex(export['head'])), 'AUTHENTICATED-HEAD')
    c = semantic.setup(inputs['root'])
    for context in CONTEXTS:
        print('Validating saved projection/procedure:', context, flush=True)
        occ = parse(e[context + '/occurrences.json'])
        duty = parse(e[context + '/procedure-result.json'])
        c.check_binding(occ['binding'])
        # Existing procedure validation regenerates its result, including source
        # projection validation, typed guarded rows, semantic pairs and duty counts.
        prospective_procedure.validate_result(duty, inputs['procedure'], inputs['directory'],
                                              inputs['rules'], occ, export)
    return export

def _execute(inputs, receipt, records):
    _validate_semantics(inputs)
    import universe
    print('Consuming validated receipt through universe.count_acquisition_bag', flush=True)
    raw = universe.count_acquisition_bag(inputs['root'], inputs['universe'], records)
    merged = {k: n for row in records for k, n in row['counts'].items()}
    same(raw['counts'], merged, 'EXISTING-COUNTER-CONSERVATION')
    same(raw['supplied_acquisition_contexts'], len(CONTEXTS), 'ACQUISITION-CONTEXT-CONSERVATION')
    need(raw['production_complete'] is False and raw['full_expansion_ready'] is False,
         'COUNTER-STATUS-ESCALATION')
    return {'format': 'I164-EVIDENCE-COUNT-CONSUMPTION-1', 'receipt_sha256': sha(enc(receipt)),
        'acquisition_id': receipt['acquisition_id'], 'export_identity': receipt['export_identity'],
        'validated_directory_count': len(merged),
        'finite_counts_by_context': [{k: row[k] for k in ('context', 'finite_tokens',
            'finite_structural_pairs', 'finite_semantic_pairs')} for row in receipt['contexts']],
        'existing_counter_result': raw, 'scope': receipt['scope'], 'obligations': receipt['obligations'],
        'production_cardinalities': None, 'global_lifetime_bound': None, 'global_storage_byte_bound': None,
        'assessment': 'SOURCE-ONLY', 'classification': 'UNKNOWN', 'qualification': 'UNAVAILABLE',
        'cross_acquisition_joins': False, 'operational_assurance': False, 'canonical_registration': False,
        'full_expansion_ready': False, 'final_binding': 'BLOCKED', 'actual_admission': False,
        'stream_identities': 'UNCOMPUTED', 'backup': 'KERNEL-ONLY'}

def build(root, draft):
    inputs = _prepare(root, draft)
    receipt, records = _claims(inputs)
    result = _execute(inputs, receipt, records)
    return copy.deepcopy({'receipt': receipt, 'consumption': result})

def consume(root, draft, receipt):
    # Current inputs/evidence supply every expectation. Neither successful object
    # history nor mutated returned dictionaries can change validation expectations.
    inputs = _prepare(root, draft)
    expected, records = _claims(inputs)
    same(receipt, expected, 'EVIDENCE-COUNT-RECEIPT-SUBSTITUTION')
    return copy.deepcopy(_execute(inputs, expected, records))

def validate(root, draft, receipt, result=None):
    inputs = _prepare(root, draft)
    expected, records = _claims(inputs)
    same(receipt, expected, 'EVIDENCE-COUNT-RECEIPT-SUBSTITUTION')
    # Fast rejection of obvious consumption mutations; a matching submission
    # still runs the full retained validation and counter path below.
    if result is not None:
        need(type(result) is dict, 'CONSUMPTION-TYPE')
        need(result.get('receipt_sha256') == sha(enc(expected)), 'DETACHED-CONSUMPTION')
        need(result.get('full_expansion_ready') is False and result.get('actual_admission') is False
             and result.get('final_binding') == 'BLOCKED', 'CONSUMPTION-STATUS')
        same(result.get('obligations'), expected['obligations'], 'CONSUMPTION-OBLIGATIONS')
        merged = {k: n for r in records for k, n in r['counts'].items()}
        same(result.get('existing_counter_result', {}).get('counts'), merged, 'CONSUMPTION-COUNTS')
    actual = _execute(inputs, expected, records)
    if result is not None:
        same(result, actual, 'CONSUMPTION-SUBSTITUTION')
    return {'format': 'I164-EVIDENCE-COUNT-VALIDATED-1', 'scope': expected['scope'],
            'receipt_sha256': sha(enc(expected)), 'full_expansion_ready': False,
            'final_binding': 'BLOCKED', 'actual_admission': False}

def require_ready(*args, **kwargs):
    raise Rejected('LIFETIME-CARDINALITIES-AND-QUALIFICATION-REMAIN-UNRESOLVED')

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('action', choices=('build', 'validate', 'consume'))
    ap.add_argument('--root', required=True, type=Path)
    ap.add_argument('--draft', required=True, type=Path)
    ap.add_argument('--receipt', type=Path)
    ap.add_argument('--consumption', type=Path)
    ap.add_argument('--output', required=True, type=Path)
    a = ap.parse_args()
    need(not os.path.lexists(a.output), 'OUTPUT-EXISTS')
    if a.action == 'build':
        need(a.receipt is None and a.consumption is None, 'BUILD-INPUTS')
        value = build(a.root, a.draft)
    else:
        need(a.receipt is not None, 'RECEIPT-REQUIRED')
        receipt = load(a.receipt)
        value = validate(a.root, a.draft, receipt, load(a.consumption) if a.consumption else None) if a.action == 'validate' else consume(a.root, a.draft, receipt)
    a.output.mkdir(parents=True)
    for key, item in (value.items() if a.action == 'build' else [(a.action, value)]):
        with (a.output / (key + '.json')).open('xb') as f:
            f.write(enc(item) + b'\n')
    print('PASS bounded evidence-count correspondence; lifetime/readiness/final binding BLOCKED')

if __name__ == '__main__':
    main()
