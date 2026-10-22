"""Focused nested output substitutions against the actual saved candidate example."""
import copy,gzip
from candidate_pipeline import *
r=ROOT/'integration/results';c=Candidate();e=parse((ROOT/'support/fixtures/ord-early.json').read_bytes(),200000000);x=parse(gzip.decompress((r/'ordinary-example.json.gz').read_bytes()),500000000);results=[]
def check(name,edit):
 b=copy.deepcopy(x);edit(b)
 try:c.validate_output(b,e)
 except Invalid as exc:results.append({'check':name,'result':'PASS','rejection':str(exc)});return
 raise AssertionError(name)
check('out-of-directory candidate class',lambda b:b['candidate_occurrences'][0].update({'class':'I164:UNDECLARED'}))
check('mixed symbolic context',lambda b:b.update({'context':'SYMBOLIC-U-TWO'}))
check('nested response request binding',lambda b:b['response_associations'][0]['authenticated_association'].update({'request_hash':'0'*64}))
check('derived framing wrong exact type',lambda b:b['derived_framing'][0].update({'exact_bytes_hex':enc(1).hex()}))
check('signature value substitution',lambda b:next(z for z in b['supporting_pipeline']['actual_occurrences'] if z['record']=='RESPONSE' and z['pointer']=='/signature').update({'exact_bytes_hex':enc('forged').hex()}))
check('missing ancestry association',lambda b:b['association_index'].pop(0))
(r/'output-mutations.json').write_bytes(enc({'count':len(results),'checks':results,'runtime_actions':0}));print('PASS',len(results))
