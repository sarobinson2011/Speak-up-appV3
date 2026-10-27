"""New reference entry input gate tests, using disposable persistent copies."""
from pathlib import Path
import hashlib,json,os,shutil,sys,types
root=Path(sys.argv[1]).resolve();fixture=Path(sys.argv[2]).resolve();out=Path(sys.argv[3]).resolve()
out.mkdir(parents=True,exist_ok=False);shutil.copytree(root,fixture)
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def audit(event,args):
 if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo'):raise AssertionError('PROHIBITED:'+event)
 if event=='open' and isinstance(args[0],(str,bytes)) and os.fsdecode(args[0]).startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
sys.addaudithook(audit)
def profile(frame,event,arg):
 if event=='call' and frame.f_code.co_filename.rsplit('/',1)[-1] in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('APPLICATION-EXECUTION')
sys.setprofile(profile)
path=fixture/'code/correspondence.py';m=types.ModuleType('input_probe');m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__)
original_loader=m._module
def forbidden_import(*args,**kwargs):raise AssertionError('CANDIDATE-CONSUMED-BEFORE-INPUT-REJECTION')
m._module=forbidden_import
base=fixture/'retained/fields';checks=[]
def reject(label):
 try:m.reference_inputs(fixture)
 except (ValueError,FileNotFoundError) as e:checks.append({'check':label,'result':'REJECTED','message':str(e),'before_candidate_consumption':True});return
 raise AssertionError('UNEXPECTED ACCEPTANCE: '+label)
receipt=base/'results/status-field-correspondence.json';original=receipt.read_bytes()
try:
 receipt.unlink();reject('missing required field receipt')
finally:receipt.write_bytes(original)
try:
 receipt.write_bytes((base/'retained/occurrence/results/occurrence-connection.json').read_bytes());reject('substituted predecessor occurrence receipt')
finally:receipt.write_bytes(original)
context=base/'retained/occurrence/retained/correction/retained/candidate/candidate/contexts.json';original=context.read_bytes()
try:
 changed=original.replace(b'SYMBOLIC-U-ONE',b'SYMBOLIC-U-TWO');assert changed!=original;context.write_bytes(changed);reject('mixed symbolic context definition')
finally:context.write_bytes(original)
extra=base/'unexpected-reference.json'
try:
 extra.write_text('{}\n');reject('undeclared input member')
finally:extra.unlink()
m._module=original_loader
answer=m.validate(fixture,(fixture/'results/reference-correspondence.json').read_bytes());assert answer['result']=='PASS'
checks.append({'check':'restored legitimate exact input tree accepts','result':'PASS'})
originals={p.relative_to(root).as_posix():ident(p.read_bytes()) for p in root.rglob('*') if p.is_file()};restored={p.relative_to(fixture).as_posix():ident(p.read_bytes()) for p in fixture.rglob('*') if p.is_file()};assert originals==restored
result={'result':'PASS','assertions':len(checks),'checks':checks,'fixture_restored_to_exact_original':True,'original_and_implementation_files_unchanged':True,'no_application_or_database_operations':True}
(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
