import hashlib, json, os, re, stat, subprocess, tempfile, traceback, zipfile
from pathlib import Path

TARGET = 'engineering/engineering-288/i164-laboratory'
MILESTONE = 'Bounded laboratory snapshot correspondence complete'
CODE = {'.py', '.md', '.go', '.rs', '.sol', '.toml'}
OMIT = {'evidence', 'results', 'failures', 'fixtures', 'results-predecessor', '__pycache__'}
PATTERNS = [
    ('private-key', re.compile(rb'(?m)^\s*-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),
    ('github-token', re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b')),
    ('aws-access-key', re.compile(rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b')),
    ('slack-token', re.compile(rb'\bxox[baprs]-[A-Za-z0-9-]{20,}\b')),
    ('credential-url', re.compile(rb'https?://[^\s/"\x27:@]+:[^\s/"\x27@]+@')),
    ('literal-secret', re.compile(rb'(?im)^\s*["\x27]?(?:password|api[_-]?key|access[_-]?token|client[_-]?secret)["\x27]?\s*[:=]\s*["\x27][A-Za-z0-9+/=_-]{16,}["\x27]'))
]

def need(v, message):
    if not v: raise RuntimeError(message)

def enc(v): return json.dumps(v, sort_keys=True, indent=2, ensure_ascii=True).encode() + b'\n'
def ident(raw): return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
def read(p):
    need(stat.S_ISREG(p.lstat().st_mode), 'NONREGULAR: ' + str(p))
    fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as f: return f.read()
def load(p): return json.loads(read(p))
def safe_name(n):
    p = Path(n)
    need(not p.is_absolute() and '..' not in p.parts, 'UNSAFE MEMBER: ' + n)
    return p
def scan(name, raw):
    for label, pattern in PATTERNS:
        need(not pattern.search(raw), 'SECRET SCAN BLOCKED ' + label + ': ' + name)
def archive(path, expected):
    raw = read(path); need(ident(raw) == expected, 'ARCHIVE IDENTITY: ' + str(path))
    with zipfile.ZipFile(path) as z:
        names = z.namelist(); need(len(names) == len(set(names)) and z.testzip() is None, 'ZIP CRC/DUPLICATES')
        for n in names: safe_name(n)
        m = json.loads(z.read('PACKAGE-MANIFEST.json'))
        need(set(names) == set(m) | {'PACKAGE-MANIFEST.json'}, 'ZIP MEMBERSHIP')
        for n, v in m.items(): need(ident(z.read(n)) == v, 'ZIP HASH: ' + n)
        return {n: z.read(n) for n in names}

def run(cfg):
    os.umask(0o077)
    repo, base, downloads, composition = (Path(cfg[k]).absolute() for k in ('repo', 'base', 'downloads', 'composition'))
    evidence = Path(tempfile.mkdtemp(prefix='I164-git-checkpoint-', dir=base))
    receipt = {'milestone': MILESTONE, 'status': 'INCOMPLETE', 'repository': str(repo), 'staging_root': TARGET,
               'readiness': 'BLOCKED', 'final_binding': 'BLOCKED', 'streams': 'UNCOMPUTED', 'admission': 'DISABLED'}
    print('PERSISTENT GIT EVIDENCE:', evidence, flush=True)
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GIT_OPTIONAL_LOCKS='0')
    def git(*args):
        p = subprocess.run(['git', '-C', str(repo), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        with (evidence / 'git.log').open('ab') as f:
            f.write(('git ' + ' '.join(args) + '\n').encode())
            # Do not save remote error text which could contain credential-bearing URLs.
            f.write(('exit=' + str(p.returncode) + '\n').encode())
        need(p.returncode == 0, 'Git failed: ' + ' '.join(args) + '; exit ' + str(p.returncode))
        return p.stdout
    def text(*a): return git(*a).decode().strip()
    try:
        print('Checking main/origin/main and preserving unrelated files', flush=True)
        need(text('rev-parse', '--show-toplevel') == str(repo.resolve()), 'REPOSITORY ROOT')
        need(text('symbolic-ref', '--short', 'HEAD') == 'main', 'EXPECTED BRANCH main')
        need(text('rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{upstream}') == 'origin/main', 'UPSTREAM')
        need(not git('diff', '--name-only', 'HEAD'), 'TRACKED WORK OR STAGED CHANGES: preserve and stop')
        before = git('status', '--porcelain=v1', '-z', '--untracked-files=all')
        need(all(x.startswith(b'?? ') for x in before.split(b'\0') if x), 'UNEXPECTED INDEX STATE')
        head = text('rev-parse', 'HEAD'); receipt['parent_commit'] = head
        remote = text('ls-remote', '--exit-code', 'origin', 'refs/heads/main').split()
        need(len(remote) == 2 and remote[0] == head and remote[1] == 'refs/heads/main', 'REMOTE main differs; no merge/reset attempted')
        dest = repo / TARGET
        need(not os.path.lexists(dest), 'CHECKPOINT DESTINATION EXISTS: no overwrite')
        # Repository-specific instructions must be inspected before introducing a new subtree.
        for parent in [repo, *(repo / TARGET).parents]:
            if parent == repo or parent.is_relative_to(repo):
                need(not (parent / 'AGENTS.md').exists(), 'Applicable AGENTS.md requires source inspection: ' + str(parent / 'AGENTS.md'))

        recovery = base / 'I164-reviewed-recovery-0s8zad3j'
        candidate, draft = Path(cfg.get('candidate', recovery / 'current-candidate')), Path(cfg.get('draft', recovery / 'draft-connection'))
        impl = composition / 'implementation'
        mpins = {
            'candidate-members.json': 'feef1fd4b423c067fa073b9aacb788a6553ec6fe99cde2dbfb0154ff25119209',
            'draft-members.json': '98328cd843a8a4522be2a0f3e3d4811800087ec65e5cab486be62d94e91b30ed'}
        source_groups = {}
        for label, root, name in [('candidate', candidate, 'candidate-members.json'), ('draft', draft, 'draft-members.json')]:
            raw = read(impl / 'provenance' / name); need(ident(raw)['sha256'] == mpins[name], 'SOURCE MANIFEST PIN')
            pins = json.loads(raw)
            for n, v in pins.items(): need(ident(read(root / safe_name(n))) == v, 'SOURCE BYTES: ' + label + '/' + n)
            source_groups[label] = (root, pins)
        cm = read(composition / 'MANIFEST.json')
        need(ident(cm)['sha256'] == 'e0a72db9245267bfe06d90cfaf22711a085d4030768051e20e9fad5dc80e00e7', 'CORRECTED BOOTSTRAP MANIFEST PIN')
        source_groups['bootstrap'] = (composition, json.loads(cm))
        need(ident(read(impl / 'code/lab_bootstrap.py'))['sha256'] == 'b2ce7f0fdf9aabb578da7330a9987a34b7c76e1fe1f543f913ba759aededc2f6', 'BR01 LAUNCHER PIN')

        acq_id = {'bytes': 70665, 'sha256': '554d27a0c5eb5d97c762eb082001930be9317c8f317ea62759557d01727177a4'}
        eval_id = {'bytes': 1480216, 'sha256': '333556b28a08669df72e0f0202c866c5da53720b337e4fb4079dba88b6698e1d'}
        acq = archive(downloads / 'I164-snapshot-acquisition-egpf25d9.zip', acq_id)
        ev = archive(downloads / 'I164-snapshot-evaluation-v3-3m90kxzp.zip', eval_id)
        result = json.loads(ev['RESULT.json'])
        need(result['status'] == 'PASS — bounded saved-snapshot correspondence' and result['environment_mode'] == 'prepared-host', 'SNAPSHOT VERDICT')
        need(result['actual_admission'] is False and result['final_binding'] == 'BLOCKED' and result['streams'] == 'UNCOMPUTED', 'STATUS BOUNDARY')
        need(ev['preserved/export.json'] == acq['export.json'], 'EXACT ACQUISITION LINEAGE')
        script = read(downloads / 'I164-evaluate-saved-snapshot-v3.py')
        need(ident(script) == result['script'], 'TESTED EVALUATOR IDENTITY')

        payload, mapping = {}, {}
        for label, (root, pins) in source_groups.items():
            rows = {}
            for n, expected in pins.items():
                p = safe_name(n)
                selected = not any(a in OMIT for a in p.parts) and (
                    p.suffix in CODE or (p.suffix == '.json' and expected['bytes'] <= 262144))
                if label == 'bootstrap':
                    selected = selected and (p.parts[0] in {'code', 'provenance'} or
                        n in {'RECOVERY.md', 'REPORT.md', 'MARKER-REPAIR.md', 'CHANGED-IDENTITIES.json', 'UBUNTU-VERIFY.sh'} or
                        n.startswith('implementation/code/') or n.startswith('implementation/provenance/') or n == 'implementation/laboratory-configuration.json')
                if selected:
                    raw = read(root / p); need(ident(raw) == expected, 'SELECTED SOURCE IDENTITY: ' + n)
                    payload['sources/' + label + '/' + n] = raw
                rows[n] = {**expected, 'storage': 'GIT' if selected else 'EXTERNAL-EXACT-DEPENDENCY'}
            mapping[label] = {'original_root': str(root), 'members': rows}
        payload['sources/evaluation/I164-evaluate-saved-snapshot-v3.py'] = script
        payload['tools/checkpoint.py'] = read(Path(__file__).absolute())
        payload['provenance/source-membership.json'] = enc(mapping)
        payload['provenance/snapshot-result.json'] = ev['RESULT.json']
        payload['provenance/acquisition-lineage.json'] = ev['lineage.json']
        payload['provenance/consumed-inputs.json'] = ev['consumed-inputs.json']
        payload['provenance/external-evidence.json'] = enc({
            'acquisition': {'path': str(downloads / 'I164-snapshot-acquisition-egpf25d9.zip'), **acq_id},
            'evaluation': {'path': str(downloads / 'I164-snapshot-evaluation-v3-3m90kxzp.zip'), **eval_id},
            'original_retry_archive': {'status': 'UNAVAILABLE; not recovered', 'bytes': 54899989,
                'sha256': '1f06a4034fab8ab7e0c17ea409ea15d113c9106f63bbfad96291fcb1368e5f09'},
            'independent_bootstrap_closure': {'bytes': 15203899, 'entries': 56,
                'sha256': '4c8dea732115276259e05744f5d86f40d47aa767733f25a55ba76cfea1f68df8',
                'scope': 'BR01 closure; 34 independent controls distinct from 27 inspected Engineering controls'}})
        payload['README.md'] = ('''# Engineering 288 I164 laboratory checkpoint

Bounded laboratory snapshot correspondence complete. SOURCE-ONLY.
Readiness and final binding BLOCKED; streams UNCOMPUTED; admission DISABLED.
This is not definition acceptance, canonical registration, qualification or deployment readiness.

This new Git subtree checkpoints reviewed source bytes and exact provenance.
It does not replace STATE.md or designate a prospective canonical model HEAD.
Public deterministic laboratory identities in reviewed source are test-only, not operational custody.
No session state, databases, environments, operational credentials, archives or large generated artifacts are committed.
All 666 candidate members and 163 draft members retain exact identities in provenance/source-membership.json.
GIT entries mirror their source-relative paths beneath sources/{candidate,draft,bootstrap}.
EXTERNAL-EXACT-DEPENDENCY entries are intentionally not included; this checkout alone is not a runnable installation.
Read provenance/external-evidence.json for exact saved acquisition/evaluation identities.

## Recovery
Keep original reviewed archives, recovered source roots, session state and saved evidence unchanged outside Git.
For each source group, verify every original relative member against its bytes and SHA-256 in source-membership.json.
Recover unavailable members only from exact retained checkpoint dependencies; never substitute files by basename.
To materialize elsewhere, use a new isolated directory and combine the GIT members with all verified external members,
preserving their original relative layout. Verify all member identities before invoking the existing recovery/validation procedures.
Do not run the bootstrap or initialize a session as part of recovery. The saved snapshot evaluation requires the preserved acquisition ZIP.
Its evaluator is sources/evaluation/I164-evaluate-saved-snapshot-v3.py; existing default paths refer to the original laboratory workspace.

Snapshot counts are finite per acquisition and per symbolic context; they are not production or lifetime bounds.
No cross-acquisition joins, new allowances, retention/compaction, policy change, lifecycle rerun or full expansion is adopted.
All inherited relationships, ordinals, historical identities, scoped review limitations and unresolved obligations remain intact.
Backup support remains kernel-only. Decision B remains in force.
''').encode()
        payload['.gitignore'] = b'__pycache__/\n*.pyc\n*.sqlite*\n*.db\n*.zip\n*.gz\n.env*\n*.pem\n*.key\nvenv/\n.venv/\n'
        for name, raw in payload.items(): scan(name, raw)
        print('Source/provenance selection:', len(payload), 'files;', sum(map(len, payload.values())), 'bytes', flush=True)
        need(not git('diff', '--name-only', 'HEAD') and git('status', '--porcelain=v1', '-z', '--untracked-files=all') == before, 'REPOSITORY CHANGED DURING PREPARATION')
        dest.mkdir(parents=True)
        for name, raw in payload.items():
            p = dest / name; p.parent.mkdir(parents=True, exist_ok=True)
            with p.open('xb') as f: f.write(raw)
        manifest = {n: ident(raw) for n, raw in payload.items()}
        (dest / 'MANIFEST.json').write_bytes(enc(manifest))
        git('add', '--', TARGET)
        staged = git('diff', '--cached', '--name-only', '-z').decode().split('\0')
        staged = {p for p in staged if p}
        expected = {TARGET + '/' + n for n in payload} | {TARGET + '/MANIFEST.json'}
        need(staged == expected, 'EXACT STAGED MEMBERSHIP')
        for name in sorted(staged):
            raw = git('show', ':' + name); scan(name, raw)
            rel = str(Path(name).relative_to(TARGET))
            wanted = enc(manifest) if rel == 'MANIFEST.json' else payload[rel]
            need(raw == wanted, 'STAGED BYTES CHANGED: ' + name)
        whitespace = subprocess.run(['git', '-C', str(repo), 'diff', '--cached', '--check'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        need(whitespace.returncode in (0, 2), 'UNEXPECTED WHITESPACE CHECK FAILURE')
        (evidence / 'inherited-whitespace.txt').write_bytes(whitespace.stdout + whitespace.stderr)
        receipt['whitespace_check'] = 'PASS' if whitespace.returncode == 0 else 'Inherited pinned whitespace preserved; see inherited-whitespace.txt'
        need(git('status', '--porcelain=v1', '-z', '--untracked-files=all', '--', '.', ':(exclude)' + TARGET) == before, 'UNRELATED WORK CHANGED')
        receipt.update({'secret_scan': 'PASS heuristic staged-content scan; not a proof of absence', 'staged_files': len(staged),
                        'source_bytes': sum(map(len, payload.values())), 'unrelated_status_before_hex': before.hex()})
        (evidence / 'PRECOMMIT.json').write_bytes(enc(receipt))
        print('Committing exact staged checkpoint; unrelated files excluded', flush=True)
        git('commit', '-m', 'Engineering 288: bounded laboratory snapshot correspondence complete', '-m',
            'Preserve reviewed I164 candidate/bootstrap sources and snapshot bindings. SOURCE-ONLY; readiness/final binding blocked; streams UNCOMPUTED; admission disabled. Large artifacts and laboratory state remain external exact dependencies.')
        commit, tree = text('rev-parse', 'HEAD'), text('rev-parse', 'HEAD^{tree}')
        receipt.update({'commit': commit, 'tree': tree, 'commit_created': True})
        need(text('rev-parse', 'HEAD^') == head, 'UNEXPECTED COMMIT PARENT')
        committed = {x for x in git('diff-tree', '--no-commit-id', '--name-only', '-r', '-z', 'HEAD').decode().split('\0') if x}
        need(committed == expected, 'COMMIT MEMBERSHIP')
        for name in sorted(expected): need(git('show', 'HEAD:' + name) == read(repo / name), 'COMMITTED BYTES')
        need(git('status', '--porcelain=v1', '-z', '--untracked-files=all') == before, 'UNRELATED WORK/POST-COMMIT STATUS CHANGED')
        print('Pushing main to origin/main (no force)', flush=True)
        git('push', 'origin', 'HEAD:refs/heads/main')
        receipt['push_command_succeeded'] = True
        remote = text('ls-remote', '--exit-code', 'origin', 'refs/heads/main').split()
        need(len(remote) == 2 and remote[0] == commit, 'REMOTE TIP CONFIRMATION')
        receipt.update({'status': 'PASS — committed and pushed bounded laboratory checkpoint', 'remote_commit': remote[0], 'unrelated_work_preserved': True})
    except BaseException as exc:
        receipt['status'] = 'STOP — Git checkpoint incomplete; preserve existing files/index and inspect receipt'
        receipt['error'] = type(exc).__name__ + ': ' + str(exc)
        (evidence / 'failure.txt').write_text(traceback.format_exc())
    (evidence / 'GIT-RESULT.json').write_bytes(enc(receipt))
    summary = downloads / (evidence.name + '-result.json')
    with summary.open('xb') as f: f.write(enc(receipt))
    print(receipt['status'])
    if 'error' in receipt: print(receipt['error'])
    print('COMMIT:', receipt.get('commit', 'NOT ESTABLISHED'))
    print('TREE:', receipt.get('tree', 'NOT ESTABLISHED'))
    print('PUSH:', receipt.get('remote_commit', 'NOT CONFIRMED'))
    print('REPORT:', summary)
    print('SOURCE-ONLY; readiness/final binding BLOCKED; streams UNCOMPUTED; admission disabled.')
    return receipt

if __name__ == '__main__':
    base = Path('/home/steve/dev/Engineering-288-execution')
    run({'repo': '/home/steve/dev/Speak-up-appV3', 'base': str(base), 'downloads': '/home/steve/Downloads',
         'composition': str(base / 'I164-lab-bootstrap-reviewed-001/composition')})
