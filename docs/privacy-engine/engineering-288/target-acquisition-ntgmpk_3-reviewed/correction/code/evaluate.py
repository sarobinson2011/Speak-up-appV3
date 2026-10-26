"""Bounded offline orchestration. Root and acquisition pins precede all executable imports."""
import argparse,ast,copy,datetime,importlib,importlib.util,platform,sys,time,traceback,os,stat
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import contract as c
P=Path(__file__).resolve().parents[1]
def denied(event,args):
 if event in ('sqlite3.connect','socket.connect','socket.bind','subprocess.Popen','os.system'):raise c.Rejected('OFFLINE-FORBIDDEN:'+event)
 if event=='open' and isinstance(args[0],(str,bytes)) and str(args[0]).startswith('/home/steve/'):raise c.Rejected('ORIGINAL-PATH-ACCESS')
def pins():
 raw=c.read(P/'provenance/component-pins.json')
 # Authority is the reviewed checkpoint digest; this file separates source pins from output pins.
 p=c.parse(raw)
 for n,v in p.items():c.same(c.ident(c.read(P/n)),v,'COMPONENT-PIN:'+n)
 return p

def tree(root,expected):
 """Check all names and types before reading any payload. Never follow symlinks."""
 root=Path(root)
 c.need(stat.S_ISDIR(root.lstat().st_mode),'ROOT-DIRECTORY-TYPE')
 c.need(type(expected) is dict,'ROOT-MANIFEST-TYPE')
 allowed_dirs=set()
 for name in expected:
  c.need(type(name) is str and bool(name),'ROOT-MEMBER-NAME')
  path=Path(name)
  c.need(not path.is_absolute() and '..' not in path.parts and path.as_posix()==name and name!='.','ROOT-MEMBER-PATH')
  allowed_dirs.update(p.as_posix() for p in path.parents if p.as_posix()!='.')
 c.need(not set(expected)&allowed_dirs,'ROOT-FILE-DIRECTORY-CONFLICT')
 files=set();directories=set()
 def scan(parent):
  with os.scandir(parent) as entries:
   for entry in entries:
    path=parent/entry.name;name=path.relative_to(root).as_posix()
    mode=entry.stat(follow_symlinks=False).st_mode
    if stat.S_ISDIR(mode):
     c.need(name in allowed_dirs,'UNDECLARED-ROOT-DIRECTORY:'+name)
     directories.add(name);scan(path)
    elif stat.S_ISREG(mode):
     c.need(name in expected,'UNDECLARED-ROOT-FILE:'+name);files.add(name)
    else:raise c.Rejected('UNSUPPORTED-ROOT-ENTRY:'+name)
 scan(root)
 c.same(sorted(files),sorted(expected),'EXACT-ROOT-FILES')
 c.same(sorted(directories),sorted(allowed_dirs),'EXACT-ROOT-DIRECTORIES')
 # c.read performs lstat and O_NOFOLLOW again before each regular-file read.
 for name in sorted(files):c.same(c.ident(c.read(root/name)),expected[name],'ROOT-FILE-IDENTITY:'+name)

def receipt_correspondence(out,bundle):
 """Standalone receipt uses contract.enc: sorted ASCII JSON plus one LF.
 No mutation or normalization is written back to either input.
 """
 raw=c.read(Path(out)/'count-receipt.json');saved=c.parse(raw)
 c.need(c.enc(saved)==raw,'COUNT-RECEIPT-SERIALIZATION')
 c.need(c.enc(bundle['evidence_count_receipt'])==raw,'EMBEDDED-COUNT-RECEIPT')
 return c.ident(raw)

def recover(dest):
 pins();dest=Path(dest);c.need(not dest.exists(),'RECOVERY-EXISTS');dest.mkdir(parents=True)
 for role in ['candidate','draft']:
  raw=c.read(P/'inputs'/f'{role}.zip');data=c.archive(raw,c.ident(raw),'RECOVERY-MANIFEST.json');expected=c.parse(data.pop('RECOVERY-MANIFEST.json'))
  root=dest/role;root.mkdir()
  for n,b in data.items():
   f=root/n;f.parent.mkdir(parents=True,exist_ok=True)
   with f.open('xb') as out:out.write(b)
  tree(root,expected)
 c.write(dest/'recovery.json',{'status':'PASS exact source recovery','roots':{role:c.ident(c.read(P/'inputs'/f'{role}.zip')) for role in ['candidate','draft']},'execution':'none'})

