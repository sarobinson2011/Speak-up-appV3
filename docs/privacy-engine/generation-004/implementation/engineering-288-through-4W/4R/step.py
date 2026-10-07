"""One bounded generation/replay slice through unmodified retained 4A controller."""
import argparse,importlib.util,json,resource,sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('operation',choices=['generate','replay']);p.add_argument('--descriptor',type=Path,required=True);p.add_argument('--job',type=Path,required=True);p.add_argument('--candidates',type=int,required=True);p.add_argument('--seconds',type=float,required=True);a=p.parse_args()
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
s=importlib.util.spec_from_file_location('retained',ROOT/'runner/run.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
if a.operation=='generate':result=r.run(a.descriptor,a.job,max_segments=1,segment_candidates=a.candidates,budget=a.seconds,execute_full=True)
else:result=r.verify(a.descriptor,a.job,budget=a.seconds,max_segments=1)
print(json.dumps(result))
