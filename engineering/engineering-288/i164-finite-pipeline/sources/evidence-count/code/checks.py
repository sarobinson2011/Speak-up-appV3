"""Focused controls for the new receipt boundary; not an independent review."""
import argparse
import collections
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import traceback
sys.path.insert(0, str(Path(__file__).resolve().parent))
import evidence_counts as v

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--draft', type=Path, required=True)
    ap.add_argument('--built', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    v.need(not a.output.exists(), 'TEST-OUTPUT-EXISTS')
    a.output.mkdir(parents=True)
    checks = []
    attempts = []
    def audit(event, args):
        if event == 'sqlite3.connect':
            attempts.append(str(args[0]))
            raise AssertionError('DATABASE CONNECTION ATTEMPT')
    sys.addaudithook(audit)
    receipt = v.load(a.built / 'receipt.json')
    result = v.load(a.built / 'consumption.json')
    pristine = v.enc(receipt)
    start = time.monotonic()
    def passed(name, evidence):
        checks.append({'name': name, 'status': 'PASS', 'evidence': evidence})
        print('PASS', name, flush=True)
    def reject(name, fn, marker):
        began = time.monotonic()
        try:
            fn()
        except v.Rejected as e:
            v.need(marker in str(e), 'WRONG-REJECTION:' + name + ':' + str(e))
            passed(name, {'rejection': str(e), 'seconds': time.monotonic() - began})
        else:
            raise AssertionError('ACCEPTED MUTATION:' + name)
    def mutant(name, change):
        value = copy.deepcopy(receipt)
        change(value)
        v.need(v.enc(value) != pristine, 'NO-OP-MUTATION:' + name)
        reject(name, lambda: v.consume(a.root, a.draft, value), 'RECEIPT-SUBSTITUTION')
    try:
        inputs = v._prepare(a.root, a.draft)
        expected, records = v._claims(inputs)
        v.same(expected, receipt, 'CURRENT-CLAIMS')
        passed('fresh source/evidence claims match semantically built receipt',
               {'directories': sum(len(x['counts']) for x in receipt['contexts'])})
        v.need(len(receipt['contexts']) == 2 and sum(len(x['counts']) for x in receipt['contexts']) == 18678,
               'COMPLETE-CONTEXT-DIRECTORIES')
        v.need(all(sum(x['counts'].values()) == 2376 for x in receipt['contexts']), 'SOURCE-EXPECTED-TOKEN-SUM')
        passed('complete 18678-directory vectors and independently summed tokens', {'per_context': 2376})
        for row in receipt['contexts']:
            v.need(row['finite_structural_pairs'] == 2376 - 11 and row['finite_semantic_pairs'] == 3,
                   'SAVED-FINITE-COUNTS')
        passed('small snapshot structural count agrees with tokens minus eleven emitted roots', {'pairs': 2365})
        e = inputs['archives']['evaluation']
        for context in v.CONTEXTS:
            occ = v.parse(e[context + '/occurrences.json'])
            rows = occ['candidate_occurrences']
            value_groups = collections.defaultdict(list)
            for r in rows:
                value_groups[r['occurrence']].append(r['id'])
            repeated = [ids for ids in value_groups.values() if len(ids) > 1]
            v.need(repeated and all(len(ids) == len(set(ids)) for ids in repeated), 'EQUAL-VALUE-OCCURRENCES')
        passed('equal observed values retain distinct source occurrence identities in both contexts', {'constructed_execution': False})
        positive = next(k for k, n in receipt['contexts'][0]['counts'].items() if n)
        zero = next(k for k, n in receipt['contexts'][0]['counts'].items() if not n)
        mutant('altered positive count', lambda x: x['contexts'][0]['counts'].__setitem__(positive, 0))
        mutant('omitted zero-count directory', lambda x: x['contexts'][0]['counts'].pop(zero))
        mutant('omitted present directory', lambda x: x['contexts'][0]['counts'].pop(positive))
        mutant('boolean substituted for integer count', lambda x: x['contexts'][0]['counts'].__setitem__(zero, False))
        mutant('float substituted for integer count', lambda x: x['contexts'][0]['counts'].__setitem__(zero, 0.0))
        mutant('unknown substituted into complete snapshot count', lambda x: x['contexts'][0]['counts'].__setitem__(zero, None))
        mutant('context order reversed', lambda x: x['contexts'].reverse())
        mutant('duplicate acquisition/context claim', lambda x: x['contexts'].append(copy.deepcopy(x['contexts'][0])))
        mutant('different acquisition ancestry', lambda x: x.__setitem__('acquisition_id', 'unrelated-acquisition'))
        mutant('mixed export identity', lambda x: x['export_identity'].__setitem__('sha256', 'f' * 64))
        mutant('wrong archive/member provenance', lambda x: x['evidence']['evaluation'].__setitem__('path', 'different-archive.zip'))
        mutant('stale current directory binding', lambda x: x['bindings']['layout_outputs/directory.json'].__setitem__('sha256', 'e' * 64))
        mutant('unsupported cross-acquisition joins', lambda x: x.__setitem__('cross_acquisition_joins', True))
        mutant('production unknown changed to zero', lambda x: x.__setitem__('production_cardinalities', 0))
        mutant('finite global bound manufactured', lambda x: x.__setitem__('global_lifetime_bound', 1))
        mutant('obligation removed', lambda x: x['obligations']['source_only'].pop())
        mutant('classification promoted', lambda x: x.__setitem__('classification', 'QUALIFIED'))
        mutant('operational assurance promoted', lambda x: x.__setitem__('operational_assurance', True))
        mutant('readiness promoted', lambda x: x.__setitem__('full_expansion_ready', True))
        mutant('admission promoted', lambda x: x.__setitem__('actual_admission', True))
        def coordinated(x):
            x['contexts'][0]['counts'][positive] = 0
            x['contexts'][0]['finite_tokens'] -= 1
            x['contexts'][0]['membership_sha256'] = 'a' * 64
        mutant('coordinated count/token/membership substitution', coordinated)
        # A shared reference and repeated calls cannot mutate a future expected value.
        aliased = copy.deepcopy(receipt)
        alias = aliased['contexts'][0]['counts']
        alias[positive] = 0
        for i in range(2):
            reject('aliased mutation repeated ' + str(i + 1), lambda: v.validate(a.root, a.draft, aliased), 'RECEIPT-SUBSTITUTION')
        fresh, _ = v._claims(v._prepare(a.root, a.draft))
        v.same(fresh, v.parse(pristine), 'MUTATION-CONTAMINATED-EXPECTATIONS')
        passed('pristine current expectations survive returned-object/alias mutation', {})
        # Serialize and read the mutated value at the actual public file boundary.
        serialized = v.parse(v.enc(aliased))
        reject('serialized mutant rejects', lambda: v.consume(a.root, a.draft, serialized), 'RECEIPT-SUBSTITUTION')
        changed_result = copy.deepcopy(result)
        changed_result['existing_counter_result']['counts'][positive] = 0
        reject('consumption count detached from evidence', lambda: v.validate(a.root, a.draft, receipt, changed_result), 'CONSUMPTION-COUNTS')
        changed_result = copy.deepcopy(result)
        changed_result['receipt_sha256'] = '0' * 64
        reject('detached consumption receipt', lambda: v.validate(a.root, a.draft, receipt, changed_result), 'DETACHED-CONSUMPTION')
        changed_result = copy.deepcopy(result)
        changed_result['obligations']['ledger'].clear()
        reject('consumption obligations removed', lambda: v.validate(a.root, a.draft, receipt, changed_result), 'CONSUMPTION-OBLIGATIONS')
        reject('readiness stays blocked', lambda: v.require_ready(), 'LIFETIME-CARDINALITIES')
        # Real filesystem mutation of a separate copy-on-write hardlink fixture.
        # No original file is opened for writing. The altered file is unlinked
        # before replacement, so the predecessor inode cannot be modified.
        fixture = Path(tempfile.mkdtemp(prefix='I164-count-source-fixture-', dir=v.PACKAGE.parent))
        for name in inputs['pins']['candidate']:
            p = fixture / name
            p.parent.mkdir(parents=True, exist_ok=True)
            os.link(a.root / name, p)
        changed = fixture / 'layout_outputs/directory.json'
        changed.unlink()
        changed.write_bytes(b'{}\n')
        reject('altered actual current directory input rejects before consumption',
               lambda: v.consume(fixture, a.draft, receipt), 'SOURCE-IDENTITY:layout_outputs/directory.json')
        (a.output / 'source-fixture.json').write_bytes(v.enc({
            'path': str(fixture), 'construction': 'hardlinks to exact source members; directory.json unlinked then replaced',
            'replacement': '{}\\n', 'original_sources_modified': False}) + b'\n')
        # Source-layer negative independent of the new archive identity gate.
        # Mutate a saved projection and call the actual existing projection validator.
        import semantic, common, ingest
        c = semantic.setup(a.root)
        export = common.parse(inputs['archives']['acquisition']['export.json'], 200000000)
        occurrence = v.parse(e[v.CONTEXTS[0] + '/occurrences.json'])
        occurrence['candidate_occurrences'].pop()
        try:
            c.validate_output(occurrence, export)
        except common.Invalid as exc:
            v.need('DOWNSTREAM-SUBSTITUTION' in str(exc), 'PROJECTION-NEGATIVE-LABEL')
            passed('missing observed occurrence rejects independently of capture hash gate', {'existing_validator': str(exc)})
        else:
            raise AssertionError('MISSING OBSERVATION ACCEPTED')
        export = copy.deepcopy(export)
        response = common.parse(bytes.fromhex(export['journal'][0][2]))
        old_signature = response['signature']
        response['signature'] = ('00' if old_signature[:2] != '00' else '01') + old_signature[2:]
        v.need(response['signature'] != old_signature, 'NO-OP-SIGNATURE-MUTATION')
        export['journal'][0][2] = common.enc(response).hex()
        try:
            ingest.validate_export(export)
        except common.Invalid as exc:
            v.need(str(exc) == 'AUTHENTICATION', 'AUTHENTICATION-NEGATIVE-LABEL')
            passed('substituted response signature rejects in pinned fold independent of capture hash', {'existing_validator': str(exc)})
        else:
            raise AssertionError('SUBSTITUTED SIGNATURE ACCEPTED')
        v.need(not attempts, 'DATABASE CONNECTIONS')
        v.tree(a.root, inputs['pins']['candidate'])
        v.tree(a.draft, inputs['pins']['draft'])
        passed('all 666 candidate and 163 draft members unchanged; no database connections', {})
        v.same(receipt, v.load(a.built / 'receipt.json'), 'SAVED-RECEIPT-MODIFIED')
        report = {'status': 'PASS focused author controls', 'checks': checks, 'count': len(checks),
                  'seconds': time.monotonic() - start, 'database_connection_attempts': attempts,
                  'evidence_kind': 'fresh offline validation of retained snapshot; no producer/session execution',
                  'independent_review': False}
    except BaseException:
        (a.output / 'failure.txt').write_text(traceback.format_exc())
        report = {'status': 'FAIL author controls', 'checks': checks, 'count': len(checks),
                  'seconds': time.monotonic() - start, 'database_connection_attempts': attempts}
        raise
    finally:
        if 'report' in locals():
            (a.output / 'checks.json').write_bytes(v.enc(report) + b'\n')
    print('PASS', len(checks), 'focused controls;', report['seconds'], 'seconds')

if __name__ == '__main__':
    main()
