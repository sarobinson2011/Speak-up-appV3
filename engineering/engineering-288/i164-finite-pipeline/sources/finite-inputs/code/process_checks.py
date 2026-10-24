"""Fresh-process serialized negatives through the complete public CLI."""
import argparse,copy,gzip,json,subprocess,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import finite_inputs as f
def main():
    ap=argparse.ArgumentParser()
    for n in ['component','root','draft','bundle','output']:ap.add_argument('--'+n,required=True,type=Path)
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False);original=f.parse(f.read(a.bundle));results=[]
    for label in ['cross-acquisition','status-escalation']:
        value=copy.deepcopy(original)
        if label=='cross-acquisition':value['contexts'][1]['semantic_pairs'][0]['from'][0]='UNAUTHORIZED-ACQUISITION'
        else:value['ledger_rebound']=True;value['full_expansion_ready']=True
        raw=f.enc(value)+b'\n';assert raw!=f.read(a.bundle)
        path=a.output/(label+'.json');path.write_bytes(raw);out=a.output/(label+'-result')
        command=[sys.executable,'-I','-B',str(Path(f.__file__).resolve()),'validate','--component',str(a.component.resolve()),'--root',str(a.root.resolve()),'--draft',str(a.draft.resolve()),'--bundle',str(path.resolve()),'--output',str(out.resolve())]
        start=time.monotonic()
        with (a.output/(label+'.log')).open('wb') as log:p=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
        text=(a.output/(label+'.log')).read_text();assert p.returncode!=0 and 'FINITE-NATIVE-INPUT-SUBSTITUTION' in text
        assert not (out/'validation.json').exists() and not (out/'bundle.json').exists()
        with gzip.open(a.output/(label+'.json.gz'),'wb') as g:g.write(raw)
        # The exact serialized mutation remains preserved compressed.
        path.unlink()
        results.append({'name':label,'status':'REJECTED','exit':p.returncode,'command':command,'seconds':time.monotonic()-start,'mutation_identity':f.ident(raw)})
        print('PASS fresh-process rejection',label,flush=True)
    (a.output/'process-results.json').write_bytes(f.enc(results)+b'\n')
if __name__=='__main__':main()
