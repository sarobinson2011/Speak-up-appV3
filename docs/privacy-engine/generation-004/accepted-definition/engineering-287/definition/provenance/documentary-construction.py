"""Fresh documentary construction only. No imported historical constructor executes."""
from pathlib import Path
import csv,json,re,hashlib,shutil,io,zipfile
S=Path('Engineering-286-source-closure'); O=Path('PE-G4-successor-candidate');O.mkdir(exist_ok=True)
def h(b):return hashlib.sha256(b).hexdigest()
def write(n,t):
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t.rstrip()+'\n')
def js(n,x):write(n,json.dumps(x,ensure_ascii=False,indent=2))
def cp(p,n):
 q=O/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
def readtab(p):return list(csv.DictReader(p.open(),delimiter='\t'))
def tabtext(rows):
 f=io.StringIO();w=csv.DictWriter(f,list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows);return f.getvalue()
def tab(n,rows):write(n,tabtext(rows))
oldreg=json.loads((S/'composed-sources/source-register.json').read_text())
ids={v:f'PE-G4-SOURCE-S{i}' for i,v in enumerate(oldreg,73)}
# Explicit finite identifier map; generic PE-TSE names and component IDs are unchanged.
texts='\n'.join(p.read_text() for p in (S/'supporting-program').iterdir() if p.is_file())
for token in set(re.findall(r'E28[34]-DRAFT-[A-Z0-9-]+',texts)):
 if token not in ids:ids[token]='PE-G4-CAP-'+re.sub(r'^E28[34]-DRAFT-','',token)
assert len(ids.values())==len(set(ids.values()))
def rename(t):
 return re.sub(r'E28[34]-DRAFT-[A-Z0-9-]+',lambda m:ids.get(m[0],m[0]),t)
# Include complete previous bounded source packet as evidence; active artifacts are separate.
shutil.copytree(S,O/'basis/Engineering-286-source-closure',dirs_exist_ok=True)
cp(Path('SU-Engineering-standing-working-rule.md'),'WORKING-RULE.md')
js('identity.json',{'generation_id':'PE-PROTOCOL-GENERATION-004','label':'G4','namespace':'PE-G4','version':'4.0.0','specification_id':'PE-PROTOCOL-SPECIFICATION-G4','predecessor_basis':'PE-PROTOCOL-GENERATION-003','mapping_candidate_id':'PE-G4-TMAP-000001','profile_candidate_id':'PE-G4-TSE-PROFILE-000001-V0001','registry_identity_reserved_for_candidate':'PE-G4-TRANSITION-MAPPING-REGISTRY-001','status':'UNPUBLISHED-CONSTRUCTION-CANDIDATE','published':False,'succession_performed':False,'profile_admitted':False,'registry_inserted':False,'collision_scope':'Supplied Engineering[286] source and evidence only; no global uniqueness claim.'})
write('AUTHORIZATION.md','''# Construction authorization in Engineering[286]

User instruction: “successor construction authorized. proceed”. This authorizes the exact unpublished successor identity/composition and selected mapping/profile candidate construction in the preceding DECISION.md. The prior decision request is satisfied and must not be asked again.

The four decisions remain fixed: latest sixteen valid root-introduction occurrences; one required successful atomic scoped unused-to-used effect; distinct A for each new authoritative admission; strict canonical scalar-domain assessment before admission. No new policy ballot is opened.

This record is a transcript-based authoring record, not an independent signature, source appointment, privacy appointment, profile admission, publication or succession record. No such excluded lifecycle action is performed. No live occurrence facts are invented. Work stays in Engineering[286].
''')
tab('composition/identifier-map.tsv',[{'original_id':a,'candidate_id':b,'treatment':'explicit alpha-renaming; no semantic replacement'} for a,b in sorted(ids.items())])
source_rows=[]
for i in range(3,73):
 p=S/f'baseline/sources/S{i:02}.md';n=f'sources/retained/S{i:02}.md';cp(p,n)
 source_rows.append({'source_id':f'PE-G4-SOURCE-S{i:02}','path':n,'sha256':h(p.read_bytes()),'basis_id':f'PE-G3-SOURCE-S{i:02}','basis_sha256':h(p.read_bytes()),'mode':'EXACT-BY-REFERENCE','root_anchor':f'ROOT:PE-G4-SOURCE-S{i:02}','status':'CANDIDATE-NOT-APPOINTED'})
