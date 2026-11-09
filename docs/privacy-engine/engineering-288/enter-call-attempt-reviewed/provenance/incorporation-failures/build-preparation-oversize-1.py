from pathlib import Path
import ast,base64,hashlib,json,zipfile,zlib,collections

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'source'; REVIEW=ROOT/'review'; HOST=ROOT/'host'
OUT=ROOT/'selection'; DELIVERY=ROOT/'delivery'
OUT.mkdir(); DELIVERY.mkdir()
def enc(x):return (json.dumps(x,sort_keys=True,indent=2)+'\n').encode()
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def put(name,b):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def cp(base,name,target=None):put(target or name,(base/name).read_bytes())
def record(name,x):put(name,enc(x))
def doc(name,x):put(name,(x.strip()+'\n').encode())
BASE='8af23682a1757ea584f04b2b26303e7cb7f91160'
PREFIX='docs/privacy-engine/engineering-288/enter-call-attempt-reviewed'
RID='libfile_fde3_f-eeeeeda6c1c48191bede2f043aa4cb96_39c64cf85e608191bb9545db7327fd84'
REVIEW_PIN={'bytes':8272994,'sha256':'381bc024997b4c7c136dbb1c656a5dd3ababcb4fefa40dcc04d055334a261995'}
review_json=json.loads((REVIEW/'CHECKPOINT.json').read_bytes())
inputs=json.loads((REVIEW/'INPUTS.json').read_bytes())
deps={'review':dict(REVIEW_PIN,filename='I164-enter-call-attempt-1-independent-review.zip',library_file_id=RID,link='https://chatgpt.com/library?file_id='+RID+'&account_id=personal'),**inputs}
deps.pop('instructions')
for v in deps.values():v['git_included']=False

# Exact new component bytes and small source records. Shared defining/reference
# files are already preserved at the confirmed lookup commit, not resaved here.
for p in SOURCE.rglob('*'):
 if not p.is_file():continue
 n=p.relative_to(SOURCE).as_posix()
 if n=='MANIFEST.json':cp(SOURCE,n,'provenance/full-source-MANIFEST.json')
 elif not n.startswith(('reference/','source-evidence/')):cp(SOURCE,n,'extension/'+n)
prior=json.loads((SOURCE/'provenance/prior-selection-manifest.json').read_bytes())['members']
shared={}
for n in ['source-evidence/lab_bootstrap.py','reference/cpython-3.12.14/bytecodes.c','reference/cpython-3.12.14/typeobject.c','reference/cpython-3.12.14/compound_stmts.rst','reference/cpython-3.12.14/LICENSE','reference/r1/tests/fixtures.py']:
 b=(SOURCE/n).read_bytes();pin=ident(b);assert prior['extension/'+n]==pin
 shared[n]={'commit':BASE,'repository_path':'docs/privacy-engine/engineering-288/context-special-lookup-reviewed/extension/'+n,'identity':pin}
record('provenance/shared-defining-sources.json',shared)

# Exact review records, including raw rows, failed audit attempts and witness.
# Omit only the large input and the already-saved lookup review excerpt tree.
for p in REVIEW.rglob('*'):
 if not p.is_file():continue
 n=p.relative_to(REVIEW).as_posix()
 if not n.startswith(('inputs/','reused-lookup-review/')):cp(REVIEW,n,'review/'+n)
for n in ['RESULTS.txt','CHECKPOINT.json','SOURCE-CHECKPOINT.json','attempt-1/RECONCILIATION.json','attempt-1/exit.json']:
 if (ROOT/'supplied-results'/n).is_file():cp(ROOT/'supplied-results',n,'engineering/'+n)
for n in ['validation/RECONCILIATION.json','validation/results/RESULT.json','validation/results/actual-public-result.json','validation/results/actual-parent-provenance.json','validation/results/actual-receipt-comparison.json','validation/results/calls.json','validation/results/input-root.json','validation/results/final-root.json','validation/process/launch.json','validation/process/process.json','validation/process/exit.json','manager-exit.json','service-exit.json','ONE-ATTEMPT-RESERVATION.json','LAUNCH-RECEIPT.json','assembled-root.json','lookup-root.json','r1-root.json']:
 cp(HOST,n,'host/'+n)
