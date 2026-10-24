"""Focused CF-01 full-chain fault injection; all original stage commands execute."""
import argparse,importlib.util,pathlib,traceback

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--connect',required=True);ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 path=pathlib.Path(a.connect).absolute();s=importlib.util.spec_from_file_location('corrected_full',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 out=pathlib.Path(a.output).absolute();out.mkdir(parents=True,exist_ok=False);source=m.ident(m.read(path));config=m.load(a.config);original=m.stage
 def injected(output,name,script,args):
  original(output,name,script,args)
  if name=='04-ledger':
   p=output/name/'result.json';raw=m.read(p);v=m.parse(raw)
   assert v['contexts'][0]['node_duties']==9339
   m.write(out/'mutation.json',{'field':'contexts[0].node_duties','before':9339,'after':0,'original_summary':m.ident(raw),'ledger':m.ident(m.read(output/name/'ledger.json'))})
   (out/'original-summary.json').write_bytes(raw);v['contexts'][0]['node_duties']=0;p.write_bytes(m.enc(v)+b'\n')
 m.stage=injected
 try:
  try:m.run(config,out/'chain')
  except m.Rejected as e:
   assert str(e)=='LEDGER-RESULT-CORRESPONDENCE',str(e)
  else:raise AssertionError('CF-01 WAS ACCEPTED')
  executions=[m.load(out/'chain'/(n+'-execution.json')) for n in ['01-inputs','02-consumer','03-verification','04-ledger']]
  assert all(x['returncode']==0 for x in executions) and not (out/'chain/receipt.json').exists()
  assert m.ident(m.read(path))==source
  ledger=m.load(out/'chain/04-ledger/ledger.json');assert len(ledger['contexts'][0]['node_duties'])==9339
  assert m.read(out/'chain/04-ledger/ledger.json')==m.read(config['saved_ledger'])
  m.write(out/'result.json',{'status':'PASS full public-run witness rejection','reason':'LEDGER-RESULT-CORRESPONDENCE','all_four_actual_stages_executed':True,'final_receipt_written':False,'actual_node_duties':9339,'injected_summary_count':0,'code_unchanged':source,'executions':executions,'scope':'Constructed fault injection after real stage completion; no corruption claimed on Steve host'})
  print('PASS CF-01 rejected after four real stages; no final receipt',flush=True)
 except BaseException:
  (out/'harness-failure.txt').write_text(traceback.format_exc());raise
if __name__=='__main__':main()
