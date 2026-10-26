"""New binding controls, no backend/session/lifecycle execution."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]


def main():
    out=Path(sys.argv[1]).absolute();out.mkdir(parents=True,exist_ok=False)
    spec=importlib.util.spec_from_file_location('status_correspondence',ROOT/'code/correspondence.py')
    c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
    raw=(ROOT/'provenance/status-correspondence.json').read_bytes();base=json.loads(raw)
    checks=[];processes=[]
    def need(ok,label):
        if not ok:raise AssertionError(label)
        checks.append(label)
    def rejects(b,label,root=ROOT):
        try:c.validate(root,b)
        except (ValueError,RuntimeError):checks.append(label)
        else:raise AssertionError(label)
    need(c.validate(ROOT,raw)['result']=='PASS','legitimate exact serialized binding')
    need(base['contexts'][0]['site_ids']==base['contexts'][1]['site_ids'],'both contexts cover all affected sites')
    for name,change in [
      ('contract',lambda x:x['contract'].update(sha256='0'*64)),
      ('decision',lambda x:x['adoption'].update(sha256='0'*64)),
      ('entry',lambda x:x['entry'].update(sha256='0'*64)),
      ('omitted-site',lambda x:x['sites'].pop()),
      ('omitted-context',lambda x:x['contexts'].pop()),
      ('context-substitution',lambda x:x['contexts'][1].update(context='SYMBOLIC-U-ONE')),
      ('missing-relation',lambda x:x['contexts'][0]['relationships'].pop()),
      ('missing-inherited-join',lambda x:x['contexts'][1]['inherited_requirements'].pop()),
      ('invented-multiplicity',lambda x:x['contexts'][0].update(multiplicity=1)),
      ('invented-historical-frames',lambda x:x['occurrence_contract'].update(historical_launcher_frames='COMPLETE')),
      ('upgraded-classification',lambda x:x['contexts'][0].update(classification='PUBLIC')),
      ('upgraded-admission',lambda x:x['limits'].update(actual_admission=True)),
    ]:
        x=copy.deepcopy(base);change(x);rejects(c.enc(x),'reject '+name)
    rejects(json.dumps(base,indent=2).encode(),'reject alternate serialization')
    rejects(c.enc({'summary':'all fine'}),'reject summary substitution')
    root=out/'recovered-root'
    for name in ('code','contract','retained','basis','provenance'):
        shutil.copytree(ROOT/name,root/name)
    need(c.validate(root,raw)['result']=='PASS','recovered root reproduces exact binding')
    for name,relative in [('new-entry','code/prospective_entry.py'),('historical-launcher','retained/launcher/code/lab_bootstrap.py'),('inherited-model','basis/candidate/managed-route/model.json')]:
        p=root/relative;original=p.read_bytes();p.write_bytes(original+b'\n')
        rejects(raw,'reject changed '+name,root)
        p.write_bytes(original)  # Restore only this disposable mutation fixture.
    for label,path in [('fresh',ROOT),('recovered',root)]:
        args=[sys.executable,'-I','-B',str(path/'code/correspondence.py'),'check',str(path/'provenance/status-correspondence.json')]
        r=subprocess.run(args,capture_output=True,text=True,timeout=30)
        (out/(label+'.stdout')).write_text(r.stdout);(out/(label+'.stderr')).write_text(r.stderr)
        processes.append({'label':label,'command':args,'returncode':r.returncode})
        need(r.returncode==0 and json.loads(r.stdout)['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],label+' process exact validation')
    result={'result':'PASS','checks':checks,'count':len(checks),'processes':processes,'saved_binding':c.identity(raw),'backend_execution':False,'qualification':False}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'result':'PASS','checks':len(checks),'processes':len(processes)}))


if __name__=='__main__':main()
