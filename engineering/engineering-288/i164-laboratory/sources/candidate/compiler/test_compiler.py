import sys,json,copy,time,traceback
from pathlib import Path
import compiler as m
ROOT=Path(sys.argv[1]).resolve();DEST=Path(sys.argv[2]);DEST.mkdir(exist_ok=True);checks=[]
def ok(name,b=True):
 assert b,name
 checks.append({'name':name,'result':'PASS'})
def reject(name,fn):
 try:fn()
 except (m.Invalid,ValueError,KeyError,TypeError) as e:checks.append({'name':name,'result':'PASS','rejection':str(e)});return
 raise AssertionError('ACCEPTED '+name)
def main():
 c=m.setup(ROOT);out=m.compile_candidate(c);ok('actual output roundtrip',m.validate(json.loads(m.enc(out)),c));ok('count-only actual directories',m.count_only(out,c)['exact_metadata']['directories']==18678)
 for name,edit in [('missing directory',lambda o:o['directories'].pop()),('conflicting duplicate directory',lambda o:o['directories'].append(o['directories'][0])),('wrong guard',lambda o:o['directories'][0].update(guard='always')),('wrong type',lambda o:o['directories'][0].update(type='INTEGER')),('endpoint',lambda o:o['relations'][0].update(endpoints=['missing','missing'])),('malformed join',lambda o:o['relations'][0]['join'].update(operator='CARTESIAN')),('duplicate ordinal',lambda o:o['relations'][1].update(ordinal=o['relations'][0]['ordinal'])),('zero unknown',lambda o:o['directories'][0]['cardinality'].update(exact=0,status='EXACT')),('observed count substituted',lambda o:o['directories'][0]['cardinality'].update(exact=1,status='EXACT')),('missing source form',lambda o:o['source_coverage'].update(checked_families=58)),('mixed candidate',lambda o:o['candidate_binding']['candidate'].update(sha256='0'*64)),('classifications qualified',lambda o:o['directories'][0].update(visibility='PUBLIC')),('readiness override',lambda o:o.update(full_expansion_ready=True))]:
  b=copy.deepcopy(out);edit(b);reject(name,lambda:m.validate(b,c))
 for name,edit in [('live context definitions',lambda o:o['context_definitions'].clear()),('live nested type',lambda o:o['directories'][0]['type'].clear())]:
  live=m.compile_candidate(c);edit(live);reject(name,lambda:m.validate(live,c))
 reject('unresolved readiness',lambda:m.readiness(out,c))
 # Independent audit omissions: mutate candidate view rather than compiled expected-list.
 for name,edit in [('omitted native field',lambda:c.c['fields.json']['prospective'].pop()),('omitted source form',lambda:c.c['source-forms.json']['prospective'].pop()),('unsupported declaration type',lambda:c.c['fields.json']['prospective'][0]['native_template'].update(type={'unsupported':True}))]:
  backup=copy.deepcopy(c.c);edit();reject(name,lambda:m.independent_coverage(c));c.c=backup
 # Concrete count algebra agrees with exhaustive tiny pair enumeration, including duplicates of join keys.
 a=[{'id':'a'+str(i),'key':i%2,'parent':i//2} for i in range(4)];b=[{'id':'b'+str(i),'key':i%2} for i in range(3)]
 for op in ['SAME-KEY','PARENT-KEY','CARTESIAN']:
  explicit=[(x['id'],y['id']) for x in a for y in b if op=='CARTESIAN' or x['parent' if op=='PARENT-KEY' else 'key']==y['key']]
  ok('count vs explicit '+op,m.fixture_join_count(op,a,b)==len(explicit))
 reject('malformed algebra',lambda:m.fixture_join_count('ALL',a,b))
 reject('duplicate instance',lambda:m.fixture_join_count('SAME-KEY',a+[a[0]],b))
 receipts=[]
 cases=['ord-early','zk-early','failed-ord-proceed','failed-zk-proceed','ord-abandon','zk-abandon','ord-cleanup','zk-cleanup','exit-after_retry_commit']
 for name in cases:
  e=json.loads((ROOT/'support/fixtures'/ (name+'.json')).read_bytes())
  for ctx in sorted(c.contexts):
   o=c.ingest(e,ctx,c.binding);counts=m.count_actual_fixture(out,o,e)
   ok(name+'/'+ctx+'/actual guarded joins',counts['structural_pairs']>0)
   # Parent/reference count exactly equals explicit one-target-per-source enumeration checked by adapter.
   rows=m.instance_rows(out,o,e);expected=sum(len(rows.get(r['endpoints'][0],[])) for r in out['relations'] if r['kind']!='SOURCE-FOLD-OBLIGATION')
   ok(name+'/'+ctx+'/count agreement',expected==counts['structural_pairs'])
   receipts.append({'name':name,'context':ctx,'export_sha256':m.sha(m.enc(e)),'accounting':o['supporting_pipeline']['validation']['counts'],'resources':o['supporting_pipeline']['validation']['resources'],'action_kinds':o['supporting_pipeline']['validation']['action_kinds'],'counts':counts})
  print(name,'PASS',flush=True)
 (DEST/'checks.json').write_bytes(m.enc({'count':len(checks),'checks':checks,'fixture_receipts':receipts,'no_runtime_execution':True}));print('PASS',len(checks))
if __name__=='__main__':
 try:main()
 except Exception:
  (DEST/'FAILED.txt').write_text(traceback.format_exc());(DEST/'FAILED-checks.json').write_text(json.dumps(checks));raise
