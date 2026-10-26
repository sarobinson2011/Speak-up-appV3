"""Focused adaptation controls only; no completed review or historical pipeline rerun."""
import argparse,copy,json,sys,traceback
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import evaluate as e
c=e.c
rows=[]
def accept(name,fn):
 fn();rows.append({'name':name,'status':'PASS','expected':'accept'})
def reject(name,fn):
 try:fn()
 except (ValueError,KeyError,TypeError,RuntimeError) as ex:rows.append({'name':name,'status':'PASS','expected':'reject','reason':str(ex)})
 else:raise AssertionError('UNREJECTED:'+name)
def changed(a,n,fn):
 b=dict(a);v=c.parse(b[n]);fn(v);b[n]=c.enc(v);return b

def contract_controls(roots):
 e.pins();pin,a,lineage=e.acquire_contract()
 accept('exact nine-record quiescent acquisition',lambda:c.target(a,pin))
 oldraw=c.read(e.P/'inputs/legacy-acquisition.zip');old=c.archive(oldraw,{'bytes':70665,'sha256':'554d27a0c5eb5d97c762eb082001930be9317c8f317ea62759557d01727177a4'})
 aid='I164-snapshot-acquisition-egpf25d9'
 accept('legacy two-database saved-head contract',lambda:c.legacy(old,aid))
 tests=[('missing ninth record','source-before.json',lambda x:x.pop(next(iter(x)))),('changing metadata','source-after.json',lambda x:x['confirmed-close.json']['metadata'].__setitem__(6,0)),('mixed lineage acquisition','locked-copy.json',lambda x:x['lineage'][0].update(acquisition_id=aid)),('conflicting lineage source','locked-copy.json',lambda x:x['lineage'][0].update(source_path='/elsewhere')),('duplicate lineage','locked-copy.json',lambda x:x['lineage'].append(x['lineage'][0])),('wrong copy member','locked-copy.json',lambda x:x['lineage'][0].update(copy_member='records/wrong')),('stale target acquisition','RESULT.json',lambda x:x.update(acquisition_id=aid)),('guard changes','locked-copy.json',lambda x:x['guard_after'].clear()),('wrong session export','export.json',lambda x:x['config'].update(session='I164-lab-session-001'))]
 for name,n,fn in tests:reject(name,lambda n=n,fn=fn:c.target(changed(a,n,fn),pin))
 reject('missing copy payload',lambda:c.target({k:v for k,v in a.items() if k!='databases/ownership.sqlite'},pin))
 reject('unexpected records entry',lambda:c.target({**a,'records/extra.json':b'{}'},pin))
 reject('summary substituted for source evidence',lambda:c.target({'RESULT.json':a['RESULT.json']},pin))
 reject('old export mixed with target',lambda:c.target({**a,'export.json':old['export.json']},pin))
 reject('missing old saved request',lambda:c.legacy({k:v for k,v in old.items() if k!='saved-head/request.bin'},aid))
 reject('legacy missing database identity',lambda:c.legacy(changed(old,'database-identities-before.json',lambda x:x.pop('session.sqlite')),aid))
 reject('legacy saved response omission',lambda:c.legacy(changed(old,'export.json',lambda x:x['journal'][0].__setitem__(2,None)),aid))
 export=c.parse(a['export.json']);accept('empty journal needs no request triad',lambda:c.request_evidence(a,export))
 reject('partial saved request triad',lambda:c.request_evidence({**a,'saved-head/request.bin':old['saved-head/request.bin']},export))
 legacy_export=c.parse(old['export.json']);row=copy.deepcopy(legacy_export['journal'][0]);row[1]=''
 reject('actual request missing wire bytes',lambda:c.request_evidence({},dict(legacy_export,journal=[row])))
 row=copy.deepcopy(legacy_export['journal'][0]);row[2]=None
 accept('schema permits unanswered request with exact packet',lambda:c.request_evidence({},dict(legacy_export,journal=[row])))
 e.load_sources(roots)
 import ingest
 accept('actual target authenticated export',lambda:ingest.validate_export(export))
 accept('actual legacy authenticated export',lambda:ingest.validate_export(legacy_export))
 b=copy.deepcopy(legacy_export);b['journal'][0][1]='';reject('schema rejects missing actual signed request',lambda:ingest.validate_export(b))
 b=copy.deepcopy(legacy_export);packet=c.parse(bytes.fromhex(b['journal'][0][1]));packet['request']['session']='wrong';b['journal'][0][1]=c.enc(packet).hex();reject('schema rejects conflicting session request',lambda:ingest.validate_export(b))
 b=copy.deepcopy(legacy_export);b['journal'][0][2]='';reject('schema rejects empty supplied response',lambda:ingest.validate_export(b))
 # Existing event fixture bytes, inspected for focused missing-request edge only.
 fixtures=list((Path(roots)/'candidate/support/fixtures').glob('*.json'))
 chosen=None
 for f in fixtures:
  v=c.parse(c.read(f))
  if isinstance(v,dict) and v.get('events') and v.get('journal'):chosen=v;break
 c.need(chosen is not None,'EVENT-CONTROL-FIXTURE')
 chosen=copy.deepcopy(chosen);chosen['journal']=[]
 reject('event requires a retained actual request',lambda:ingest.validate_export(chosen))
 reject('database audit denial',lambda:__import__('sqlite3').connect(':memory:'))
 return rows

