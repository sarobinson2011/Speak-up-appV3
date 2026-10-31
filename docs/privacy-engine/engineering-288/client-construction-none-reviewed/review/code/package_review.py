"""Package completed independent review evidence. No validation campaign rerun."""
from pathlib import Path
import sys,json,hashlib,stat,zipfile
BASE=Path('/workspace/scratch/ace5c9b2f18b');REVIEW=BASE/'cln-review'
def enc(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def completed(label):
 r=json.loads((REVIEW/'results'/label/'RESULT.json').read_bytes());e=json.loads((REVIEW/'processes'/label/'exit-status.json').read_bytes());p=[json.loads(s) for s in (REVIEW/'results'/label/'progress.jsonl').read_text().splitlines()];printed=[]
 for line in (REVIEW/'processes'/label/'stdout.log').read_text().splitlines():
  head=line.split(' ',1)
  if len(head)==2 and head[0].isdigit():name,status=head[1].rsplit(' ',1);printed.append((int(head[0]),name,status))
 assert r['result']=='PASS' and r['error'] is None and e['returncode']==0 and not e['timed_out']
 assert r['rows']==p and r['checks']==len(p)==len(printed)
 assert printed==[(i+1,v['check'],v['result']) for i,v in enumerate(p)]
 assert not (REVIEW/'processes'/label/'stderr.log').read_bytes()
 return {'controls':len(p),'PASS':sum(v['result']=='PASS' for v in p),'REJECTED':sum(v['result']=='REJECTED' for v in p),'exit':e,'environment':r['environment'],'scope':r['scope'],'result_identity':identity((REVIEW/'results'/label/'RESULT.json').read_bytes()),'row_stdout_result_reconciled':True}
def main():
 integrity=json.loads((REVIEW/'results/integrity.json').read_bytes());audit=json.loads((REVIEW/'results/source-audit/preservation-and-supplied.json').read_bytes());groups={k:completed(k) for k in ('source-audit','fresh-recovered')}
 target=BASE/'cln-input/I164-client-construction-none-correspondence-1.zip';assert identity(target.read_bytes())==integrity['input']
 final={}
 sys.path.insert(0,str(REVIEW/'code'));from integrity import verify_root
 for k,v in integrity['roots'].items():final[k]=verify_root(v['path'])
 (REVIEW/'results/final-preservation.json').write_bytes(enc(final))
 public=json.loads((REVIEW/'results/fresh-recovered/public-result.json').read_bytes());assert public['result']=='PASS' and public['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and public['actual_admission'] is False
 checkpoint={'checkpoint':'Formal-Lab6-I164-client-construction-none-independent-review','target':target.name,'target_identity':integrity['input'],'target_entries':3414,'target_manifested_hashes':3413,'reviewer':'Formal-Lab[6]','construction_author':'SU-Engineering[288D]','author_independent':True,'verdict':'SCOPED SUPPORT WITH RETAINED OBSERVATION AND ACCOUNTING QUALIFICATIONS','integrity':integrity,'independent_groups':groups,'supplied_Engineering_groups':audit['supplied'],'public_validation':public,'fresh_full_public_validations':1,'private_core_mutants_not_full_public_derivations':True,'new_independent_defect_witness':None,'new_independent_failed_groups':0,'source_derived_findings':['Client(token) argument construction inside BaseException client handler; both absent and normally completed control prefixes','Same registered-owner exact-None guard is an explicit premise, not proof of absent historical failure storage','Bare rethrow preserves selected active construction-error role and adds no explicit cause; existing cause/context/suppression remain UNKNOWN','Handler-evaluation replacement, finally entry, removal attempt, completion, cleanup replacement and termination remain distinct','Mandatory current relation in both contexts is derived through actual validated predecessor source/evidence; source catalogue, semantic claims and constructed outputs are checked separately','Exact-type enforcement and copied returns prevent tested coordinated and nested-result changes from redefining expectations'],'preservation':audit['scope_limits'],'historical_accounting':audit['qualified_prior_records'],'supplied_failed_attempts':audit['new_failures'],'limitations':['No observed Client construction/error/handler/bare-rethrow/removal runtime chain','No allocation or initializer-progress mechanism established','Existing cause/context/suppression, physical object identity and lock/durability facts remain unestablished','Guard-slot and registered-owner continuity are conditional premises','Non-None construction-error handler branch and full outer cleanup outside this slice','18 historical traced invocations and separate frameless Client.state observer remain unjoined','One full public positive; negative core controls reuse its actual passively observed authenticated basis; no full-public negative derivation per mutant','Prepared-host Cryptography41.0.7 compatibility not tested; actual environment recorded separately','Original intermediate recovery-cut compressed ZIP not freshly verified or reconstructed; retained members verified exactly'],'prohibited_operations_performed':0,'completed_suite_reruns':0,'Git_saves':0,'actual_admission':False}
 (REVIEW/'CHECKPOINT.json').write_bytes(enc(checkpoint))
 report=f'''Formal-Lab[6] independent review: I164-client-construction-none-correspondence-1.zip

VERDICT: SCOPED SUPPORT WITH RETAINED OBSERVATION AND ACCOUNTING QUALIFICATIONS.
Construction author: SU-Engineering[288D]. Reviewer: Formal-Lab[6], separate from the construction author. No implementation changes were made. No residual defect witness was found in this bounded review.

Verified input: 134,972,464 bytes; 3,414 regular entries; SHA-256 550a9f0bf5e0643d79bbf7ac48a098015a06f05dc79ccde7f3eeb34a8cfbd1fe. CRC, safe exact membership and all 3,413 manifested hashes passed. Two separately recovered roots have 3,414 files and 977 implied directories each. All 3,260 exact predecessor members and 85 non-input members of its completed review remain byte-identical. The 3,361 frozen and 3,365 recovery-cut member identities agree. The original intermediate recovery-cut ZIP's compressed bytes are continuity-only, not freshly verified or reconstructed. Final root verification confirms no changes.

Source-backed findings
The defining prospective_entry.py at 174 and 176–188 registers owner/token, optionally completes the control path, and evaluates Client(token) at 179 inside the client try. The argument must finish before invocation of client. A modeled construction error therefore establishes neither a completed Client nor client callback execution. The Client.__init__ assignment at 111–112 is source information, not evidence that allocation, initializer entry or assignment occurred. The two prefix variants are checked separately and preserve earlier selected control completion when present. Conditional client reference symbols are not completed objects; separate error roles do not establish physical inequality. The reused callback-handler labels identify source regions, not client-callback execution.

The BaseException handler at 180 binds the selected construction error as client_error on normal handler entry. The same-owner slot is exactly None at the guard under an explicit continuity premise. The false branch of `owner.failure is not None` reaches bare raise at 183. This is not an inference that no earlier failure was ever stored. Bare raise introduces no explicit cause; existing cause, context and suppression remain UNKNOWN. Handler evaluation may itself fail, replacing pending propagation before finally.

Finally at 186–188 has distinct modeled entry, pop-attempt and normal-completion boundaries. `_OWNERS.pop(token, None)` discards its result. Normal selected-key absence is scoped to completed pop; selected-owner removal additionally needs the stated registry-continuity premise. Cleanup error may replace pending propagation. Termination/unobserved continuation does not prove Python unwind or later completion. Earlier established registration, construction error and selected control progress remain preserved. No cleanup, lock release, physical identity, exclusivity, durability, renewed authorization or successful _run follows.

Mandatory integration and source authentication
The current adapter refreshes exact predecessor inputs, rederives their validated receipt and compares it to the pinned saved receipt. It compiles the new relation from defining source and inherited declarations, binds both contexts to validated instance anchors, and checks constructed token prefixes through the retained token validator. None-guard and error-role expectations are independently regenerated from that basis. Submitted catalogue/claim/output equality alone is insufficient. Public validation requires all seven applicable relations and compares the complete saved receipt with current derivation. Tests of private cores are explicitly distinguished from full public calls.

Independent evidence
Source-audit process: {groups['source-audit']['controls']} controls, exit 0, corroborated RESULT/progress/stdout. Independently derived AST coordinates, exact guards and prefix ordering; source/catalogue mutations; all 123 inherited producer functions unchanged, with six additive functions. Declared changes match both code identities and the exact diff. Runtime sources are unchanged. Prior context fields/ordinals and original receipt values are preserved except the declared extension envelope.
Fresh recovered process: {groups['fresh-recovered']['controls']} controls ({groups['fresh-recovered']['PASS']} PASS, {groups['fresh-recovered']['REJECTED']} REJECTED), exit 0, corroborated RESULT/progress/stdout. One actual unchanged full public positive on the recovered root accepted both contexts. Subsequent new constructed/semantic negative controls use the passively observed authenticated basis; no validator replacement and no claim that each mutant triggered another full derivation. Checks include both prefixes, distinct invocation identities, conditional continuity, handler/cleanup replacement, all modeled termination/unobserved frontiers, missing/reordered stages, owner/token/error/context/acquisition substitutions, exact types, false completion, invented cause/mechanism/authority, and nested returned-object mutation. Mandatory public omissions reject at their pre-derivation gate. Expected totals are not the test oracle.
Both processes had finite timeouts, retained incremental logs, explicit exit records and empty stderr. A timeout or harness failure would not count as rejection. No fresh independent failed group occurred. Actual environment: CPython3.12.14, isolated -I -B, optimization0, Cryptography50.0.2. This does not establish prepared-host41.0.7 compatibility or runtime execution.

Supplied evidence, kept separate
Engineering's 498 primary and 210 recovery/process rows reconcile exactly to their result files, progress, stdout and exit0 records. They are not independent controls. Their zero-control preparation error and failed membership attempt, original manifests and extra-file bytes remain preserved. The cause of those entries is unestablished. The prior independent 159/80 completed groups and qualified 61-row failed audit remain historical support; none were rerun. Prior Engineering 285/71 interrupted rows and two separately completed one-check groups remain qualified. Older 520 result-recorded/517 corroborated, coordinated106/103/103 with rows104–106 qualified, nine partial public rows, separately completed public rejection, and 308/307/303 discrepancy are preserved without inventing a combined completed total. See retained records and CHECKPOINT.json for exact provenance.

Remaining limits
This supports static conditional correspondence, not occurrence coverage or execution of the constructor/handler/removal chain. The separate observer Client.state call remains unjoined. The non-None construction handler and full outer-cleanup paths remain outside scope. The current checks do not discharge qualification, operational ownership, lifetime or authority obligations. The eleven obligations, four inventory UNKNOWNs, fourteen lifetime UNKNOWNs, Decision B, retention and allowances remain. SOURCE-ONLY; cumulative-envelope unadopted; backup kernel-only; streams UNCOMPUTED; readiness/final binding blocked; admission disabled.

Recovery
The checkpoint contains the exact input archive and all new reviewer scripts, logs, process exits, source expectations and preserved pending draft. Read RECOVERY.txt. Recovery of evidence is authorized; rerunning completed controls is not implied. No application/session/database operations, requests, acquisitions, pipelines, policy adoption or Git saves were performed.
'''
 (REVIEW/'REPORT.txt').write_text(report)
 (REVIEW/'RECOVERY.txt').write_text('Verify this review ZIP against the delivered outer identity, CRC, safe unique regular membership and MANIFEST.json before extracting into a new empty persistent directory. Verify input/I164-client-construction-none-correspondence-1.zip against CHECKPOINT.json and its 3413 hashes before separately recovering its members. Preserve failure and partial files as declared evidence, outside strict predecessor roots where placed by the supplied composition. Dependencies are flattened in the exact input archive. Original intermediate compressed archives not present remain continuity identities only. Review scripts/results are evidence, not permission to rerun completed work. No dependencies were installed. No application/session/database access is needed to inspect this checkpoint.\n')
 files={'input/'+target.name:target.read_bytes()}
 for p in sorted(REVIEW.rglob('*')):
  assert not p.is_symlink()
  if p.is_file():files['review/'+p.relative_to(REVIEW).as_posix()]=p.read_bytes()
 files['MANIFEST.json']=enc({n:identity(b) for n,b in sorted(files.items())})
 out=BASE/'Formal-Lab6-I164-client-construction-none-independent-review.zip';assert not out.exists()
 with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
  for n,b in sorted(files.items()):
   info=zipfile.ZipInfo(n,(2026,10,31,0,0,0));info.create_system=3;info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
 with zipfile.ZipFile(out) as z:
  assert z.namelist()==sorted(files) and len(z.namelist())==len(set(z.namelist()))
  for n,b in files.items():assert z.read(n)==b,n
 pin={**identity(out.read_bytes()),'entries':len(files),'manifested_hashes':len(files)-1,'CRC_safe_membership_hashes':'PASS','file':str(out)}
 (BASE/'cln-package.json').write_bytes(enc(pin));print(json.dumps(pin),flush=True)
if __name__=='__main__':main()
