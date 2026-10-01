from pathlib import Path
import csv,json,io,hashlib,shutil
O=Path('PE-G4-public-relationships')
def wr(p,s):
 q=O/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(s.rstrip()+'\n')
def js(p,v):wr(p,json.dumps(v,indent=2))
def rr(p):return list(csv.DictReader((O/p).open(),delimiter='\t'))
def tb(p,rs):
 f=io.StringIO();w=csv.DictWriter(f,list(rs[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rs);wr(p,f.getvalue())
sha=lambda b:hashlib.sha256(b).hexdigest()
wr('privacy/PUBLIC-RELATIONSHIP-AUTHORIZATION.md','''# Approved bounded public relationships

On 29 September 2026 the assistant asked whether unpublished G4 may explicitly permit: same root within its authenticated membership scope; same a as a shared public action context; and same (a,n) for duplicate recognition within that action context. It explicitly excluded actor identification, cross-action nullifier tracking and removal of any actor-graph edge, and retained full composition assessment.

The user's response was “approved”. This authorizes exactly those three bounded relationships. It supersedes the earlier no-new-exceptions instruction only for these relationships. Observation-aware correlation, full actor protection, unknown-visibility failure, the original four decisions and successor construction remain authorized. Do not ask these decisions again.

This is an unpublished semantic construction authorization, not source appointment, evidence signing, independent acceptance, profile admission, publication, registry insertion, implementation adoption or deployment.
''')
# Historical status cannot remain the active decision record.
shutil.copyfile(O/'privacy/KNOWN-PUBLIC-ROOT-BOUNDARY.md',O/'evidence/public-root-boundary-before-approval.md')
wr('privacy/KNOWN-PUBLIC-ROOT-BOUNDARY.md','''# Shared-root policy boundary resolved within approved scope

The previously demonstrated blanket shared-root rejection is superseded by the explicit public-relationship approval. S84 permits only equality of public root-role values with the same independently authenticated source meaning and membership scope. The value remains a changing root, never a generation constant. Different scope/source meanings, missing binding evidence, cross-role scalar equality, independent correlation paths and actor-reconstruction paths remain failures.

The approved action-context and action-local duplicate relationships are integrated in the same source, preventing a sequence of separate public-input exception requests. This resolves the identified policy conflict for these scoped relationships; it does not establish full privacy admission or source evidence.
''')
clauses=[('root','MAY','Equality of public r values MAY express only their shared membership-root relationship when both exact canonical root values and independently authenticated owning source meaning and membership scope agree.'),('action','MAY','Equality of public a values MAY express only a shared public action context when both exact canonical values and independently authenticated owning action-context meaning and scope agree.'),('duplicate','MAY','Equality of public n values MAY express duplicate recognition only as equality of the scoped pair (a,n), with the same independently authenticated action-context meaning, exact a value and owning uniqueness scope; it MUST NOT permit a cross-action nullifier join.'),('bindings','MUST','Each permitted public relationship MUST bind the exact declared public-input role, canonical in-domain scalar bytes, occurrence-local field identity and independently authenticated source/scope references; missing or inconsistent binding evidence MUST fail without granting the permission.'),('preservation','MUST','These permissions MUST apply only to the matching public equality checks for uniqueness and observer-visible correlation; every edge MUST remain in actor reconstruction, and no permission MUST clear an independent correlation path, create a reusable participant identifier or grant an actor-identification relationship.')]
source='''# PE-G4-SOURCE-S84 — approved bounded public-input relationships

Status: unpublished construction candidate, not appointed or admitted. The exact approval basis is privacy/PUBLIC-RELATIONSHIP-AUTHORIZATION.md. This source specializes S83#no-exceptions only for the three approved public relationships and their corresponding public uniqueness checks. The other S83 duties remain active. The published G3 sources remain byte-exact.

The unchanged PRIV-003 obligation expressly allows a narrower non-identifying public relationship when defined by the governing published generation. This candidate supplies the proposed successor definitions; publication has not occurred. No current deployed behavior is authorized by this construction.

'''
for anchor,strength,text in clauses:source+=f'<a id="{anchor}"></a>\n## {anchor}\n\n{text}\n\n'
source+='''<a id="binding-schema"></a>
## Exact source-established binding schema

One binding per declared public PI surface uses exactly: role, owner_source_id, source_sha256, source_anchor, scope_id, value_hex, action_node. role is n, a or r. The graph token's internal template key is context::PUBLIC-PI:role, bound to its actual context; it creates no new protocol subject. The token remains PUBLIC with reuse NONE. value_hex is one complete canonical TSEV1 PE-TSE-UINT value in [0,p), and its SHA-256 equals the token digest. The complete source reference and scope must be independently authenticated; spelling and equality cannot establish authority or scope truth.

For r and a, action_node is NOT-APPLICABLE. For n it identifies the a-role token of that same context. Both a tokens must have matching authenticated action-context domain and exact value before an n relationship is permitted. Both n tokens must independently have matching owning uniqueness domain. Neither r nor a permission is a proof of shared actor, common participant or global identity. Equal numerals belonging to different roles receive no permission.

The binding schema adds source-evidence metadata, not public proof inputs or new public disclosure. It must remain within its source-governed custody boundary and be included in complete evidence/source/observer composition. Full canonical privacy-member integration must bind these fields and their authentication evidence before admission. There is no trust-on-first-use and no caller flag which grants scope authority.

<a id="procedure"></a>
## Exact updated graph procedure

The exact newly authored graph subroutine follows. It is a subroutine of the full mandatory regeneration, source appointment, authentication, universe, visibility and failure-order pipeline; it does not itself verify source signatures or return a profile admission PASS. Missing, inconsistent or out-of-domain role bindings fail. Scope and values are compared exactly, never modulo p. A relationship permission removes only its matching EQUALS edge from the correlation test and its matching pair from the blanket public-uniqueness rejection. It never deletes any edge from the actor graph. Visibility, coalition and alternative-path checks remain mandatory.

The original unbound-root negative vector remains valid: without the required role/source binding no exception exists. The new scoped vectors establish the permitted cases and retained failures. No synthetic source identity in these vectors appoints a real source.

```python
'''+(O/'privacy/observation_correlation.py').read_text()+'```\n'
wr('sources/PE-G4-SOURCE-S84.md',source)
inv=rr('composition/source-inventory.tsv');inv.append({'source_id':'PE-G4-SOURCE-S84','path':'sources/PE-G4-SOURCE-S84.md','sha256':sha((O/'sources/PE-G4-SOURCE-S84.md').read_bytes()),'basis_id':'EXPLICIT-USER-APPROVED-PUBLIC-RELATIONSHIPS','basis_sha256':'NOT-APPLICABLE','mode':'APPROVED-SCOPED-PUBLIC-RELATIONSHIPS','root_anchor':'ROOT:PE-G4-SOURCE-S84','status':'CANDIDATE-NOT-APPOINTED'});tb('composition/source-inventory.tsv',inv)
req=json.loads((O/'composition/requirement-inventory.json').read_text());new=[]
for i,(anchor,strength,text) in enumerate(clauses,71):
 r={'requirement_id':f'PE-G4-CAP-{i:03}','basis_requirement_id':'USER-APPROVED-BOUNDED-PUBLIC-RELATIONSHIPS','requirement_family':'RF-11','strength':strength,'applicability':'conditional','scope':'Only the three approved G4 public-input relationships, with exact source/scope bindings','text':text,'owner_sources':'PE-G4-SOURCE-S84#'+anchor,'supporting_references':'PE-G4-PRIV-003, PE-G4-SOURCE-S83','treatment':'APPROVED-SCOPED-PUBLIC-RELATIONSHIP'};new.append(r);req.append(r)
js('composition/requirement-inventory.json',req);js('composition/public-relationship-requirement-delta.json',new)
p=O/'PE-PROTOCOL-SPECIFICATION-G4.candidate.md';s=p.read_text().replace('Neither 931 homes','Neither 936 homes');s+='\n## RF-11 — approved bounded public relationships\n\nFive source-scoped homes supplement the original 931; current total 936. S84 specializes S83\'s no-exceptions rule only as explicitly approved. No publication or conformance admission is asserted.\n\n| Requirement | Strength | Applicability | Scope | Normative text | Owner source | Supporting references |\n|---|---|---|---|---|---|---|\n'
for r in new:s+='| <a id="'+r['requirement_id'].lower()+'"></a> '+r['requirement_id']+' | '+' | '.join(r[k] for k in ('strength','applicability','scope','text','owner_sources','supporting_references'))+' |\n'
p.write_text(s)
fam=rr('composition/family-composition.tsv')
for r in fam:
 if r['requirement_family']=='RF-11':r['candidate_delta_homes']=str(int(r['candidate_delta_homes'])+5)
tb('composition/family-composition.tsv',fam)
p=O/'verify-candidate.py';s=p.read_text().replace("'81 unique source identities',len(source)==len(inventory)==81","'82 unique source identities',len(source)==len(inventory)==82").replace("'931 unique candidate normative homes',len(reqdict)==len(req)==931","'936 unique candidate normative homes',len(reqdict)==len(req)==936");p.write_text(s)
p=O/'verify-update.py';s=p.read_text();s=s.replace("assert (O/'privacy/observation_correlation.py').read_text() in (O/s83['path']).read_text()", "s84=next(r for r in inv if r['source_id']=='PE-G4-SOURCE-S84')\nassert hashlib.sha256((O/s84['path']).read_bytes()).hexdigest()==s84['sha256']\nassert (O/'privacy/observation_correlation.py').read_text() in (O/s84['path']).read_text()")
s=s.replace("assert len(req)==931 and [r['requirement_id'] for r in req[-5:]]==[f'PE-G4-CAP-{i:03}' for i in range(66,71)]", "assert len(req)==936 and [r['requirement_id'] for r in req[-5:]]==[f'PE-G4-CAP-{i:03}' for i in range(71,76)]")
s=s.replace("report={'author_checks'", "with contextlib.redirect_stdout(io.StringIO()):relationship_results=runpy.run_path(str(O/'privacy/test_public_relationships.py'))['results']\nassert len(relationship_results)==21\nreport={'author_checks'")
s=s.replace("'public_linkage_exceptions_added':False", "'public_relationship_permissions':['SAME-SCOPED-ROOT','SAME-SCOPED-A','SAME-SCOPED-A-N'], 'relationship_vectors':relationship_results")
s=s.replace("print('BOUNDARY — shared public root still fails uniqueness and correlation; no exception added.')", "print('PASS — 21 scoped relationship vectors; approved root, action and duplicate cases pass.')\nprint('PASS — cross-action nullifier links and actor-reconstruction paths remain rejected.')")
p.write_text(s)
# Exact approval changes the identified boundary; retain its former report as evidence.
defects=rr('acceptance-defects.tsv')
for r in defects:
 if r['id']=='G4-P01':
  r['kind']='RESOLVED-WITHIN-APPROVED-SCOPE';r['defect']='Blanket shared-root rejection is replaced by the three explicit S84 scoped public relationships; no wider equality exception exists.';r['closure_evidence']='21 scoped vectors plus 12 retained graph vectors passed. Real source/observer evidence and full composition remain admission gates.';r['needs_new_user_policy']='Approval recorded; do not ask again.'
tb('acceptance-defects.tsv',defects)
identity=json.loads((O/'identity.json').read_text());identity['candidate_revision']='SCOPED-PUBLIC-RELATIONSHIPS-INTEGRATED';identity['approved_public_relationship_source']='PE-G4-SOURCE-S84';js('identity.json',identity)
wr('COMPLETION.md','''# G4 approved public relationships integrated

The user-approved same-root, same-a and same-(a,n) relationships are integrated in unpublished source S84 with exact source/scope/value binding checks. The earlier no-exceptions rule is specialized only for these three cases. Root and action values remain public PI, not generation constants. No new actor identity, proof input, public trace, provider or appointment is introduced.

Correctly scoped shared roots, shared action contexts and action-local duplicates now pass the bounded graph checks. Different root/action/uniqueness domains, cross-action nullifier equality, absent bindings, mismatched bytes, out-of-domain values, cross-role scalar collisions and attempts to reclassify unrelated subjects fail. Alternative correlation paths remain failures. Every permitted edge remains in the full actor graph; an actor-reconstruction bridge still fails.

The identified G4-P01 policy boundary is resolved within that exact approved scope. Twelve previous graph vectors and twenty-one new relationship vectors pass. The declared 118-field model regenerates exactly. These are bounded author-construction results, not independently authenticated source facts, full-profile privacy acceptance or publication.

The original 861 inherited requirements retain their exact text, scope and strength. Five new scoped relationship homes bring the current candidate inventory to 936 homes and 82 source members. Counts are not readiness evidence. S84 explicitly states the approved specialization of S83 and the inherited privacy procedures.

Remaining work is unchanged and explicit: source-complete coordinates/materiality; concrete producer dependency/observer/custody closure; full canonical privacy/evidence integration including role-binding metadata and equality expansion; independently appointed source/privacy evidence. No complete canonical profile or admitted mapping exists yet. The repository and all published generations remain unchanged. The approvals persist; no repeat policy ballot or numbered handover is required.
''')
wr('START-HERE.md','''# Continue Engineering[286] — approved scoped public relationships integrated

Read WORKING-RULE.md, privacy/PUBLIC-RELATIONSHIP-AUTHORIZATION.md and COMPLETION.md. Active S84 now specializes S83's earlier no-new-exceptions instruction only for the explicitly approved root/action/duplicate relationships. Earlier negative unbound-root vectors remain evidence and still fail without exact source bindings. Do not confuse their historical status with the new scoped permission.

Run verify-update.py for documentary checks. PASS is not independent privacy admission. Remaining C01-C04/A01 construction and authority gates remain explicit in acceptance-defects.tsv; G4-P01 is resolved within its approved scope. Keep working here without re-requesting the recorded decisions. No historical constructor, repository edit, .env access, source appointment, publication, deployment or registry insertion is performed.
''')
# Small exact source-data schema for subsequent canonical evidence integration.
tb('privacy/public-relationship-binding-schema.tsv',[{'field_order':f'{i:04}','field':name,'domain':domain,'source':'PE-G4-SOURCE-S84#binding-schema'} for i,(name,domain) in enumerate([('role','n|a|r'),('owner_source_id','Independently authenticated owning source identifier'),('source_sha256','64 lowercase hex; exact owning source bytes'),('source_anchor','Exact adequate owning anchor'),('scope_id','Exact source-owned role scope'),('value_hex','Complete canonical in-domain TSEV1 UINT bytes'),('action_node','Same-context public a node for n; NOT-APPLICABLE for r/a')],1)])
print('S84 integrated; scoped relationship boundary resolved in candidate.')
