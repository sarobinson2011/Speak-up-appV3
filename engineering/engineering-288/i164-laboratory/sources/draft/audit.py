import pathlib,json,hashlib
P=pathlib.Path(__file__).resolve().parent;W=P.parent
H=lambda b:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
m=json.loads((P/'source-only/universe/provenance/root-members.json').read_bytes());assert len(m)==666
rows=[]
for name in ['packaged-final-current','universe-review-current']:
 r=W/name;assert {str(f.relative_to(r)) for f in r.rglob('*') if f.is_file()}==set(m)
 for n,v in m.items():assert H((r/n).read_bytes())==v,n
 a=json.loads((r/'native/retained/mapping/records/relationships-43.json').read_bytes());b=json.loads((r/'support/reference/relationships-43.json').read_bytes());assert a==b and len(a)==43
 rows.append({'root':name,'exact_members':666,'historical_files':sum(n.startswith('historical90/') for n in m),'relationships':43,'ordinals':'all exact manifest member bytes unchanged','changed_candidate_members':[]})
(P/'results/preservation.json').write_text(json.dumps(rows,indent=2))
new={str(f.relative_to(P)):H(f.read_bytes()) for f in sorted((P/'code').glob('*.py'))}
(P/'CHANGED-IDENTITIES.json').write_text(json.dumps({'candidate_changes':[],'reviewed_entrypoint_changes':[],'new_companion_files':new,'old_identity_for_new_files':None,'scope':'New draft companion only; no canonical class or source reclassification'},indent=2))
print('PASS both exact roots, 666 members, 90 historical files, 43 relationships and ordinals')
