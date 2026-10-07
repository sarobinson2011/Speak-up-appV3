"""Pause after two source segments, then resume and compare all populated data."""
import hashlib,json,subprocess,sys,time
from pathlib import Path
from ledger_kernel.retained import ROOT,sha

def main():
    work=ROOT/'work/inventory-recovery';out=ROOT/'results/inventory-recovery';out.mkdir(parents=True,exist_ok=False)
    assert not work.exists(),'fresh recovery workspace required'
    rows=[]
    for name,args,expected in [('pause',['--stop-after','2'],3),('resume',[],0)]:
        t=time.monotonic();cmd=[sys.executable,'-m','ledger_kernel.inventory','build','--output',str(work),'--seconds','150',*args]
        with (out/(name+'.log')).open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,cwd=ROOT,timeout=170)
        assert r.returncode==expected
        state=json.loads((work/'construction-state.json').read_bytes())
        rows.append({'operation':name,'command':cmd,'exit_code':r.returncode,'seconds':time.monotonic()-t,'committed_segments':len(state['completed'])})
        if name=='pause':assert len(state['completed'])==2
    paths=['node-duties.jsonl','structural-duties.jsonl','potential-domain.json','governing-slots.json','required-security-duties.json']
    hashes={p:sha(work/p) for p in paths};assert hashes=={p:sha(ROOT/'ledger_data'/p) for p in paths}
    result={'result':'PASS','runs':rows,'resumed_files_equal_uninterrupted':hashes,'full_pair_or_link_stream_executed':False,'profile_admitted':False}
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
