"""Finish post-recovery provenance audit; do not repeat byte recovery or controls."""
from pathlib import Path
import sys,zipfile,ast
sys.path.insert(0,str(Path(__file__).parent))
from integrity import *
root=AREA/'recovered';prior=root/'retained/loop';construction=AREA/'construction'
rv=verify(root);pv=verify(prior);current=js((construction/'CHECKPOINT.json').read_bytes());ad=js((construction/'ADDITIONS-MANIFEST.json').read_bytes());assert current['active_files']==ad
assert rv['files']==4044 and rv['directories']==1124 and rv['manifest']==current['root_manifest']
prefix=(prior/'code/managed_coverage.py').read_bytes();new=(root/'code/managed_coverage.py').read_bytes();added=(construction/'tools/write_call_addition.py').read_bytes();assert len(prefix)==375597 and new==prefix+added
oldnames={n.name for n in ast.parse(prefix).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};nodes=ast.parse(added).body;assert all(isinstance(n,ast.FunctionDef) and n.name not in oldnames for n in nodes)
for n in ('lab_bootstrap.py','prospective_entry.py','live_connection.py'):assert (root/'source-evidence'/n).read_bytes()==(prior/'source-evidence'/n).read_bytes()
fixtures={}
with zipfile.ZipFile(AREA/'dependencies/loop-construction.zip') as z:
 for p in sorted((root/'fixtures/loop').glob('*.json')):
  member='new/results/focused-recovered/fixtures/'+p.name;assert p.read_bytes()==z.read(member);fixtures[p.name]={'source_archive':'loop-construction.zip','source_member':member,'identity':file_ident(p),'runtime_observation':False}
historical=js((construction/'new/provenance/changed-files.json').read_bytes())['files'];correction=js((construction/'new/provenance/receipt-format-correction.json').read_bytes())
differing=[n for n in ad if ad[n]!=historical[n]];assert set(differing)=={'code/correspondence.py','receipts/prepared-write-call-replacement.json'}
for n in differing:assert file_ident(construction/'new/failures/receipt-format'/n)==historical[n]
assert correction['changed_files']=={n:ad[n] for n in differing}
deps={}
for p in sorted((AREA/'dependencies').glob('*.zip')):
 with zipfile.ZipFile(p) as z:deps[p.name]={**file_ident(p),'entries':len(z.namelist())}
out={'status':'PASS remaining intake/provenance verification','input':PIN,'outer_entries':8,'outer_manifested_hashes':7,'archive_CRC_safe_membership_manifest_checks':'Completed before preserved reviewer provenance assertion failure; no byte recovery replay','dependencies':deps,'recovered_root':rv,'unchanged_predecessor':pv,'preserved_predecessor_members':pv['files'],'declared_additions':len(ad),'active_files':ad,'source_prefix_unchanged_bytes':375597,'new_functions':[n.name for n in nodes],'source_runtime_bytes_unchanged':True,'fixtures':fixtures,'historical_changed_file_map_qualified_by_correction':correction,'preserved_failure':'failures/intake-fixture-origin','candidate_executions':0,'recovery_replayed':False}
(BASE/'results/intake.json').write_bytes(enc(out));print(enc(out).decode(),flush=True)
