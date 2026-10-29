from pathlib import Path
import sys,copy,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);mode=sys.argv[3];error=None
try:
 monitor=guard(root);m=module(root/'code/correspondence.py');monitor(m);raw=(root/'results/client-state-correspondence.json').read_bytes();saved=json.loads(raw)
 if mode=='public':
  first=rec.check('public accepts exact current saved receipt',lambda:m.validate(root,raw));rec.check('public both contexts and unavailable runtime',lambda:first['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and first['actual_admission'] is False and first['runtime_client_state_chain']=='UNAVAILABLE')
  first['contexts'].reverse();first['receipt'].clear();first['actual_admission']=True
  rec.check('public repeated pristine call isolated from returned mutations',lambda:m.validate(root,raw)['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
 elif mode=='public-negative':
  bad=copy.deepcopy(saved);bad['contexts'][0]['client_state_return_correspondence']['conditional_links'][0]['conditional_value_at_validated_frontier']['head']='f'*64
  rec.reject('public changed current receipt rejects by fresh derivation',lambda:m.validate(root,enc(bad)),'STALE-OR-ALTERED')
  for label,change in [('missing relation',lambda x:x['contexts'][0].pop('client_state_return_correspondence')),('missing context',lambda x:x['contexts'].pop())]:
   b=copy.deepcopy(saved);change(b);rec.reject('public '+label,lambda b=b:m.validate(root,enc(b)),'MANDATORY-RELATION')
 elif mode=='semantic-alias':
  d=m.inputs(root);cat=m.catalogue(d);rows=rec.check('semantic legitimate mandatory current relation',lambda:m.semantic(d,cat));rec.check('semantic exact saved two-context rows',lambda:enc(rows)==enc([v['client_state_return_correspondence'] for v in saved['contexts']]))
  rows.reverse();rows[0]['declaration']['ordered_hops'].clear();rows[1]['validated_state_anchor']['instance']['binding']='f'*64
  rows[1]['conditional_links'][0]['conditional_value_at_validated_frontier']['counts'].clear()
  rec.check('semantic returned nested/context mutation cannot poison future expectations',lambda:enc(m.semantic(d,cat))==enc([v['client_state_return_correspondence'] for v in saved['contexts']]))
 elif mode=='semantic-coordinated':
  d=m.inputs(root);cat=m.catalogue(d);rows=copy.deepcopy([v['client_state_return_correspondence'] for v in saved['contexts']]);ev=m.inner(d)['ctx']['e'];p='evidence/recovery-export-0.json';v=json.loads(ev[p]);h=json.loads(bytes.fromhex(v['head']));h['head']='f'*64;v['head']=enc(h).hex();ev[p]=enc(v)
  for r in rows:
   r['validated_state_anchor']['validated_state']['head']='f'*64
   for link in r['conditional_links']:link['conditional_value_at_validated_frontier']['head']='f'*64
  rec.reject('semantic mutually altered HEAD reports and evidence reject',lambda:m.semantic(d,cat,rows,ev),'STATE-VALUE-ORIGIN:/head')
 elif mode=='derive-wrong-instance':
  d=m.inputs(root);cat=m.catalogue(d);rows=copy.deepcopy([v['client_state_return_correspondence'] for v in saved['contexts']]);r=rows[1]
  r['validated_state_anchor']['instance']['binding']='f'*64;r['invocation_scope']['instance']['binding']='f'*64
  rec.reject('derivation wrong-instance coordinated row rejects',lambda:m.derive_client_state(d,cat,rows),'CLIENT-STATE-CONTEXT-CORRESPONDENCE')
 else:raise AssertionError(mode)
 rec.check('required predecessor derivation was actually invoked',lambda:any(c['function']=='derive_client' for c in CALLS))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode)
