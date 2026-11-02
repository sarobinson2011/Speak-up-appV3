"""Read-only final evidence packaging. Does not execute candidate or any controls."""
from pathlib import Path
import sys,json,collections,zipfile,stat,hashlib
sys.path.insert(0,str(Path(__file__).parent))
from intake import BASE,AREA,INPUT,PIN,identity,enc,archive
def read(p):return json.loads(Path(p).read_bytes())
def reconcile(label):
 rdir=BASE/'results'/label;pdir=BASE/'processes'/label
 r=read(rdir/'RESULT.json');ex=read(pdir/'exit-status.json');rows=r['rows']
 progress=[json.loads(x) for x in (rdir/'progress.jsonl').read_bytes().splitlines()]
 stdout=[json.loads(x[4:]) for x in (pdir/'stdout.log').read_bytes().splitlines() if x.startswith(b'ROW ')]
 individual=[read(p) for p in sorted(rdir.glob('ROW-*.json'))]
 streams={'RESULT':rows,'progress':progress,'stdout':stdout,'individual':individual}
 maps={}
 for name,rs in streams.items():
  assert len({x['ordinal'] for x in rs})==len(rs),(label,name,'duplicate ordinal')
  maps[name]={x['ordinal']:x for x in rs}
 allids=set(maps['RESULT']);assert all(set(m)<=allids for m in maps.values())
 agreed=[i for i in sorted(allids) if all(i in m and m[i]==maps['RESULT'][i] for m in maps.values())]
 record={'result':r['result'],'explicit_exit':ex,'counts':{k:len(v) for k,v in streams.items()},'kinds':{k:dict(collections.Counter(x['result'] for x in v)) for k,v in streams.items()},'all_records_identical':all(v==rows for v in streams.values()),'all_record_corroborated_ordinals':agreed,'missing_ordinals':{k:sorted(allids-set(m)) for k,m in maps.items()},'discrepancy_cause':'UNKNOWN' if len(agreed)!=len(rows) else None,'layers':dict(collections.Counter(x.get('layer') for x in rows)),'record_identities':{str(p.relative_to(BASE)):identity(p.read_bytes()) for p in [rdir/'RESULT.json',rdir/'progress.jsonl',pdir/'stdout.log',pdir/'stderr.log',pdir/'exit-status.json']}}
 return record,r