source_text={}
for a,b in oldreg.items():
 sid=ids[a];raw=(S/b['file']).read_text()
 # Original narrative is visibly retained as history; status overlay is explicit.
 source_text[sid]=(f'# {sid} — unpublished G4 source candidate\n\n'
 'Status: candidate construction, not appointed or published. The following inherited authoring narrative is preserved with explicit identifier substitution. Its references to unallocated identities and earlier chat status are historical; identity.json and sources/PE-G4-SOURCE-S82.md govern this candidate. No compatible semantic duty is waived.\n\n'+rename(raw))
# Freeze action source before constructing source-reference literals. It has no program definitions.
sid='PE-G4-SOURCE-S76';write(f'sources/{sid}.md',source_text[sid]);action_hash=h((O/f'sources/{sid}.md').read_bytes())
# Fresh TSEV1 serializer for declared literals, not a runtime/source-acceptance implementation.
def val(t,k,body):return b'TSEV1'+len(t).to_bytes(4,'big')+t.encode()+bytes([k])+len(body).to_bytes(8,'big')+body
def ident(s):return val('PE-TSE-ID',2,s.encode())
def sequence(t,vs,k=17):return val(t,k,len(vs).to_bytes(4,'big')+b''.join(len(v).to_bytes(8,'big')+v for v in vs))
def recode(data):
 assert data[:5]==b'TSEV1';z=int.from_bytes(data[5:9],'big');t=data[9:9+z].decode();k=data[9+z];n=int.from_bytes(data[10+z:18+z],'big');body=data[18+z:];assert n==len(body)
 if k in (16,17):
  count=int.from_bytes(body[:4],'big');p=4;children=[]
  for _ in range(count):
   size=int.from_bytes(body[p:p+8],'big');p+=8;children.append(recode(body[p:p+size]));p+=size
  assert p==len(body)
  if k==16:children.sort()
  return sequence(rename(t),children,k)
 if k==2:body=rename(body.decode()).encode()
 return val(rename(t),k,body)
def transformtext(t):
 # Embedded type names in literal bytes require re-encoding length prefixes.
 t=re.sub(r'literal\(([^,]+),([0-9a-f]+)\)',lambda m:'literal('+rename(m[1])+','+recode(bytes.fromhex(m[2])).hex()+')',t)
 return rename(t)
for p in (S/'supporting-program').iterdir():
 if p.is_file():write('profile/fragments/'+p.name,transformtext(p.read_text()))
P=O/'profile/fragments';types=readtab(P/'types.tsv');defs=readtab(P/'definitions.tsv');recovery=readtab(P/'recovery.tsv')
recoveryfields=[x for x in recovery[0] if x!='recovery_order'];assert len(recoveryfields)==11
for t,kind,element,fields in [('PE-G4-CAP-RECOVERY-ROW','TUPLE','NOT-APPLICABLE',','.join(['PE-TSE-ID']*11)),('PE-G4-CAP-RECOVERY-ROW-SET','SET','PE-G4-CAP-RECOVERY-ROW','NOT-APPLICABLE')]:
 types.append(dict(zip(types[0], [f'{len(types)+1:04}',t,kind,element,fields])))
def adddef(name,kind,inputs,output,expr,owner,anchor):defs.append(dict(zip(defs[0],[f'{len(defs)+1:04}',name,kind,inputs,output,expr,owner,anchor])))
def source_literal(anchor):
 t='PE-G4-CAP-SOURCE-REFERENCE';v=sequence(t,[ident(sid),val('PE-TSE-BYTES',1,bytes.fromhex(action_hash)),ident(anchor)]);return f'literal({t},{v.hex()})'
adddef('PE-G4-CAP-APPLICABILITY','CONDITION','PE-G4-CAP-SOURCE-REFERENCE,PE-G4-CAP-SOURCE-REFERENCE,PE-TSE-UINT,PE-TSE-UINT,PE-G4-CAP-SCOPED-STATE','PE-TSE-BOOL3',f'and(equal(arg(0001),{source_literal("action-type")}),equal(arg(0002),{source_literal("rules")}),apply(PE-G4-CAP-IS-SOURCE,arg(0003),arg(0004),arg(0005)))','PE-G4-SOURCE-S73','applicability')
lits=[]
for row in recovery:
 b=sequence('PE-G4-CAP-RECOVERY-ROW',[ident(row[k]) for k in recoveryfields]);lits.append('literal(PE-G4-CAP-RECOVERY-ROW,'+b.hex()+')')
