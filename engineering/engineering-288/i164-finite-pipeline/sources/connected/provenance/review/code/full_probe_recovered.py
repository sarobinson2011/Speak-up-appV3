import copy,hashlib,importlib.util,json,shutil,stat,sys,traceback
from pathlib import Path
W=Path(__file__).resolve().parents[2];R=W/'cf-review';s=importlib.util.spec_from_file_location('cf',W/'cf-recovered/code/connect.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
c=m.load(R/'config.json')
original=m.stage
# Reviewer fault injection: all original stage functions execute unmodified.
# Change only a generated summary after the actual ledger stage has succeeded.
def observe(output,name,script,args):
 original(output,name,script,args)
 if name=='04-ledger':
  p=output/name/'result.json';raw=m.read(p);(R/'results/original-ledger-result.json').write_bytes(raw)
  value=m.parse(raw);assert value['contexts'][0]['node_duties']==9339
  value['contexts'][0]['node_duties']=0;p.write_bytes(m.enc(value)+b'\n')
  m.write(R/'results/injected-change.json',{'path':'04-ledger/result.json','field':'contexts[0].node_duties','before':9339,'after':0,'original':m.ident(raw),'altered':m.ident(m.read(p)),'implementation_modified':False})
m.stage=observe
try:
 receipt=m.run(c,R/'results/fault-chain-2')
 assert receipt['outputs']['ledger_contexts'][0]['node_duties']==0
 m.write(R/'results/witness.json',{'finding':'CF-01','public_run_accepted_altered_intermediate_summary':True,'reported_node_duties':0,'actual_node_duties':9339,'all_four_real_stages_executed':True,'receipt':m.ident(m.read(R/'results/fault-chain-2/receipt.json'))})
 print('WITNESS: public run accepted false ledger node-duty count',flush=True)
except BaseException:
 (R/'failures/probe.txt').write_text(traceback.format_exc());raise