def main():
 public,pr=reconcile('public-recovered');monitor,mr=reconcile('slot5')
 assert pr['result']=='PASS' and public['explicit_exit']['returncode']==0 and not public['explicit_exit']['timed_out']
 assert mr['result']=='PASS' and monitor['explicit_exit']['returncode']==0 and not monitor['explicit_exit']['timed_out']
 assert monitor['kinds']['RESULT']=={'PASS':12,'QUALIFIED':1}
 actual=read(BASE/'results/public-recovered/actual-public-result.json');pred=read(BASE/'results/public-recovered/actual-predecessor-public-result.json')
 scope=read(BASE/'results/public-recovered/scope-result.json');audit=read(BASE/'results/audit/AUDIT.json');intake=read(BASE/'results/intake.json')
 assert actual['result']==pred['result']=='PASS' and actual['contexts']==pred['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
 receipt=identity((AREA/'recovered/receipts/prepared-cleanup-loop.json').read_bytes())
 assert actual['receipt']==receipt=={'bytes':16960806,'sha256':'f296a50dd9fa74a405c7965662b7594594cc18da454b379bb25cf9c41fe1b842'}
 final=read(BASE/'results/public-recovered/final-verification.json');assert final==intake['recovered_root']
 assert identity(INPUT.read_bytes())==PIN
 verdict='SUPPORTED within the bounded conditional SOURCE-ONLY cleanup-loop exhaustion correspondence contract, with explicit execution-record and monitoring qualifications; no candidate defect demonstrated.'
 checkpoint={'title':'Formal-Lab[6] independent review of I164-cleanup-loop-exhaustion-correspondence-1.zip','authorship':'Formal-Lab[6], separate reviewer; Engineering construction and supplied campaign are supporting evidence','verdict':verdict,'input':{'name':'I164-cleanup-loop-exhaustion-correspondence-1.zip',**PIN,'entries':81,'manifested_hashes':80},'intake':intake,'fresh_independent_public_and_core':public,'fresh_independent_slot5':monitor,'slot5_interruption_qualification':read(BASE/'results/slot5/qualified-cleanup-interruption.json'),'actual_public_result':actual,'actual_unchanged_predecessor_public_result':pred,'actual_test_environment':pr['environment'],'actual_validation_layers':scope,'supplied_and_historical_audit':audit,'candidate_defect_witness':None,'no_unqualified_cross_group_total':True,'full_public_negative_derivations':0,'runtime_loop_observations':0,'implementation_changes':0,'requests':0,'acquisitions':0,'database_connections':0,'session_operations':0,'completed_campaigns_replayed':0,'Git_saves':0,'confirmed_save_reused':'5ffd368df1012296a128c2dde134149d341780bc','source_limits':['Aggregate handler departure does not specify hidden opcode order or observed interpreter state','Explicit conditional owner, invocation, local, iterator/list and error continuity','Interrupted departure preserves uncertainty and earlier acknowledgements','Ordinary exhaustion is not a new propagating error','Stop before any line174 evaluation/write attempt','Non-None construction and remaining outer-cleanup gaps remain'],'monitoring_limits':['Cooperative CPython3.12.14 live-marker identity only','Synthetic predecessors are not actual authentication','Cleanup failure/repeated interruption/termination/hostile replacement remain qualified','A free slot alone proves no complete cleanup','No actual authenticated same-process reuse after qualified cleanup interruption is claimed'],'preserved':{'both_acquisitions':'SEPARATE','obligations':11,'inventory_UNKNOWN':4,'lifetime_UNKNOWN':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','admission':False}}
 (BASE/'CHECKPOINT.json').write_bytes(enc(checkpoint))
 count=public['counts'];kinds=public['kinds']['RESULT'];corrob=len(public['all_record_corroborated_ordinals'])
 review=f'''Formal-Lab[6] independent review — cleanup-loop exhaustion

Target: I164-cleanup-loop-exhaustion-correspondence-1.zip
{PIN['bytes']} bytes; 81 entries; SHA-256 {PIN['sha256']}
Authorship: Formal-Lab[6] is the separate reviewer. Engineering authored the construction and supplied controls. No implementation changes.

Verdict: {verdict}

Integrity and preservation
The exact outer bytes, CRC, safe unique regular-file membership, 80 manifested hashes and all nested recovery dependencies passed independent verification. Fresh byte-only recovery produced 4,025 files and 1,116 directories matching ROOT-MANIFEST.json. All 4,015 predecessor members are unchanged. The entire 359,095-byte reviewed producer prefix, actual predecessor validator and runtime source copies are preserved. The addition introduces six new function bodies without redefining inherited names. Declared active counterparts and receipt identities match actual bytes. The new receipt preserves all inherited JSON fields under their documented relocation; historical receipts remain unchanged.

Source and language findings
Defining lab_bootstrap.py169–172 has exactly [('raw',raw),('managed',managed)], the identity-based non-None guard, a shared protected close/normal-append try and one selected error-report append. Validated raw=None skips the first body; managed is second and last. The new source traversal and independent AST oracle agree on six distinct acknowledgements: departure attempt, completed inner-handler exit, selected body completion, final advance attempt, ordinary exhaustion and completed loop. Explicit continuation and exact iterator/list continuity are required; prior append completion alone establishes none of these later facts.

Python3.12 reference sections8.3 and8.4.1 were consulted at https://docs.python.org/3.12/reference/compound_stmts.html (page labelled3.12.16; retained test profile3.12.14). The iterator and exception-handler rules support the declared aggregate departure, restoration and target-lifetime assumptions. They do not establish hidden opcode order, physical destruction or observed interpreter state. Detailed independent source positions and the reference assessment are included.

Normal continuation clears the caught-name role and restores the outer constructor error as the last acknowledged handled/pending role, while retaining selected cleanup-error evidence and the last acknowledged inner caught error separately. The original constructor error remains pending and terminal_python_exception_in_model stays True. Ordinary exhaustion introduces no new propagating error. Replacement/catchable interruption retain their distinct pending replacement; termination/unobserved frontiers use None and stop immediately. Interrupted departure does not fabricate clearing, restoration, unwind or completion.

Both symbolic contexts, both control prefixes and close-versus-normal-append failure origins were checked. The selected parent was revalidated by the unchanged predecessor with the actual returned authenticated basis. Exact occurrence, scope, instance, owner/token, handler/error and details/list roles bind each case. Source-derived count/order/index, raw skip, last-entry status, missing/reordered stages, premature exhaustion and coordinated substitutions were challenged. Close acknowledgement survives a later append failure. Acknowledged error reporting and UNKNOWN prior append effects survive loop continuation; complete list contents and physical effects remain unestablished. Exact False fields and dynamic details origins are preserved.

Actual validation and fresh independent evidence
One fresh recovered actual current public validation passed through the unchanged actual predecessor, using the exact new receipt: {receipt['bytes']} bytes, SHA-256 {receipt['sha256']}. The unchanged predecessor validated its original 15,694,813-byte prepared-error-report receipt. New receipt preparation was not used as authentication; exact live authenticated assembly matched the submitted bytes. No predecessor function/output or validation expectation was replaced.

Main process: explicit exit0, no timeout. RESULT/progress/stdout/individual-row counts: {count['RESULT']}/{count['progress']}/{count['stdout']}/{count['individual']}; RESULT kinds {kinds}; {corrob} rows agree across all four records. Missing ordinals: {public['missing_ordinals']}; discrepancy cause: {public['discrepancy_cause']}. These counts are not combined with any other group. All individual rows state their actual layer. Public negatives were required-relation pre-input gates. Other negatives used actual-authenticated-basis parent/source/type/output/semantic/evidence or exact-receipt comparisons. No full public negative derivation is claimed. Nested returned-object mutations did not change pristine expectations.

Separate new slot5 process:12 PASS controls and1 QUALIFIED observation, exit0. Real CPython monitoring APIs were exercised with synthetic predecessors, including normal/nested use, missing/extra basis returns, assembly mismatch, predecessor failure, C-return interruptions after reservation/registration/event setup, foreign ownership and equal-valued distinct-marker races. Failed acquisition preserved foreign monitoring state. These are mechanism tests, not authenticated public evidence. The qualified cleanup-interruption observation left local event bits after callback removal and slot release. No reviewer cleanup, complete release or actual authenticated reuse is claimed for that case; its isolated process ended. Normal slot5/4/3/2 state was separately inspected after the genuine public positive. The new helper is AST-equivalent to retained slot4 after declared slot/label/marker normalization. All LD01 cleanup-failure, repeated-interruption, termination, alternate-interpreter and hostile-replacement limits carry forward. CHECKPOINT's short monitoring wording is not interpreted as broadening that qualification.

Actual environment: CPython3.12.14, Cryptography50.0.2, isolated, bytecode writing disabled, optimization0. No new host41.0.7 compatibility or application runtime qualification is claimed. Read-only supplied-fixture/source consistency inspection and byte/accounting audits executed no candidate controls; they are not added to the authenticated group.

Supplied and historical accounting — preserved separately
Engineering:722 RESULT rows (232PASS/490REJECTED),721 matching progress/stdout (231PASS/490REJECTED),exit0. Row134, unobserved inner-handler-departure frontier for0-False-append, remains RESULT-only; causeUNKNOWN. Supervisor stdout observation168,139 bytes differs from frozen167,912 bytes; both retained, causeUNKNOWN. No reconstruction, stream repair or campaign replay.
Prior independent line172 review:146RESULT/145progress/125stdout; only1–125 three-way;126RESULT-only;127–146RESULT/progress only; causeUNKNOWN. Separate slot4 failed attempt remains12PASS+1QUALIFIED,exit1 with failed reviewer finalization, outside completed groups. Engineering392RESULT/stdout versus391progress remains qualified at row392. Older incomplete primary remains1,300progress/165stdout, missing final records and UNKNOWN discrepancy cause; withdrawn corroboration claim retained. All zero-control failures, partial evidence, retained undeclared files and earlier scoped LD01/EC01 support remain preserved in exact retained archives. No unqualified aggregate is offered.

Witnesses, gaps and boundaries
No candidate defect demonstrated by this slice. The qualified monitoring observation is a retained limit, not evidence of successful complete cleanup. There is no observed runtime loop chain; the separate observer remains unjoined. Completion does not establish normal overall return, physical cleanup, durability, exclusivity or renewed authorization. Stop before any line174 evaluation/write attempt. Line175 suppression, line176 final rethrow, owner finalization, managed-local clear, ACTIVE removal, non-None construction and remaining outer-cleanup routes are outside this bounded support. No new implementation task, policy, authority or numerical allowance is adopted.

Both acquisitions, eleven obligations, four inventory/fourteen lifetime UNKNOWN totals, Decision B, retention and allowances are unchanged. SOURCE-ONLY; cumulative-envelope unadopted; backup kernel-only; streams UNCOMPUTED; readiness/final binding blocked; admission disabled. Confirmed save5ffd368df1012296a128c2dde134149d341780bc is reused as supplied evidence, not repeated or independently fetched from Git.
'''
 (BASE/'REVIEW.txt').write_text(review)
 recovery='''Read REVIEW.txt and CHECKPOINT.json first. This is a preserved independent-review checkpoint, not authorization to rerun controls.
1. Verify this review ZIP against its externally supplied size/hash. Require safe unique regular files, exact MANIFEST.json membership, CRC and each manifested length/hash. Extract only into a new absent persistent evidence directory, never /tmp. Preserve original records and statuses.
2. input/I164-cleanup-loop-exhaustion-correspondence-1.zip is the exact reviewed169,181,718-byte construction, SHA-256 a48cb3be9002e8dbdcf3ac8c6e2d0ed45ea1eced14126af3d9d1862ec1963dd5. Verify its81 entries and80 manifested hashes before extraction. It contains the exact retained line172 review and all nested byte-recovery dependencies.
3. Read that construction's RECOVERY.txt. Its tools/recover.py reconstructs bytes only into a new absent persistent directory with retained Python3.12.14. It performs no database connection, session operation or candidate validation. Verify the resulting root against its ROOT-MANIFEST.json:4,025 files/1,116 directories; manifest1,551,485 bytes, SHA-25672cf251ceca9dcfbc531967a5db8f891be23aed7720aa67535367c95a79a2de7. The independent byte-only recovery and its explicit result are in review/code/intake.py and review/results/intake.json.
4. Inspect preserved process launch/stdout/stderr/progress/exit and per-row records. Do not replay campaigns to fill missing records. Main public validation and focused checks used the actual returned authenticated basis in one bounded fresh process. Slot5 tests were in a separate bounded process with synthetic predecessors. Recovery of evidence does not require running either process again.
5. Review scripts retain their executed absolute paths; they are evidence, not a portable automatic rerun command. No pending process or session needs resuming after the recorded exits. No Git save is required. Submitted receipts and implementation files must not be repaired during review.
All scope, authority, observation and accounting limitations in REVIEW.txt and nested historical records remain in force; admission disabled.
'''
 (BASE/'RECOVERY.txt').write_text(recovery)
 items={'REVIEW.txt':(BASE/'REVIEW.txt').read_bytes(),'CHECKPOINT.json':(BASE/'CHECKPOINT.json').read_bytes(),'RECOVERY.txt':(BASE/'RECOVERY.txt').read_bytes(),'input/I164-cleanup-loop-exhaustion-correspondence-1.zip':INPUT.read_bytes()}
 for folder in ('code','results','processes','sources'):
  for p in sorted((BASE/folder).rglob('*')):
   if p.is_file():assert stat.S_ISREG(p.lstat().st_mode);items['review/'+str(p.relative_to(BASE))]=p.read_bytes()
 for name in ('intake.stdout','intake.stderr'):items['review/'+name]=(BASE/name).read_bytes()
 manifest={n:identity(b) for n,b in items.items()};items['MANIFEST.json']=enc(manifest)
 target=BASE.parent/'Formal-Lab6-I164-cleanup-loop-exhaustion-independent-review.zip';assert not target.exists()
 with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n,b in sorted(items.items()):
   zi=zipfile.ZipInfo(n,(2026,11,2,0,0,0));zi.create_system=3;zi.external_attr=(stat.S_IFREG|0o644)<<16;zi.compress_type=zipfile.ZIP_STORED if n.endswith('.zip') else zipfile.ZIP_DEFLATED;z.writestr(zi,b)
 raw=target.read_bytes();pin=identity(raw);z,m=archive(raw,pin,len(items));z.close()
 package={'file':str(target),**pin,'entries':len(items),'manifested_hashes':len(manifest),'CRC':'PASS','safe_exact_membership':'PASS','all_manifested_hashes':'PASS','verdict':verdict}
 (BASE.parent/'loop-review-package-verification.json').write_bytes(enc(package));print(json.dumps(package),flush=True)
if __name__=='__main__':main()
