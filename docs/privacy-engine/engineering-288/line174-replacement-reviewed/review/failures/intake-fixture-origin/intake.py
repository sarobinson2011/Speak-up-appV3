"""Independent nested recovery; supplied recovery code is inspected, not executed."""
from pathlib import Path
import sys,ast,traceback
sys.path.insert(0,str(Path(__file__).parent))
from integrity import *
def main():
 AREA.mkdir(parents=True,exist_ok=False);(BASE/'results').mkdir(parents=True,exist_ok=True);deps=[]
 def nested(z,name,pin,count,label):
  put(AREA/'dependencies',label+'.zip',z.read(name));p=AREA/'dependencies'/(label+'.zip');a=archive(p,pin,count);deps.append({'label':label,**pin,'entries':count,'CRC_membership_hashes':'PASS'});return a
 outer=archive(INPUT,PIN,8);extract(outer,AREA/'outer');outerc=js(outer.read('CHECKPOINT.json'))
 cp=outerc['construction_checkpoint'];rp=outerc['result_checkpoint']
 con=nested(outer,'retained/I164-line174-NEW-replacement-prerun-2.zip',{k:cp[k] for k in ('bytes','sha256')},136,'construction');extract(con,AREA/'construction')
 records=nested(outer,'results/I164-line174-NEW-replacement-final-records.zip',{k:rp[k] for k in ('bytes','sha256')},767,'final-records');extract(records,AREA/'final-records');records.close();outer.close()
 print('Outer, corrected pre-run and final-record archives verified',flush=True)
 review=nested(con,'retained/cleanup-loop-review.zip',{'bytes':176585667,'sha256':'da62fa43eaf66a37d86830bdbb3aa93a3f9f91aa3258237713cde69a196e53c7'},275,'loop-review')
 loop=nested(review,'input/I164-cleanup-loop-exhaustion-correspondence-1.zip',{'bytes':169181718,'sha256':'a48cb3be9002e8dbdcf3ac8c6e2d0ed45ea1eced14126af3d9d1862ec1963dd5'},81,'loop-construction')
 for n in ('CHECKPOINT.json','REVIEW.txt','RECOVERY.txt'):put(AREA/'prior-review',n,review.read(n))
 for n in ('common.py','monitor.py','supervise.py'):put(BASE/'retained-review-code',n,review.read('review/code/'+n))
 line_review=nested(loop,'retained/Formal-Lab6-I164-cleanup-error-report-independent-review.zip',{'bytes':160663290,'sha256':'156f5a7cca4b3966ac348d3bf6a0636a69ebd1c66375bb0c1277d929e4e37251'},83,'line172-review')
 line=nested(line_review,'input/I164-cleanup-error-report-correspondence-1.zip',{'bytes':159370715,'sha256':'2b6d61b3f9dc756740a0c66f4bdf70a729cfb77d43beb495424965331aa72bd1'},83,'line172-construction');line_review.close()
 ec_review=nested(line,'retained/Formal-Lab6-I164-EC01-independent-closure.zip',{'bytes':154107404,'sha256':'7971a5cd95ef8775ff05e2db0ef5c3521903586c0d530b9e590b4bb54029fcef'},52,'EC01-review')
 ec=nested(ec_review,'input/I164-EC01-terminal-exception-correction-1.zip',{'bytes':153799952,'sha256':'ae83c5eeb7bf4ab09943f66f239bea3c7802777899f4fe6417e10e39dc9b1f71'},57,'EC01-construction');ec_review.close()
 append_review=nested(ec,'retained/Formal-Lab6-I164-exceptional-cleanup-append-independent-review.zip',{'bytes':156078207,'sha256':'212d2f0886cb09cddb119470ba908e2142bb141a6eb6bdca83a3e5f83b82cbcb'},85,'append-review')
 original=nested(append_review,'input/I164-exceptional-cleanup-append-correspondence-1.zip',{'bytes':155659416,'sha256':'14bfe3fcc3da3f5f8e2ab6cfb3c820229f1520b439b9ebaf5f6bad83daf25c50'},3982,'append-construction');append_review.close()
 root=AREA/'recovered';prior=root/'retained/loop';report=prior/'retained/report';old=report/'retained/cleanup'
 extract(original,old);original.close()
 for n,p in js(ec.read('OVERLAY-MANIFEST.json')).items():
  b=ec.read('overlay/'+safe(n));assert ident(b)==p;q=old/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 (old/'MANIFEST.json').write_bytes(ec.read('ROOT-MANIFEST.json'));ec.close();ecv=verify(old)
 lv=additions(line,report,'retained/cleanup');line.close();pv=additions(loop,prior,'retained/report');loop.close()
 rv=additions(con,root,'retained/loop')
 print('Fresh independent root reconstructed and exact membership verified',flush=True)
 current=js(con.read('CHECKPOINT.json'));ad=js(con.read('ADDITIONS-MANIFEST.json'));assert current['active_files']==ad
 for n,p in ad.items():assert file_ident(root/n)==p
 new=(root/'code/managed_coverage.py').read_bytes();prefix=(prior/'code/managed_coverage.py').read_bytes();added=con.read('tools/write_call_addition.py');assert len(prefix)==375597 and new==prefix+added
 oldnames={n.name for n in ast.parse(prefix).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};nodes=ast.parse(added).body;assert all(isinstance(n,ast.FunctionDef) and n.name not in oldnames for n in nodes)
 for n in ('lab_bootstrap.py','prospective_entry.py','live_connection.py'):assert (root/'source-evidence'/n).read_bytes()==(prior/'source-evidence'/n).read_bytes()
 for p in (root/'fixtures/loop').glob('*.json'):assert p.read_bytes()==review.read('review/results/public-recovered/fixture-'+p.name)
 review.close()
 historical=js(con.read('new/provenance/changed-files.json'))['files'];correction=js(con.read('new/provenance/receipt-format-correction.json'))
 differing=[n for n in ad if ad[n]!=historical[n]];assert set(differing)=={'code/correspondence.py','receipts/prepared-write-call-replacement.json'}
 for n in differing:assert ident(con.read('new/failures/receipt-format/'+n))==historical[n]
 assert correction['changed_files']=={n:ad[n] for n in differing}
 result={'input':PIN,'outer_entries':8,'outer_manifested_hashes':7,'CRC':'PASS','safe_exact_membership':'PASS','dependencies':deps,'recovered_root':rv,'unchanged_predecessor':pv,'line172':lv,'EC01':ecv,'preserved_predecessor_members':pv['files'],'declared_additions':len(ad),'active_files':ad,'source_prefix_unchanged_bytes':375597,'new_functions':[n.name for n in nodes],'source_runtime_bytes_unchanged':True,'eight_parent_fixtures_exact_prior_review_copies':True,'preparation_correction_separate':correction,'supplied_pre_run_status_preserved':current['status'],'candidate_executions':0}
 (BASE/'results/intake.json').write_bytes(enc(result));print(json.dumps(result),flush=True)
if __name__=='__main__':main()
