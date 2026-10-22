"""Checklist-to-source-template joins, not checklist-as-universe."""
import csv
from common import *
from static_declarations import build,constructor_coverage,schemas
b=build();ids={r['id'] for r in b['templates']};links=[]
for row in csv.DictReader((ROOT/'reference/FIELD-CORRESPONDENCE.csv').open()):
 rec,sel=row['record'],row['selector'];target=rec;path='/'+sel
 if sel=='$record':path=''
 elif sel.startswith('@'):path='#'+sel[1:]
 elif rec=='RESPONSE':
  if sel=='signature':path='/signature'
  else:target='ERROR-RESPONSE' if sel=='error' else 'SUCCESS-RESPONSE'
 elif rec=='U-ENTRY' and sel=='<u-key>':target='HEAD';path='/u/*#key'
 elif sel in ['<attempt-ref-key>','<retry-id-key>','<backup-id-key>']:target={'TRANSPORT-ENTRY':'STAGE','RETRY-ID-ENTRY':'STAGE','BACKUP-ENTRY':'STAGE'}[rec];path={'TRANSPORT-ENTRY':'/transport/*#key','RETRY-ID-ENTRY':'/retry_ids/*#key','BACKUP-ENTRY':'/backups/*#key'}[rec]
 elif rec in ['RETRY-ID-ENTRY','BACKUP-ENTRY'] and sel in ['attempt_ref','status']:path='/value'
 elif rec=='OWNERSHIP-ROW' and sel in ['coord','raw','hash']:target='OWNERSHIP-ROW-SQL';path='/raw_hex' if sel=='raw' else '/'+sel
 elif rec in ['JOURNAL','BLOB-STORE'] and sel in ['request','response','raw']:path='/'+sel+'_hex'
 elif rec=='RELEASE-RESULT' and sel=='attempt':target='RETRY-RELEASE-RESULT'
 identity=target+':'+path;need(identity in ids,'UNCOVERED-CHECKLIST:'+row['spec_class']+'->'+identity);links.append({'spec_class':row['spec_class'],'template':identity})
need(len(links)==424,'CHECKLIST');(ROOT/'declarations/checklist-links.json').write_bytes(enc(links))
g,_,_=schemas();del g['ACTION-OUTCOME-TABLE']
try:constructor_coverage(g)
except Invalid as e:need('UNDECLARED-SOURCE-CONSTRUCTOR' in str(e),'SOURCE-COVERAGE')
else:raise AssertionError('omitted source variant table accepted')
(ROOT/'results/checklist-coverage.json').write_bytes(enc({'links':424,'source_constructor_omission_rejected':True,'template_rows':len(b['templates']),'contexts':b['context_slots']}));print('424 exact links; independent constructor omission rejected')
