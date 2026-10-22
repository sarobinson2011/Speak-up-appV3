import copy,json,pathlib,sys,subprocess,shutil
import construction_inputs as c
P=pathlib.Path(__file__).resolve().parents[1];root=pathlib.Path(sys.argv[1]);base=c.read_bundle(P/'outputs');work=P/'process-fixture';rows=[]
def write(v):
 if work.exists():shutil.rmtree(work)
 c.write_bundle(work,v)
def run(name):
 x=subprocess.run([sys.executable,'-B',str(P/'code/construction_inputs.py'),'--root',str(root),'--validate',str(work)],capture_output=True,text=True)
 (P/'results'/('process-'+name+'.log')).write_text(x.stdout+x.stderr)
 assert x.returncode!=0,name
 assert 'ValueError:' in x.stderr,name
 rows.append({'case':name,'status':'PASS','exit':x.returncode,'rejection':x.stderr.splitlines()[-1]})
for name,edit in [('mixed-context',lambda x:x['model-input.json']['directory_program']['contexts'].reverse()),('missing-duty',lambda x:x['ledger-input.json']['procedure_input']['relation_duties'].pop()),('detached-scope-obligation',lambda x:x['source-only-result.json']['obligations'].pop())]:
 bad=copy.deepcopy(base);edit(bad)
 vals={n:bad[n] for n in ('model-input.json','ledger-input.json')};bad['provenance.json']=c.provenance(vals,bad['source-only-result.json'])
 write(bad);run(name)
write(base);(work/'ledger-input.json').unlink();run('missing-required-file')
write(base);q=work/'extra.json';q.write_text('{}');run('unexpected-file')
(P/'results/process.json').write_text(json.dumps(rows,indent=2));print('PASS',len(rows),'fresh-process negatives')
