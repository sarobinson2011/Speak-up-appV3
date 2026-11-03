"""Independent record-to-binding audit after actual public-basis capture; no replay."""
from pathlib import Path
import sys,json,zipfile,ast
sys.path.insert(0,str(Path(__file__).parent))
from integrity import AREA,BASE,ident,file_ident,enc
root=AREA/'recovered';manifest=json.loads((root/'MANIFEST.json').read_bytes());facts=json.loads((BASE/'results/public-recovered/basis-facts.json').read_bytes())
archive_path=next(n for n in manifest if n.endswith('/inputs/smoke.zip'));assert file_ident(root/archive_path)==manifest[archive_path]
with zipfile.ZipFile(root/archive_path) as z:
 names=('evidence/SMOKE-ABOUT-TO-START.json','evidence/session-records/binding.json');raw={n:z.read(n) for n in names}
for n,b in raw.items():assert ident(b)==facts['evidence'][n]
start=json.loads(raw[names[0]]);binding=json.loads(raw[names[1]]);launcher=(root/'source-evidence/lab_bootstrap.py').read_bytes();assert ident(launcher)==facts['source_identities'][0]
fn=next(n for n in ast.parse(launcher).body if isinstance(n,ast.FunctionDef) and n.name=='owner_lock');source={'site':f'{fn.lineno}:{fn.col_offset}:{fn.end_lineno}:{fn.end_col_offset}:FunctionDef','expression':ast.get_source_segment(launcher.decode(),fn),'guards':[],'continuation':[]}
assert ast.unparse(fn.body[0])=='dest = Path(destination).absolute()' and ast.unparse(fn.body[2])=='parent = dest.parent.resolve()' and ast.unparse(fn.body[4])=='dest = parent / dest.name'
ys=[n for n in ast.walk(fn) if isinstance(n,ast.Yield)];assert len(ys)==1 and ast.unparse(ys[0].value)=='dest'
rows=[]
for index,sb in enumerate(facts['session_bindings']):
 assert sb['acquisition']=='sha256:'+manifest[archive_path]['sha256'];assert sb['recorded_destination']==start['destination'] and type(start['destination']) is str
 assert sb['instance']['session_label']==binding['configuration']['config']['session']
 assert {k:binding['launcher'][k] for k in ('bytes','sha256')}==ident(launcher)
 assert sb['source_owner_lock']==source and sb['physical_resolved_destination'] is None
 assert sb['start_record']=={'path':names[0],'identity':ident(raw[names[0]]),'pointer':'/destination'}
 assert sb['binding_record']=={'path':names[1],'identity':ident(raw[names[1]]),'pointer':'/configuration/config/session'}
 rows.append({'context_index':index,'nominal_destination_correspondence':True,'session_label_correspondence':True,'acquisition_archive_correspondence':True,'owner_lock_source_correspondence':True,'physical_resolution':'UNOBSERVED'})
(BASE/'results/returned-evidence-audit.json').write_bytes(enc({'actual_basis_capture':'results/public-recovered/basis-facts.json','archive':{'path':archive_path,'identity':manifest[archive_path]},'exact_members':{n:ident(b) for n,b in raw.items()},'contexts':rows,'recorded_assertions_are_runtime_verification':False,'new_invocations_or_physical_copies_inferred':False,'application_execution':False}));print('PASS: two-context actual-returned evidence binding audit; no candidate validation replay',flush=True)
