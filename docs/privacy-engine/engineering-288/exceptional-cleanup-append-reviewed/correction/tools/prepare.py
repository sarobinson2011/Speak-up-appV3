from pathlib import Path
import ast,copy,difflib,hashlib,json
T=Path(__file__).resolve().parents[1];old=T/'historical';bundle=T/'bundle';overlay=bundle/'overlay'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def save(n,b):
 p=overlay/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
changed={};diff=[]
n='code/managed_coverage.py';before=(old/n).read_bytes();a=b"'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True if terminal=='raise' else False,"
z=b"'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True,"
assert before.count(a)==1;producer=before.replace(a,z)
updates={n:producer}
n='code/correspondence.py';before=(old/n).read_text();oldline=next(x for x in before.splitlines() if x.startswith('PRODUCER_PIN='));new=before.replace(oldline,'PRODUCER_PIN='+repr(ident(producer)));assert new!=before;updates[n]=new.encode()
n='tests/cases.py';before=(old/n).read_text();needle=' if terminal:\n';assert before.count(needle)==1
new=before.replace(needle," # EC-01: lab_bootstrap.py:167-171 remains in the constructor-error handler.\n # A normal cleanup append does not establish normal overall return.\n if terminal is None:assert out['terminal_python_exception_in_model'] is True\n"+needle);updates[n]=new.encode()
for n,after in updates.items():
 before=(old/n).read_bytes();compile(after,n,'exec');save(n,after);save('ec01/original/'+n,before);changed[n]={'before':ident(before),'after':ident(after)}
 diff.extend(difflib.unified_diff(before.decode().splitlines(True),after.decode().splitlines(True),fromfile='historical/'+n,tofile='corrected/'+n))
save('ec01/original/MANIFEST.json',(old/'MANIFEST.json').read_bytes())
save('ec01/provenance/changed-files.json',enc({'intentional_existing_file_changes':changed,'runtime_sources_changed':False,'predecessor_changed':False,'monitoring_helper_changed':False,'scope':'EC-01 terminal classification; producer pin; omitted normal-path test oracle assertion'}))
save('ec01/provenance/implementation.diff',''.join(diff).encode())
receipt_path=old/'results/recovered/cleanup-append.json';raw=receipt_path.read_bytes();v=json.loads(raw);before=copy.deepcopy(v)
v['extension_components']={n:ident(updates['code/'+n]) for n in ('managed_coverage.py','correspondence.py')}
prepared=(json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode();assert v!=before
probe=copy.deepcopy(v);probe['extension_components']=before['extension_components'];assert probe==before
save('ec01/receipts/prepared-cleanup-append.json',prepared)
save('ec01/provenance/prepared-receipt.json',enc({'status':'NEWLY PREPARED, NOT YET VALIDATED','historical_receipt_path':'results/recovered/cleanup-append.json','historical_receipt':ident(raw),'new_receipt_path':'ec01/receipts/prepared-cleanup-append.json','new_receipt':ident(prepared),'only_changed_fields':['extension_components.managed_coverage.py','extension_components.correspondence.py'],'preparation_is_validation':False,'original_receipt_unchanged':True}))
for n in ('EC01-smallest-case.json','EC01-accepted-result.json','EC01-source-consistent-one-field-output.json','EC01-witness.json'):
 save('ec01/witnesses/'+n,(T/'review/review/results/public-recovered'/n).read_bytes())
save('ec01/provenance/review-CHECKPOINT.json',(T/'review/CHECKPOINT.json').read_bytes());save('ec01/provenance/review-REVIEW.txt',(T/'review/REVIEW.txt').read_bytes())
save('ec01/START-HERE.txt',b'Active EC-01 correction only. Historical root-level documents/results keep their original statuses. Read ec01/provenance/changed-files.json, prepared-receipt.json and review-REVIEW.txt. New prepared receipt: ec01/receipts/prepared-cleanup-append.json. Original receipts are unchanged. Only new focused checks are authorized. Independent closure is pending; all prior boundaries remain.\n')
print(json.dumps({'changed':changed,'new_prepared_receipt':ident(prepared),'historical_receipt':ident(raw)},indent=2))