adddef('PE-G4-CAP-RECOVERY-ROWS','SET','NONE','PE-G4-CAP-RECOVERY-ROW-SET','apply(PE-TSE-SET,'+','.join(lits)+')','PE-G4-SOURCE-S75','recovery-relation')
adddef('PE-G4-CAP-RECOVERY','CONDITION',','.join(['PE-TSE-ID']*11),'PE-TSE-BOOL3','member(tuple(PE-G4-CAP-RECOVERY-ROW,'+','.join(f'arg({i:04})' for i in range(1,12))+'),PE-G4-CAP-RECOVERY-ROWS)','PE-G4-SOURCE-S75','recovery-relation')
source_text['PE-G4-SOURCE-S73']+='''\n<a id="applicability"></a>
## Exact candidate applicability definition

PE-G4-CAP-APPLICABILITY has ordered inputs (type source reference, rule-set source reference, a, n, Q0). Its expression tests exact byte-bound references to S76 action-type and rules and Q0=(a,n,FALSE). It is a mapping applicability predicate within the independently validated domain, not a proof of complete R, source competence, scalar bounds, privacy, an accepting D or authorization. Those antecedents remain mandatory admission/context checks. No caller chooses the expected references: the literals bind the actual S76 bytes in this candidate.

A TRUE result alone never permits E, authorization, execution or commitment. The rule source explicitly requires every additionally applicable rule resolved before E. That obligation is preserved, rather than replaced with a TRUE default. The mapping candidate remains blocked wherever its material/source conditions are unclosed.
'''
source_text['PE-G4-SOURCE-S75']+='''\n<a id="recovery-relation"></a>
## Exact candidate recovery relation

PE-G4-CAP-RECOVERY validates an entire recovery row, not merely a recognized event. Its eleven ordered ID inputs are stage, event, unchanged_d_sufficiency, u_classification, authorization_disposition, evaluation_required, determination_required, authorization_required, u_required, execute_permission, commit_permission. TRUE means this entire tuple equals one of the twenty-one unchanged governing rows. A changed disposition fails even for a recognized event. It does not establish unchanged-D sufficiency, select an event, revive failed U or authorize an occurrence. Actual independently established inputs determine the unique governing row; its exact disposition and the selected A/E/D overlay then apply. No new recovery event or outcome subject is introduced.
'''
# Own the exact declarations at their source anchors, without circular self-hash literals.
for owner in source_text:
 owned=[d for d in defs if d['source_id']==owner]
 if owned:
  source_text[owner]+='\n## Exact source-owned definition declarations\n\nThe following declarations specialize the retained PE-TSE-EXPR-V2 grammar. The source_anchor column identifies the semantic clause above. They are construction candidates, not independently admitted declarations.\n\n```tsv\n'+tabtext(owned)+'```\n'
 if owner=='PE-G4-SOURCE-S73':source_text[owner]+='\n## Exact type declarations\n\n```tsv\n'+tabtext(types)+'```\n'
 write(f'sources/{owner}.md',source_text[owner])
assert h((O/'sources/PE-G4-SOURCE-S76.md').read_bytes())==action_hash
for a,v in oldreg.items():
 b=ids[a];p=f'sources/{b}.md';source_rows.append({'source_id':b,'path':p,'sha256':h((O/p).read_bytes()),'basis_id':a,'basis_sha256':v['sha256'],'mode':'ALLOCATED-OWNER-WITH-EXPLICIT-DECLARATIONS','root_anchor':'ROOT:'+b,'status':'CANDIDATE-NOT-APPOINTED'})
