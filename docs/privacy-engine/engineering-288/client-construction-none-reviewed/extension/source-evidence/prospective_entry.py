"""Status-contract boundary for trusted, single-threaded prospective integration.

General callers receive only Client.state/handle data, never the historical
wrapper, manager, scheduler, control capability or raw diagnostic exception.
This is API discipline inside a trusted Python process, not an introspection,
debugger, monkeypatch, hostile callback, OS-stream or timing security boundary.
The exact retained launcher owns initialization, records, cleanup and recovery.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import types

_ROOT = Path(__file__).resolve().parents[1]
_DEPENDENCY_SHA = 'ca01fd9b3c1543e8daa5796b09f7334beea2fef30eabd0f5e068c12c12c607c8'
_OWNERS = {}
_STATE_KEYS = frozenset(('binding', 'seq', 'head', 'counts', 'partitions', 'u', 'active', 'resources'))


class ClientFailure(RuntimeError):
    """Coarse boundary failure, never a proof of nonexecution or permission retry."""


def _fail():
    raise ClientFailure('MANAGED-OPERATION-UNAVAILABLE; outcome uncertain; no renewed authorization') from None


def _identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def _regular(path):
    if not stat.S_ISREG(path.lstat().st_mode):
        raise RuntimeError('NONREGULAR-DEPENDENCY')
    return path.read_bytes()


def verify_inputs(root=_ROOT):
    """No application import/session access. Stable trusted filesystem assumed."""
    root = Path(root)
    raw = _regular(root / 'provenance/dependency-pins.json')
    if hashlib.sha256(raw).hexdigest() != _DEPENDENCY_SHA:
        raise RuntimeError('DEPENDENCY-PINS')
    pins = json.loads(raw)
    expected_dirs = {str(p) for n in pins for p in Path(n).parents if str(p) != '.'}
    # Classify every dependency entry before reading any candidate payload.
    files, directories = set(), set()
    def walk(directory):
        if not stat.S_ISDIR(directory.lstat().st_mode):
            raise RuntimeError('DEPENDENCY-DIRECTORY')
        directories.add(str(directory.relative_to(root)))
        with os.scandir(directory) as entries:
            for e in entries:
                q = Path(e.path); name = str(q.relative_to(root))
                mode = e.stat(follow_symlinks=False).st_mode
                if stat.S_ISDIR(mode):
                    if name not in expected_dirs:
                        raise RuntimeError('UNDECLARED-DIRECTORY')
                    walk(q)
                elif stat.S_ISREG(mode) and name in pins:
                    files.add(name)
                else:
                    raise RuntimeError('UNDECLARED-OR-NONREGULAR-DEPENDENCY')
    for name in ('contract', 'retained'):
        walk(root / name)
    if files != set(pins) or directories != expected_dirs:
        raise RuntimeError('DEPENDENCY-MEMBERSHIP')
    for name, expected in pins.items():
        if _identity(_regular(root / name)) != expected:
            raise RuntimeError('STALE-DEPENDENCY')
    return pins


def _load_launcher():
    verify_inputs()
    if not sys.dont_write_bytecode:
        raise RuntimeError('REQUIRE-PYTHON-B')
    path = _ROOT / 'retained/launcher/code/lab_bootstrap.py'
    module = types.ModuleType('_i164_retained_status_launcher')
    module.__file__ = str(path)
    # Execute the authenticated source bytes, never an ambient lab_bootstrap.
    exec(compile(_regular(path), str(path), 'exec'), module.__dict__)
    return module


def _data(value):
    """Detach only exact JSON value types; never invoke object copy/repr hooks."""
    if type(value) in (str, int, bool, type(None)):
        return value
    if type(value) is list:
        return [_data(v) for v in value]
    if type(value) is dict and all(type(k) is str for k in value):
        return {k: _data(v) for k, v in value.items()}
    raise RuntimeError('UNSUPPORTED-CLIENT-VALUE')


class _Owner:
    __slots__ = ('wrapper', 'failure')
    def __init__(self, wrapper):
        self.wrapper = wrapper
        self.failure = None


class Client:
    """General client surface: state and authenticated packet handling only."""
    __slots__ = ('__token',)
    def __init__(self, token):
        self.__token = token
    def state(self):
        return _dispatch(self.__token, 'state', None)
    def handle(self, authenticated_packet):
        return _dispatch(self.__token, 'handle', authenticated_packet)
    def __repr__(self):
        return '<I164 general client>'
    def __reduce_ex__(self, protocol):
        raise TypeError('CLIENT-CAPABILITY-NOT-SERIALIZABLE')
    def __copy__(self):
        raise TypeError('CLIENT-CAPABILITY-NOT-COPYABLE')
    def __deepcopy__(self, memo):
        raise TypeError('CLIENT-CAPABILITY-NOT-COPYABLE')


class _Control:
    """Designated trusted diagnostics only; never handed to the general client."""
    __slots__ = ('__token',)
    def __init__(self, token):
        self.__token = token
    def status(self):
        owner = _OWNERS.get(self.__token)
        if owner is None:
            _fail()
        return owner.wrapper.status()
    def __repr__(self):
        return '<I164 internal control>'
    def __reduce_ex__(self, protocol):
        raise TypeError('CONTROL-CAPABILITY-NOT-SERIALIZABLE')


def _dispatch(token, operation, packet):
    owner = _OWNERS.get(token)
    if owner is None or owner.failure is not None:
        _fail()
    try:
        if operation == 'handle':
            if type(packet) is not bytes:
                raise TypeError('PACKET-BYTES')
            result = owner.wrapper.handle(packet)
            if type(result) is not bytes:
                raise TypeError('RESPONSE-BYTES')
            return result  # Preserve exact authenticated response; no re-encoding.
        if operation != 'state':
            raise RuntimeError('CLIENT-OPERATION')
        result = owner.wrapper.state()
        if type(result) is not dict or set(result) != _STATE_KEYS:
            raise RuntimeError('STATE-SHAPE')
        return _data(result)
    except BaseException as error:
        # Keep the ORIGINAL failure for the launcher's existing retention/cleanup
        # path. No new log and no swallowed fault if the client catches failure.
        owner.failure = error
    # Outside the handler: no original engine exception in __context__/__cause__.
    _fail()


def _run(launcher, candidate, draft, runtime, destination, client, create, control):
    """Trusted orchestration seam; production callers use run/run_controlled."""
    failed = False
    try:
        with launcher.session(candidate, draft, runtime, destination, create=create) as wrapper:
            owner = _Owner(wrapper); token = object(); _OWNERS[token] = owner
            try:
                if control is not None:
                    control(_Control(token))  # Explicit separately authorized use.
                try:
                    client(Client(token))
                except BaseException as client_error:
                    if owner.failure is not None:
                        raise owner.failure from client_error
                    raise
                if owner.failure is not None:
                    raise owner.failure
            finally:
                # Revoke before close, including failed/uncertain cleanup.
                _OWNERS.pop(token, None)
        # Callback returns are deliberately not forwarded to another recipient.
    except BaseException:
        # Original launcher already handled original failure/cleanup evidence.
        # Do not print it, transform its retained record, or infer nonexecution.
        failed = True
    if failed:
        _fail()


def run(candidate, draft, runtime, destination, client, *, create=False):
    """General entry: no control capability, status return or status publication."""
    failed = False
    try:
        launcher = _load_launcher()
    except BaseException:
        failed = True
    if failed:
        _fail()
    return _run(launcher, candidate, draft, runtime, destination, client, create, None)


def run_controlled(candidate, draft, runtime, destination, client, *, control, create=False):
    """Trusted owner entry ONLY; control may consume/capture exact status under
    separate authorization. This callable is not authentication of its caller.
    No capture sink, logger, serializer or retention permission is added here.
    """
    failed = False
    try:
        launcher = _load_launcher()
    except BaseException:
        failed = True
    if failed:
        _fail()
    return _run(launcher, candidate, draft, runtime, destination, client, create, control)


class _Arguments(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError('ARGUMENTS')


def main(argv=None):
    """Prospective initialize CLI. Fixed completion/failure only, no raw traceback."""
    try:
        parser = _Arguments(add_help=False, exit_on_error=False)
        parser.add_argument('operation', choices=['initialize'])
        for name in ('candidate', 'draft', 'runtime', 'destination'):
            parser.add_argument('--' + name, required=True)
        args = parser.parse_args(argv)
        run(args.candidate, args.draft, args.runtime, args.destination, lambda client: None, create=True)
    except BaseException:
        print('FAILED; outcome uncertain; admission disabled', file=sys.stderr)
        return 1
    print('PASS initialization and confirmed close; admission disabled')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
