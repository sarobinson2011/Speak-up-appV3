"""Bounded adaptation: selected reviewed pure functions; acceptance is in evaluate.py."""
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
        'basis_sha256': sha(enc(inputs['basis'])), 'implementation_identity': ident(read(__file__)),
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
