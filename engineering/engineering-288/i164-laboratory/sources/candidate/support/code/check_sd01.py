"""Focused correction checks only; no runtime execution or source-file mutation."""
import copy,importlib.util,json
from common import *
import static_declarations as current
from response_obligations import source_obligations,check_rows
from static_ingest import ingest
from pipeline import integrate
from ingest import validate_export
results=[]
def check(name,fn):
 try:d=fn();results.append({'name':name,'status':'PASS','detail':d})
 except Exception as e:results.append({'name':name,'status':'FAIL','error':repr(e)});raise
 finally:(ROOT/'results/sd01-checks.json').write_bytes(enc(results));print(json.dumps(results[-1]),flush=True)
def reject(fn,expected):
 try:fn()
 except Invalid as e:need(expected in str(e),'WRONG-REJECTION:'+str(e));return str(e)
 raise AssertionError('accepted omission')
x=parse((ROOT/'preserved-review/SD-01-minimal.json').read_bytes(),200000000)
need(sha((ROOT/'preserved-review/SD-01-minimal.json').read_bytes())=='0b24589fc1be5bcc63b1d1ef6c53af320b478c1a4d1f1b7d312cc7c2b0352c3d','WITNESS-IDENTITY')
spec=importlib.util.spec_from_file_location('preserved_old',ROOT/'preserved-review/static_declarations-old.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
def old_witness():
 original=old.schemas
 def omit():
  g,o,p=original();del g['SUCCESS-RESPONSE']['data']['request_method_choice']['head'];return g,o,p
 try:
  old.schemas=omit;b=old.build();old.validate(b);failure=reject(lambda:old.validate_export_templates(x,b),'REQUEST-METHOD-CONTEXT');return {'incomplete_catalogue_accepted':True,'source_admitted_response_rejected':failure,'templates':len(b['templates'])}
 finally:old.schemas=original
check('preserved-original-witness-old-checker',old_witness)
bundle=current.build();obligations=source_obligations();(ROOT/'results/source-response-obligations.json').write_bytes(enc(obligations))
def mutant(label,change,expected='SOURCE-RESPONSE-COVERAGE'):
 def run():
  original=current.schemas
  def altered():
   g,o,p=original();change(g,o,p);return g,o,p
  try:
   current.schemas=altered;return reject(current.build,expected)
  finally:current.schemas=original
 check(label,run)
for method in sorted(obligations['method_map']):
 mutant('omit-response-variant:'+method,lambda g,o,p,m=method:g['SUCCESS-RESPONSE']['data']['request_method_choice'].pop(m))
for family in ['RESPONSE','SUCCESS-RESPONSE','ERROR-RESPONSE','SIGNED-RESULT','RELEASE-RESULT','RETRY-RELEASE-RESULT']:
 for field in obligations['groups'][family]:
  mutant('omit-response-field:'+family+'.'+field,lambda g,o,p,n=family,f=field:g[n].pop(f))
for family,field in [('HEAD','resources'),('RESOURCES','query_holds'),('COUNTS','attempt'),('PARTITIONS','snapshot'),('U-ENTRY','stage'),('STAGE','pending'),('TRANSPORT-ENTRY','queried'),('PENDING','result'),('LAST','tx'),('QUERY','attempt')]:
 mutant('omit-nested-field:'+family+'.'+field,lambda g,o,p,n=family,f=field:g[n].pop(f))
mutant('wrong-nested-type',lambda g,o,p:g['RESOURCES'].update(holds='BOOLEAN'))
mutant('wrong-return-family',lambda g,o,p:g['SUCCESS-RESPONSE']['data']['request_method_choice'].update(head={'ref':'ERROR-RESPONSE'}))
mutant('missing-error-branch',lambda g,o,p:g['RESPONSE']['response']['variants'].pop('false'))
mutant('wrong-discriminator',lambda g,o,p:g['RESPONSE']['response'].update(choice_by='request'))
mutant('wrong-optional-guard',lambda g,o,p:p['PENDING'].update(result='always'),'SOURCE-RESPONSE-GUARD')
mutant('omit-request-method',lambda g,o,p:g['REQUEST']['body']['union'][0]['variants'].pop('head'),'SOURCE-REQUEST-METHOD-COVERAGE')
mutant('omit-request-body-field',lambda g,o,p:g['BODY-backup'].pop('id'),'SOURCE-REQUEST-BODY-COVERAGE')
for f in ['presence','availability','encoding_length','member_count','exact_bytes','type_tag','key_encoding','separator_encoding','opening_delimiter','closing_delimiter']:
 check('omit-emitted-framing:'+f,lambda f=f:reject(lambda:check_rows([r for r in bundle['templates'] if r['id']!='RESPONSE:/signature#'+f],obligations),'SOURCE-MISSING-FRAMING'))
for label,change in [('guard',lambda r:r.update(guard='always')),('parent',lambda r:r.update(parent='ERROR-RESPONSE:')),('type',lambda r:r.update(type='INTEGER'))]:
 def run(change=change):
  rows=copy.deepcopy(bundle['templates']);change(next(r for r in rows if r['id']=='SUCCESS-RESPONSE:/data/@method/head'));return reject(lambda:check_rows(rows,obligations),'SOURCE-ROW-BINDING')
 check('emitted-row-'+label,run)
check('original-head-accepted-corrected',lambda:{'selector_joins':len(ingest(x,bundle)['response_selector_coverage'])})
# Same source method variants use both method-specific historical fixtures. No new lifecycle.
forms=set()
for file in sorted((ROOT/'fixtures').glob('*.json')):
 if file.name=='INDEX.json':continue
 def valid(file=file):
  export=parse(file.read_bytes(),200000000);coverage=current.validate_export_templates(export,bundle)
  for _,p,r in export['journal']:
   request=parse(hexbytes(p))['request'];forms.add((request['method'],'unanswered' if r is None else 'success' if parse(hexbytes(r))['response']['ok'] else 'error'))
  return {'typed_records':coverage['typed_records_checked']}
 check('saved-legitimate:'+file.stem,valid)
for name in ['ord-early','zk-early','exit-after_signature_commit']:
 def match(name=name):
  export=parse((ROOT/'fixtures'/(name+'.json')).read_bytes(),200000000);a=ingest(export,bundle);b=integrate(export);need(a['actual_occurrences']==b['actual_occurrences'] and a['response_selector_coverage']==b['response_selector_coverage'],'IA01');need(enc(ingest(parse(enc(export),200000000),bundle))==enc(a),'REOPEN');return {'envelope_joins':len(a['response_selector_coverage']),'stable_reopening':True,'new_process_exit':False}
 check('IA01-and-reopening:'+name,match)
check('independent-source-methods',lambda:need(set(obligations['method_map'])=={'head','retire','open','decide','query','observe','backup','sign','release','retry_release'},'ADMITTED-SOURCE-METHODS'))
(ROOT/'results/sd01-summary.json').write_bytes(enc({'checks':len(results),'forms':sorted(forms),'fresh_lifecycles':0,'fresh_process_exits':0,'candidate_changes':False,'source_families':sorted(obligations['groups']),'scope':'pinned response dispatch/fields/returned HEAD closure and framing; no general model completeness'}))
