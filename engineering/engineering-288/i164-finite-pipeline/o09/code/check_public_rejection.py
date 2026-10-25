"""Fresh-process public entry rejects stale validator code before stage execution."""
import argparse,pathlib,shutil,subprocess,sys,json,hashlib
ap=argparse.ArgumentParser();ap.add_argument('--code-root',required=True);ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
o=pathlib.Path(a.output);o.mkdir(parents=True,exist_ok=False);root=o/'recovered-code';shutil.copytree(a.code_root,root,ignore=shutil.ignore_patterns('__pycache__'))
p=root/'code/copies.py';p.write_bytes(p.read_bytes()+b'\n# stale fixture\n')
cmd=[sys.executable,'-I','-B',str(root/'code/connect.py'),'--config',a.config,'--output',str(o/'validation')]
r=subprocess.run(cmd,capture_output=True);(o/'stdout.log').write_bytes(r.stdout);(o/'stderr.log').write_bytes(r.stderr)
assert r.returncode!=0 and b'COPY-VALIDATOR-PIN' in r.stderr
assert not (o/'validation/receipt.json').exists() and not (o/'validation/01-inputs').exists()
(o/'result.json').write_text(json.dumps({'status':'PASS public stale-code rejection before stage execution','command':cmd,'returncode':r.returncode,'final_receipt_emitted':False,'stage_executed':False},indent=2)+'\n')
print('PASS public stale-code rejection')