write('sources/PE-G4-SOURCE-S82.md','''# PE-G4-SOURCE-S82 — candidate composition and generation binding

<a id="identity"></a>
## Candidate identity

This unpublished construction binds generation PE-PROTOCOL-GENERATION-004, namespace PE-G4, version 4.0.0, specification PE-PROTOCOL-SPECIFICATION-G4. It has no published successor status. G3 remains immutable. Allocation was authorized by the user; source appointment, publication and admission were not.

<a id="composition"></a>
## Exact composition

The source inventory has seventy retained byte-exact source members by reference, nine allocated capability owners and this binding source. ROOT:SOURCE-ID denotes the whole registered byte span; original named anchors continue to identify the unchanged section span. Retained internal labels, historical narrative, example fixtures and historical M=0 construction counts remain documentary history. They do not impose old identities or an empty registry on the new candidate.

Only the active generation-dependent schema parameters are bound to G4: SUCCESSOR-GENERATION-ID, active protocol namespace, registry identifier, mapping/profile identity grammar and their same-ordinal joins. Thus active mapping grammar is PE-G4-TMAP-{NNNNNN}; profile grammar is PE-G4-TSE-PROFILE-{NNNNNN}-V0001; registry identity is PE-G4-TRANSITION-MAPPING-REGISTRY-001. Generic PE-TSE identifiers, canonical encodings, expression grammar, hash algorithms, admission checks, evidence and privacy obligations remain unchanged. No historical source file or source algorithm is executed or edited. Before using inherited validator notation in a future realization its active generation parameters must be bound explicitly; unmodified hard-coded G3 validators cannot validate this candidate. No global blind replacement of historical names is licensed.

The explicit identifier map allocates capability definitions, fields and owner identities. Original requirement IDs are translated one-to-one PE-G3 to PE-G4 while their text, strength, scope and applicability remain exact. Supporting artifact references retain their G3 identifiers where they name historical evidence; they do not assert a fabricated G4 artifact. Each inherited requirement has one home in the candidate specification. The reviewed delta register has 97 sentence units: preserved-obligation restatements reference inherited homes; new/qualified/adapter modal sentences get candidate CAP homes; explanatory sentences remain attached source interpretation. Multi-modal sentences retain their full text and all modalities, matching the retained inventory's sentence-level convention. No claim of 97 new requirements is made.

<a id="scope"></a>
## Status and precedence

The retained baseline constrains all new capability clauses. The four selected policies add their exact reviewed scope. Adapter-only duties remain conditional on selection of that adapter. SHALL in the two retained adapter clauses has mandatory force only in that scope; their wording is not silently changed. The complete profile admission procedure and every independently applicable material condition still govern. Formal type/definition declarations are source-owned supporting definitions, not an alternative normative requirement set.

No new actor subject, public input, public trace, host-call primitive, failure/result subject, provider appointment, shared-chain requirement, lock requirement or total-map FALSE default is created. Ordering-coordinate NONE in the bounded projection remains an unresolved completeness marker and cannot be serialized as a proved-empty full profile. No registry file, canonical outer profile container or profile digest is fabricated before complete admission inputs exist. The intended mapping target is one selected effect; a zero-mapping successor is not substituted for it.
''')
p='sources/PE-G4-SOURCE-S82.md';source_rows.append({'source_id':'PE-G4-SOURCE-S82','path':p,'sha256':h((O/p).read_bytes()),'basis_id':'AUTHORIZED-CONSTRUCTION','basis_sha256':'NOT-APPLICABLE','mode':'EXPLICIT-COMPOSITION-BINDING','root_anchor':'ROOT:PE-G4-SOURCE-S82','status':'CANDIDATE-NOT-APPOINTED'})
tab('composition/source-inventory.tsv',source_rows)
tab('profile/fragments/types.tsv',types);tab('profile/fragments/definitions.tsv',defs)
ops=readtab(P/'operations.tsv');edges=readtab(P/'operation-edges.tsv')
# Preserve existing operation IDs and topology; insert new definition operations before component stages.
for d in defs[53:]:
 order=int(d['definition_order']);opid=f'PE-TSE-OP-DEFINITION-{order:04}'
 calls=[]
 for callee in re.findall(r'(?:apply|member)\(([^,()]+)',d['expression']):
  # member's first argument is tuple, so separately collect its final SET target below.
  if callee in {z['definition_id'] for z in defs}:calls.append(callee)
 if d['definition_id']=='PE-G4-CAP-RECOVERY':calls.append('PE-G4-CAP-RECOVERY-ROWS')
 callids=sorted({f"PE-TSE-OP-DEFINITION-{next(z['definition_order'] for z in defs if z['definition_id']==c)}" for c in calls})
 op={'operation_order':'','operation_id':opid,'operation_kind':'DEFINITION','expression_owner_id':d['definition_id'],'permitted_read_field_ids':'NONE','permitted_call_operation_ids':','.join(callids) or 'NONE','owner_source_id':d['source_id'],'owner_anchor':d['source_anchor']}
 ops.insert(order,op)
 for c in callids:edges.append({'caller_operation_id':opid,'callee_operation_id':c})
