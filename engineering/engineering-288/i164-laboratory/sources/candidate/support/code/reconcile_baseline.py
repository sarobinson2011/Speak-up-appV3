"""Exact pinned-input reconciliation. Trust pin must come from canonical route.
This program verifies correspondence; it cannot authenticate project authority.
"""
import argparse
from common import *
REQUIRED={'register/fields.json','register/schemas.json','register/source-forms.json','register/dependencies.json','records/expanded-contract.json','records/relation-rules.json','profile-binding.json','candidate-identity.json','ledger-binding.json','relationships-43.json'}
def members(root,manifest):
 need(type(manifest) is dict,'MEMBER-MANIFEST');actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p!=root/'manifest.json'}
 need(actual==set(manifest),'EXACT-MEMBERSHIP');data={}
 for n,v in manifest.items():
  need(type(n) is str and n and not n.startswith('/') and all(x not in ['','.','..'] for x in n.split('/')),'PATH');p=root/n;need(not p.is_symlink() and all(not x.is_symlink() for x in p.parents if x!=root.parent),'SYMLINK');keys(v,'bytes sha256');integer(v['bytes']);digest(v['sha256']);raw=p.read_bytes();need(len(raw)==v['bytes'] and sha(raw)==v['sha256'],'MEMBER-IDENTITY');data[n]=raw
 return data

def classes(raw,files):
 rows=parse(raw,50000000);need(type(rows) is list,'CLASSES');out={}
 for row in rows:
  keys(row,'id source source_sha256 selector type guard parent');text(row['id'],512);need(row['id'] not in out,'DUPLICATE-CLASS');need(row['source'] in files and sha(files[row['source']])==row['source_sha256'],'CLASS-SOURCE');need(type(row['selector']) is str and type(row['type']) is str and type(row['guard']) is str,'DECLARATION-TYPE');need(row['parent'] is None or type(row['parent']) is str,'PARENT-TYPE');out[row['id']]=row
 return out

def parents(rows):
 for key in rows:
  seen=set();n=key
  while n is not None:
   need(n in rows,'MISSING-PARENT');need(n not in seen,'PARENT-CYCLE');seen.add(n);n=rows[n]['parent']

def reconcile(root,authority_bytes,expected_authority_sha256):
 root=Path(root);digest(expected_authority_sha256);need(sha(authority_bytes)==expected_authority_sha256,'AUTHORITY-PIN');a=parse(authority_bytes,2000000);keys(a,'format baseline_manifest_sha256 delta_sha256 head contexts authority_record_sha256 historical_relationships_sha256');need(a['format']=='I164-CANONICAL-INPUT-PIN-1','PIN-VERSION');digest(a['authority_record_sha256']);need(type(a['contexts']) is list and len(a['contexts'])==2 and all(type(x) is str and x for x in a['contexts']) and a['contexts'][0]!=a['contexts'][1],'CONTEXTS')
 base=root/'baseline';raw=(base/'manifest.json').read_bytes();need(sha(raw)==a['baseline_manifest_sha256'],'BASELINE-PIN');m=parse(raw,2000000);keys(m,'format files contexts authority_record_sha256');need(m['format']=='I164-BASELINE-MANIFEST-1' and m['contexts']==a['contexts'] and m['authority_record_sha256']==a['authority_record_sha256'],'BASELINE-CONTEXT');files=members(base,m['files']);need(REQUIRED<=set(files),'MISSING-BASELINE-ARTIFACT');need(bool({'register/custody.tsv','register/custody.json'} & set(files)),'MISSING-CUSTODY-ARTIFACT');need(sha(files['relationships-43.json'])==a['historical_relationships_sha256'],'HISTORICAL-RELATIONSHIPS')
 original=classes(files['register/fields.json'],files);parents(original);need(all(v['parent'] is None or v['parent'] in original for v in original.values()),'BASELINE-PARENT');current=dict(original);head=sha(raw)
 need(type(a['delta_sha256']) is list,'CHAIN');delta_root=root/'deltas';expected_dirs={str(i).zfill(6) for i in range(1,len(a['delta_sha256'])+1)};need(({p.name for p in delta_root.iterdir()} if delta_root.exists() else set())==expected_dirs,'DELTA-MEMBERSHIP')
 for i,expected in enumerate(a['delta_sha256'],1):
  digest(expected);droot=delta_root/str(i).zfill(6);raw=(droot/'manifest.json').read_bytes();need(sha(raw)==expected,'DELTA-PIN');d=parse(raw,2000000);keys(d,'format ordinal previous baseline contexts files after_classes_sha256');integer(d['ordinal'],1);need(d['format']=='I164-REGISTER-DELTA-1' and d['ordinal']==i and d['previous']==head and d['baseline']==a['baseline_manifest_sha256'] and d['contexts']==a['contexts'],'CHAIN-ORDER');new=members(droot,d['files']);need('added-fields.json' in new,'MISSING-DELTA-RECORDS')
  for n,b in new.items():
   if n=='added-fields.json':continue
   need(n not in files,'IMMUTABLE-SOURCE-OVERWRITE');files[n]=b
  added=classes(new['added-fields.json'],files)
  for k,v in added.items():need(k not in current,'CLASS-CONFLICT');current[k]=v
  need(all(v['parent'] is None or v['parent'] in current for v in current.values()),'DELTA-PARENT');parents(current);need(sha(enc([current[k] for k in sorted(current)]))==d['after_classes_sha256'],'DELTA-AFTER');head=sha(raw)
 need(head==a['head'],'STALE-HEAD');need(all(v['parent'] is None or v['parent'] in current for v in current.values()),'MISSING-PARENT');need(all(enc(current[k])==enc(v) for k,v in original.items()),'HISTORICAL-OVERWRITE')
 return {'status':'EXACT-PINNED-INPUT-CORRESPONDENCE','baseline':a['baseline_manifest_sha256'],'head':head,'deltas':len(a['delta_sha256']),'classes':len(current),'contexts':a['contexts'],'authority_record_sha256':a['authority_record_sha256'],'authority_provenance_authenticated_by_this_tool':False,'canonical_registration':False,'actual_admission':False,'remaining':['external validation of canonical authority pin and completeness statement','semantic model/profile/ledger binding','qualified classifications and appointments','lifetime/operational obligations']}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('pin');p.add_argument('pin_sha256');a=p.parse_args();print(enc(reconcile(a.root,Path(a.pin).read_bytes(),a.pin_sha256)).decode(),end='')
