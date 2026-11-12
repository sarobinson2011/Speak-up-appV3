"""Final preservation and review-record audit only; no control rerun."""
from pathlib import Path
import json,hashlib,collections,importlib.util
B=Path(__file__).resolve().parent;R=B/'candidate';H=B/'host';O=B/'independent'
def read(p):return json.loads(p.read_bytes())
def fid(p):return {'bytes':p.stat().st_size,'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()}
def jl(p):return [json.loads(x) for x in p.read_text().splitlines()]
def main():
 rows=[read(p) for p in sorted(O.glob('[0-9][0-9][0-9][0-9].json'))];result=read(O/'RESULT.json');ex=read(B/'independent-exit.json')
 assert rows==jl(O/'progress.jsonl')==jl(B/'independent.stdout') and [r['sequence'] for r in rows]==list(range(1,len(rows)+1))
 counts=collections.Counter(r['status'] for r in rows);assert counts['FAIL']==0 and result['rows']==len(rows) and result['counts']=={s:counts[s] for s in ('PASS','REJECTED','FAIL')}
 assert ex['exit_code']==0 and ex['timed_out'] is False and (B/'independent.stderr').read_bytes()==b'' and not (O/'FAILURE.json').exists()
 assert result['public_calls']==result['full_public_negative_derivations']==0 and result['authenticated_constructed_path']=='UNEXECUTED'
 p=H/'code/common_r1.py';s=importlib.util.spec_from_file_location('final_bytes_only',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 tree=m.exact_tree(R,read(H/'expected/ASSEMBLED-ROOT-MANIFEST.json'));assert tree['files']==4963 and tree['directories']==1264
 assert (H/'inputs/I164-res-null-test-1-source.zip').read_bytes()==(B/'parent-review/inputs/I164-res-null-test-1-source.zip').read_bytes()
 assert read(B/'parent-review/audits/final-root-audit.json')['exact_types_membership_hashes']=='PASS'
 # Verify the reusable helper identity only; do not import native monitoring or application modules.
 pins=__import__('ast').literal_eval(next(x.value for x in __import__('ast').parse((H/'code/recovery.py').read_text()).body if isinstance(x,__import__('ast').Assign) and any(isinstance(n,__import__('ast').Name) and n.id=='HARNESS_PINS' for n in x.targets)))
 for n,pin in pins.items():assert fid(H/'observer-reference'/n)==pin
 declaration=read(H/'validation/results/actual-derived-receipt.json')
 summary={'status':'PASS','independent':{'rows':len(rows),'counts':dict(counts),'exit':ex,'all_raw_progress_stdout_exact':True,'layers':dict(collections.Counter(r['layer'] for r in rows))},'final_candidate':tree,'new_implementation':declaration['extension_components'],'reviewed_parent_source_zip_byte_identical':True,'unchanged_observer_files':len(pins),'original_failures_preserved':['input-audit-original-failure.json','recovery.exit.json','recovery.stderr'],'campaign_replays':0,'public_replays':0}
 (B/'final-audit.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