for i,row in enumerate(ops,1):row['operation_order']=f'{i:04}'
tab('profile/fragments/operations.tsv',ops);tab('profile/fragments/operation-edges.tsv',edges)
proj=readtab(P/'BOUNDED-NOT-ADMITTED-projection.tsv');sourcedict={r['source_id']:r for r in source_rows}
for row in proj:row['authoritative_source_sha256']=sourcedict[row['authoritative_source_id']]['sha256']
tab('profile/fragments/BOUNDED-NOT-ADMITTED-projection.tsv',proj)
scalars=[('profile-identifier','PE-G4-TSE-PROFILE-000001-V0001'),('profile-version','V0001'),('governing-successor-generation','PE-PROTOCOL-GENERATION-004'),('governing-mapping-identifier','PE-G4-TMAP-000001'),('profile-sha256-algorithm','SHA-256'),('projection-component-count','000002'),('definition-count',f'{len(defs):06}'),('equivalence-definition-id','PE-G4-CAP-EQ'),('material-conflict-definition-id','PE-G4-CAP-MC'),('applicability-definition-id','PE-G4-CAP-APPLICABILITY'),('determination-dependency-definition-id','PE-G4-CAP-COMPONENT-DEPENDENCY'),('comparison-timing-rule','PRE-EXECUTION-AND-SEMANTIC-COMMITMENT'),('execution-gate','EQUIVALENT-ONLY'),('commitment-gate','EQUIVALENT-ONLY'),('recovery-definition-id','PE-G4-CAP-RECOVERY'),('privacy-classification','MINIMUM-ACTION-BOUNDED-NON-ACTOR'),('observability-classification','PUBLIC-RESULT-ONLY-NON-AUTHORITATIVE-DIAGNOSTICS')]
write('profile/fragments/scalars.tsv',''.join(k+'\t'+v+'\n' for k,v in scalars))
js('mapping/PE-G4-TMAP-000001.candidate.json',{'mapping_id':'PE-G4-TMAP-000001','profile_id':'PE-G4-TSE-PROFILE-000001-V0001','generation_id':'PE-PROTOCOL-GENERATION-004','status':'UNPUBLISHED-NONADMITTED-CANDIDATE','action_type_source':{'source_id':'PE-G4-SOURCE-S76','sha256':action_hash,'anchor':'action-type'},'rule_set_source':{'source_id':'PE-G4-SOURCE-S76','sha256':action_hash,'anchor':'rules'},'applicability_definition_id':'PE-G4-CAP-APPLICABILITY','source_class_definition_id':'PE-G4-CAP-IS-SOURCE','successor_class_definition_id':'PE-G4-CAP-IS-SUCCESSOR','successor_relation_definition_id':'PE-G4-CAP-SUCCESSOR-RELATION','successor_relation_ordered_arguments':['a','n','Q0','Q1'],'state_type_id':'PE-G4-CAP-SCOPED-STATE','source_state':'(a,n,FALSE)','successor_state':'(a,n,TRUE)','frame':'All other scoped keys, membership/history and product state preserved. No stale snapshot restoration.','required_successful_effect_count':1,'accepted_no_transition_selected':False,'recovery_definition_id':'PE-G4-CAP-RECOVERY','profile_sha256':None,'profile_sha256_absence_reason':'Complete canonical outer container does not yet exist; fragment digests are not profile digests.','registry_row_created':False})
# Compose sealed inherited rows exactly; retain historical supporting references.
base=(S/'baseline/exact-861-published-rows.md').read_text().splitlines();assert len(base)==861
roles=json.loads((S/'evidence/retained/requirement-dispositions-861.json').read_text());rf={r['requirement_id']:r['requirement_family'] for r in roles}
reqs=[];rendered={}
for line in base:
 cells=[v.strip() for v in line.strip('|').split('|')];oldid=re.search(r'PE-G3-[A-Z0-9-]+',cells[0])[0];newid=oldid.replace('PE-G3-','PE-G4-')
 nr={'requirement_id':newid,'basis_requirement_id':oldid,'requirement_family':rf[oldid],'strength':cells[1],'applicability':cells[2],'scope':cells[3],'text':cells[4],'owner_sources':cells[5].replace('PE-G3-','PE-G4-'),'supporting_references':cells[6],'treatment':'INHERITED-EXACT-SEMANTICS'};reqs.append(nr)
 rendered[newid]='| <a id="'+newid.lower()+'"></a> '+newid+' | '+' | '.join([nr[k] for k in ['strength','applicability','scope','text','owner_sources','supporting_references']])+' |'