def load_sources(roots):
 bindings=pins();roots=Path(roots).resolve();root=roots/'candidate';draft=roots/'draft'
 for role in ['candidate','draft']:
  with __import__('zipfile').ZipFile(P/'inputs'/f'{role}.zip') as z:expected=c.parse(z.read('RECOVERY-MANIFEST.json'))
  tree(roots/role,expected)
 sys.path[:0]=[str(root/'support/code'),str(root/'compiler'),str(root/'integration'),str(draft/'source-only/universe/code')]
 locations={'common':root/'support/code/common.py','ingest':root/'support/code/ingest.py','compiler':root/'compiler/compiler.py','semantic':root/'compiler/semantic.py','prospective_procedure':root/'compiler/prospective_procedure.py','universe':draft/'source-only/universe/code/universe.py'}
 for name,path in locations.items():
  m=importlib.import_module(name);c.same(str(Path(m.__file__).resolve()),str(path.resolve()),'MIXED-ROOT:'+name)
 import semantic
 candidate=semantic.setup(root)
 return root,draft,candidate,bindings

def acquire_contract():
 pin=c.parse(c.read(P/'provenance/target-pin.json'));a=c.archive(c.read(P/'inputs/target-acquisition.zip'),pin['archive']);lineage=c.target(a,pin)
 return pin,a,lineage

def obligation_check(value):
 expected=c.parse(c.read(P/'inputs/obligations.json'));c.same(value,expected,'EXACT-ELEVEN-OBLIGATIONS')
 c.same([r['id'] for r in value['source_only']],['O%02d'%n for n in range(1,12)],'ELEVEN-OBLIGATIONS')

