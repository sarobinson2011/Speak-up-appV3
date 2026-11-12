"""Static documentation, identity audit and packaging only; no launch."""
from pathlib import Path
import ast,base64,hashlib,json,shutil,zipfile,stat,datetime
B=Path(__file__).resolve().parent;O=B/'package';C=B/'candidate';H=B/'parent-host';plan=json.loads((O/'PLAN.json').read_bytes());W=plan['workspace'];A=plan['attempt']
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def wr(p,v):p.write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
def locations(p):return {n.name:n.lineno for n in ast.parse(p.read_bytes()).body if isinstance(n,ast.FunctionDef)}
loc=locations(C/'code/correspondence.py');ploc=locations(C/'retained/res-null/code/correspondence.py')
(O/'AUTHENTICATION-PATH.txt').write_text(f'''PLANNED ONLY. Preparation performed no authentication, public validation, authenticated constructed-path execution, application/helper execution or host action.

1. public_positive.py verifies the exact assembled root and expected receipt, installs the retained native observer after qualified host preflight, then invokes m.validate(root, expected) ONCE. The pinned expected bytes are an input, never a returned basis.
2. Current correspondence.py validate:{loc['validate']} -> derive:{loc['derive']} -> _basis:{loc['_basis']}(inputs:{loc['inputs']}(root)). inputs checks retained/res-null exact membership, types, all hashes, component pins and parent receipt. _basis rechecks inputs, calls the unchanged parent _receipt_shape, actual _basis and _assemble, and requires equality to the pinned parent receipt. It then compiles the new catalogue and returns its basis. Neither the candidate nor parent is changed.
3. Parent res-null correspondence.py _basis:{ploc['_basis']} performs its unchanged fast-completion authentication/receipt equality. The unchanged fast, enter-decref, return-to-res, enter-call, lookup and R1 substantive authentication paths follow. R1 calls helper._checked(pd, helper.catalogue(pd)) and helper._receipt_checked. Helper._checked/_basis reaches helper._public_predecessor, which invokes the retained deeper write-call PUBLIC validate under the existing cooperative monitoring contract. These mandatory internal computations belong to this one new public positive, not a replay of completed control/review campaigns.
4. The unchanged observer captures the new _basis actual return by exact code identity, with exactly one capture required. The harness follows actual parent_module/parent_basis objects through res-null, fast, decref, return, enter, lookup, R1 and helper. It verifies each module origin, reassembles each actual basis, and compares exact saved receipt bytes and identities. These post-return serialization/comparison calls do not authenticate again.
5. The current receipt is reassembled from the actual captured basis and compared byte-for-byte to expected/expected-exit-decref-receipt.json, including both contexts. The new validate wrapper count must be1. Res-null/fast/decref/return/enter/lookup/R1/helper thin validate wrappers must each be0; their substantive authentication executes internally instead. The deeper write-call public validate and older mandatory chain remain unchanged and are recorded.
6. No new _construct_checked or constructed_projection call is authorized. Authenticated constructed-path execution stays UNTESTED. This run authenticates mandatory declaration-receipt derivation, not constructed true-branch example execution or runtime decrement arrival. Full public negative derivations remain zero.

Record actual-public-result.json, actual-parent-provenance.json, actual-derived-receipt.json, actual-receipt-comparison.json, calls.json, timestamped computation events/counts, stdout/stderr chunks, RESULT.json, explicit child exit and distinct service/manager observations. Completion requires agreeing records. A heartbeat, inactive service or free monitoring slot is not completion or complete cleanup evidence.

The existing execution guards, observer, native binary, supervisor, runtime profile and byte recovery are preserved. No saved PASS substitution, stub, injected return basis or weakened authentication. Offline expectation assembly called the fixed pure exit_decref_catalogue and serializer _assemble/_rows/declaration_rows using saved data; its separate record is preparation-records/offline-assembly.json. No candidate authentication was called.
''')
(O/'OPERATE.txt').write_text(f'''PREPARED ONLY. Launch requires separate explicit authorization for {A}. No host reservation or launch occurred in preparation.

One NEW required Ubuntu file:
/home/steve/Downloads/I164-launch-exit-decref-attempt-public-1.py
This self-contained launcher embeds the exact preparation ZIP and verifies payload and inner-launcher identities. The separately delivered ZIP is for review/recovery; no separate Ubuntu download is necessary. The launcher creates its embedded ZIP at /home/steve/Downloads/I164-exit-decref-attempt-1-public-preparation.zip only after the exact authorization argument, preserving conflicting files.

Existing dependency, identity-checked at its exact known path before recovery:
{plan['launcher_host_path']}
{plan['launcher_archive']['bytes']} bytes; SHA-256 {plan['launcher_archive']['sha256']}
Do not execute the ZIP or transfer it again. This preparation recovered it directly and verified all required bytes. Host existence is checked by the launcher, not claimed here.

Qualified installed interpreter:
{plan['python']}
Exact retained CPython3.12.14/Linux x86_64 ABI/interpreter/header/native/dependency profile; Cryptography50.0.0. Reuse installed runtime and completed dummies, no installation/rebuild/new qualification. Retained50.0.2 laboratory profile stays distinct. Preflight stops on mismatch. Ubuntu24.04,systemd>=254,active user manager,existing Linger=yes and8GiB free required; no host cleanup.

After separate authorization ONLY, use the delivered outer SHA256 check and then:
python3 -I -B /home/steve/Downloads/I164-launch-exit-decref-attempt-public-1.py --authorize {A}

Workspace: {W}
Service: {plan['unit']}, Restart=no. Exactly one exclusive reservation, zero automatic retries. Existing/partial workspace or service is preserved; no automatic reset/relaunch.
Estimate60–90minutes plus1–3minutes preflight/recovery (disk dependent). Retained parent took3564.5549862799817seconds (~59.4minutes). Soft6600seconds(110minutes), child-supervisor6900(115), manager7200(120), plus normal stop grace. No timing promise or new benchmark.

Read-only status after launch:
python3 -I -B {W}/code/status.py

Computation events: {W}/validation/results/events.jsonl
Raw streams/chunks: {W}/validation/process/ (stdout.log,stderr.log and indexed chunks)
Public result: {W}/validation/results/RESULT.json
Actual receipt: {W}/validation/results/actual-derived-receipt.json
Explicit child exit: {W}/validation/process/exit.json
Reconciliation: {W}/validation/RECONCILIATION.json
Service wrapper exit: {W}/service-exit.json
Manager observation: {W}/manager-exit.json
Start receipt: {W}/LAUNCH-RECEIPT.json (start only, never completion)

After service AND original child have stopped, export saved evidence without validation:
python3 -I -B {W}/code/export_evidence.py
Output: /home/steve/Downloads/I164-exit-decref-attempt-public-1-host-evidence.tar.gz
The exporter preserves failed/UNKNOWN outcomes, checks stable bytes and refuses existing/partial exports. Once the exact export is saved, subsequent chats retrieve it directly; no repeated transfer or execution.
''')
(O/'RECOVERY.txt').write_text('''Verify preparation ZIP identity,CRC,safe unique regular membership and flat MANIFEST.json hashes. The exact source/results ZIPs are embedded under inputs/. Reuse289controls(79PASS/210REJECTED), five exit0 batches; raw/progress/stdout/RESULT agree. No replay. Historical159independent,145timeout rows(missing final records),171continuation andoneUbuntu parent positive stay distinct, with all earlier qualifications.

Exact parent retained/res-null:4729files/1238directories; manifest2260614bytes SHA96942689c3066bda9a80629672dc877850598658d44964dfa6119f824c37060d; receipt19046155bytes SHA1fbbea61a963361dd0369aefa97f6b2954bc9a5099dd891fbc02e9f239620e6e. Byte-only assembly verified every nested root. New assembled tree4963files/1264directories. Restore with unchanged recovery.py/common_r1.py, pinned embedded sources, exact external helper archive and expected manifests. Never import application sources or open databases for recovery.

expected/expected-exit-decref-receipt.json is OFFLINE EXPECTED OUTPUT ONLY. See PLAN and preparation-records/offline-assembly.json. Do not substitute it for a returned basis or regenerate on mismatch. The future one public positive must obtain actual returned basis through unchanged predecessor authentication and compare the entire receipt byte-for-byte in both contexts.

No host attempt reserved or launched here. The exact attempted identity needs separate approval. Existing partial workspace/reservation consumes its path: preserve, inspect, no retry. Exact installed runtime/observer/preflight and old recording dummies reused. Source/hash/syntax audits during preparation are not new control campaigns, public validation or runtime qualification.

Scope ends at conditional Py_DECREF(exit) attempt after true res==NULL and explicit continuation/exit-role continuity. CNULL differs from non-NULL PythonNone. No decrement completion/effects, destructor, error routing or false-branch operation. Authenticated constructed-path untested, runtime arrival/object state/physical effects and qualified-binary correspondence unestablished; zero-count destructor gap persists. Full public negative derivations zero; independent acceptance pending.

Both acquisitions,eleven obligations,4inventory/14lifetimeUNKNOWN,DecisionB,retention/allowances persist. SOURCE-ONLY;cumulative-envelope unadopted;backup kernel-only;streamsUNCOMPUTED;readiness/final binding blocked;admission disabled. Historical failures,UNKNOWNs,DOC-ENTER-01,separateR1 discrepancy,monitoring/free-slot qualifications and50.0.0/50.0.2 distinction retained. Confirmed Gitdc0851dae241ffaaf7ed84e75830f672981c020e reused; no Git operations.
''')
deps=json.loads((O/'INPUTS.json').read_bytes())
for d in deps.values():d['link']='https://chatgpt.com/library?file_id='+d['library_file_id']+'&account_id=personal'
wr(O/'INPUTS.json',deps)
wr(O/'CHECKPOINT.json',{'identity':plan['identity'],'status':'PREPARED ONLY; separate launch authorization pending','attempt':A,'source':plan['source_archive'],'results':plan['focused_results_archive'],'parent_manifest':plan['res_null_root_manifest'],'parent_files':4729,'parent_directories':1238,'parent_receipt':plan['res_null_receipt'],'candidate_manifest':plan['assembled_root_manifest'],'candidate_files':4963,'candidate_directories':1264,'expected_receipt':plan['expected_receipt'],'preparation_authentication_calls':0,'preparation_public_calls':0,'authenticated_constructed_path':'UNEXECUTED','completed_checks_replayed':0,'new_focused_controls':0,'reused_controls':289,'candidate_changes':0,'runtime_source_changes':0,'host_operations':0,'git_operations':0,'deadlines_seconds':{'soft':6600,'supervisor':6900,'manager':7200},'independent_acceptance':'PENDING','admission':False})
(O/'START-HERE.txt').write_text('PREPARED ONLY. Read CHECKPOINT.json,OPERATE.txt,AUTHENTICATION-PATH.txt,RECOVERY.txt. The sole prospective attempt is '+A+'. Download only I164-launch-exit-decref-attempt-public-1.py to Ubuntu after separate approval; it embeds the complete preparation ZIP. The existing large dependency is checked at its pinned preserved path. No controls, public runs or Git saves repeated.\n')
shutil.copyfile(B/'finish_preparation.py',O/'preparation-records/finish_preparation.py')
# Static consistency/byte audit only. No host, observer, candidate auth or test entry.
manifest=json.loads((O/'expected/ASSEMBLED-ROOT-MANIFEST.json').read_bytes());found={p.relative_to(C).as_posix() for p in C.rglob('*') if p.is_file()};assert found==set(manifest)
for n,pin in manifest.items():assert ident((C/n).read_bytes())==pin,n
assert len(manifest)==4963
assert ident((O/'expected/expected-exit-decref-receipt.json').read_bytes())==plan['expected_receipt']
receipt=json.loads((O/'expected/expected-exit-decref-receipt.json').read_bytes());assert receipt['format']=='I164-EXIT-DECREF-ATTEMPT-1'
assert [x['context'] for x in receipt['contexts']]==plan['contexts']
assert all(x['exit_decref_attempt_correspondence']['comparison_outcome'] is None and x['exit_decref_attempt_correspondence']['exit_decref_attempt'] is None for x in receipt['contexts'])
syntax=[]
for p in sorted((O/'code').glob('*.py')):ast.parse(p.read_bytes());compile(p.read_bytes(),str(p),'exec');syntax.append(p.name)
for n in ('host_prepare_launch.py','service_entry.py','public_positive.py'):
 s=(O/'code'/n).read_text();assert 'expected/expected-exit-decref-receipt.json' in s and 'expected/expected-res-null-receipt.json' not in s
