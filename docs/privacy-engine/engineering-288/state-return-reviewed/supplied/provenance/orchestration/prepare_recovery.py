import hashlib,json,runpy,sys
from pathlib import Path
base=Path(__file__).resolve().parents[1]
root=base/'state-return'
ns=runpy.run_path(str(root/'tools/checkpoint.py'),run_name='_packaging_only')
enc=ns['enc'];ident=ns['identity']
review=json.loads((root/'provenance/input-verification.json').read_bytes())
receipt=json.loads((root/'provenance/previous-git-receipt.json').read_bytes())
dependencies={
 'config_checkpoint':dict(review['config_archive'],entries=review['config_entries'],decoded_root='retained/config'),
 'config_independent_review':dict(review['review'],entries=review['review_entries'],compact_root='retained/config-review',external_preservation_dependencies=review['omitted_review_decoded_members_retained_external']),
 'prior_support':{'Engineering':{'primary':127,'recovered':105,'process_results':'retained, not rerun'},'Formal-Lab':{'primary':146,'recovered':62,'static_type_audit':'retained','offline_command':'retained'},'failed_attempts':'Retained separately; excluded from completed assertion totals'},
 'runtime_getter_observations':'UNAVAILABLE',
 'prior_successful_git_save':{'receipt':ident((root/'provenance/previous-git-receipt.json').read_bytes()),'commit':'16ece61efdb4189b9edcac1baf67759f49ca0232','new_save_performed':False},
 'current_independent_review':'PENDING',
 'executable_inputs':'All present in decoded predecessor; external large artifacts preserve prior archival failures only.'}
(root/'DEPENDENCIES.json').write_bytes(enc(dependencies))
files={n:b for n,b in ns['inventory'](root).items() if not n.startswith('results/primary/')}
target=base/'state-tools/recovery-input.zip';out=ns['pack'](files,target)
recovered=base/'state-tools/recovered-root';ns['verify'](target,recovered)
record={'identity':out,'construction':'Stable new code, controls, docs, exact retained inputs and saved receipt; excludes primary in-progress results and subsequent result metadata.','extraction':'separate new root','intermediate_not_final_checkpoint':True}
(root/'results/recovery-input.json').write_bytes(enc(record))
print(json.dumps(record,sort_keys=True))
