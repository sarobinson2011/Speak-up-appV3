"""Focused prospective profile and source-extracted primitive controls; no databases."""
import argparse,ast,base64,copy,hashlib,importlib.util,json,os,shutil,subprocess,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def need(ok,label):
 if not ok:raise AssertionError(label)
def main():
 a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);a.add_argument('--fresh-only',action='store_true');args=a.parse_args();out=args.output.absolute()
 need(not out.exists() and not str(out).startswith('/tmp/'),'NEW-PERSISTENT-OUTPUT');out.mkdir(parents=True)
 results=[]
 def blocked(label,fn):
  try:fn()
  except Exception as e:results.append({'case':label,'result':'rejected','exception':type(e).__name__,'reason':str(e)})
  else:raise AssertionError('Negative accepted: '+label)
 def passed(label,fn):fn();results.append({'case':label,'result':'PASS'})
 def no_db(event,arguments):
  if event=='sqlite3.connect':raise AssertionError('DATABASE-CONNECTION')
 sys.addaudithook(no_db)
 try:
  g=load(ROOT/'code/environment5002.py','tested_environment5002');l=load(ROOT/'code/lab_bootstrap.py','tested_launcher5002')
  p=g.load_profile();expected=copy.deepcopy(p['expected_environment']);prefix=p['venv_prefix']
  old=out/'old-session';old.mkdir();oldbinding={'format':'I164-LAB-BOOTSTRAP-BINDING-1','configuration':json.loads((ROOT/'provenance/configuration-41.0.7.json').read_bytes())}
  (old/'binding.json').write_text(json.dumps(oldbinding));(old/'session.sqlite').write_bytes(b'NOT A DATABASE; MUST NOT OPEN')
  before={q.name:q.read_bytes() for q in old.iterdir()}
  def enter_old():
   with l.session('unavailable-candidate','unavailable-draft','unavailable-runtime',old):raise AssertionError('OLD SESSION YIELDED')
  blocked('public new launcher rejects old session before runtime/DB',enter_old)
  need(before=={q.name:q.read_bytes() for q in old.iterdir()},'OLD-FIXTURE-PRESERVATION')
  if args.fresh_only:
   print(json.dumps(results));return
  passed('supplied exact host observation matches pinned profile',lambda:g.validate_observation(expected,prefix))
  returned=g.validate_observation(expected,prefix);returned['packages']['cryptography']['version']='41.0.7'
  passed('returned observation mutation does not affect pristine validation',lambda:g.validate_observation(expected,prefix))
  for key,value in [('python','3.12.3'),('implementation','PyPy'),('optimize',True),('machine','aarch64'),('cryptography_openssl','OpenSSL 3.1.4 24 Oct 2023'),('executable','/other/python'),('stdlib_ssl','other')]:
   x=copy.deepcopy(expected);x[key]=value;blocked('wrong '+key,lambda x=x:g.validate_observation(x,prefix))
  for package,version in [('cryptography','41.0.7'),('cryptography','50.0.1'),('cffi','2.0.0'),('pycparser','3.10')]:
   x=copy.deepcopy(expected);x['packages'][package]['version']=version;blocked('package '+package+' '+version,lambda x=x:g.validate_observation(x,prefix))
  for field in ['sha256','bytes']:
   x=copy.deepcopy(expected);x['packages']['cryptography']['build_files'][0]['identity'][field]='altered';blocked('installed '+field,lambda x=x:g.validate_observation(x,prefix))
  x=copy.deepcopy(expected);x['packages']['cryptography']['build_files'].pop();blocked('missing installed member',lambda:g.validate_observation(x,prefix))
  blocked('old environment prefix',lambda:g.validate_observation(expected,str(Path(prefix).parents[1]/'I164-python31214-01qgue5t/venv')))
  x=copy.deepcopy(expected);x['packages']['cryptography']['requires']=[];blocked('omitted requirement markers',lambda:g.validate_observation(x,prefix))
  # Real public environment gate: this assessment host is NOT the pinned Steve host.
  need(sys.prefix!=prefix,'UNEXPECTED-PINNED-HOST-IN-LOCAL-TEST')
  blocked('real current cloud host correctly refused by exact host gate',g.enforce)
  blocked('create=True refuses preexisting old directory',lambda:g.session_frontier(old,True))
  blocked('create flag integer rejected',lambda:g.session_frontier(out/'missing',1))
  passed('fresh destination frontier is admitted without creating it',lambda:g.session_frontier(out/'not-created',True));need(not (out/'not-created').exists(),'FRONTIER-WRITE')
  b={'format':'I164-LAB-BOOTSTRAP-BINDING-5002-1','configuration':json.loads((ROOT/'laboratory-configuration.json').read_bytes()),'environment_profile':g.ident(ROOT/'environment-profile.json'),'environment':expected}
  prospective=out/'prospective-metadata-fixture';prospective.mkdir();(prospective/'binding.json').write_text(json.dumps(b))
  passed('new metadata frontier accepted; not full session validation',lambda:g.session_frontier(prospective,False))
  for field in ['configuration','environment_profile','environment']:
   altered=copy.deepcopy(b);altered[field]={};(prospective/'binding.json').write_text(json.dumps(altered));blocked('mixed session '+field,lambda:g.session_frontier(prospective,False))
  # Recovered-root mutation checks, using independent pinned expectations.
  recovered=out/'recovered';shutil.copytree(ROOT,recovered,ignore=shutil.ignore_patterns('__pycache__'))
  gg=load(recovered/'code/environment5002.py','recovered_environment5002')
  passed('recovered exact profile accepted',gg.load_profile)
  cfg=recovered/'laboratory-configuration.json';original=cfg.read_bytes();cfg.write_bytes(original+b' ');blocked('altered configuration bytes',gg.load_profile);cfg.write_bytes(original)
  pp=recovered/'environment-profile.json';original=pp.read_bytes();alter=json.loads(original);alter['expected_environment']['packages']['cryptography']['version']='41.0.7';pp.write_text(json.dumps(alter));blocked('coordinated submitted profile expectation rejected by source pin',gg.load_profile);pp.write_bytes(original)
  lock=recovered/'requirements.lock';original=lock.read_bytes();lock.write_bytes(b'cryptography>=41\n');blocked('weakened dependency lock',gg.load_profile);lock.write_bytes(original)
  manifest=recovered/'provenance/runtime-layout.json';original=manifest.read_bytes();manifest.write_bytes(b'{}');blocked('stale runtime mapping',gg.load_profile);manifest.write_bytes(original)
  helper=recovered/'code/environment5002.py';original=helper.read_bytes();helper.write_bytes(original+b'\n');blocked('changed guard module before execution',lambda:load(recovered/'code/lab_bootstrap.py','badlauncher'));helper.write_bytes(original)
  # Installed RECORD checks on isolated fake package files; no installer invoked.
  from unittest.mock import patch
  site=out/'record-fixture';site.mkdir();payload=site/'module.py';payload.write_bytes(b'public fixture')
  rec=site/'fixture.dist-info/RECORD';rec.parent.mkdir()
  hashvalue=base64.urlsafe_b64encode(hashlib.sha256(payload.read_bytes()).digest()).rstrip(b'=').decode()
  rec.write_text('module.py,sha256='+hashvalue+',14\nfixture.dist-info/RECORD,,\n')
  class Distribution:
   files=[Path('fixture.dist-info/RECORD')]
   def locate_file(self,member):return site/member
  with patch.object(g.md,'distribution',return_value=Distribution()),patch.object(sys,'prefix',str(site)):
   passed('installed RECORD payload exact',g.check_installed_records)
   payload.write_bytes(b'altered fixture');blocked('installed RECORD payload substitution',g.check_installed_records)
   payload.write_bytes(b'public fixture');original=rec.read_text();rec.write_text('module.py,,\n');blocked('unhashed executable source',g.check_installed_records);rec.write_text(original)
  # Actual source functions, AST-selected so no Authority/database/module side effects.
  from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey,Ed25519PublicKey
  from cryptography.hazmat.primitives import serialization
  import importlib.metadata
  pins=json.loads((ROOT/'provenance/candidate-members.json').read_bytes())
  sources={'authority.py':'support/reference/runtime/authority.py','anchor.py':'support/reference/retained/anchor.py','correspondence.py':'support/code/correspondence.py','signed_eth.py':'support/reference/retained/signed_eth.py'}
  for name,path in sources.items():need(g.ident(ROOT/'sources'/name)==pins[path],'SOURCE-BYTES:'+name)
  ns={'hashlib':hashlib,'json':json,'Ed25519PrivateKey':Ed25519PrivateKey,'Ed25519PublicKey':Ed25519PublicKey,'serialization':serialization}
  t=ast.parse((ROOT/'sources/anchor.py').read_bytes());nodes=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='enc'];exec(compile(ast.Module(body=nodes,type_ignores=[]),'pinned anchor.enc','exec'),ns)
  t=ast.parse((ROOT/'sources/authority.py').read_bytes());nodes=[]
  for node in t.body:
   if isinstance(node,ast.FunctionDef) and node.name in ['public','sig','verify']:nodes.append(node)
   if isinstance(node,ast.Assign) and any(isinstance(x,ast.Name) and x.id in ['VERSION','SEEDS','PUB'] for x in node.targets):nodes.append(node)
  exec(compile(ast.Module(body=nodes,type_ignores=[]),'pinned authority public/sig/verify','exec'),ns)
  fixture={'session':'isolated-profile-interface-test','challenge':'a'*64,'request':{'method':'head','body':{}},'attempt':None}
  sig=ns['sig']('observer',fixture);passed('actual source Ed25519 signing and verification',lambda:ns['verify']('observer',fixture,sig))
  independent=(json.dumps(fixture,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
  Ed25519PublicKey.from_public_bytes(ns['PUB']['observer']).verify(bytes.fromhex(sig),b'I164-PROSPECTIVE-LAB-RETRY-3\0'+independent)
  need(ns['sig']('observer',fixture)==sig,'DETERMINISTIC-EXACT-SIGNATURE')
  for field in ['session','challenge','attempt','request']:
   bad=copy.deepcopy(fixture);bad[field]='substituted';blocked('authenticated '+field+' substitution',lambda bad=bad:ns['verify']('observer',bad,sig))
  blocked('wrong role',lambda:ns['verify']('server',fixture,sig))
  blocked('truncated signature',lambda:ns['verify']('observer',fixture,sig[:-2]))
  blocked('wrong signed type',lambda:ns['verify']('observer',fixture,[]))
  blocked('domain substitution',lambda:Ed25519PublicKey.from_public_bytes(ns['PUB']['observer']).verify(bytes.fromhex(sig),b'wrong\0'+independent))
  (out/'signature-fixture.json').write_text(json.dumps({'scope':'public laboratory seeds, source-extracted primitive fixture; no transaction','fixture':fixture,'message_hex':(ns['VERSION'].encode()+b'\0'+independent).hex(),'public_key_hex':ns['PUB']['observer'].hex(),'signature_hex':sig},indent=2))
  cmd=[sys.executable,'-I','-B',str(recovered/'tests/checks.py'),'--fresh-only','--output',str(out/'fresh-process')]
  r=subprocess.run(cmd,capture_output=True,text=True);(out/'fresh-process.log').write_text(r.stdout+r.stderr);need(r.returncode==0,'FRESH-PROCESS');results.append({'case':'fresh process recovered-root old-session rejection','result':'PASS'})
  report={'status':'PASS bounded local controls','controls':results,'count':len(results),'environment':g.collect(),'pinned_host_execution':'NOT EXECUTED HERE; local gate correctly rejects different host','positive_profile_check':'replay of captured exact host inventory, not attestation of current host','databases_opened':False,'persistent_session_initialized':False,'transaction_signed':False,'lab_authentication_signatures_created':True,'admission':False}
  (out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(results),'controls')
 except BaseException:
  (out/'failure.txt').write_text(traceback.format_exc());raise
if __name__=='__main__':main()
