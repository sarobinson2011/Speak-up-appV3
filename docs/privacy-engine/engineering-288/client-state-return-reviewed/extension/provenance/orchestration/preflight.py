import ast,json,runpy,types
from pathlib import Path
r=Path(__file__).resolve().parents[1]/'client-state-return';runpy.run_path(str(r/'tests/guard.py'))['install'](r)
p=r/'code/correspondence.py';m=types.ModuleType('_preflight');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__)
d=m.inputs(r);cat=m.catalogue(d);c=d['coverage'];assert c.validate_client_state(*m.sources(d),m.manager_state(d),d['prior_module'].catalogue(d['prior_data']),m.inner(d)['ctx']['binding'],cat)
result={'source_catalogue':'PASS','normal_hops':cat['ordered_hops'],'source_pins':cat['source']['sources'],'state_keys':cat['source']['state_keys'],'data_primitive_types':cat['source']['data_primitives'],'runtime_operations':0}
(r/'results/source-preflight.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
