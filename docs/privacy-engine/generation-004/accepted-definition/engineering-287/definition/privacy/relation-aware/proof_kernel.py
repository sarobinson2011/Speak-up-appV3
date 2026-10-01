"""Closed symbolic derivation checker. No hash evaluation or security assumption discharge."""
import hashlib,json

def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def application(secret,action):return ['POSEIDON3',[secret,action,'SIGN_DOMAIN']]
PREMISES={
 'action-distinct':['NE','a1','a2'],
 'left-relation':['EQ','n1',application('s1','a1')],
 'right-relation':['EQ','n2',application('s2','a2')],
 'output-equal':['EQ','n1','n2']}

def derive(proof,binding):
 if type(proof) is not dict or set(proof)!={'binding','steps'} or proof['binding']!=binding:raise ValueError('proof binding')
 if type(binding) is not dict or not binding or any(type(k) is not str or type(v) is not str or len(v)!=64 or any(c not in '0123456789abcdef' for c in v) for k,v in binding.items()):raise ValueError('digest binding')
 steps=proof['steps']
 if type(steps) is not list or len(steps)!=6:raise ValueError('closed proof length')
 out=[]
 for i,step in enumerate(steps):
  if type(step) is not dict:raise ValueError('proof step')
  rule=step.get('rule')
  if rule=='PREMISE':
   if set(step)!={'rule','name'} or step['name'] not in PREMISES:raise ValueError('unrecognized premise')
   out.append(PREMISES[step['name']])
  elif rule=='ORDERED-TUPLE-DISTINCT':
   if set(step)!={'rule','refs'} or type(step['refs']) is not list or len(step['refs'])!=1:raise ValueError('tuple rule schema')
   r=step['refs'][0]
   if type(r) is not int or not 0<=r<i or out[r]!=PREMISES['action-distinct']:raise ValueError('tuple rule premise')
   out.append(['NE',['s1','a1','SIGN_DOMAIN'],['s2','a2','SIGN_DOMAIN']])
  elif rule=='COLLISION-DEFINITION':
   if set(step)!={'rule','refs'} or type(step['refs']) is not list or len(step['refs'])!=4 or any(type(r) is not int or not 0<=r<i for r in step['refs']):raise ValueError('collision references')
   got=[out[r] for r in step['refs']]
   want=[['NE',['s1','a1','SIGN_DOMAIN'],['s2','a2','SIGN_DOMAIN']],PREMISES['left-relation'],PREMISES['right-relation'],PREMISES['output-equal']]
   if got!=want:raise ValueError('collision premises')
   out.append(['COLLISION','POSEIDON3',['s1','a1','SIGN_DOMAIN'],['s2','a2','SIGN_DOMAIN']])
  else:raise ValueError('unsupported rule')
 if out[-1][0]!='COLLISION':raise ValueError('wrong conclusion')
 return {'result':'VALID-CONDITIONAL-DERIVATION','assumptions':PREMISES,'conclusion':out[-1],'binding':binding,'security_established':False,'profile_admitted':False}

def certificate(binding):
 return {'binding':binding,'steps':[{'rule':'PREMISE','name':x} for x in PREMISES]+[{'rule':'ORDERED-TUPLE-DISTINCT','refs':[0]},{'rule':'COLLISION-DEFINITION','refs':[4,1,2,3]}]}
