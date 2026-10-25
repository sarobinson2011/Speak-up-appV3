"""Additional derived-linkage controls; consumes the successful new public result."""
import argparse,importlib.util,pathlib,copy,json
ap=argparse.ArgumentParser();ap.add_argument('--code',required=True);ap.add_argument('--config',required=True);ap.add_argument('--receipt',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
s=importlib.util.spec_from_file_location('inventory_tested',a.code);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
c=m.parse(m.read(a.config));r=m.parse(m.read(a.receipt));raw=m.read(c['inventory_archive']);prior=m.read(c['expression_receipt']);expected=m._attach(r['evaluation'],m.inventory(raw),raw,prior);m.same(expected,r,'PREREQUISITE-RECEIPT');results=[]
for role in ('ledger','model','source_only'):
 m.same([x['id'] for x in r['obligations'][role]],['O%02d'%i for i in range(1,12)],'ELEVEN-OBLIGATIONS')
for i in range(11):
 x=copy.deepcopy(r)
 for role in ('ledger','model','source_only'):x['obligations'][role].pop(i)
 try:m.same(expected,x,'OBLIGATION-CONTINUITY')
 except ValueError:results.append({'name':'coordinated-omission-O%02d'%(i+1),'status':'REJECTED'})
 else:raise AssertionError('ACCEPTED')
for i in range(14):
 x=copy.deepcopy(r);x['evaluation']['expressions'][i]['lifetime'].update(value=0,status='FINITE')
 try:m.same(expected,x,'LIFETIME-CONTINUITY')
 except ValueError:results.append({'name':'lifetime-zero-'+str(i),'status':'REJECTED'})
 else:raise AssertionError('ACCEPTED')
# All copy links preserve two records and do not invent physical/invocation facts.
by={x['record_id']:x for x in r['inventory_records']}
for x in by.values():
 if x['copy_of']:
  m.need(x['copy_of'] in by and x['record_id']!=x['copy_of'],'COPY-ENDPOINT');m.same(x['identity'],by[x['copy_of']]['identity'],'COPY-IDENTITY');m.need(x['adds_invocation'] is False and x['runtime_invocation_id'] is None,'COPY-NOT-INVOCATION')
results.append({'name':'all-copy-links-preserve-distinct-records','status':'PASS'})
p=pathlib.Path(a.output);p.mkdir(parents=True,exist_ok=False);(p/'results.json').write_bytes(m.enc({'status':'PASS','controls':len(results),'scope':'constructed derived-linkage checks, not additional public evaluator runs','results':results})+b'\n');print('PASS',len(results))