deltas=json.loads((S/'source-delta/normative-requirement-deltas.json').read_text());deltaindex=[];count=0
family={'root-window':'RF-18','root-padding':'RF-18','root-stages':'RF-30','effect-state':'RF-31','effect-required':'RF-28','effect-frame':'RF-30','admission-domain':'RF-20','admission-fixed':'RF-22','occurrence-new':'RF-20','occurrence-recovery':'RF-35','verifier-binding':'RF-17','verifier-negative':'RF-17','observation-scope':'RF-31','observation-cut':'RF-31','observation-joint':'RF-31','observation-phase':'RF-30','carrier-exact':'RF-12','adapter-validation':'RF-12','adapter-history':'RF-18','adapter-state':'RF-31','comparison-core':'RF-26'}
for d in deltas:
 coord=d['local_proposal_coordinate'];entry={'coordinate':coord,'classification':d['classification'],'exact_text':d['text'],'source_id':ids[d['owning_local_source']],'source_anchor':d['owning_anchor'],'basis_requirement_ids':d['preserved_requirement_basis'],'all_modalities':d['strengths']}
 if d['classification']=='PRESERVED-OBLIGATION':entry.update(disposition='SUPPORTING-RESTATEMENT-NO-SECOND-HOME',candidate_requirement_id=None)
 elif not d['strengths']:entry.update(disposition='SOURCE-INTERPRETATION-NO-INVENTED-MODALITY',candidate_requirement_id=None)
 else:
  count+=1;rid=f'PE-G4-CAP-{count:03}';mods=re.findall(r'MUST NOT|MUST|MAY|SHALL',d['text']);strength=mods[0].replace('SHALL','MUST')
  req={'requirement_id':rid,'basis_requirement_id':coord,'requirement_family':family[coord.split('/')[0]],'strength':strength,'applicability':'conditional','scope':d['scope'],'text':d['text'],'owner_sources':entry['source_id']+'#'+entry['source_anchor'],'supporting_references':', '.join(d['preserved_requirement_basis']),'treatment':d['classification']};reqs.append(req)
  rendered[rid]='| <a id="'+rid.lower()+'"></a> '+rid+' | '+' | '.join(req[k].replace('|','&#124;') for k in ['strength','applicability','scope','text','owner_sources','supporting_references'])+' |'
  entry.update(disposition='CANDIDATE-NORMATIVE-HOME',candidate_requirement_id=rid)
 deltaindex.append(entry)
assert count==65 and len(reqs)==926
js('composition/requirement-inventory.json',reqs);js('composition/delta-disposition-97.json',deltaindex)
families=[]
for l in Path('handover/baseline/evidence/E270-spec.md').read_text().splitlines():
 if l.startswith('| SF-'):
  c=[x.strip() for x in l.strip('|').split('|')];families.append((c[0],c[1],c[2]))
