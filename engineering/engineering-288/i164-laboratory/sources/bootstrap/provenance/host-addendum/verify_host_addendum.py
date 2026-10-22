import hashlib,json,re,shutil,sys,zipfile
from pathlib import Path
sys.path.insert(0,'br-review/code')
from verify_checkpoint import verify,identity
root=Path('br-host-return');root.mkdir(exist_ok=False)
text=Path('upload/Pasted text(20261022-082656).txt').read_text()
shutil.copyfile('upload/Pasted text(20261022-082656).txt',root/'HOST-TRANSCRIPT.txt')
record,_=json.JSONDecoder().raw_decode(text[text.index('{\n'):])
lines=re.findall(r'(?m)(?:^|(?<=\}))[ \t]*(\d+)\t(.*)$',text)
assert [int(n) for n,_ in lines]==list(range(1,134))
lock='\n'.join(s for _,s in lines)+'\n'
assert identity(lock.encode())=={k:record['original_record_identities']['requirements.lock'][k] for k in ('bytes','sha256')}
(root/'requirements.lock').write_text(lock)
(root/'HOST-PROBE-RESULT.json').write_text(json.dumps(record,indent=2)+'\n')
wanted={};hash_counts={};pending=''
for line in lock.splitlines():
 line=line.strip()
 if not line or line.startswith('#'):continue
 more=line.endswith('\\')
 pending+=(' '+line[:-1].rstrip() if more else ' '+line)
 if more:continue
 tokens=pending.split();pending=''
 m=re.fullmatch(r'([A-Za-z0-9_.-]+)==([A-Za-z0-9_.+!-]+)',tokens[0]);assert m
 name=re.sub('[-_.]+','-',m[1]).lower();assert name not in wanted
 assert tokens[1:] and all(re.fullmatch(r'--hash=sha256:[0-9a-f]{64}',t) for t in tokens[1:])
 wanted[name]=m[2];hash_counts[name]=len(tokens)-1
assert not pending
assert wanted==record['current_environment']['distributions']=={'cffi':'2.1.1','cryptography':'41.0.7','pycparser':'3.11'}
assert record['current_environment']['python']=='3.12.14' and record['current_environment']['implementation']=='CPython' and record['current_environment']['optimize']==0
prior=Path('Engineering-Anchor2-I164-lab-bootstrap-independent-review.zip')
old=verify(prior,{'bytes':30265291,'entries':194,'sha256':'a1a551594b744c505ab58527101dcf1f18b567686f52d502e6e6358c862b90e5'})
shutil.copyfile(prior,root/prior.name)
result={'reviewer':'Codex, separate from SU-Engineering[288C] construction author','recipient':'Engineering-Anchor[2]','verdict':'CORRECTIONS REQUIRED; BR-01 and BR-02 remain open','prior_checkpoint':old,'host_evidence':'Supplied terminal transcript; no direct access to the host','lock_reconstruction':'133 numbered lines reconstructed; bytes and SHA-256 match the captured original lock identity','versions_from_lock':wanted,'hash_options_per_requirement':hash_counts,'host_reported_launcher_environment_gate':'PASS CPython 3.12.14, optimize=0, Cryptography 41.0.7','host_failure':'Reviewer probe cannot parse hash-pinned multi-line lock; not a launcher finding','host_operations_not_reached':['pip check','runtime recovery','temporary session creation/reopening'],'remaining_environment_limits':['Original ENVIRONMENT-RESULT.json and COMPATIBILITY-RESULT.json bodies not supplied; exact record reconciliation remains pending','Installed version agreement is not verification of installed wheel bytes against lock hashes','No public 41.0.7 runtime compatibility execution established'],'new_runtime_execution':False,'candidate_modifications':0,'persistent_session_created':False,'readiness':'BLOCKED','final_binding':'BLOCKED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','admission':False}
(root/'ADDENDUM.json').write_text(json.dumps(result,indent=2)+'\n')
(root/'RETURN-TO-ANCHOR.txt').write_text('''To Engineering-Anchor[2]

Author-independent bootstrap review: CORRECTIONS REQUIRED.
Implementation author: SU-Engineering[288C]. Reviewer: Codex, separate author.

This packet contains the unchanged verified independent-review ZIP and Steve's
subsequent host transcript. Original findings and all failure evidence are retained.

BR-01: the launcher requires an undeclared partial draft file as a mandatory
164th member. The clean, declared 163-file recovered dependency is rejected.
BR-02: recovery writes the authenticated native helper without executable mode;
authentication fails with PermissionError / BACKEND-UNAVAILABLE.

Host addendum: the public environment gate accepted CPython 3.12.14 (optimize=0)
and Cryptography 41.0.7. The three reported installed distribution versions agree
exactly with the supplied hash-pinned lock. The lock was reconstructed from the
terminal transcript and matches its recorded 11,173-byte SHA-256 identity.

The subsequent UNSUPPORTED-LOCK-LINE failure is in the reviewer's diagnostic
script: it only supported single-line name==version records. The actual lock
uses continuation lines and SHA-256 options. Preserve this harness failure;
do not treat it as a candidate defect or alter the valid lock to fit the probe.
Runtime recovery and temporary create/reopen were not reached on Steve's host.
The original environment/compatibility record bodies and installed artifact
hash reconciliation remain outstanding; passing version checks is not full
runtime compatibility confirmation. Earlier mechanics tests used 50.0.2.

Next bounded implementation task: correct BR-01's recovery-membership binding
and BR-02's authenticated helper permissions, preserve accidental partials
outside strict recovered roots, and return exact changed identities with focused
recovery/authentication controls for independent closure. In that correction,
reconcile the prepared host records and use a hash-lock-aware temporary probe.
Do not patch Steve's lock, fabricate partial files, or initialize a persistent
session to work around either defect. No lifecycle or completed-review rerun.

SOURCE-ONLY unchanged. Readiness/final binding blocked; backup kernel-only;
streams UNCOMPUTED; admission disabled. No candidate edits or policy adoption.
''')
shutil.copyfile('br-host-package.py',root/'verify_host_addendum.py')
manifest={p.relative_to(root).as_posix():identity(p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file()}
(root/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
out=Path('Engineering-Anchor2-I164-bootstrap-review-host-addendum.zip')
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(root).as_posix())
print(json.dumps({'host_check':result,'checkpoint':verify(out)},indent=2))
