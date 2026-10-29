from pathlib import Path,PurePosixPath
import sys,json,hashlib,zipfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
from integrity import check_tree,ident,PIN
w=Path(__file__).resolve().parents[2];base=w/'sr-review';archive=w/'upload/I164-internal-status-return-correspondence-1(1).zip';raw=archive.read_bytes();assert ident(raw)==PIN
with zipfile.ZipFile(archive) as z:
 names=z.namelist();m=json.loads(z.read('MANIFEST.json'));dirs={str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'};mi=ident(z.read('MANIFEST.json'))
roots=['sr-clean-recovered','sr-clean-primary','sr-full-type-root','sr-core-primary','sr-core-recovered','sr-entry-primary','sr-entry-coordinated','sr-entry-derive','sr-entry-public-negative','sr-witness-recovered','sr-cli-root','sr-key-root','sr-key-recovered']
for n in roots:check_tree(w/n,names,dirs,m,mi)
groups={};totals={};findings=[]
for label in ['primary','recovered']:
 out=[];counts={}
 for p in sorted((base/('independent-'+label)).glob('*/RESULT.json')):
  r=json.loads(p.read_bytes());rows=[json.loads(x) for x in p.with_name('progress.jsonl').read_text().splitlines()];assert r['error'] is None and r['result'] in ('PASS','COMPLETED_WITH_FINDINGS') and r['checks']==len(rows) and r['rows']==rows
  for x in rows:counts[x['result']]=counts.get(x['result'],0)+1
  findings.extend(r.get('findings',[]));out.append({'path':p.parent.relative_to(base).as_posix(),'result':r['result'],'checks':r['checks'],'identity':ident(p.read_bytes()),'environment':r['environment']})
 groups[label]=out;totals[label]={'checks':sum(counts.values()),'outcomes':counts,'groups':len(out)}
assert totals['primary']['checks']==206 and totals['primary']['outcomes']['DEFECT-ACCEPTED']==8
assert totals['recovered']['checks']==165 and totals['recovered']['outcomes']['DEFECT-ACCEPTED']==9
assert len(findings)==17
f=base/'failures/initial-root-membership';fr=json.loads((f/'RECORD.json').read_bytes());assert fr['failed_processes']==5
for x in fr['undeclared_regular_files']:
 original=w/x['root']/x['path'];preserved=f/x['preserved_copy'];assert original.read_bytes()==preserved.read_bytes();assert ident(original.read_bytes())=={'bytes':x['bytes'],'sha256':x['sha256']}
for p in f.glob('*/RESULT.json'):assert json.loads(p.read_bytes())['checks']==0
cli=json.loads((base/'cli-recovered/RESULT.json').read_bytes());assert cli['result']=='PASS' and cli['process']['exit_code']==0
report={'result':'VERIFIED_WITH_SCOPED_FINDING','verdict':'NOT FULLY SUPPORTED: IS-01 residual exact-type acceptance in status dictionary keys, submitted outputs and semantic claims','input_identity':ident(raw),'exact_unchanged_recovered_roots':roots,'members_each':len(names),'implied_directories_each':len(dirs),'independent_results':totals,'groups':groups,'findings':findings,'smallest_witness':'Replace one hop/sample reason with a str subclass holding the same characters; output validator and full semantic/derive accept. Files and evidence unchanged.','public_byte_contract':'No subclass can be represented in JSON bytes. Serialization-equivalent subclass claim produces the same legitimate receipt bytes; no forged different public receipt is claimed.','original_witnesses_reproduced_and_corrected':12,'supplied_results_separate':{'focused_exact_types':36,'recovered_correspondence':205,'recovered_exact_types':34,'fresh_process':5,'pre_hardening':204,'failed_harness_excluded':17},'new_zero_check_root_refusals':5,'refused_root_originals_and_partial_bytes_preserved':True,'partial_file_cause':'UNKNOWN','CLI':cli,'implementation_modified':False}
(base/'results/final-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'result':report['result'],'independent_results':totals,'residual_confirmations':17,'original_witnesses':12,'clean_final_roots':len(roots),'zero_check_failed_roots_preserved':5}))
