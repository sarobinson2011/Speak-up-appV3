import json,runpy,sys,time,types,traceback
from pathlib import Path
r=Path(__file__).resolve().parents[1]/'status-forwarding';runpy.run_path(str(r/'tests/guard.py'))['install'](r)
out={'kind':'new source preflight','runtime_operations':0};start=time.monotonic()
try:
 p=r/'code/correspondence.py';m=types.ModuleType('_status_preflight');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__)
 d=m.inputs(r);cat=m.catalogue(d);assert d['coverage'].validate_status_forward(*m.sources(d),m.manager_fields(d),m.inner(d)['ctx']['binding'],cat)
 out.update(result='PASS',sources=cat['source']['sources'],hops=cat['ordered_hops'],phases=cat['source']['source_phase_literals'],owner_guard=cat['source']['owner_guard'],guard_semantics=cat['guard_semantics'])
except BaseException as e:
 out.update(result='FAIL',error=repr(e),traceback=traceback.format_exc());raise
finally:
 out['seconds']=time.monotonic()-start;(r/'results/source-preflight.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
