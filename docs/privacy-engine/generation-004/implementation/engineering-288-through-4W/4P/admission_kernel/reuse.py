"""Bind saved CP2 outputs without expansion or equality enumeration."""
import hashlib
import json
import time
import zipfile
from pathlib import Path
from v4_ingest.records import require, digest
from .failures import Failures

EXPECTED = '3740c21246000bad0aeb2d34d081548914e073885b304df7f3eddad2b78501cd'


def checkpoint2(archive):
    start = time.monotonic()
    h = hashlib.sha256()
    with Path(archive).open('rb') as f:
        while data := f.read(1024*1024): h.update(data)
    require(h.hexdigest() == EXPECTED, 'exact independently saved CP2 ZIP identity')
    with zipfile.ZipFile(archive) as z:
        prefix = 'Engineering-288-checkpoint-2/'
        manifest = json.loads(z.read(prefix+'PACKAGE-MANIFEST.json'))
        hashes = {e['path']: e for e in manifest['files']}
        def get(name):
            raw = z.read(prefix+name)
            require(digest(raw) == hashes[name]['sha256'], 'retained result identity')
            return json.loads(raw)
        report = get('results/expansion/expansion-results.json')
        verification = get('results/expansion/verification-results.json')
        state = get('results/expansion/RECOVERY.json')
        require(report['model_identity']['sha256'] == hashes['results/expansion/model.json']['sha256'] == state['model_identity']['sha256'], 'saved model/file/recovery identity join')
        require(report['tokens'] == verification['tokens_verified'] and report['structural_edges'] == verification['structural_rows_verified'], 'reuse construction/verification count joins')
        require(report['equality_plan']['sha256'] is None and verification['full_pair_stream_verified'] is False, 'do not promote unexecuted full stream')
    f = Failures()
    f.add('INVALID-EVIDENCE-AUTHORITY', 'Actual policy, assessor, model classifier, observer, producer/proof and evidence source qualification unavailable')
    f.add('MISSING-EVIDENCE', 'Completed independently governed three-member V4 profile and its qualified external records/three signed bundles are unavailable')
    f.add('INVALID-SURFACE-LABELS', 'CP2 new semantic/framing/parser custody remains UNKNOWN; no qualified label/view resolution')
    f.add('INCOMPLETE-EVIDENCE-UNIVERSE', 'Null full-stream digest; canonical qualified obligation/composition directory and actual correspondence remain unavailable')
    result = f.result('ACTUAL', {'checkpoint_2_archive_sha256': EXPECTED, 'reused_model_identity': report['model_identity'],
                               'tokens': report['tokens'], 'structural_rows': report['structural_edges'],
                               'pair_count_descriptor': report['equality_plan']['rows']})
    result.update({'result': 'REUSED-CP2-BINDING-VERIFIED-ACTUAL-ADMISSION-BLOCKED', 'expansion_rerun': False,
                   'full_pair_stream_executed': False, 'seconds': round(time.monotonic()-start, 3),
                   'scope': 'Saved output binding and explicit actual-admission input barrier; no integration witness'})
    return result
