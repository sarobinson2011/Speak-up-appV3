"""One authorized unfinished public check; no baseline/campaign re-execution."""
from pathlib import Path
import datetime, hashlib, json, os, sys, time, traceback, zipfile

BASE = Path('/workspace/scratch/ace5c9b2f18b')
ROOT = Path('/workspace/review-evidence/FL6-control-20261030/recovered')
OUT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(BASE / 'cc-review/code'))
from common import guard, module, environment, CALLS
from integrity import verify_root, identity, PIN, INPUT

START = time.monotonic()
EXPECTED = 'CONTROL-STALE-OR-ALTERED-RECEIPT'
INVOCATIONS = 0

def save(name, data):
    with (OUT / name).open('x') as f:
        json.dump(data, f, sort_keys=True, indent=2)
        f.write('\n'); f.flush(); os.fsync(f.fileno())

def progress(stage, **details):
    row = {'stage': stage, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'seconds': time.monotonic() - START, **details}
    with (OUT / 'progress.jsonl').open('a') as f:
        f.write(json.dumps(row, sort_keys=True) + '\n'); f.flush(); os.fsync(f.fileno())
    print(json.dumps(row, sort_keys=True), flush=True)

def differences(a, b, path=()):
    if type(a) is not type(b): return [(list(path), a, b)]
    if type(a) is dict:
        assert set(a) == set(b), ('UNPLANNED-KEY-CHANGE', path)
        return [d for k in a for d in differences(a[k], b[k], path + (k,))]
    if type(a) is list:
        assert len(a) == len(b), ('UNPLANNED-LENGTH-CHANGE', path)
        return [d for i in range(len(a)) for d in differences(a[i], b[i], path + (i,))]
    return [] if a == b else [(list(path), a, b)]

try:
    assert sys.flags.isolated and sys.dont_write_bytecode and sys.flags.optimize == 0
    progress('started', pid=os.getpid(), environment=environment(), intended_validator_invocations=1)
    # Reauthenticate current bytes; reuse earlier CRC/composition and baseline results.
    assert identity(INPUT.read_bytes()) == PIN, 'TARGET-ARCHIVE-IDENTITY'
    with zipfile.ZipFile(INPUT) as z:
        manifest_bytes = z.read('MANIFEST.json')
    assert (ROOT / 'MANIFEST.json').read_bytes() == manifest_bytes, 'ROOT-MANIFEST-IDENTITY'
    before = verify_root(ROOT)
    save('input-verification.json', {'archive': PIN, 'manifest': identity(manifest_bytes), 'root': str(ROOT), 'verification': before})
    progress('unchanged-inputs-verified', **before)
    monitor = guard(ROOT, OUT)
    m = module(ROOT / 'code/correspondence.py'); monitor(m)
    saved = (ROOT / 'results/primary/control-exception.json').read_bytes()
    assert identity(saved) == {'bytes': 7426382, 'sha256': 'b2344acaa2370d94a03f59c7f505df84c423f41dc4937ec81d6f939a01240eb5'}
    original = json.loads(saved); q = json.loads(saved)
    assert [r['context'] for r in q['contexts']] == ['SYMBOLIC-U-ONE', 'SYMBOLIC-U-TWO']
    for row in q['contexts']:
        c = row['control_exception_revocation_correspondence']
        assert c['exception_chain_observation'] is None
        assert c['client_handler_applicable'] is False
        assert c['declaration']['source']['new_explicit_cause_assignment'] is False
        c['exception_chain_observation'] = {'existing_cause': None}
        c['client_handler_applicable'] = True
        c['declaration']['source']['new_explicit_cause_assignment'] = True
    delta = differences(original, q)
    expected_paths = []
    for i in range(2):
        p = ['contexts', i, 'control_exception_revocation_correspondence']
        expected_paths.extend([p + ['exception_chain_observation'], p + ['client_handler_applicable'], p + ['declaration', 'source', 'new_explicit_cause_assignment']])
    assert sorted(map(repr, [d[0] for d in delta])) == sorted(map(repr, expected_paths))
    altered = m.enc(q)
    assert altered != saved
    with (OUT / 'coordinated-claims-receipt.json').open('xb') as f:
        f.write(altered); f.flush(); os.fsync(f.fileno())
    save('witness.json', {'original': identity(saved), 'altered': identity(altered), 'changes': delta, 'validator': 'correspondence.validate(root, altered_bytes)', 'expected_error': EXPECTED, 'no_baseline_rerun': True})
    progress('intended-six-field-mutation-verified', original=identity(saved), altered=identity(altered), changed_fields=len(delta))
    INVOCATIONS += 1
    progress('public-validator-started', invocation=INVOCATIONS)
    try:
        returned = m.validate(ROOT, altered)
    except ValueError as e:
        frames = []
        tb = e.__traceback__
        while tb:
            frames.append({'file': tb.tb_frame.f_code.co_filename, 'function': tb.tb_frame.f_code.co_name, 'line': tb.tb_lineno})
            tb = tb.tb_next
        text = traceback.format_exc()
        (OUT / 'validator-rejection.traceback.txt').write_text(text)
        save('validator-exception.json', {'type': type(e).__name__, 'message': str(e), 'frames': frames})
        assert type(e) is ValueError and str(e) == EXPECTED, ('UNEXPECTED-REJECTION', type(e).__name__, str(e))
        # Require the actual public post-derivation comparison, not a missing-input/harness rejection.
        assert [f['function'] for f in frames[-2:]] == ['validate', 'require'], frames
        assert all(f['file'] == str(ROOT / 'code/correspondence.py') for f in frames[-2:]), frames
        observed = {'check': 'public coordinated client-handler and cause invention', 'result': 'REJECTED', 'exception_type': 'ValueError', 'error': str(e), 'validator_invocations': INVOCATIONS}
        save('check-result.json', observed)
        progress('intended-validator-rejection-confirmed', **observed)
    else:
        save('unexpected-acceptance.json', {'returned': returned})
        raise AssertionError('UNEXPECTED-ACCEPTANCE')
    assert (ROOT / 'MANIFEST.json').read_bytes() == manifest_bytes
    after = verify_root(ROOT)
    save('final-verification.json', after)
    save('calls.json', CALLS)
    save('RESULT.json', {'status': 'PASS', 'checks': 1, 'rows': [observed], 'environment': environment(), 'seconds': time.monotonic() - START, 'reused_baselines': True, 'runtime_operations': 0, 'session_operations': 0, 'database_connections': 0, 'validator_invocations': INVOCATIONS})
    progress('finished', status='PASS', checks=1, final_input_verification=after)
except BaseException:
    error = traceback.format_exc()
    (OUT / 'harness-failure.txt').write_text(error)
    save('FAILED-ATTEMPT.json', {'status': 'FAILED-ATTEMPT', 'error': error, 'validator_invocations': INVOCATIONS, 'seconds': time.monotonic() - START})
    progress('failed-attempt', validator_invocations=INVOCATIONS)
    raise