assert len(families)==50
spec='''# PE-PROTOCOL-SPECIFICATION-G4 — unpublished composition candidate\n\nVersion 4.0.0. Candidate source generation PE-PROTOCOL-GENERATION-004 is not published. This is not a completed published Protocol Specification or a conformance basis.\n\nAll 50 inherited requirement families in 16 section families are composed below. The 861 inherited requirement meanings are preserved exactly, with successor requirement/source identifiers and historical supporting references. The 65 additional candidate sentence homes include scoped qualifications and two optional-adapter representation duties. All 97 reviewed sentence units are accounted for in the delta disposition register; restatements and explanatory units do not manufacture new obligations. Formal source declarations and all admission/privacy requirements remain applicable.\n\nThe boundary is incomplete profile/materiality/privacy construction and absent independent appointment/admission, as precisely recorded in acceptance-defects.tsv. Neither 926 homes nor author checks establish normative admission or summit completion.\n\n'''
for sf,fr,title in families:
 spec+='## '+sf+' / '+fr+' — '+title+'\n\n| Requirement | Strength | Applicability | Scope | Normative text | Owner source | Supporting references |\n|---|---|---|---|---|---|---|\n'
 for q in reqs:
  if q['requirement_family']==fr:spec+=rendered[q['requirement_id']]+'\n'
 spec+='\n'
