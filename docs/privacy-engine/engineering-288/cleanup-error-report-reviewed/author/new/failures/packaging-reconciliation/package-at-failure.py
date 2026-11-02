"""Package saved bounded results; never execute a validator or reconstruct missing records."""
from pathlib import Path
import json,hashlib,zipfile,stat,collections
W=Path(__file__).resolve().parents[1];root=Path((W/'source-path.txt').read_text()).parent/'recovered'
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(n):return (W/n).read_bytes()
def js(n):return json.loads(read(n))
def main():
 result=js('results/focused-recovered/RESULT.json');ex=js('processes/focused-recovered/exit-status.json')
 assert result['result']=='PASS' and ex['returncode']==0 and ex['timed_out'] is False
 progress=[json.loads(x) for x in read('results/focused-recovered/progress.jsonl').splitlines()]
 assert progress==result['rows'] and len(progress)==result['checks']
 stdout=read('processes/focused-recovered/stdout.log');stderr=read('processes/focused-recovered/stderr.log')
 rows=[line for line in stdout.decode().splitlines() if line and line.split(' ',1)[0].isdigit()]
 assert len(rows)==len(progress)
 for i,(line,row) in enumerate(zip(rows,progress),1):assert line==f"{i} {row['check']} {row['result']}"
 assert ex['streams_bytes_observed']=={'stdout.log':len(stdout),'stderr.log':len(stderr)}
 frozen=json.loads((root/'MANIFEST.json').read_bytes());input_final=js('results/focused-recovered/final-verification.json')
 assert input_final==js('results/focused-recovered/input-verification.json')
 assert input_final['manifest']==ident((root/'MANIFEST.json').read_bytes())
 recovery_exit=js('processes/delivery-byte-recovery/exit-status.json')
 recovery_result=json.loads(read('processes/delivery-byte-recovery/stdout.log').splitlines()[-1])
 assert recovery_exit['returncode']==0 and recovery_exit['timed_out'] is False and recovery_result['candidate_executed'] is False
 assert recovery_result['manifest']==input_final['manifest'] and recovery_result['files']==4015 and recovery_result['directories']==1110
 # Copy only declared root additions. The predecessor is supplied as exact nested archives.
 additions={n:(root/n).read_bytes() for n in frozen if not n.startswith('retained/cleanup/')}
 for n,b in additions.items():assert ident(b)==frozen[n]
 archive=W.parent/'upload/Formal-Lab6-I164-EC01-independent-closure(1).zip'
 assert ident(archive.read_bytes())=={'bytes':154107404,'sha256':'7971a5cd95ef8775ff05e2db0ef5c3521903586c0d530b9e590b4bb54029fcef'}
 files={'ROOT-MANIFEST.json':(root/'MANIFEST.json').read_bytes(),'ADDITIONS-MANIFEST.json':enc({n:ident(b) for n,b in additions.items()})}
 files.update({'root-additions/'+n:b for n,b in additions.items()})
 for directory in ('results','processes','provenance','tools','code','tests','intake','failures'):
  for p in sorted((W/directory).rglob('*')):
   if p.is_file() and not p.name.startswith('.') and p.suffix!='.pyc':files['new/'+str(p.relative_to(W))]=p.read_bytes()
 files['tools/recover.py']=(W/'tools/recover.py').read_bytes();files['RECOVERY.txt']=(W/'RECOVERY.txt').read_bytes()
 # Exact failed preparation output and original recovery code; no reconstructed stdout.
 for n in ('recovery.stdout','recovery.stderr'):files['new/failures/byte-recovery/'+n]=(W/'base'/n).read_bytes()
 files['new/failures/byte-recovery/original-recover.py']=(W.parent/'ec01-save-work/author/tools/recover.py').read_bytes()
 kinds=collections.Counter(x['result'] for x in progress);layers=collections.Counter(x['layer'] for x in progress)
 checkpoint={'target':'I164-cleanup-error-report-correspondence-1','status':'AUTHOR FOCUSED CONTROLS COMPLETED; INDEPENDENT REVIEW PENDING','scope':'Bounded selected protected-operation failure to line172 caught binding/evaluation/append; both contexts/control prefixes',
  'new_focused':{'checks':len(progress),'kinds':dict(kinds),'layers':dict(layers),'exit':ex,'stdout_progress_RESULT_reconciled':True,'full_current_public_positive':1,'actual_unchanged_predecessor_public_positive':1,'full_public_negative_derivations':0},
  'current_receipt':js('results/focused-recovered/validated-receipt-identity.json'),'input_root':input_final,'byte_only_delivery_recovery':{'exit':recovery_exit,'result':recovery_result},'changed_file_identities':json.loads(additions['provenance/changed-files.json']),
  'confirmed_saves_reused':['c2fb30a1a427db2a1066df4d40e17574fa51bcbf','c43954ff5ee384c6fb6e7a85d83eb36bfea342d1'],
  'prior_accounting':'See new/provenance/review-and-save-incorporation.json and exact retained closure; no totals combined or missing records repaired',
  'new_preparation_failure':js('failures/recovery-preparation.json'),'new_semantic_failures':result['error'],
  'operations':{'runtime_changes':0,'requests':0,'acquisitions':0,'database_connections':0,'session_operations':0,'Git_saves':0,'completed_campaign_replays':0},
  'preserved':js('provenance/review-and-save-incorporation.json')['preserved'],
  'limitations':['Conditional selected-error/owner/local/name/list/method continuity','No physical reference identity, runtime catch/evaluation/append observations or physical cleanup','Concrete generated error names/messages/bytes unavailable','Earlier append partial effects remain UNKNOWN even after normal error-report append','No handler exit/later iterations/loop completion/failure write/final rethrow/owner finalization','Original/selected/replacement exceptions remain distinct; cause/context/suppression qualifications retained','Non-None construction and remaining outer cleanup not completed','Cooperative CPython3.12.14 monitoring qualifications unchanged; installed runtime not newly qualified']}
 files['RESULTS.json']=enc(checkpoint)
 files['START-HERE.txt']=b'Read README.txt, RESULTS.json and RECOVERY.txt. New mandatory entry code/correspondence.py in the byte-recovered root; current receipt receipts/prepared-error-report.json. Author checks are not independent closure. Reuse all completed controls; no campaigns or Git saves may be replayed. Historical missing records remain missing.\n'
 files['README.txt']=f'''I164 cleanup error-report correspondence — bounded engineering checkpoint

Implemented the selected protected close/normal-message-append failure -> close_error
binding -> source-ordered error-item evaluation/append at lab_bootstrap.py:172.
Both symbolic contexts and both reviewed control prefixes are mandatory. Runtime
sources and the entire reviewed EC01 predecessor are unchanged. Independent review
of this extension remains PENDING.

The exact source expression is details['cleanup'].append([name,
type(close_error).__name__,str(close_error)]). Handler type evaluation, matching,
selection, entry and binding are separate conditional stages. A failure outside
the shared line171 try cannot acquire this handler. The same validated occurrence,
instance, invocation, owner/token, selected manager/name and details/list roles
flow from the unchanged predecessor's actual public validator. A source anchor or
eligibility never establishes runtime delivery.

Callable evaluation precedes arguments. The item evaluates name, then type's
callable/selected-error argument/call and __name__ attribute, then str's callable/
selected-error argument/call, then the list and append attempt/completion. These
are semantic boundaries, not observed opcode/allocation histories. Generated
names, messages, concrete values and formatted bytes remain unavailable. Existing
parent dynamic-field origins and exact False flags are preserved. Symbolic
container/reference records are not observed Python objects.

The original constructor error, selected cleanup error and any later matching/
binding/reporting replacement remain distinct. Normal error reporting retains a
True pending-exception classification; it proves neither normal overall return
nor final rethrow. Process termination/unobserved continuation retain None.
Catchable interruption is a conditional raise frontier, not inferred from process
termination. At matching/binding/reporting failure, earlier acknowledged storage,
close and reference facts persist. The last acknowledged caught error is distinct
from a pending replacement and from unavailable actual terminal observations.

The selected failure may come from close OR the subsequent normal-message append.
An append failure preserves a previously established normal close return. The
name close_error alone never establishes that close failed. Any UNKNOWN partial
effects from the earlier append remain UNKNOWN even when the later error-item
append completes. The output records an acknowledged symbolic append separately
from incomplete knowledge of the list's full contents; no silent reset or repair.

Stop after the selected append or first nonnormal frontier. Handler exit, later
iterations, loop completion, failure-file writing, final rethrow, owner finalization,
physical closure/durability/released ownership and renewed authorization remain
unestablished. Non-None construction and other outer-cleanup gaps remain open.
The separate observer stays unjoined; no runtime occurrence is manufactured.

New focused group: {len(progress)} completed rows ({kinds.get('PASS',0)} PASS,
{kinds.get('REJECTED',0)} expected REJECTED), exit0. Saved stdout, progress and RESULT
reconcile exactly. This includes one fresh recovered actual public positive and
its unchanged predecessor positive. See row-specific layers: required-relation
public gates before derivation, actual-authenticated semantic/constructed/output
cores, and authenticated receipt comparisons. No full public negative derivation
is claimed. Tests use isolated constructed inputs and retained evidence only.
The new receipt was prepared separately, then actually validated; original receipts
remain unchanged. Return-object mutation controls do not mutate expectations.

The bounded process used a 4500-second hard limit, 3900-second control deadline and
600-second finalization reserve; exact exits and incremental logs are saved.
The delivered recovery recipe separately reconstructed all 4015 files and 1110
directories with exact manifest identities and entry types, without candidate execution.
Initial byte recovery failed before any controls on undeclared local files. Those
exact partial files and the failed attempt are retained outside the strict input
root. A separate exact declared tree was recovered and verified. No originals
were repaired, and no missing historical records were reconstructed.

Formal-Lab EC01 closure remains scoped:93 independent checks (34 PASS/59 REJECTED,
exit0) separate from Engineering105. Earlier Engineering46/341 remain completed
and separate from incomplete primary1300 progress/165 stdout, missing final records
and UNKNOWN discrepancy cause. Historical rejection, four DEFECT-OBSERVED rows in
the separate170 group, separate21 completion, failed50 source attempt, preparation
failures, zero-replay audits and withdrawn corroboration claim are preserved.
No aggregate unqualified total is asserted. Prior LD01/EC01 closure is not reopened.

Host receipt confirms save c2fb30a1a427db2a1066df4d40e17574fa51bcbf; prior
c43954ff5ee384c6fb6e7a85d83eb36bfea342d1 is reused. This construction performs no Git
save, request, acquisition, database connection or session operation.

Both acquisitions, all eleven obligations, four inventory/fourteen lifetime
UNKNOWN totals, Decision B, retention and allowances remain. SOURCE-ONLY;
cumulative-envelope unadopted; backup kernel-only; streams UNCOMPUTED; readiness/
final binding blocked; admission disabled.
'''.encode()
 files['retained/Formal-Lab6-I164-EC01-independent-closure.zip']=archive.read_bytes()
 files['MANIFEST.json']=enc({n:ident(b) for n,b in sorted(files.items())})
 out=W.parent/'I164-cleanup-error-report-correspondence-1.zip'
 assert not out.exists()
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n,b in sorted(files.items()):
   i=zipfile.ZipInfo(n,(2026,11,2,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=(stat.S_IFREG|0o644)<<16;z.writestr(i,b)
 with zipfile.ZipFile(out) as z:
  assert len(z.namelist())==len(set(z.namelist()))==len(files) and set(z.namelist())==set(files) and z.testzip() is None
  for n,b in files.items():assert ident(z.read(n))==ident(b),n
 delivery={**ident(out.read_bytes()),'entries':len(files),'manifested_hashes':len(files)-1,'CRC':'PASS','membership_hashes':'PASS','path':str(out)}
 (W/'delivery-identity.json').write_bytes(enc(delivery));print(json.dumps(delivery),flush=True)
if __name__=='__main__':main()
