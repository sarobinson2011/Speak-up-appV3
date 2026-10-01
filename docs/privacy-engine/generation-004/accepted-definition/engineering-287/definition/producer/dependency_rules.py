"""Documentary acquisition dependencies. Not a scheduler, source validator or protocol runtime.
DONE means a caller-supplied synthetic/externally validated work-state, never authority.
The dependency planner cannot grant E/D/U permissions.
"""
from pathlib import Path
import csv
O=Path(__file__).resolve().parents[1]
PHASES=('ADMISSION','VERIFICATION','E','AUTHORIZED','PRE-EXECUTION','EXECUTION','PRE-COMMITMENT','DELIVERY','RECOVERY','STATIC')
def allowed_phases(work):
 if work.startswith('admit-') or work=='fix-rc':return ('ADMISSION',)
 if work.startswith('proof-'):return ('VERIFICATION',)
 if work in ('history-view','history-validate','history-project','state-view','state-validate','phase-bind','joint-view'):return ('E','PRE-EXECUTION','PRE-COMMITMENT')
 if work in ('carrier-translate','carrier-validate','component-produce'):return ('E','AUTHORIZED','PRE-EXECUTION','PRE-COMMITMENT') if work!='component-produce' else ('AUTHORIZED','PRE-EXECUTION','PRE-COMMITMENT')
 return {'entry-evaluate':('E',),'execution-gate':('PRE-EXECUTION',),'prepare-intent':('EXECUTION',),'final-gate-write':('PRE-COMMITMENT',),'delivery-reconcile':('DELIVERY',),'recover-replay':('RECOVERY',),'recover-fresh':('RECOVERY',),'privacy-assemble':('STATIC',)}[work]
def table(path):return list(csv.DictReader((O/path).open(),delimiter='\t'))
def requirements(work,phase,available=()):
 if phase not in PHASES:raise ValueError('Unknown phase')
 if not set(available)<={'history','state'}:raise ValueError('Unknown availability domain')
 base={r['work_id']:r for r in table('privacy/producer-proposal/dependencies.tsv')}
 if work not in base:raise ValueError('Unknown work')
 if phase not in allowed_phases(work):raise ValueError('Work not applicable in phase')
 # These are source evidence obligations, not invented executable work IDs.
 special={
 'phase-bind': [('WORK','fix-rc')] if phase=='E' else [('EVIDENCE','authorization-basis')],
 'joint-view':[('WORK','phase-bind')]+[('WORK',x+'-validate') for x in ('history','state') if x in available],
 'proof-artifacts':[('EVIDENCE','verifier-input-basis')],
 'component-produce': [('EVIDENCE','original-authorized-component-basis'),('WORK','carrier-validate')] if phase=='AUTHORIZED' else [('WORK','joint-view'),('WORK','carrier-validate')],
 'carrier-translate':[('EVIDENCE','consumed-field-records')],
 'final-gate-write':[('WORK','prepare-intent'),('EVIDENCE','fresh-final-component-view'),('EVIDENCE','indivisible-final-boundary')],
 'delivery-reconcile':[('EVIDENCE','selected-completed-outcome')],
 'recover-replay':[('EVIDENCE','prior-completed-E-D'),('EVIDENCE','terminal-U')],
 'privacy-assemble':[('EVIDENCE','complete-static-declarations')],
 }
 if work in special:return special[work]
 return [('WORK',x.strip()) for x in base[work]['predecessors'].split(';') if x.strip()!='NONE']
def readiness(work,phase,states,evidence,available=()):
 """Classify dependency availability only; unknown inputs never become DONE."""
 req=requirements(work,phase,available)
 missing=[];failed=[]
 for kind,key in req:
  status=(states if kind=='WORK' else evidence).get(key,'UNKNOWN')
  if status not in ('DONE','FAILED','UNKNOWN'):raise ValueError('Invalid state')
  if status=='FAILED':failed.append((kind,key))
  elif status!='DONE':missing.append((kind,key))
 return {'dependency_state':'FAILED' if failed else 'UNRESOLVED' if missing else 'READY-FOR-SOURCE-WORK','failed':failed,'missing':missing,'protocol_permission':False}
def consumed_records(field_id):
 """Exact record directory membership; authority validation still required."""
 fields={r['field_id'] for r in table('profile/fragments/fields.tsv')}
 if field_id not in fields:raise ValueError('Unknown field')
 return sorted({r['record'] for r in table('privacy/producer-proposal/evidence-fields.tsv') if field_id in r['consumer_fields'].split(';')})
def custody_matrix():
 out=[]
 for e in table('privacy/producer-proposal/evidence-fields.tsv'):
  for r in table('privacy/producer-proposal/observer-custody-register.tsv'):
   if e['group'] in r['groups'].split(';'):
    out.append({'record':e['record'],'field':e['field'],'role':r['role'],'context_scope':'BOTH-POTENTIAL','visibility':'UNKNOWN','role_is_appointed_actor':'FALSE'})
 return out