for n in ['PREPARED.json','PLAN.json','START-HERE.txt','RECOVERY.txt','ACCOUNTING.json','PREPARATION-AUDIT.json']:
 cp(HOST,n,'chronology/preparation/'+n)
for p in (ROOT/'preparation-failures').iterdir():cp(p.parent,p.name,'provenance/incorporation-failures/'+p.name)
cp(SOURCE,'provenance/confirmed-lookup-save.json','provenance/confirmed-predecessor-save.json')
record('provenance/recovery-dependencies.json',deps)
record('provenance/review-intake.json',{'file':deps['review'],'entries':228,'manifested_hashes':227,'safe_unique_regular_membership':True,'crc':'PASS','all_manifest_hashes':'PASS','implementation_executed':False,'controls_replayed':0,'review_replayed':0})
record('provenance/save-search.json',{'date':'2026-11-09','queries':['SEND-TO-ANCHOR git enter','SEND-TO-ANCHOR-git-enter-call-attempt','enter-call-attempt git'],'matching_successful_receipt_found':False,'qualification':'No matching receipt found in returned saved-file results; not proof of host absence. Host command checks receipts and already-committed matching selection before any mutation.','host_repository_accessible_here':False,'confirmed_predecessor_commit':BASE,'previous_save_repeated':False})
record('provenance/review-incorporation.json',{
 'target':'I164-ENTER-CALL-ATTEMPT-1','reviewer':'Formal-Lab[6], separate from Engineering construction',
 'exact_review_verdict':'SUPPORTED within the bounded conditional SOURCE-ONLY enter-call-attempt correspondence contract. No candidate semantic defect demonstrated.',
 'review_identity':REVIEW_PIN,'review_library_file_id':RID,'candidate_changed':False,
 'documentation_finding':json.loads((REVIEW/'documentation-witness.json').read_bytes()),
 'independent_controls':{'rows':147,'PASS':64,'REJECTED':83,'exit':0,'reused_not_replayed':True,'layers':'review/independent-reconciliation.json and exact individual rows'},
 'engineering_controls':{'rows':489,'PASS':101,'REJECTED':388,'exit':0,'reused_not_replayed':True,'layers':'review/focused-record-audit.json; original source/result artifacts unchanged'},
 'host_public':{'positives':1,'actual_basis_captures':1,'bytes_equal':True,'exit':0,'seconds':3338.2737165039944,'new_validate_calls':1,'thin_lookup_R1_helper_validate_calls':0,'reused_not_replayed':True},
 'computation_events':{'entered':17812,'returned':17812,'meaning':'computation only, zero control credit'},
 'authenticated_constructed_path_execution':'UNTESTED','full_public_negative_derivations':0,
 'historical_groups':'117 independent/421 Engineering lookup, one lookup public positive, R1 340 and one public positive, helper443/30, unavailable331, failed75-minute and3Nov18:22:36 UNKNOWN remain separate',
 'failures':'Exact review/FAILURES.json and raw original audit failures retained; EVENT-prefix failure stays reported without reconstructed raw records; current incorporation parse failure retained separately',
 'runtime_profile':'CPython3.12.14/Cryptography50.0.0 validation evidence distinct from historical50.0.2 host fixture; no equivalence',
 'monitoring':'Cooperative contract; free slot/hook removal does not establish full cleanup or same-process reuse; hostile/repeated-interruption/termination qualifications retained',
 'runtime_arrival_call_outcome_physical_effects':'UNESTABLISHED',
 'confirmed_predecessor_save':BASE,'prior_save_repeated':False,'next_task_implemented':False,
 'both_acquisitions_preserved':True,'obligations_preserved':11,'inventory_unknowns':4,'lifetime_unknowns':14,
 'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED',
 'cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False})

doc('NEXT-TASK.txt',r'''
ASSESSMENT ONLY — proposed smallest next relationship; NOT IMPLEMENTED

Start from the exact authenticated selected enter-call attempt and explicit
continuation. Model the call-site completion and C result assignment in
res = _PyObject_CallNoArgs(enter), CPython3.12.14 Python/bytecodes.c:2515.
Stop immediately before Py_DECREF(enter) at2516. Do not advance to the res==NULL
test2517, decrement of exit2518, ERROR_IF2519, context entry or binding f.

Defining source: lab_bootstrap.py:23–24, pinned BEFORE_WITH at bytecodes.c:2488–2520.
compound_stmts.rst:491–500 is supporting protocol context, not a substitute for
the exact interpreter order. Identities/confirmed Git source paths are in
provenance/shared-defining-sources.json; all bytes are already retained.

Actual missing implementation (not inferred solely from adjacency):
extension/code/managed_coverage.py:3604–3607 declares only continuation and
attempt; 3676 explicitly sets call_outcome/call_result_role=None and
res_assignment_established=False. Its final exact-output validator3684–3685
recomputes that same frontier. extension/code/correspondence.py:70–78 makes that
attempt projection mandatory on its constructed path;80–92 embeds/validates
only the current relation and retains the explicit outcome/assignment exclusions
at84. There is no new declaration, result role or mandatory correspondence for
the selected helper return into res. Existing previous open-return and state/
handle returns have different source occurrences, callables and result roles;
they do not supply this selected enter-call relationship. Review independently
confirms this exact stop. Missing runtime observations are a separate gap.

Proposed bounded scope: both contexts/prefixes and close-versus-append failure
origins; exact predecessor authentication/selected invocation/owner/token,
enter/exit symbolic roles and earlier error/effect lineage. A call attempt does
not imply continuation, successful callability, dispatch/body entry or return.
Only an explicitly modeled completed C return permits the subsequent res
assignment in that expression. Carry a non-NULL symbolic returned-object role;
distinguish a C-NULL result from a Python None object, with neither a concrete
object identity nor a fabricated method return value. Assignment of a C result
is not evidence that f was bound or that context entry completed.

Preserve nonnormal/catchable interruption, process termination and unobserved
frontiers and stop at the first such frontier. Do not conflate a C-NULL return
with a Python-level normal return, infer an exact exception merely from NULL,
or claim what happens at later error handling. Original constructor and earlier
cleanup-error evidence survive replacement/uncertainty. A new conditional error
must retain its distinct origin and explicit cause/context/suppression unknowns.
Normal conditional completion retains the original pending outer error under
the inherited premises; no overall normal-return/final-propagation claim.

Retained inputs suffice for this conditional call-site/result-assignment slice:
fixed current producer/adapter, independently reviewed predecessor sources and
receipts, the eight constructed context/prefix/origin premises, and exact C/Python
source bytes. Do not execute retained controls or treat a prepared receipt as
an authenticated in-memory basis. Full public or authenticated constructed-path
execution would require its own bounded execution authorization; the latter
remains untested for the current milestone.

Deeper helper dispatch/body, guarantees about how _PyObject_CallNoArgs produces
an error indicator, concrete return values, build-equivalence and runtime
arrival/physical effects are NOT supplied by this call-site source. Any future
claim about those requires the exact helper/dispatch defining-source contract
from the CPython source owner and, for observed execution/build provenance,
evidence from the qualified runner/operator. No such input is necessary merely
to propose or construct the conditional call-site assignment slice above.

No implementation, new execution, policy adoption, acquisition or Git operation
was performed by this assessment. All11 obligations,4/14 UNKNOWN totals,
DecisionB,retention/allowances and both acquisitions remain. Admission disabled.
''')
doc('README.txt',r'''
I164-ENTER-CALL-ATTEMPT-1 — reviewed milestone incorporation

SUPPORTED within the bounded conditional SOURCE-ONLY enter-call-attempt
correspondence contract. No candidate semantic defect demonstrated.
The fixed implementation is unchanged.147 independent controls64PASS/83REJECTED,
489 Engineering controls101PASS/388REJECTED and one completed Ubuntu public
positive/actual returned-basis capture remain three separate groups. Review
rows retain exact rejection layers. Authenticated constructed-path execution
is untested; full public negative derivations remain zero.

DOC-ENTER-01: five functions were appended, not six. Historical CHANGES.json,
original producer bytes, review witness and failed audit attempts are unchanged.
The five are compile_enter_call,validate_enter_call,enter_call_binding,
enter_call_projection,validate_enter_call_projection. This finding is distinct
from inherited R1 documentation/fixture discrepancies. No semantic defect or
missing required sixth function was demonstrated.

This compact selection contains exact new component bytes, declarations/fixtures,
focused-check source, exact review records/raw controls/failures, compact host
evidence, current incorporation and recovery instructions. Large archives and
receipt/root datasets remain external and are identity-linked. Original source
and review MANIFEST files may describe members deliberately excluded from this
compact Git selection; SELECTION-MANIFEST.json alone defines this selection.
It is not a self-contained executable recovered root.

The confirmed lookup save8af23682a1757ea584f04b2b26303e7cb7f91160 and older
milestones are reused. No matching new successful save was found in retrieved
saved-file results; host receipt/committed-selection checks run before mutation.
The host command is self-contained. It needs only the new command file in
Downloads, existing Git repository/credentials and normal persistent execution
directory. Steve need not download or locate large evidence archives.

Scope ends at modeled _PyObject_CallNoArgs(enter) call attempt. Runtime arrival,
callability, call outcome/res assignment, context entry/f binding and physical
effects remain unestablished. NEXT-TASK.txt is assessment only, not implemented.
SOURCE-ONLY; cumulative envelope unadopted; backup kernel-only; streams UNCOMPUTED;
both acquisitions,11 obligations,4/14 UNKNOWN totals,DecisionB,retention/allowances
preserved; readiness/final binding blocked; admission disabled.
''')
doc('RECOVERY.txt',r'''
REUSE, DO NOT REPLAY
Verify this compact selection using SELECTION-MANIFEST.json. Preserve original
source, review, status and receipt bytes. Git data is a compact preservation
selection, not a substitute for the complete authenticated candidate root.

The self-contained I164-save-reviewed-enter-call-attempt-git.py checks an existing
matching successful receipt first, then an already-committed exact reviewed
selection. It never repeats the confirmed lookup predecessor save. Unconfirmed,
partial or conflicting receipts stop without overwrite or automatic retry.
Only if absent does it create this new prefix, commit only its exact files and
push once without force, with hooks disabled and [skip ci]. It checks prior
selection identities and unrelated staged/working state before/after. It does
not import candidate code or run tests, reviews, validation, pipelines, dummies,
application/helpers, database/session operations or acquisitions.

Expected receipt: /home/steve/Downloads/SEND-TO-ANCHOR-git-enter-call-attempt.json
Persistent save records: /home/steve/dev/Engineering-288-execution/
I164-reviewed-enter-call-attempt-git-<UTC>-<id>/GIT-RECEIPT.json
Repository: /home/steve/dev/Speak-up-appV3, branch main, origin/main.
New selection prefix: docs/privacy-engine/engineering-288/enter-call-attempt-reviewed
Estimate1–3minutes, network dependent. A prepared command is not host completion.
Only a matching PASS/CONFIRMED receipt establishes this save/push. Preserve any
STOP or uncertain push record and inspect it; do not retry to fix it silently.

Complete byte-only recovery, only when needed, uses the saved review and its
embedded host archive. Retrieve via exact links/IDs in provenance/recovery-
dependencies.json; never request Steve to re-upload a saved artifact. Verify
identities and read the review's RECOVERY.txt. Its recover_for_inspection.py needs
the separately retained204,417,990-byte launcher dependency, not test execution.
Use an absent persistent recovery directory and preserve failures. Recover
candidate4169files/1169dirs, lookup4124/1155 and R14090/1142 against exact full
manifests, and the saved receipt17989707bytes/SHA7fa6169a8b0e0e8b92b8c5dd71e440f8a211dc1c3a11559a2e515dd008ea98a6.
No automatic public validation or historical campaign is authorized by recovery.

Shared unchanged defining sources are already committed at the confirmed lookup
save; provenance/shared-defining-sources.json supplies exact Git paths/hashes.
Original constructor/lookup/cleanup evidence, conditional continuity, monitoring
qualifications, historical failures/UNKNOWN attempts/missing records and50.0.0
validation versus50.0.2 lab distinction remain.147/489/one-public-positive and all
prior groups are never combined. DOC-ENTER-01 is documented as five functions
without rewriting the original six-function claim or inherited R1 discrepancy.

No independent acceptance of future work. NEXT-TASK is assessment only. Both
acquisitions,11 obligations,4/14 UNKNOWN totals,DecisionB,retention/allowances,
SOURCE-ONLY and readiness/admission boundaries remain unchanged.
''')

files={p.relative_to(OUT).as_posix():p.read_bytes() for p in OUT.rglob('*') if p.is_file()}
manifest=enc({'format':'I164-COMPACT-REVIEWED-SELECTION-1','members':{n:ident(b) for n,b in sorted(files.items())}})
put('SELECTION-MANIFEST.json',manifest);files['SELECTION-MANIFEST.json']=manifest
assert all(len(b)<=524288 and Path(n).suffix not in ('.zip','.gz','.db','.sqlite','.bin') for n,b in files.items())

# Adapt the retained successfully used save mechanism; no execution here.
old=(ROOT/'input/I164-save-reviewed-context-special-lookup-git.py').read_text()
tree=ast.parse(old);assignments={n.targets[0].id:n for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
functions={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
payload_raw=enc({n:base64.b64encode(b).decode() for n,b in sorted(files.items())})
essential={n:ident(files[n]) for n in ['review/CHECKPOINT.json','extension/code/correspondence.py','extension/code/managed_coverage.py','provenance/review-incorporation.json']}
replacements=[]
for name,val in {'PAYLOAD':base64.b64encode(zlib.compress(payload_raw,9)).decode(),'PAYLOAD_ID':ident(payload_raw),'PREFIX':PREFIX,'BASE':BASE,'RECEIPT':'SEND-TO-ANCHOR-git-enter-call-attempt.json','REQUIRED':{},'REVIEW_ID':REVIEW_PIN,'ESSENTIAL':essential}.items():
 node=assignments[name];replacements.append((node.lineno,node.end_lineno,name+' = '+repr(val)))
external='''def external_evidence(downloads):
 # Exact compact bytes are embedded and verified. Large saved artifacts remain
 # externally retained; no new local archive transfer or host rehash is claimed.
 return {k:{'identity':{'bytes':v['bytes'],'sha256':v['sha256']},'filename':v['filename'],'library_file_id':v['library_file_id'],'link':v['link'],'git_included':False,'verification_basis':'verified retained review/input identities at preparation; host verifies embedded compact selection; no host archive rehash claimed'} for k,v in parse(payload()['provenance/recovery-dependencies.json']).items()}
'''
node=functions['external_evidence'];replacements.append((node.lineno,node.end_lineno,external.strip()))
prior_fn="def prior_milestones(repo,head):\n return [prior_selection(repo,head,'docs/privacy-engine/engineering-288/context-special-lookup-reviewed',{'bytes':9654,'sha256':'e038d0a07818851ee1f377ecdccb332472eea0fff2539c7aef0cd46f40aaf08d'},63)]"
node=functions['prior_milestones'];replacements.append((node.lineno,node.end_lineno,prior_fn))
lines=old.splitlines()
for start,end,text in sorted(replacements,reverse=True):lines[start-1:end]=text.splitlines()
script='\n'.join(lines)+'\n'
script=script.replace('context-special-lookup','enter-call-attempt')
# Restore predecessor prefix replaced by the naming change.
script=script.replace("prior_selection(repo,head,'docs/privacy-engine/engineering-288/enter-call-attempt-reviewed',{'bytes':9654", "prior_selection(repo,head,'docs/privacy-engine/engineering-288/context-special-lookup-reviewed',{'bytes':9654")
script=script.replace('context special lookup correspondence','enter call-attempt correspondence')
script=script.replace('compact independently reviewed I164 context-special-lookup selection','compact independently reviewed I164 enter-call-attempt selection')
name='I164-save-reviewed-enter-call-attempt-git.py'
(DELIVERY/name).write_text(script)

# Preparation checks only: syntax, payload decode, exact selection/manifest and
# inherited mechanism body identity. Never run candidate functions or Git.
parsed=ast.parse(script);const={n.targets[0].id:ast.literal_eval(n.value) for n in parsed.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
assert const['BASE']==BASE and const['PREFIX']==PREFIX
decoded=zlib.decompress(base64.b64decode(const['PAYLOAD'],validate=True));assert ident(decoded)==const['PAYLOAD_ID']
decoded_files={n:base64.b64decode(v,validate=True) for n,v in json.loads(decoded).items()};assert decoded_files==files
for name0 in ['git','outside_state','committed_selection','write_new','prior_selection','safe_prefix','checkpoint_selection']:
 old_node=functions[name0];new_node=next(n for n in parsed.body if isinstance(n,ast.FunctionDef) and n.name==name0)
 assert ast.dump(old_node,include_attributes=False)==ast.dump(new_node,include_attributes=False),name0
assert len([n for n in ast.parse((SOURCE/'code/managed_coverage.py').read_bytes()[429112:]).body if isinstance(n,ast.FunctionDef)])==5
script_pin=ident(script.encode())
audit={'status':'PASS','kind':'preparation syntax/payload/read-only identity audit, not model controls','review_identity':REVIEW_PIN,'review_entries':228,'review_hashes':227,'selection':{'files':len(files),'bytes':sum(map(len,files.values())),'manifest':ident(manifest)},'command':dict(filename=name,**script_pin),'candidate_changes':0,'new_model_controls':0,'public_runs':0,'review_runs':0,'git_operations':0,'prior_mechanism_functions_unchanged':['git','outside_state','committed_selection','write_new','prior_selection','safe_prefix','checkpoint_selection'],'host_execution':'PENDING matching receipt','failed_intake_display_preserved':True}
(DELIVERY/'PREPARATION-AUDIT.json').write_bytes(enc(audit))
archive_files={'selection/'+n:b for n,b in files.items()}
archive_files[name]=script.encode();archive_files['PREPARATION-AUDIT.json']=enc(audit)
archive_files['MANIFEST.json']=enc({n:ident(b) for n,b in sorted(archive_files.items())})
archive=DELIVERY/'I164-enter-call-attempt-1-reviewed-git-preparation.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,b in sorted(archive_files.items()):
  zi=zipfile.ZipInfo(n,date_time=(2026,11,9,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o100644<<16;z.writestr(zi,b)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(archive_files)
 assert {n:z.read(n) for n in z.namelist()}==archive_files
delivery={'archive':dict(filename=archive.name,entries=len(archive_files),manifested_hashes=len(archive_files)-1,**ident(archive.read_bytes())),'command':dict(filename=name,**script_pin),'selection':audit['selection'],'host_save':'PREPARED ONLY; not executed','expected_receipt':'/home/steve/Downloads/SEND-TO-ANCHOR-git-enter-call-attempt.json'}
(DELIVERY/'DELIVERY-IDENTITY.json').write_bytes(enc(delivery));print(json.dumps(delivery,indent=2))
