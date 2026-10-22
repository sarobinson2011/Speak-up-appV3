"""Type-sensitive correspondence for the existing C4 JSON schemas.
Does not reinterpret values. Floats remain permitted in opaque JSON fields;
only declared integer/bool/etc fields and exact joins impose their own type.
"""
from anchor import need

def shape(value,template,path='binding'):
 need(type(value) is type(template),'TYPE:'+path+':'+type(template).__name__)
 if type(template) is dict:
  need(value.keys()==template.keys(),'FIELDS:'+path)
  for key in template:shape(value[key],template[key],path+'.'+key)
 elif type(template) is list:
  need(len(value)==len(template),'LENGTH:'+path)
  for n,(v,t) in enumerate(zip(value,template)):shape(v,t,path+'['+str(n)+']')

def same(value,template,path='binding'):
 shape(value,template,path)
 return value==template

def uint(value,bits,path):
 need(type(value) is int,'TYPE:'+path+':int')
 need(0<=value<2**bits,'RANGE:'+path)

def context(value):
 # query ordinal is a positive count supplied by durable query accounting.
 need(type(value) is dict,'TYPE:context:dict')
 uint(value['query_ordinal'],64,'context.query_ordinal')
 need(value['query_ordinal']>0,'RANGE:context.query_ordinal')

def near_spec(value):
 need(type(value) is dict,'TYPE:near_spec:dict')
 for key,bits in [('nonce',64),('gas',64),('deposit',128)]:uint(value[key],bits,'near_spec.'+key)

def transaction(value):
 need(type(value) is dict,'TYPE:transaction:dict')
 uint(value['nonce'],64,'transaction.nonce')
 if 'priority_fee' in value:uint(value['priority_fee'],64,'transaction.priority_fee')
 need(type(value['actions']) is list,'TYPE:transaction.actions:list')
 for n,action in enumerate(value['actions']):
  need(type(action) is dict and set(action)=={'FunctionCall'},'FIELDS:transaction.action')
  call=action['FunctionCall'];need(type(call) is dict,'TYPE:FunctionCall:dict')
  uint(call['gas'],64,'transaction.actions['+str(n)+'].FunctionCall.gas')
