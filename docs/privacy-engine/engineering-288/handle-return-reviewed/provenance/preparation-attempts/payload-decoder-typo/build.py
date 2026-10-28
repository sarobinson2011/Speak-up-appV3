"""Package reviewed bytes and prepare host-only Git save. No validator executes."""
from pathlib import Path
import ast,base64,hashlib,json,zlib
R=Path(__file__).resolve().parent;C=R/'inputs/handle';V=R/'inputs/review';S=R/'selection'
S.mkdir(exist_ok=False)
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def put(n,b):
 p=S/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
cp=json.loads((V/'CHECKPOINT.json').read_bytes());verification=json.loads((R/'review-verification.json').read_bytes())
for p in C.rglob('*'):
 if p.is_file():
  n=p.relative_to(C).as_posix();put(n if n.startswith('code/') else 'supplied/'+n,p.read_bytes())
for p in V.rglob('*'):
 if p.is_file():put('independent/'+p.relative_to(V).as_posix(),p.read_bytes())
put('provenance/review-verification.json',enc(verification))
previous=(R/'previous-save/SEND-TO-ANCHOR-git-state-return.json').read_bytes();receipt=json.loads(previous)
assert receipt['status']=='PASS' and receipt['push_status']=='CONFIRMED' and receipt['commit']=='1782e0cecc8231b8507c7c6745124d0421270cff'
assert receipt['selection']['manifest']==ident((R.parent/'state-review-save/selection/SELECTION-MANIFEST.json').read_bytes())
put('provenance/previous-git-receipt.json',previous)
reviewpin={k:verification['review'][k] for k in ('bytes','sha256')}
put('provenance/SOURCE-LINEAGE.json',enc({'review':reviewpin,'review_entries':142,'implementation':cp['input'],'reviewed_code':cp['identities']['current_code'],'reviewed_receipt':cp['identities']['new_receipt'],'verdict':cp['verdict'],'independent_results':cp['independent_results'],'supplied_results':cp['supplied_results'],'observation_limits':cp['observation_limits'],'previous_git_commit':receipt['commit'],'previous_save_repeated':False,'completed_checks_rerun':False,'boundaries':cp['boundaries']}))
put('provenance/EXTERNAL-EVIDENCE.json',enc({'all_large_archives_and_databases_outside_Git':True,'required_for_host_save':{'Formal-Lab6-I164-handle-return-correspondence-independent-review':reviewpin},'review_contains_exact_implementation_archive':cp['input'],'compact_omissions':verification['compact_omissions_retained_in_exact_external_archive'],'prior_external_dependencies':json.loads((C/'DEPENDENCIES.json').read_bytes()),'historical_manifests_keep_original_scopes':True}))
# Preserve the preparation error separately. It was neither a validator test nor
# an independent review attempt; no completed controls are attributed to it.
f=R/'preparation-attempts/manifest-not-decoded'
for n in ('verify_inputs.py','failure.txt'):put('provenance/preparation-attempts/manifest-not-decoded/'+n,(f/n).read_bytes())
put('provenance/preparation-attempts/NOTE.txt',b'No validation suite ran during Git preparation. One read-only packaging attempt assumed an archive-generated MANIFEST.json also existed in the unsealed local directory. The attempt stopped; its script and failure note are retained separately. The corrected preparation uses the exact verified archive manifest. This contributes no assertions to supplied or independent totals.\n')
O=R.parent/'handle-return/retained/state/retained/config/retained/binding/retained/hf01/original/retained/references/retained/fields/retained/occurrence'
B=O/'retained/correction'
excerpts=[];source_ids={}
for label,p,ranges in [
 ('compiler/live_connection.py',B/'retained/candidate/compiler/live_connection.py',[(25,43)]),
 ('retained/launcher/code/lab_bootstrap.py',B/'retained/launcher/code/lab_bootstrap.py',[(119,124),(157,175)]),
 ('code/prospective_entry.py',B/'code/prospective_entry.py',[(24,29),(100,116),(143,166),(169,195)]),
 ('boundary/code/correspondence.py',B/'code/correspondence.py',[(65,85),(101,122)]),
 ('occurrence/code/smoke_occurrences.py',O/'code/smoke_occurrences.py',[(235,249),(310,337)]),
 ('current/code/managed_coverage.py',C/'code/managed_coverage.py',[(1188,1243),(1302,1329)]),
 ('current/code/correspondence.py',C/'code/correspondence.py',[(38,57),(58,98),(100,123)])]:
 raw=p.read_bytes();source_ids[label]=ident(raw);lines=raw.decode().splitlines();excerpts.extend([label,json.dumps(ident(raw),sort_keys=True),''])
 for a,b in ranges:
  excerpts.extend([f'{i+1}: {lines[i]}' for i in range(a-1,min(b,len(lines)))]);excerpts.append('')
