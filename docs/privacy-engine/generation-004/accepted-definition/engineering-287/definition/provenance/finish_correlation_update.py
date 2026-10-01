from pathlib import Path
import json,csv,io,hashlib,shutil
O=Path('PE-G4-correlation-update');sha=lambda b:hashlib.sha256(b).hexdigest()
def wr(p,s):
 q=O/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(s.rstrip()+'\n')
def js(p,v):wr(p,json.dumps(v,indent=2))
def rr(p):return list(csv.DictReader((O/p).open(),delimiter='\t'))
def tb(p,r):
 f=io.StringIO();w=csv.DictWriter(f,list(r[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(r);wr(p,f.getvalue())
clauses=[('universe','MUST','The G4 privacy construction MUST include every declared program field, root argument, component side/status, ReadObject metadata cell, operation, expression branch, parameter/call/control relationship, governing owning schema, public PI alias and source-required producer observation/custody path; absent source completeness MUST remain an admission failure.'),('visibility','MUST','Every required observer and coalition visibility assessment MUST be independently source-established for the exact regenerated graph; missing or unknown visibility MUST fail, and a caller-supplied completeness flag MUST NOT substitute for that evidence.'),('correlation','MUST','Cross-context correlation assessment MUST use the independently established observable graph for each required observer coalition, preserve the existing permitted constant-equality exception only in that assessment, and include equality of values visible to that coalition.'),('actor','MUST','Actor-reconstruction assessment MUST retain the complete regenerated graph, including confidential, non-observed and permitted constant-equality edges, without visibility filtering.'),('no-exceptions','MUST NOT','The observation-aware correction MUST NOT introduce public-linkage exceptions, suppress existing public PI, convert changing roots or action-local values into generation constants, or waive the unchanged public uniqueness and actor-protection obligations.')]
source='''# PE-G4-SOURCE-S83 — approved observation-aware correlation construction

Status: unpublished G4 source candidate; user-authorized construction, not independently appointed or admitted. The precise user approval is preserved in privacy/AUTHORIZATION.md.

This source specializes the G4 interpretation of retained S70/S71/S72 privacy construction, specifically full declared-surface regeneration and the correlation graph criterion. Historical G3 sources remain byte-exact. This is an explicit approved procedural delta, not a silent correction of published G3. Every other governing validation, source/evidence appointment, evidence authentication, full actor graph, uniqueness duty and ordered failure precedence remains binding.

'''
for anchor,strength,text in clauses:source+=f'<a id="{anchor}"></a>\n## {anchor}\n\n{text}\n\n'
source+='''<a id="producer-boundary"></a>
## Producer and completeness boundary

The graph templates preserve all supplied program declarations and proposed producer surfaces. Prose producer predecessors/targets without exact operation/field identities are explicit UNRESOLVED nodes; they do not become fabricated executable links. Shared serialization and total-map FALSE examples remain optional unappointed mechanisms, not new protocol policy. Unknown actual provider, custody, observer and collusion facts remain missing evidence. No source-truth or completeness claim is established by this authoring model.

<a id="procedure"></a>
## Exact graph procedure and staged integration

privacy/observation_correlation.py below supplies the exact graph subroutine and twelve synthetic author vectors. It requires the complete independently regenerated graph, including the unchanged conservative equality expansion, and externally authenticated required observer/coalition scope and visibility cells. The graph subroutine does not perform those external validations and never returns a profile admission PASS. Its complete per-view cell domain rejects missing entries. Coalition views cannot erase observations of their members. Visible value equality cannot be hidden by an issuer's edge label. Negative visibility requires source evidence; confidentiality labels do not prove non-observation.

Actor reconstruction uses every graph edge even when visibility is invalid. Uniqueness retains its original public-byte equality condition. Failures are collected in the inherited ordered list; e.g. shared public root equality produces UNIQUENESS-FAILURE before CORRELATION-FAILURE. No earlier authentication failure is bypassed in the full governing pipeline.

The declaration model includes every supplied 118-field program input and metadata cell, all AST branches, owning schemas, operations and the optional producer inventory. It remains a static construction template, not a full runtime graph. Source-complete observer/custody declarations, conservative two-context equality expansion, repeated occurrence/replay bindings, canonical binding of the expanded privacy member and integrated evidence validation remain mandatory before outer-profile admission. None is inferred from graph-vector success. Source adequacy of the producer proposal and remaining coordinates/material conditions stays open.

The construction's new declaration inputs and output templates are digest-bound by privacy/model/manifest.json. Until the complete model/evidence is canonically incorporated into the governing PRIVACY member, no final full-profile digest exists. No ad hoc extra graph attached to the old immutable container can substitute for that incorporation.

The following executable notation is newly authored G4 construction code. Its source-validation prerequisites are normative; fixture test inputs have no source authority. No historical constructor has been executed.

```python
'''+(O/'privacy/observation_correlation.py').read_text()+'```\n'
wr('sources/PE-G4-SOURCE-S83.md',source)
inv=rr('composition/source-inventory.tsv');inv.append({'source_id':'PE-G4-SOURCE-S83','path':'sources/PE-G4-SOURCE-S83.md','sha256':sha(source.rstrip().encode()+b'\n'),'basis_id':'EXPLICIT-USER-APPROVED-PRIVACY-CORRECTION','basis_sha256':'NOT-APPLICABLE','mode':'APPROVED-G4-PROCEDURAL-SPECIALIZATION','root_anchor':'ROOT:PE-G4-SOURCE-S83','status':'CANDIDATE-NOT-APPOINTED'});tb('composition/source-inventory.tsv',inv)
tb('composition/privacy-procedure-delta.tsv',[{'retained_source':'PE-G4-SOURCE-S70/S71/S72','original_role':a,'G4_specialization':b,'owner':'PE-G4-SOURCE-S83','status':'Authorized for unpublished construction; no admission'} for a,b in [('Fixed six-schema/component-only privacy model','Complete declaration-model coverage added; source-complete canonical PRIVACY integration remains required'),('Unfiltered full-graph correlation','Source-established observation graph per required coalition; unknown visibility fails'),('Full-graph actor reconstruction','Preserved unchanged; no constant or visibility filter'),('Public-value uniqueness','Preserved unchanged; known shared public root equality fails'),('Original failure order','Preserved; graph-only results are not overall admission results')]])
req=json.loads((O/'composition/requirement-inventory.json').read_text());new=[]
for i,(anchor,strength,text) in enumerate(clauses,66):
 r={'requirement_id':f'PE-G4-CAP-{i:03}','basis_requirement_id':'USER-APPROVED-OBSERVATION-AWARE-CORRELATION','requirement_family':'RF-11','strength':strength,'applicability':'conditional','scope':'G4 profiles subject to the approved observation-aware privacy construction','text':text,'owner_sources':'PE-G4-SOURCE-S83#'+anchor,'supporting_references':'PE-G4-SOURCE-S70, PE-G4-SOURCE-S80#privacy','treatment':'APPROVED-PRIVACY-PROCEDURAL-DELTA'};req.append(r);new.append(r)
js('composition/requirement-inventory.json',req);js('composition/privacy-requirement-delta.json',new)
p=O/'PE-PROTOCOL-SPECIFICATION-G4.candidate.md';s=p.read_text();s+='\n## RF-11 — approved observation-aware procedural delta\n\nThese five homes supplement the original 926 candidate homes; total 931. This is unpublished construction, not conformance admission.\n\n| Requirement | Strength | Applicability | Scope | Normative text | Owner source | Supporting references |\n|---|---|---|---|---|---|---|\n'
for r in new:s+='| <a id="'+r['requirement_id'].lower()+'"></a> '+r['requirement_id']+' | '+' | '.join(r[k] for k in ('strength','applicability','scope','text','owner_sources','supporting_references'))+' |\n'
p.write_text(s)
fam=rr('composition/family-composition.tsv')
for r in fam:
 if r['requirement_family']=='RF-11':r['candidate_delta_homes']=str(int(r['candidate_delta_homes'])+5)
tb('composition/family-composition.tsv',fam)
# Retain original verifier evidence; adjust only newly authorized source/home counts.
shutil.copyfile(O/'verify-candidate.py',O/'evidence/verify-pre-correlation-candidate.py')
p=O/'verify-candidate.py';s=p.read_text().replace("'80 unique source identities',len(source)==len(inventory)==80","'81 unique source identities',len(source)==len(inventory)==81").replace("'926 unique candidate normative homes',len(reqdict)==len(req)==926","'931 unique candidate normative homes',len(reqdict)==len(req)==931");p.write_text(s)
js('privacy/model/manifest.json',[{'path':str(p.relative_to(O)),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in sorted((O/'privacy/model').iterdir()) if p.is_file() and p.name!='manifest.json'])
wr('COMPLETION.md','''# G4 observation-aware correlation integration

The user's approved criterion is integrated as unpublished source S83 and five explicit requirement homes. The original 861 inherited meanings and all four selected policies remain unchanged. The detailed correlation procedure has the explicitly authorized specialization; G3 sources remain exact by reference. The updated candidate has 81 source members and 931 sentence-level normative homes. These are construction counts, not acceptance evidence.

Every one of the 118 declared fields now has a dedicated surface, with nine non-value ReadObject metadata cells each. All 94 root arguments, 89 operations, 56 definitions and 944 expression nodes/branches are represented. The 32 optional producer work rows and 174 evidence fields are explicit. Ambiguous producer prose is recorded as unresolved, not converted to invented executable dependencies. The static template has 2,947 nodes and 9,426 structural edges; it is not the full conservative two-context actor graph or occurrence transcript.

The graph procedure now rejects missing/unknown visibility, checks coalition observation preservation and prevents suppression of visible equality. All actor edges remain available to actor testing, including confidential and constant edges. Original public uniqueness and failure precedence remain unchanged. Twelve bounded vectors exercise these behaviors; they do not authenticate sources or admit a profile.

A remaining concrete boundary is demonstrated: two contexts sharing the same visible public root fail both unchanged uniqueness and observation-aware correlation. Earliest graph-policy failure is UNIQUENESS-FAILURE. No public-root exception has been granted or added. The correction does not itself make the profile admissible.

Still required: source-complete observer/custody/coalition and producer dependency declarations; full canonical privacy-member/evidence integration and equality expansion; coordinate/materiality completion; and independently appointed source/privacy evidence. The actual profile, appointments, registry, publication, succession and repository remain untouched. The new correlation approval is recorded and must not be requested again. Continue within these limits without a numbered handover.
''')
defects=rr('acceptance-defects.tsv')
for r in defects:
 if r['id']=='G4-C02':
  r['defect']='Dedicated fields/metadata/AST/producer surface templates and approved correlation source now constructed. Full source-complete producer/observer universe, equality expansion and canonical PRIVACY/evidence integration remain unclosed; unresolved producer clauses are enumerated.'
  r['closure_evidence']='Resolve privacy/model/unresolved-producer-conditions.tsv from source; independently establish exact observer/coalition/visibility evidence; bind complete regenerated model and full actor graph in revised canonical privacy member.'
defects.append({'id':'G4-P01','kind':'KNOWN-POLICY-BOUNDARY','artifact':'privacy/KNOWN-PUBLIC-ROOT-BOUNDARY.md','defect':'Visible equality of a legitimate shared public root in two contexts fails unchanged uniqueness and approved correlation. No public-linkage exception is authorized.','closure_evidence':'Preserve this failure. Any future source determination must explicitly resolve the public-relationship/assessment boundary without silently suppressing r or weakening actor protection.','needs_new_user_policy':'No exception inferred; current approval explicitly grants none.'})
tb('acceptance-defects.tsv',defects)
p=O/'privacy/KNOWN-PUBLIC-ROOT-BOUNDARY.md';s=p.read_text().replace('Therefore the approved observation-aware criterion still returns CORRELATION-FAILURE','Therefore the unchanged uniqueness check returns UNIQUENESS-FAILURE and the approved observation-aware criterion also returns CORRELATION-FAILURE');p.write_text(s)
wr('START-HERE.md','''# Continue Engineering[286] — approved correlation integrated

Read WORKING-RULE.md, privacy/AUTHORIZATION.md and COMPLETION.md. Source S83 contains the explicitly authorized privacy procedural specialization. Earlier requests to approve observation-aware correlation are historical and satisfied. Existing four decisions and successor construction remain authorized.

Run verify-update.py for document-only checks of the updated candidate. No repository, .env, historical constructor, live source, appointment or lifecycle action is used. PASS means bounded author construction verified, not admission. See acceptance-defects.tsv and the preserved public-root failure vector before making any readiness claim. The graph-template and observer-source gaps are explicit; no public-linkage exception has been added.
''')
print('Integrated S83, approved source delta and unchanged-policy boundary.')