def evaluate(roots,out):
 start=time.monotonic();out=Path(out).resolve();c.need(not out.exists(),'OUTPUT-EXISTS');c.need(not out.is_relative_to(Path(roots).resolve()),'PROTECTED-OUTPUT');out.mkdir(parents=True)
 try:
  print('1/6 authenticating source roots and acquisition contract',flush=True)
  root,draft,candidate,components=load_sources(roots);pin,a,lineage=acquire_contract()
  import common,ingest,prospective_procedure as pp,universe
  import adapted_evidence_counts as counts,adapted_finite_inputs as finite,adapted_consumer as consumer,adapted_verify_finite as verifier,adapted_ledger as ledger,adapted_multiplicity as expressions
  export=common.parse(a['export.json'],200000000);fold=ingest.validate_export(export)
  c.same(fold,c.parse(a['authenticated-export-validation.json']),'SAVED-FOLD-CORRESPONDENCE')
  c.same(fold['binding'],pin['binding'],'FOLD-TARGET-BINDING')
  c.write(out/'contract.json',lineage);c.write(out/'authenticated-fold.json',fold)
  d=c.parse(c.read(root/'layout_outputs/directory.json'));r=c.parse(c.read(root/'layout_outputs/rules.json'));proc=c.parse(c.read(root/'layout_outputs/procedure.json'));u=c.parse(c.read(draft/'source-only/universe/outputs/universe.json'))
  obligations=c.parse(c.read(P/'inputs/obligations.json'));obligation_check(obligations)
  evaluation={};aid=pin['acquisition_id'];evaluation_id=aid+'-offline-contract-v1'
  print('2/6 deriving exact projections and procedure duties for both symbolic contexts',flush=True)
  for ctx in c.CONTEXTS:
   occ=candidate.ingest(export,ctx,candidate.binding)
   duty=pp.consume(proc,d,r,occ,export)
   link={'acquisition_id':aid,'context':ctx,'cross_acquisition_joins':False,'acquisition_archive':pin['archive'],'export':c.ident(a['export.json']),'target_binding':pin['binding'],'ownership_incarnation':pin['incarnation'],'occurrence':c.ident(common.enc(occ)),'procedure':c.ident(common.enc(duty)),'execution':'fresh offline derivation; not historical execution evidence'}
   for name,value in [('occurrences.json',occ),('procedure-result.json',duty),('lineage.json',link)]:
    raw=common.enc(value);evaluation[ctx+'/'+name]=raw;c.write(out/'projection'/ctx/name,value)
   print(ctx+': '+str(duty['finite_tokens'])+' tokens; '+str(duty['finite_structural_pairs'])+' structural pairs; '+str(duty['finite_semantic_pairs'])+' semantic pairs',flush=True)
  basis={'acquisition_id':aid,'evaluation_id':evaluation_id,'parent_git_commit':'38031f66e44c090d09a9cc48fd1bbf37e704815c','archives':{'acquisition':{'path':'inputs/target-acquisition.zip',**pin['archive']},'evaluation':{'path':'projection/','bytes':sum(len(v) for v in evaluation.values()),'sha256':c.ident(c.enc({n:c.ident(v) for n,v in sorted(evaluation.items())}))['sha256']}},'evaluation_identity_kind':'exact derived member map; not an acquired archive','target':lineage}
  i={'root':root,'draft':draft,'basis':basis,'archives':{'acquisition':a,'evaluation':evaluation},'directory':d,'rules':r,'procedure':proc,'universe':u,'obligations':obligations,'component_bindings':components}
  receipt,records=counts._claims(i)
  receipt['target_evidence']=copy.deepcopy(lineage)
  consumed=universe.count_acquisition_bag(root,u,records)
  c.same(consumed['counts'],{k:v for row in records for k,v in row['counts'].items()},'COUNT-CONSERVATION')
  c.need(consumed['production_complete'] is False and consumed['full_expansion_ready'] is False,'COUNT-UNKNOWN')
  c.write(out/'count-receipt.json',receipt);c.write(out/'count-consumption.json',consumed)
  print('3/6 deriving finite inputs and representation through pinned pure lookup',flush=True)
  bundle=finite._derive(i,receipt);bundle['bindings']['target_acquisition']={'archive':pin['archive'],'export':c.ident(a['export.json']),'contract':c.ident(c.read(out/'contract.json')),'binding':pin['binding'],'incarnation':pin['incarnation']}
  native_consumption=finite._consume(bundle)
  receipt_correspondence(out,bundle)
  c.write(out/'bundle.json',bundle);bid=c.ident(c.read(out/'bundle.json'));component=c.ident(c.read(P/'provenance/component-pins.json'))
  native=consumer.representation(bundle,consumer.construct(bundle,pp.lookup()),bid,component)
  c.write(out/'native.json',native)
  print('4/6 independent structural verification and mechanical ledger derivation',flush=True)
  verification=verifier.check(native,bundle,bid,component);verification['submitted']=c.ident(c.read(out/'native.json'));c.write(out/'verification.json',verification)
  source_contract={'duty_names':pp.duty_names(),'sources':{n:c.ident(c.read(root/('compiler/'+n if n=='prospective_procedure.py' else 'native/code/'+n))) for n in ['bind_ledger.py','prospective_procedure.py','expand_candidate.py']}}
  mechanical=ledger.derive(native,verification['submitted'],verification,source_contract);c.write(out/'ledger.json',mechanical)
  summary=ledger.summary(mechanical);summary['ledger']=c.ident(c.read(out/'ledger.json'));c.write(out/'ledger-result.json',summary)
  print('5/6 binding carrier lineage and evaluating source-derived expressions',flush=True)
  carrier={'acquisition_id':aid,'carrier_dispositions':[{'source_contract':x} for x in u['protected_carriers']]}
  definitions=expressions.compile_expressions(carrier,root);values=expressions.evaluate(definitions,export,carrier)
  copy_receipt={'acquisition_id':aid,'acquisition_archive':pin['archive'],'contract':lineage,'projection_members':{n:c.ident(v) for n,v in sorted(evaluation.items())},'selected_database_payloads':{n:c.ident(a['databases/'+n]) for n in ['ownership.sqlite','session.sqlite']},'selected_database_payload_bytes':sum(len(a['databases/'+n]) for n in ['ownership.sqlite','session.sqlite']),'byte_scope':'two database payload members only; no physical copy or context multiplier','contexts':c.CONTEXTS,'obligations':obligations,'physical_container_count':'UNKNOWN','physical_storage_bytes':'UNKNOWN','global_lifetime_bound':'UNKNOWN','operational_assurance':False}
  c.write(out/'carrier-copy.json',copy_receipt)
  expression_result={'acquisition_id':aid,'export':c.ident(a['export.json']),'copy_receipt':c.ident(c.read(out/'carrier-copy.json')),'contexts':c.CONTEXTS,'expressions':values,'obligations':obligations,'classification':'UNKNOWN','inventory_unknowns':sum(x['selected']['value'] is None for x in values),'lifetime_unknowns':sum(x['lifetime']['value'] is None for x in values),'context_use':'references to same acquisition; never physical multipliers','global_O06_closed':False,'global_O09_closed':False}
  c.write(out/'carrier-expressions.json',expression_result)
  print('6/6 sealing acquisition-specific output identities',flush=True)
  for obj in [bundle,native,mechanical]:obligation_check(obj['obligations']);c.need(obj['classification']=='UNKNOWN' and obj['final_binding']=='BLOCKED' and obj['actual_admission'] is False,'NO-ESCALATION')
  c.same(expression_result['inventory_unknowns'],4,'INVENTORY-UNKNOWNS');c.same(expression_result['lifetime_unknowns'],14,'LIFETIME-UNKNOWNS')
  result={'status':'PASS bounded offline target evaluation; independent review pending','acquisition_id':aid,'acquisition':pin['archive'],'export':c.ident(a['export.json']),'components':component,'contexts':verification['contexts'],'native_consumption':native_consumption,'assessment':'SOURCE-ONLY','classification':'UNKNOWN','obligations':[x['id'] for x in obligations['source_only']],'inventory_unknowns':4,'lifetime_unknowns':14,'factual_history':'UNKNOWN','history_cutoff':'UNKNOWN','global_lifetime_bound':None,'production_cardinalities':None,'readiness':'BLOCKED','final_binding':'BLOCKED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','actual_admission':False,'cross_acquisition_joins':False,'database_connections':0,'session_operations':0,'new_requests':0,'evaluation_time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':platform.python_version(),'cryptography':__import__('cryptography').__version__,'seconds':time.monotonic()-start}
  c.write(out/'RESULT.json',result)
  c.write(out/'OUTPUT-MANIFEST.json',{p.relative_to(out).as_posix():c.ident(c.read(p)) for p in sorted(out.rglob('*')) if p.is_file()})
  print('PASS bounded offline chain; all blockers retained',flush=True)
 except BaseException:
  (out/'failure.txt').write_text(traceback.format_exc());raise