tree=ast.parse((C/'code/managed_coverage.py').read_bytes());functions=[n.name for n in tree.body if isinstance(n,ast.FunctionDef)]
excerpts.append('Current producer functions (read-only AST inventory): '+', '.join(functions))
current=json.loads((C/'results/handle-correspondence.json').read_bytes());excerpts.append('Current mandatory receipt context members: '+', '.join(current['contexts'][0]))
model=json.loads((B/'basis/candidate/managed-route/model.json').read_bytes())
excerpts.extend(['Existing managed source-coverage gaps:',json.dumps(model['gaps'])])
put('provenance/next-task-source.txt',('\n'.join(excerpts)+'\n').encode())
put('provenance/next-task-source-identities.json',enc(source_ids))
put('README.md',b'''# Reviewed ManagedAuthority.handle return milestone

Formal-Lab[6] supports the bounded source-derived conditional handle-return correspondence in both symbolic contexts. This save incorporates that scoped finding against exact code, receipt and review identities in provenance/SOURCE-LINEAGE.json. Original supplied documents are retained as exact historical submission records; their pending-review wording does not override the incorporated verdict.

Formal-Lab's 219 primary assertions, 133 recovered-root assertions and separate successful public CLI remain distinct from Engineering's 101 primary, 21 additional internal, 101 recovered and one fresh-process result. No completed control or review was rerun. The reviewer lookup failure stopped after seven assertions; its exact scripts and records remain under independent/failures/public-key-lookup-attempt-1. Two later interrupted runs retain 179 primary and four recovered progress rows under independent/failures/interrupted-execution-attempt-2. They have no completed-result attribution and remain excluded from all completed totals. All independent non-input members, including failed/interrupted records, are included byte-for-byte. Earlier failures, including both zero-assertion state membership failures and their binary identities, remain in the exact external input archive and prior milestone, unchanged.

The mandatory bridge preserves exact response bytes, packet/request and validated instance/acquisition bindings; normal ok:false responses remain distinct from escaping exceptions. Its expectations are rebuilt independently of mutable returned results. The isolated conditional projector is not an evidence-admission API. The authentication pair checker does not re-prove every method-specific action/history or authorize new acquisitions. Engineering's authentication envelopes are explicitly constructed using public laboratory test keys; they were never issued or promoted into the journal. The independent review generated no signatures. No runtime, session or database operation occurred in this incorporation.

Actual handle return-chain evidence remains UNAVAILABLE. The saved journal and captured handle-call count are both zero only within this capture; lifetime multiplicity remains UNKNOWN. Packet/inject values, underlying response, result local, wrapper return, physical reference identity and unobserved frames are not invented. Unknown inject is not observed None. The 18 traced invocations and separate frameless observer Client.state() remain distinct. Static source/conditional support is neither repetition completeness nor action feasibility, qualification, durability or exclusive ownership.

## Smallest next construction task; not implemented

Extend the existing typed handle-return relation across the prospective general-client forwarding path: ManagedAuthority.handle -> ManagedSession.handle -> prospective_entry._dispatch(handle) -> Client.handle. Reuse the reviewed manager bridge, existing boundary sites, adopted status contract, reference distinctions and evidence gates. Add the missing executable argument/value/normal-or-exception correspondence in both contexts; do not repeat the already supported runtime boundary correction or introduce a new surface.

The exact retained launcher defines ManagedSession.__init__ at line 121 as storage of the manager reference, and handle at line 124 as direct return of self.__managed.handle(authenticated_packet). It forwards one packet argument, so the defining ManagedAuthority.handle default inject=None applies; no client inject argument is invented. The prospective entry defines Client.handle at lines 115-116 as _dispatch(token, 'handle', authenticated_packet). Lines 143-154 resolve the owner, refuse absent/failed owners, require exact bytes for packet and response, call owner.wrapper.handle(packet), and return the same response without re-encoding. Lines 161-166 retain the original BaseException in owner.failure and raise the fixed client failure outside the handler; they do not return error bytes or establish nonexecution. A normally returned authenticated ok:false response remains bytes and is not automatically turned into ClientFailure by this route. Lines 174 and 187-188 create and revoke the token-scoped owner reference; lines 181-185 carry the original error to existing retention/cleanup even if the client catches the coarse error. These exact sources suffice for a conditional correspondence, preserving unsuccessful owner lookup, argument evaluation, type failures and escaping errors.

Already covered: the adopted boundary has exact source anchors client-handle and dispatch-and-failure, their descriptive relation, trusted owner routing and runtime capability/output controls. The occurrence adapter already joins the saved client surface and observer state record. The current handle producer has exact Authority.handle -> _run -> ManagedAuthority.handle declarations, argument forwarding, authentication and guarded results. These remain mandatory and must be reused.

Precise missing implementation: compile_handle_return selects only ManagedAuthority.handle and derives three values ending at its return; handle_value_projection consumes only underlying, run_result and wrapper_return. It does not consume ManagedSession.handle or Client.handle/_dispatch, map the token's owner/wrapper/manager relationship, or validate their byte-return and original-error/fixed-error edges. The old boundary relation is an exact source-bound descriptive site relation, not this typed value projector. The current validate -> derive -> derive_handle -> _checked -> _basis chain regenerates the manager-level catalogue and calls the state predecessor; it has no client-side return relation in either context. Source excerpts, identities, actual producer function inventory and actual receipt members are retained in provenance/next-task-source.txt. This conclusion comes from source inspection, not an assumption that integration is missing.

The next slice must bind the same independently validated request, instance and acquisition across these hops, preserve distinct conditional occurrences even when bytes match, and keep validation expectations detached from candidate results. Reference tokens are conditional premises, not evidence of physical object identity. No source changes or new execution are required to construct this static relation. Actual client/launcher handle frames and reference observations would still require separately authorized evidence from the owning trusted capture/integration operator; Steve's local factual contact role does not establish qualification. That missing runtime evidence does not block the bounded static task. No next-task implementation is included.

## Preserved boundaries

All eleven obligations, four inventory and fourteen lifetime UNKNOWN totals, Decision B, exact evidence, retention, allowances, accounting, reservations, nonce/ownership and uncertainty duties remain unchanged. SOURCE-ONLY unchanged; cumulative-envelope UNADOPTED; readiness/final binding BLOCKED; backup KERNEL-ONLY; streams UNCOMPUTED; admission disabled. Both acquisitions and previous milestones remain separate. No new policy, deletion/compaction permission, allowance, runtime limit, qualification or admission is established.
''')
put('RECOVERY.md',b'''# Recovery and one-time Git save

SELECTION-MANIFEST.json defines this compact Git selection: exact reviewed current code, supplied controls/results/receipt, every non-input independent review member including failed/interrupted attempts, compact provenance and these instructions. Historical manifests retain their original archive scopes. This selection does not replace the full recovery root. Large archives and databases remain outside Git. No deletion, compaction or evidence substitution is authorized.

Full recovery source: Formal-Lab6-I164-handle-return-correspondence-independent-review.zip, 42,069,714 bytes, 142 entries, SHA-256 d69cd5939e0fc051adee4f270dd0148d4aecf5cfef2ecae65b3ec33cedf4f31c. Its 141 manifested members include input/I164-handle-return-correspondence-1.zip, 42,330,497 bytes, 1,088 entries, SHA-256 6b486b1ca0c49da010face18132507020a07f3db84602d62a7c75af0305caa8e. Verify exact identities, safe unique regular membership, CRC and manifest hashes before extracting into a new persistent directory. The input has 1,087 manifested files. Do not overlay a predecessor, failed root, host session or database.

The complete state predecessor (1,016 members) is decoded under retained/state, and the 33 compact state-review records under retained/state-review. Its exact prior external independent review is 41,478,030 bytes, 34 entries, SHA-256 63c72c1b7ad2f42f05b8f005454748967bf3fac5fcbc26fb81058567a717a311. The two earlier state failure binaries remain exact within the embedded implementation; further historical omissions stay at the external identities in supplied/DEPENDENCIES.json. No failure artifact is an extra permissible member of a strict recovered input root.

Current full-root interfaces are code/correspondence.py and tests/fresh_check.py. These identify recovery interfaces only; completed validation results are already retained and ordinary handoff does not rerun them. Supplied and independent RECOVERY.md retain their original scope. CPython 3.12.14 / Cryptography 50.0.2 is the reviewed offline profile, not a claim of qualification elsewhere.

The previous state save is already confirmed at 1782e0cecc8231b8507c7c6745124d0421270cff; provenance/previous-git-receipt.json preserves the supplied host receipt. It is not repeated. The prepared host command first looks for a successful exact matching handle-save receipt in Downloads. If found, it verifies the committed selection and ancestry and reuses it without new files, commit or push. Otherwise it requires the exact external review archive in Downloads (a numbered download suffix is accepted), verifies the existing state milestone and local/remote main agreement, writes only docs/privacy-engine/engineering-288/handle-return-reviewed, commits only those paths with hooks/signing disabled and [skip ci], and pushes that single commit once without force or retry. Unrelated staged and working files are checked before/after. Existing destination, ambiguous or failed receipts, repository instructions needing inspection, Git lock/operation or remote divergence stops without repair.

The new selection's maximum individual text record is 1,156,238 bytes. The packaging guard permits these exact manifested text records below 2,000,000 bytes; it changes no application/profile/resource bound. No archive or database is admitted by that packaging guard. Exact supplied and independent evidence remains authoritative; preparation adds no test/review assertions.
''')
files={p.relative_to(S).as_posix():p.read_bytes() for p in S.rglob('*') if p.is_file()}
put('SELECTION-MANIFEST.json',enc({'format':'I164-REVIEWED-HANDLE-GIT-SELECTION-1','members':{n:ident(b) for n,b in sorted(files.items())}}));files['SELECTION-MANIFEST.json']=(S/'SELECTION-MANIFEST.json').read_bytes()
assert all(len(b)<2000000 and Path(n).suffix not in ('.zip','.db','.sqlite','.bin') for n,b in files.items())
old=(R.parent/'I164-save-reviewed-state-return-git.py').read_text();tree=ast.parse(old);body=old[old.index('def ident('):]
body=body.replace('git-state[._-]|state-return|managed-state','git-handle[._-]|handle-return|managed-handle').replace('state-return','handle-return')
before="return [prior_selection(repo,head,'docs/privacy-engine/engineering-288/config-return-reviewed',{'bytes':13097,'sha256':'b8ba0a76e4c1f5fe42206e4f825e2de4aa28779f1ccc185343997f466aefc799'},82)]"
after="return [prior_selection(repo,head,'docs/privacy-engine/engineering-288/state-return-reviewed',{'bytes':15347,'sha256':'78f3282444104926c5988a19b49e1f2769816fdf8c2c5e4bef5ee41290905d45'},96)]"
assert before in body;body=body.replace(before,after)
before="'independent_state_return':{'primary_assertions':108,'recovered_root_assertions':80,'static_type_origin_checks':1,'offline_commands':1,'rerun':False},'supplied_state_return':{'primary':83,'recovered':77,'fresh_process':1,'membership_failure_assertions':[0,0],'failed_attempts_in_completed_totals':False,'rerun':False}"
after="'independent_handle_return':{'primary_assertions':219,'recovered_root_assertions':133,'offline_CLI_checks':1,'failed_lookup_assertions':7,'interrupted_progress_rows':[179,4],'failed_attempts_in_completed_totals':False,'rerun':False},'supplied_handle_return':{'primary':101,'additional_internal':21,'recovered':101,'fresh_process':1,'prior_membership_failure_assertions':[0,0],'failed_attempts_in_completed_totals':False,'rerun':False}"
assert before in body;body=body.replace(before,after)
assert body.count('len(b)<1000000')==1;body=body.replace('len(b)<1000000','len(b)<2000000')
payload=enc({n:base64.b64encode(b).decode() for n,b in sorted(files.items())});encoded=base64.b64encode(zlib.compress(payload,9)).decode()
encsource=ast.get_source_segment(old,next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='enc'))
header='#!/usr/bin/env python3\n"""Prepared reviewed handle save; no candidate, test or session execution."""\nimport base64,datetime,hashlib,json,re,stat,subprocess,time,uuid,zlib\nfrom pathlib import Path,PurePosixPath\n'
constants={'PAYLOAD':encoded,'PAYLOAD_ID':ident(payload),'PREFIX':'docs/privacy-engine/engineering-288/handle-return-reviewed','BASE':receipt['commit'],'RECEIPT':'SEND-TO-ANCHOR-git-handle-return.json','REQUIRED':{'Formal-Lab6-I164-handle-return-correspondence-independent-review':reviewpin}}
script=(header+''.join(k+'='+repr(v)+'\n' for k,v in constants.items())+encsource+'\n'+body).encode();parsed=ast.parse(script)
dest=R.parent/'I164-save-reviewed-handle-return-git.py';assert not dest.exists();dest.write_bytes(script)
literal={n.targets[0].id:ast.literal_eval(n.value) for n in parsed.body if isinstance(n,ast.Assign)}
decoded=zlib.decompress(base64.b64encode(literal['PAYLOAD'],validate=True));assert ident(decoded)==literal['PAYLOAD_ID'];stored={n:base64.b64decode(b,validate=True) for n,b in json.loads(decoded).items()};assert stored==files
oldf={n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,ast.FunctionDef)};newf={n.name:ast.dump(n,include_attributes=False) for n in parsed.body if isinstance(n,ast.FunctionDef)}
changes=[n for n in newf if oldf.get(n)!=newf[n]];assert changes==['payload','prior_milestones','existing_save','perform'],changes
info={'command_file':dest.name,**ident(script),'prepared_not_executed':True,'selection':{'files':len(files),'bytes':sum(map(len,files.values())),'manifest':ident(files['SELECTION-MANIFEST.json'])},'base':receipt['commit'],'payload_hashes_and_membership':'PASS','AST_parse':'PASS','reused_host_engine_changed_functions':changes,'host_Git_not_accessed_here':True,'tests_reviews_pipeline_reruns':False}
(R/'prepared-command-identity.json').write_bytes(enc(info));print(json.dumps(info,indent=2))
