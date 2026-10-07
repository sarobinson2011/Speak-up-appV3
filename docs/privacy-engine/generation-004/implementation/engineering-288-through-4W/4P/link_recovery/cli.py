"""Authenticated local recovery state; exact prefix re-hash on every resume.

Linux/POSIX regular, quiescent input files only. The journal key is a local
execution trust boundary, never source authentication or profile qualification.
"""
import argparse
import fcntl
import hashlib
import hmac
import json
import math
import os
from pathlib import Path
import secrets
import signal
import stat
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
VERSION = 'Engineering-288-CP4C-1'
LIMIT = 1024 * 1024
EMPTY_SHA = hashlib.sha256(b'').hexdigest()


class RecoveryError(Exception):
    pass


class PauseRequested(Exception):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while b := f.read(LIMIT):
            h.update(b)
    return h.hexdigest()


def is_digest(s):
    return isinstance(s, str) and len(s) == 64 and all(c in '0123456789abcdef' for c in s)


def build():
    subprocess.run(['g++', '-O3', '-std=c++17', '-Wno-deprecated-declarations',
                    str(ROOT/'link_recovery/worker.cpp'), '-lcrypto', '-o',
                    str(ROOT/'link_recovery/worker')], check=True, timeout=60)


def validator_identity():
    paths = ['link_recovery/cli.py', 'link_recovery/worker.cpp',
             'link_recovery/worker', 'link_stream/native.cpp']
    return {'version': VERSION, 'files': {p: sha(ROOT/p) for p in paths}}


def create_key(path):
    path = Path(path)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as f:
        f.write(secrets.token_bytes(32)); f.flush(); os.fsync(f.fileno())
    fsync_dir(path.parent)


def read_key(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as f:
        s = os.fstat(f.fileno())
        if not stat.S_ISREG(s.st_mode) or s.st_uid != os.geteuid() or s.st_mode & 0o077:
            raise RecoveryError('journal key must be an owner-only regular file')
        key = f.read(33)
    if len(key) != 32:
        raise RecoveryError('journal key must contain exactly 32 bytes')
    return key


def fsync_dir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_save(path, payload, key, fault=None):
    """fault(stage) is solely a test injection point, not a CLI feature."""
    blob = canonical({'payload': payload, 'hmac_sha256':
                      hmac.new(key, canonical(payload), hashlib.sha256).hexdigest()}) + b'\n'
    if len(blob) > LIMIT:
        raise RecoveryError('checkpoint exceeds local journal budget')
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '.', suffix='.part', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(blob)
            if fault: fault('after_write')
            f.flush(); os.fsync(f.fileno())
            if fault: fault('after_file_fsync')
        os.replace(name, path)
        if fault: fault('after_replace')
        fsync_dir(path.parent)
        if fault: fault('after_dir_fsync')
    finally:
        Path(name).unlink(missing_ok=True)


def load(path, key):
    with path.open('rb') as f:
        raw = f.read(LIMIT + 1)
    if len(raw) > LIMIT:
        raise RecoveryError('oversized checkpoint')
    def unique(items):
        d = {}
        for k, v in items:
            if k in d: raise RecoveryError('duplicate checkpoint JSON key')
            d[k] = v
        return d
    try:
        obj = json.loads(raw, object_pairs_hook=unique)
        if set(obj) != {'payload', 'hmac_sha256'}:
            raise RecoveryError('checkpoint envelope shape')
        expected = hmac.new(key, canonical(obj['payload']), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, obj['hmac_sha256']):
            raise RecoveryError('checkpoint authentication failed: corruption, wrong key or tampering')
        p = obj['payload']
        if p['format'] != VERSION or p['binding']['validator'] != validator_identity():
            raise RecoveryError('incompatible format or validator executable/source version')
        if p['sequence'] < 0 or p['status'] not in ('PAUSED', 'REJECTED', 'PASS-SUPPLIED-LINK-STREAM'):
            raise RecoveryError('checkpoint status/sequence')
        return p
    except (ValueError, KeyError, TypeError) as e:
        raise RecoveryError('malformed checkpoint') from e


def initial_state():
    return {'offset': 0, 'rows': 0, 'structural': 0, 'potential': 0, 'header': 0,
            'have': 0, 'peak': 0, 'sha_h': [0x6a09e667, 0xbb67ae85, 0x3c6ef372,
                0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19],
            'sha_block': '', 'pending': '', 'previous': ['', '', '', ''], 'prefix_sha256': EMPTY_SHA}


def state_text(s):
    parts = ['CP4C-SHA256-1', s['offset'], s['rows'], s['structural'], s['potential'],
             s['header'], s['have'], s['peak'], *s['sha_h'], s['sha_block'] or '-',
             s['pending'] or '-', *(x or '-' for x in s['previous']), s['prefix_sha256']]
    return ('\n'.join(map(str, parts)) + '\n').encode('ascii')


def verify_prefix(fd, offset, expected, deadline):
    """Every prefix byte is read from the same FD subsequently passed to the worker."""
    os.lseek(fd, 0, os.SEEK_SET); h = hashlib.sha256(); total = 0; last = time.monotonic()
    while total < offset:
        if time.monotonic() >= deadline:
            raise RecoveryError('prefix verification deadline; saved checkpoint remains usable')
        b = os.read(fd, min(LIMIT, offset-total))
        if not b: raise RecoveryError('input truncated inside checkpoint prefix')
        h.update(b); total += len(b)
        if time.monotonic()-last >= 10:
            print(json.dumps({'phase': 'prefix-identity', 'verified_bytes': total,
                              'required_bytes': offset}), file=sys.stderr, flush=True)
            last = time.monotonic()
    if h.hexdigest() != expected:
        raise RecoveryError('input prefix changed: complete prefix SHA-256 mismatch')
    return total


def file_mark(fd):
    s = os.fstat(fd)
    if not stat.S_ISREG(s.st_mode): raise RecoveryError('seekable regular input file required')
    return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)