def validate_outputs(roots,out):
 """Fresh-process validation of sealed output bytes, explicit links and pure verification.
 Does not rerun projection, construction, ledger construction or any completed review.
 """
 components=pins()
 for role in ['candidate','draft']:
  with __import__('zipfile').ZipFile(P/'inputs'/f'{role}.zip') as z:tree(Path(roots)/role,c.parse(z.read('RECOVERY-MANIFEST.json')))
 pin,a,lineage=acquire_contract();out=Path(out)
 manifest=c.parse(c.read(P/'provenance/evaluation-pins.json'));tree(out,manifest)
 c.same(c.parse(c.read(out/'contract.json')),lineage,'OUTPUT-CONTRACT')
 import adapted_verify_finite as v,adapted_ledger as l
 bundle=c.parse(c.read(out/'bundle.json'));native=c.parse(c.read(out/'native.json'));ledger=c.parse(c.read(out/'ledger.json'))
 receipt_correspondence(out,bundle)
 c.same(bundle['acquisition_id'],pin['acquisition_id'],'OUTPUT-ACQUISITION');c.same(bundle['export_exact_bytes_hex'],a['export.json'].hex(),'OUTPUT-EXPORT');c.same(bundle['export_identity'],c.ident(a['export.json']),'OUTPUT-EXPORT-ID')
 for obj in [bundle,native,ledger]:obligation_check(obj['obligations'])
 checked=v.check(native,bundle,c.ident(c.read(out/'bundle.json')),c.ident(c.read(P/'provenance/component-pins.json')));checked['submitted']=c.ident(c.read(out/'native.json'))
 c.same(checked,c.parse(c.read(out/'verification.json')),'VERIFICATION-CORRESPONDENCE');c.same(ledger['verification_receipt'],checked,'LEDGER-VERIFICATION')
 summary=l.summary(ledger);summary['ledger']=c.ident(c.read(out/'ledger.json'));c.same(summary,c.parse(c.read(out/'ledger-result.json')),'SUMMARY-SUBSTITUTION')
 # Root membership was checked before any candidate/output consumption; no candidate constructors execute here.
 return {'status':'PASS sealed outputs, target bindings, pure finite verification and exact recovered roots','contexts':checked['contexts'],'evaluation_rerun':False,'review_rerun':False,'database_connections':0}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['recover','evaluate','validate']);ap.add_argument('--roots',required=True);ap.add_argument('--output');args=ap.parse_args();sys.addaudithook(denied)
 if args.action=='recover':recover(args.roots)
 elif args.action=='evaluate':evaluate(args.roots,args.output)
 else:print(c.enc(validate_outputs(args.roots,args.output)).decode())
if __name__=='__main__':main()