def output_controls(out):
 e.pins();out=Path(out)
 import adapted_verify_finite as v,adapted_ledger as ledger
 b=c.parse(c.read(out/'bundle.json'));n=c.parse(c.read(out/'native.json'));bid=c.ident(c.read(out/'bundle.json'));cid=c.ident(c.read(e.P/'provenance/component-pins.json'))
 accept('fresh actual representation structural verification',lambda:v.check(n,b,bid,cid))
 def mutate(fn):x=copy.deepcopy(n);fn(x);return x
 cases=[('stale bundle pin',lambda x:x.update(source_bundle_sha256='0'*64)),('mixed acquisition identity',lambda x:x.update(acquisition_id='I164-snapshot-acquisition-egpf25d9')),('cross acquisition occurrence',lambda x:x['contexts'][0]['occurrences'][0]['key'].__setitem__(0,'I164-snapshot-acquisition-egpf25d9')),('missing context',lambda x:x['contexts'].pop()),('summary in place of occurrences',lambda x:x['contexts'][0].update(occurrences=[])),('drop obligation',lambda x:x['obligations']['source_only'].pop()),('promote classification',lambda x:x.update(classification='QUALIFIED')),('admission escalation',lambda x:x.update(actual_admission=True)),('wrong finite edge endpoint',lambda x:x['contexts'][0]['ordered_edges'][0].update(target_index=999999)),('alter exact occurrence bytes',lambda x:x['contexts'][0]['occurrences'][0].update(payload_hex='00'))]
 for name,fn in cases:reject(name,lambda fn=fn:v.check(mutate(fn),b,bid,cid))
 mechanical=c.parse(c.read(out/'ledger.json'));expected=ledger.summary(mechanical);expected['ledger']=c.ident(c.read(out/'ledger.json'));summary=c.parse(c.read(out/'ledger-result.json'))
 accept('ledger summary derived from exact ledger',lambda:c.same(summary,expected,'SUMMARY'))
 summary['contexts'][0]['token_members']+=1;reject('coordinated summary substitution',lambda:c.same(summary,expected,'SUMMARY'))
 expr=c.parse(c.read(out/'carrier-expressions.json'));accept('four inventory unknowns and fourteen lifetime unknowns',lambda:c.same([sum(x['selected']['value'] is None for x in expr['expressions']),sum(x['lifetime']['value'] is None for x in expr['expressions'])],[4,14],'UNKNOWNS'))
 accept('eleven exact obligations in carrier output',lambda:e.obligation_check(expr['obligations']))
 return rows
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('kind',choices=['contract','outputs']);ap.add_argument('--roots');ap.add_argument('--evaluation');ap.add_argument('--result',required=True);args=ap.parse_args();sys.addaudithook(e.denied)
 try:
  result=contract_controls(args.roots) if args.kind=='contract' else output_controls(args.evaluation)
  c.write(args.result,{'status':'PASS focused adaptation controls','controls':result,'count':len(result),'completed_review_rerun':False});print('PASS',len(result),'focused controls')
 except BaseException:
  c.write(args.result,{'status':'FAIL','completed':rows,'failure':traceback.format_exc()});raise