assert "'res_null':True" in (O/'code/status.py').read_text() and "'res_null':0" in (O/'code/status.py').read_text()
assert str(plan['workspace']) in (O/'code/host_prepare_launch.py').read_text() or "BASE/'I164-exit-decref-attempt-public-1-20261112'" in (O/'code/host_prepare_launch.py').read_text()
wr(O/'preparation-records/final-static-audit.json',{'syntax_parsed_not_executed':syntax,'candidate_exact_fixed_bytes':True,'candidate_files':4963,'candidate_directories':1264,'parent_files':4729,'parent_directories':1238,'offline_receipt_both_contexts':True,'conditional_values_remain_UNESTABLISHED':True,'sole_new_public_call_AST':1,'expected_receipt_paths_consistent':True,'runtime_preflight_executed_here':False,'new_controls':0})
wr(O/'preparation-records/finalization-exit.json',{'exit':0,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Static preparation and packaging only; no launch'})
members={p.relative_to(O).as_posix():ident(p.read_bytes()) for p in sorted(O.rglob('*')) if p.is_file()};wr(O/'MANIFEST.json',members)
zp=B/'I164-exit-decref-attempt-1-public-preparation.zip'
with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in sorted(set(members)|{'MANIFEST.json'}):z.write(O/n,n)
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(members)+1
 for i in z.infolist():
  assert not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
  if i.filename in members:assert ident(z.read(i.filename))==members[i.filename]
zpin=ident(zp.read_bytes());innerpin=ident((O/'code/host_prepare_launch.py').read_bytes())
wrapper='''"""Self-contained prepared launcher. Launch requires separate approval for ATTEMPT."""
from pathlib import Path
import argparse,base64,hashlib,io,json,os,stat,zipfile
ATTEMPT=__ATTEMPT__
PIN=__PIN__
INNER=__INNER__
DEST=Path('/home/steve/Downloads/I164-exit-decref-attempt-1-public-preparation.zip')
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 p=argparse.ArgumentParser(description='Preparation only; separate launch approval required.')
 p.add_argument('--authorize',required=True);a=p.parse_args()
 if a.authorize!=ATTEMPT:raise SystemExit('STOP: wrong identified attempt authorization')
 if Path.home()!=Path('/home/steve'):raise SystemExit('STOP: expected Steve Ubuntu account')
 raw=base64.b64decode(b''.join(PAYLOAD.split()),validate=True)
 if identity(raw)!=PIN:raise SystemExit('STOP: embedded preparation identity mismatch')
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  code=z.read('code/host_prepare_launch.py')
  if identity(code)!=INNER:raise SystemExit('STOP: inner launcher identity mismatch')
 if not DEST.parent.is_dir() or DEST.parent.is_symlink():raise SystemExit('STOP: expected Downloads directory')
 if DEST.exists() or DEST.is_symlink():
  if not stat.S_ISREG(DEST.lstat().st_mode) or identity(DEST.read_bytes())!=PIN:raise SystemExit('STOP: existing bundle differs; preserved')
 else:
  with DEST.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 ns={'__name__':'_prepared_exit_decref_host_launcher','__file__':str(DEST)+'::code/host_prepare_launch.py'}
 exec(compile(code,ns['__file__'],'exec'),ns)
 ns['main'](DEST,a.authorize)
PAYLOAD=b"""__PAYLOAD__"""
if __name__=='__main__':main()
'''
wrapper=wrapper.replace('__ATTEMPT__',repr(A)).replace('__PIN__',repr(zpin)).replace('__INNER__',repr(innerpin)).replace('__PAYLOAD__',base64.encodebytes(zp.read_bytes()).decode())
lp=B/'I164-launch-exit-decref-attempt-public-1.py';lp.write_text(wrapper);tree=ast.parse(lp.read_bytes());compile(lp.read_bytes(),str(lp),'exec')
payload=next(n.value.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PAYLOAD' for t in n.targets));assert base64.b64decode(b''.join(payload.split()),validate=True)==zp.read_bytes()
summary={'preparation':{'filename':zp.name,**zpin,'entries':len(members)+1},'launcher':{'filename':lp.name,**ident(lp.read_bytes()),'self_contained':True,'embedded_preparation':zpin},'attempt':A,'expected_receipt':plan['expected_receipt'],'status':'PREPARED ONLY; NOT LAUNCHED'};wr(B/'delivery-identities.json',summary);print(json.dumps(summary,indent=2))
