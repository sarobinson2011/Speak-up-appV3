from common import *
from static_declarations import build,validate_export_templates
from static_ingest import ingest
from framing_templates import framing
b=build();results=[]
for method in ['head','backup']:
 x=parse((ROOT/'positive-fixtures'/(method+'.json')).read_bytes(),200000000);v=ingest(x,b);need(len(v['response_selector_coverage'])==40,'EXPECTED-JOINS');results.append({'method':method,'envelope_joins':40,'status':'PASS','source':'retained IA-01 synthetic parser fixture; not candidate execution'})
need(framing(None)['presence'] is True and framing(None)['type_tag']=='NULL' and framing(None,present=False)['presence'] is False,'NULL-ABSENT')
results.append({'check':'NULL versus absent framing','status':'PASS'})
(ROOT/'results/adjacent-positive.json').write_bytes(enc(results));print(len(results),'positive checks passed')