def execute(a):
    if not 0 < a.seconds or not math.isfinite(a.seconds) or a.new_bytes <= 0 or not 1 <= a.chunk_bytes <= LIMIT:
        raise RecoveryError('finite positive time/byte limits and chunk <= 1 MiB required')
    began = time.monotonic(); deadline = began + a.seconds
    checkpoint = Path(a.checkpoint).resolve(); checkpoint.parent.mkdir(parents=True, exist_ok=True)
    key = read_key(a.key)
    with open(str(checkpoint)+'.lock', 'a+b') as lock:
        try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as e: raise RecoveryError('checkpoint already in use') from e
        if a.operation == 'start':
            if checkpoint.exists(): raise RecoveryError('checkpoint exists; use resume or a new path')
            if not all(is_digest(x) for x in (a.input_sha256, a.model_sha256, a.contract_sha256)):
                raise RecoveryError('exact expected input, model and contract SHA-256 values required')
            binding = {'input': {'path': str(Path(a.input).resolve()), 'sha256': a.input_sha256},
                       'model': {'path': str(Path(a.model).resolve()), 'sha256': a.model_sha256},
                       'contract': {'path': str(Path(a.contract).resolve()), 'sha256': a.contract_sha256},
                       'validator': validator_identity(), 'phase': 'STATIC-ADMISSION',
                       'qualification': 'DISABLED'}
            p = {'format': VERSION, 'binding': binding, 'sequence': 0, 'status': 'PAUSED',
                 'state': initial_state(), 'result': None}
        else:
            if any(getattr(a, k, None) is not None for k in
                   ('input', 'input_sha256', 'model', 'model_sha256', 'contract', 'contract_sha256')):
                raise RecoveryError('resume uses the saved binding; input/model/contract overrides forbidden')
            p = load(checkpoint, key); binding = p['binding']
            if p['status'] == 'REJECTED': raise RecoveryError('terminal rejected input; start a new validation')
        if sha(binding['contract']['path']) != binding['contract']['sha256']:
            raise RecoveryError('bound contract changed')
        fd = os.open(binding['input']['path'], os.O_RDONLY | os.O_NOFOLLOW)
        try:
            fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
            before = file_mark(fd)
            if a.operation == 'start':
                binding['input']['bytes'] = before[2]
                atomic_save(checkpoint, p, key)
            elif before[2] != binding['input']['bytes']:
                raise RecoveryError('input size changed (additional check, not byte identity)')
            terminal = p['status'] == 'PASS-SUPPLIED-LINK-STREAM'
            offset = binding['input']['bytes'] if terminal else p['state']['offset']
            prefix_sha = binding['input']['sha256'] if terminal else p['state']['prefix_sha256']
            prefix_began = time.monotonic()
            checked = verify_prefix(fd, offset, prefix_sha, deadline)
            prefix_seconds = time.monotonic() - prefix_began
            if terminal:
                # Recheck model identity even for a previously complete local receipt.
                if sha(binding['model']['path']) != binding['model']['sha256']:
                    raise RecoveryError('bound model changed')
                if file_mark(fd) != before: raise RecoveryError('input changed during prefix verification')
                result = dict(p['result']); result['rechecked_completed_input'] = True
                return result
            remaining = deadline-time.monotonic()
            if remaining <= 0: raise RecoveryError('deadline before worker; checkpoint unchanged')
            with tempfile.TemporaryDirectory(prefix='cp4c-worker-') as temp:
                saved = Path(temp)/'state.txt'; saved.write_bytes(state_text(p['state']))
                cmd = [str(ROOT/'link_recovery/worker'), binding['model']['path'],
                       binding['model']['sha256'], str(fd), binding['input']['sha256'],
                       str(a.chunk_bytes), str(a.new_bytes), str(max(.001, remaining-.1)), str(saved)]
                proc = subprocess.Popen(cmd, pass_fds=(fd,), stdout=subprocess.PIPE,
                                        stderr=None, text=True)
                # Progress/error stderr is inherited live, never retained in RAM.
                try:
                    stdout, stderr = proc.communicate(timeout=remaining)
                except (subprocess.TimeoutExpired, KeyboardInterrupt, PauseRequested):
                    proc.terminate()
                    try: stdout, stderr = proc.communicate(timeout=2)
                    except subprocess.TimeoutExpired:
                        proc.kill(); proc.communicate()
                        raise RecoveryError('worker killed; resume the last durable checkpoint')
                if proc.returncode not in (0, 2, 3):
                    raise RecoveryError('worker rejected state/model or was interrupted; checkpoint unchanged')
                result = json.loads(stdout)
            if file_mark(fd) != before:
                raise RecoveryError('input metadata changed during execution; checkpoint not advanced')
            if result['bytes_consumed'] > before[2]: raise RecoveryError('input grew during execution')
            if result['complete'] and result['bytes_consumed'] != before[2]:
                raise RecoveryError('input EOF/size inconsistency')
            next_state = result.pop('state')
            result.update({'prefix_bytes_rechecked': checked, 'prefix_verification_seconds': prefix_seconds,
                           'checkpoint_sequence': p['sequence']+1, 'journal_authenticates_source': False,
                           'controller_seconds': time.monotonic()-began})
            p.update({'state': next_state, 'result': result, 'sequence': p['sequence']+1,
                      'status': result['result']})
            atomic_save(checkpoint, p, key)
            return result
        finally:
            os.close(fd)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('operation', choices=['build', 'keygen', 'start', 'resume'])
    p.add_argument('--key', type=Path)
    p.add_argument('--checkpoint', type=Path)
    p.add_argument('--input', type=Path); p.add_argument('--input-sha256')
    p.add_argument('--model', type=Path); p.add_argument('--model-sha256')
    p.add_argument('--contract', type=Path); p.add_argument('--contract-sha256')
    p.add_argument('--new-bytes', type=int, default=64*LIMIT)
    p.add_argument('--chunk-bytes', type=int, default=65536)
    p.add_argument('--seconds', type=float, default=50)
    a = p.parse_args()
    if a.operation == 'build': build(); return 0
    if a.key is None: p.error('--key required')
    if a.operation == 'keygen': create_key(a.key); return 0
    if a.checkpoint is None: p.error('--checkpoint required')
    if a.operation == 'start' and any(x is None for x in (a.input, a.model, a.contract)):
        p.error('--input, --model and --contract required for start')
    def request_pause(signum, frame): raise PauseRequested()
    signal.signal(signal.SIGTERM, request_pause)
    try:
        result = execute(a)
    except (RecoveryError, OSError, ValueError, PauseRequested, KeyboardInterrupt) as e:
        result = {'result': 'RECOVERY-ERROR', 'detail': str(e) or 'interrupted; use last durable checkpoint',
                  'complete': False, 'complete_stream_sha256': None, 'profile_admitted': False,
                  'actual_qualification_established': False}
    print(json.dumps(result, indent=2), flush=True)
    return 0 if result.get('complete') else (3 if result['result'] == 'PAUSED' else 2)


if __name__ == '__main__':
    raise SystemExit(main())
