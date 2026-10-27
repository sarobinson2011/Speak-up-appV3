"""Reproduce the nine preserved witnesses only; not the prior review suite."""
import json,sys,types
from pathlib import Path
R=Path(__file__).resolve().parents[1];root=R/'original' if (R/'original/inputs').exists() else R/'corrected';out=Path(sys.argv[1]) if len(sys.argv)>1 else R/'results/reproduction';out.mkdir(parents=True,exist_ok=False)
def guard(e,a):
 if e in ('sqlite3.connect','socket.connect','socket.bind'):raise AssertionError(e)
sys.addaudithook(guard)
def load():
 p=R/'original/code/smoke_occurrences.py';m=types.ModuleType('old');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
raw=(root/'results/occurrence-connection.json').read_bytes();records=[]
for label,fn in [('clear',lambda x:x.clear()),('pop',lambda x:x.pop()),('reverse',lambda x:x.reverse()),('duplicate',lambda x:x.__setitem__(1,x[0]))]:
 m=load();answer=m.validate(root,raw);fn(answer['contexts']);w=(R/'review/independent-primary'/('SOC-01-'+label)/'accepted-receipt.json').read_bytes();assert m.validate(root,w)['result']=='PASS'
 try:m.validate(root,raw)
 except ValueError:pass
 else:raise AssertionError('pristine did not reject')
 records.append({'variant':'SOC-01-'+label,'altered_accepted':True,'pristine_rejected':True,'exact_witness':m.identity(w)})
for label in ['constructor-epoch','unwatched-old-main','main-return-bool','main-invented-self-state','resume-nonboolean']:
 m=load();ctx=m.load(root);trace=(R/'review/independent-primary'/('SOC-02-'+label)/'altered-trace.json').read_bytes();ctx['e']=dict(ctx['e']);ctx['e']['evidence/execution-trace.json']=trace
 assert len(m.semantic(ctx,ctx['e'])['frames'])==18
 derived=m.enc(m.derive(ctx));assert derived==(R/'review/independent-primary'/('SOC-02-'+label)/'derived-receipt.json').read_bytes()
 records.append({'variant':'SOC-02-'+label,'semantic_accepted':True,'derived_matches_review':True,'exact_trace':m.identity(trace)})
(out/'RESULT.json').write_text(json.dumps({'result':'ALL NINE ORIGINAL WITNESSES REPRODUCED','records':records,'completed_review_suite_rerun':False},indent=2)+'\n');print('Reproduced',len(records),'original witness variants')
