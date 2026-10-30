"""Finite supervisor for the single authorized saved-input validation."""
from pathlib import Path
import datetime, json, os, signal, subprocess, sys, time

HERE = Path(__file__).resolve().parent
OUT = HERE / 'run'
OUT.mkdir(exist_ok=False)
TIMEOUT = 1800
START = time.monotonic()
def stamp(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(name, data):
    with (OUT / name).open('x') as f:
        json.dump(data, f, sort_keys=True, indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())
def note(data):
    data = {'utc': stamp(), 'seconds': time.monotonic() - START, **data}
    with (OUT / 'supervisor-progress.jsonl').open('a') as f:
        f.write(json.dumps(data, sort_keys=True) + '\n'); f.flush(); os.fsync(f.fileno())
    print(json.dumps(data, sort_keys=True), flush=True)
cmd = [sys.executable, '-I', '-B', '-u', str(HERE / 'only_pending_check.py'), str(OUT)]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
write('launch-plan.json', {'command': cmd, 'timeout_seconds': TIMEOUT, 'termination_grace_seconds': 5, 'retry': False, 'intended_check_count': 1})
with (OUT / 'stdout.log').open('xb') as stdout, (OUT / 'stderr.log').open('xb') as stderr:
    p = subprocess.Popen(cmd, cwd=HERE.parent, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
    write('process.json', {'pid': p.pid, 'supervisor_pid': os.getpid(), 'started_utc': stamp(), 'command': cmd, 'timeout_seconds': TIMEOUT})
    note({'event': 'launched', 'pid': p.pid})
    expired = False
    while p.poll() is None:
        remaining = TIMEOUT - (time.monotonic() - START)
        if remaining <= 0:
            expired = True; note({'event': 'timeout', 'pid': p.pid})
            os.killpg(p.pid, signal.SIGTERM)
            try: p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(p.pid, signal.SIGKILL); p.wait(timeout=5)
            break
        try: p.wait(timeout=min(30, remaining))
        except subprocess.TimeoutExpired:
            proc = Path('/proc') / str(p.pid)
            try: activity = {'stat': (proc/'stat').read_text(), 'io': (proc/'io').read_text()}
            except OSError as e: activity = {'inspection_error': repr(e)}
            note({'event': 'running', 'pid': p.pid, 'activity': activity})
    stdout.flush(); stderr.flush(); os.fsync(stdout.fileno()); os.fsync(stderr.fileno())
status = {'pid': p.pid, 'returncode': p.returncode, 'timed_out': expired, 'seconds': time.monotonic() - START, 'finished_utc': stamp(), 'retries': 0}
write('exit-status.json', status); note({'event': 'exited', **status})
sys.exit(124 if expired else (p.returncode if p.returncode is not None and p.returncode >= 0 else 1))
