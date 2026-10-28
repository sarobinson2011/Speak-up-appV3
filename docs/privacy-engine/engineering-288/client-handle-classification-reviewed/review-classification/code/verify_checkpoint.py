"""Read-only verification of the sealed independent checkpoint and input."""
from pathlib import Path,PurePosixPath
import hashlib,io,json,stat,sys,zipfile
p=Path(sys.argv[1]);raw=p.read_bytes()
def ident(v):return {'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()}
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 infos=z.infolist();assert len(infos)==len({i.filename for i in infos}) and z.testzip() is None
 for i in infos:
  n=PurePosixPath(i.filename);assert not n.is_absolute() and '..' not in n.parts and '\\' not in i.filename and str(n)==i.filename and not i.is_dir() and stat.S_IFMT(i.external_attr>>16)==stat.S_IFREG
 m=json.loads(z.read('MANIFEST.json'))['members'];assert set(m)==set(z.namelist())-{'MANIFEST.json'}
 for n,pin in m.items():assert ident(z.read(n))==pin,n
 target=z.read('input/I164-outside-catch-classification-correction-1.zip');assert ident(target)=={'bytes':60424906,'sha256':'08499f314151aef36bdbe711ad6f821bf1258d28a8c0d65fd693e3b0db4a3ba5'}
 with zipfile.ZipFile(io.BytesIO(target)) as t:
  assert len(t.infolist())==1508 and t.testzip() is None;tm=json.loads(t.read('MANIFEST.json'));assert len(tm)==1507 and set(tm)==set(t.namelist())-{'MANIFEST.json'}
  for n,pin in tm.items():assert ident(t.read(n))==pin,n
 cp=json.loads(z.read('CHECKPOINT.json'));assert cp['verdict'].startswith('SUPPORTED within stated') and cp['residual_defect_witness'] is None and cp['boundaries']['admission'] is False
 assert cp['independent_results']['primary_checks']==172 and cp['independent_results']['recovered_checks']==131 and cp['observation_limits']['runtime_handle_return_chain']=='UNAVAILABLE'
 rec=json.loads(z.read('results/progress-reconciliation.json'));old=json.loads(z.read('failures/historical-record-key-attempt-1/results/RESULT.json'));new=json.loads(z.read('independent-primary/additional/RESULT.json'));progress=z.read('independent-primary/additional/progress.jsonl');assert ident(progress)==rec['combined_progress'] and [json.loads(v) for v in progress.decode().splitlines()]==old['rows']+new['rows']
 assert b'{{COUNTS}}' not in z.read('REPORT.md')
print(json.dumps({'archive':p.name,**ident(raw),'entries':len(infos),'CRC':'PASS','safe_exact_membership':'PASS','all_manifest_hashes':'PASS','embedded_exact_target':'PASS','failure_and_reconciliation_records':'PASS','verdict':'SUPPORTED, bounded clarification/correction'},sort_keys=True))