write('PE-PROTOCOL-SPECIFICATION-G4.candidate.md',spec)
tab('composition/family-composition.tsv',[{'section_family':sf,'requirement_family':fr,'title':title,'inherited':str(sum(q['requirement_family']==fr and q['treatment']=='INHERITED-EXACT-SEMANTICS' for q in reqs)),'candidate_delta_homes':str(sum(q['requirement_family']==fr and q['treatment']!='INHERITED-EXACT-SEMANTICS' for q in reqs))} for sf,fr,title in families])
js('profile/fragment-manifest.json',[{'path':str(p.relative_to(O)),'sha256':h(p.read_bytes()),'bytes':p.stat().st_size} for p in sorted(P.iterdir()) if p.is_file()])
write('profile/README.md','''# PE-G4-TSE-PROFILE-000001-V0001 — construction fragments

The seventeen scalar fields now name actual declared applicability and exact recovery-relation definitions. The program has nineteen types and fifty-six definitions. Applicability embeds the exact S76 source digest; recovery matches every semantic column of every unchanged row. Existing entry inputs, fields, component logic and recovery meanings are preserved under the explicit namespace map. Source declarations are physically present in their owning candidate modules.

This directory is not a canonical outer profile container. The bounded projection is still marked NOT ADMITTED: its context triple is not proof of complete scope/cut coordinates, and NONE ordering is not proof that no ordering coordinates are required. The component-dependency definition classifies included projection rows only; actual Dep(D) remains the complete replay-derived closure. Privacy/observability support functions propagate external established facts and cannot create them. A source module's hash is not an appointment.

The profile's required static privacy/composition evidence, independently appointed evidence chain, complete materiality/coordinate joins and resulting full container are not supplied by this construction. No dummy appointment/key, empty evidence, synthetic signature, source-status TRUE constant or invented full-profile hash is used. fragment-manifest.json binds fragments only. The mapping JSON is likewise an authoring candidate, not an admitted mapping or registry row.
''')
defects=[
 {'id':'G4-C01','kind':'UNFINISHED-CONSTRUCTION','artifact':'profile/fragments/BOUNDED-NOT-ADMITTED-projection.tsv','defect':'Ordering lists remain NONE as unclosed markers; context(a,n,r) omits mandatory source/scope/cut/phase joins. The prior serialization tuple was not a protocol ordering rule.','closure_evidence':'Source-owned complete coordinate definitions, exact signatures and projection/header joins; establish completeness or prove any empty coordinate set. No common chain/lock/finality may be invented.','needs_new_user_policy':'No new policy choice identified.'},
 {'id':'G4-C02','kind':'UNFINISHED-CONSTRUCTION','artifact':'profile/fragments plus basis supporting producer','defect':'Exact whole-capability source-acquisition/validation operation model and static privacy/composition/actor graph are not regenerated for the allocated sources. Prior conservative 405446-edge graph is not exact evidence.','closure_evidence':'Owned exact operation/field/control/data/group graph and evidence model, complete disclosure/custody mapping and independent replay/privacy acceptance. No pruning actor edges to force PASS.','needs_new_user_policy':'No new policy choice identified.'},
 {'id':'G4-C03','kind':'UNFINISHED-CONSTRUCTION','artifact':'sources/PE-G4-SOURCE-S76.md#rules and mapping candidate','defect':'Applicability expression now fixes the type/rule source and source-state class, but cannot itself prove that every source-required material condition is covered by the two-bit projection.','closure_evidence':'Close retained source-assignment/material-condition rows against complete coordinate/acquisition model; integrate any source-required material condition and verify comparison failure/coverage rows.','needs_new_user_policy':'No new policy choice identified.'},
 {'id':'G4-A01','kind':'ABSENT-INDEPENDENT-AUTHORITY','artifact':'Source and PRIVACY admission inputs','defect':'No competent source appointment or independent privacy evidence appointment/signature is asserted. User construction authorization is not such appointment.','closure_evidence':'Separately governed competent appointments and exact independently signed evidence for finalized bytes. This author may not self-appoint or sign as reviewer.','needs_new_user_policy':'Not another four-policy authorization; appointment/admission remains outside current scope.'},
 {'id':'G4-C04','kind':'DEPENDENT-CONSTRUCTION','artifact':'Canonical profile/mapping serialization','defect':'No full outer profile bytes or profile digest exist while coordinate/privacy sections and appointment inputs are absent. Mapping cannot bind a nonexistent digest.','closure_evidence':'After C01-C03 and required A01 inputs, serialize exact full profile, hash it, then mapping and admission evidence in governed order. No actual registry insertion is authorized.','needs_new_user_policy':'No new policy choice for byte construction.'},
 {'id':'G4-R01','kind':'FUTURE-OCCURRENCE-FACTS','artifact':'Real E/D/authorization/U source observations','defect':'No live occurrence, current source cut, full actual Dep(D), unchanged-D sufficiency or gate result exists in authoring.','closure_evidence':'Obtain independently authenticated real facts at the actual occurrence; never invent them to complete documentation.','needs_new_user_policy':'Not required to author this candidate.'}
]
tab('acceptance-defects.tsv',defects)
write('COMPLETION.md',f'''# Concrete successor construction — Engineering[286]

Constructed the unpublished G4 identity/composition candidate and designated mapping PE-G4-TMAP-000001 / profile PE-G4-TSE-PROFILE-000001-V0001. No new numbered handover is issued.

The concrete change is allocation plus a traceable composition: seventy exact retained sources, nine allocated capability owners, one explicit generation-binding source; all 861 inherited requirement meanings plus 65 scoped candidate sentence homes; every one of the 97 reviewed sentence units accounted for. Definitions and their exact source owners are physically joined. This is authoring progress, not independent acceptance.

Two previously absent schema definitions are now concrete. Applicability checks fixed byte-bound type/rule source references and scoped unused source state. Recovery validates all eleven semantic columns against the unchanged twenty-one-row function; a recognized event with an altered disposition is rejected. Every existing canonical literal is re-encoded where its embedded type identity changes. No old constructor or historical code was executed.

What remains is specific: finish source-owned scope/cut/phase coordinate and materiality joins; regenerate the exact full acquisition/dependency and privacy evidence model; obtain separately governed source/privacy authority before full admission. See acceptance-defects.tsv. These are separated from future runtime facts. The new definitions do not silently certify any of those obligations.

Current G3 remains immutable and M=0. G4's target remains the selected required effect; no empty-registry publication is substituted. No profile container, fake profile digest, appointment, independent signature, publication, succession, registry insertion or implementation adoption has occurred. The constructor authorization is already granted and persists. Continue unfinished construction here; do not ask for it again or count this package as summit completion.
''')
write('START-HERE.md','''# Continue Engineering[286] with the allocated successor candidate

Read WORKING-RULE.md, AUTHORIZATION.md, COMPLETION.md and acceptance-defects.tsv. Then use identity.json, composition/source-inventory.tsv, the candidate specification and mapping/profile construction fragments as the active candidate. basis/ is exact prior evidence, including historical status and already-satisfied decision requests; it does not revoke later user authorization.

The next authoring work is G4-C01/C02/C03 in this same task. C04 depends on those and authentic admission inputs. A01 is an authority boundary; R01 is future runtime evidence, not a drafting prerequisite. Do not turn any of them into a new numbered handover, re-run accepted policy reviews, execute historical constructors, edit repositories/STATE, read .env members, invent appointments or publish a zero-mapping substitute.
''')
print(json.dumps({'sources':len(source_rows),'requirements':len(reqs),'new_sentence_homes':count,'types':len(types),'definitions':len(defs),'operations':len(ops),'path':str(O.resolve())}))
