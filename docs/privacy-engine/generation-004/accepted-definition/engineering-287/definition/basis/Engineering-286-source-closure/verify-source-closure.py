#!/usr/bin/env python3
"""Document-only composition checker; never imports or executes historical sources."""
from pathlib import Path
import csv,json,hashlib,re
P=Path(__file__).resolve().parent
R={}
def sha(b):return hashlib.sha256(b).hexdigest()
def js(n):return json.loads((P/n).read_text())
def rr(n):return list(csv.DictReader((P/n).open(),delimiter='\t'))
reg=js('composed-sources/source-register.json');cs=js('source-delta/local-clause-deltas.json');ss=js('source-delta/normative-requirement-deltas.json')
sections=rr('composed-sources/section-merge-register.tsv');loc=rr('composed-sources/clause-location-register.tsv')
assert len(reg)==9 and len(cs)==30 and len(ss)==97 and len(sections)==66 and len(loc)==30
for owner,v in reg.items():
 raw=(P/v['original_file']).read_bytes();out=(P/v['file']).read_bytes()
 assert sha(raw)==v['original_sha256'] and sha(out)==v['sha256']
 assert v['appointed'] is False and v['published'] is False
 text=raw.decode();matches=list(re.finditer(r'<a id="([^"]+)"></a>',text));expected=text[:matches[0].start()]
 for i,m in enumerate(matches):
  sec=text[m.start():matches[i+1].start() if i+1<len(matches) else len(text)]
  target=[r for r in sections if r['owner']==owner and r['anchor']==m.group(1)];assert len(target)==1
  assert sha(sec.encode())==target[0]['original_section_sha256']
  expected+=sec.rstrip()+'\n'
  for c in cs:
   if c['owner']==owner and c['anchor']==m.group(1):expected+='\n### Incorporated proposal: '+c['local_clause']+'\n\n'+c['proposed_text']+'\n'
  expected+='\n'
 assert (expected.rstrip()+'\n').encode()==out
R['exact_owner_merge']={'owners':9,'preserved_owner_anchors':66,'exact_reconstruction':'PASS'}
for c in cs:
 l=[r for r in loc if r['clause']==c['local_clause']];assert len(l)==1;l=l[0]
 lines=(P/l['composed_file']).read_text().splitlines()
 t='\n'.join(lines[int(l['line_start'])-1:int(l['line_end'])]);assert t==c['proposed_text'] and sha(t.encode())==l['text_sha256']
 sentences=[s['text'] for s in ss if s['local_proposal_coordinate'].split('/')[0]==c['local_clause']]
 assert ' '.join(sentences)==c['proposed_text']
R['clause_sentence_locations']={'clauses':30,'sentences':97,'exact_text_and_locations':'PASS'}
bs=list((P/'baseline/sources').glob('S[0-9][0-9].md'));assert len(bs)==70
base=(P/'baseline/exact-861-published-rows.md').read_text().splitlines();spec=(P/'baseline/evidence/spec.md').read_text().splitlines();assert len(base)==861 and all(x in spec for x in base)
R['baseline']={'sources':70,'requirements':861,'all_rows_in_exact_spec':True}
# Every supporting declaration resolves against the composed owner, not a nonexistent source label.
types=rr('supporting-program/types.tsv');defs=rr('supporting-program/definitions.tsv');fields=rr('supporting-program/fields.tsv');ops=rr('supporting-program/operations.tsv')
assert [len(types),len(defs),len(fields),len(ops)]==[17,53,118,86]
assert len(js('supporting-program/entry.json')['root_fields'])==94
for d in defs:
 assert d['source_id'] in reg and f'id="{d["source_anchor"]}"' in (P/reg[d['source_id']]['file']).read_text()
for r in rr('supporting-program/BOUNDED-NOT-ADMITTED-projection.tsv'):
 assert r['authoritative_source_sha256']==reg[r['authoritative_source_id']]['sha256']
 assert 'E286-DRAFT-' not in json.dumps(r)
assert not any(d['definition_id'].startswith('E286-DRAFT-') for d in defs)
R['supporting_program']={'types':17,'definitions':53,'operations':86,'root_fields':94,'all_fields':118,'owner_resolution':'PASS','unsupported_286_coordinate_extensions_imported':False,'full_profile_admitted':False}
rec=rr('supporting-program/recovery.tsv');assert len(rec)==21
R['recovery']={'rows':21,'sha256':sha((P/'supporting-program/recovery.tsv').read_bytes())}
assert {x['assignment_id'] for x in rr('closure/source-assignment-disposition.tsv')}=={f'R{i:02}' for i in range(1,13)}
assert len(rr('closure-boundary.tsv'))==9
R['completion_boundary']={'source_assignments':12,'obligations':9,'successor_identity_allocated':False,'source_appointment':False,'privacy_PASS':False,'implementation_adoption':False,'new_handover_issued':False}
R['scope']='Exact source merge/reference/preservation checks only. Not independent semantic acceptance, profile admission, source truth, privacy PASS or implementation readiness.'
(P/'verification').mkdir(exist_ok=True);(P/'verification/results.json').write_text(json.dumps(R,indent=2)+'\n')
print(json.dumps(R,indent=2))
