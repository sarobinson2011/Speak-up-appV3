"""Read-only CPython observer for an explicitly bounded laboratory call domain."""
import sys,dis,copy
TARGETS={'Authority.sign','Authority.save','Authority.blob','Authority.get','fault','tx','validate'}
def typed(x):
 t=type(x)
 if x is None:return {'type':'null'}
 if t in (bool,int,str):return {'type':t.__name__,'value':x}
 if t is bytes:return {'type':'bytes','hex':x.hex()}
 if t in (list,tuple):return {'type':t.__name__,'items':[typed(v) for v in x]}
 if t is dict and all(type(k) is str for k in x):return {'type':'dict','items':{k:typed(v) for k,v in sorted(x.items())}}
 return {'type':t.__name__,'unavailable':'outside explicit value-observer type domain'}
def untyped(x):
 if set(x)=={'type'} and x['type']=='null':return None
 if x['type'] in ['bool','int','str']:
  want={'bool':bool,'int':int,'str':str}[x['type']]
  if set(x)!= {'type','value'} or type(x['value']) is not want:raise ValueError('OBS-TYPE')
  return x['value']
 if x['type']=='bytes' and set(x)=={'type','hex'}:
  b=bytes.fromhex(x['hex'])
  if b.hex()!=x['hex']:raise ValueError('OBS-HEX')
  return b
 if x['type'] in ['list','tuple'] and set(x)=={'type','items'}:
  z=[untyped(v) for v in x['items']];return z if x['type']=='list' else tuple(z)
 if x['type']=='dict' and set(x)=={'type','items'}:return {k:untyped(v) for k,v in x['items'].items()}
 raise ValueError('OBS-UNAVAILABLE-OR-STRUCTURE')
class Observer:
 def __init__(self,sources):self.sources=sources;self.events=[];self.ids={};self.next=0;self.instructions={}
 def position(self,frame):
  code=frame.f_code
  if code not in self.instructions:self.instructions[code]={i.offset:i.positions for i in dis.get_instructions(code,show_caches=True)}
  p=self.instructions[code].get(frame.f_lasti)
  return None if p is None else {'line':p.lineno,'end_line':p.end_lineno,'column':p.col_offset,'end_column':p.end_col_offset}
 def trace(self,frame,event,arg):
  path=self.sources.get(frame.f_code.co_filename);name=frame.f_code.co_qualname
  if path and name in TARGETS and event in ['call','return','exception']:
   if event=='call':self.next+=1;self.ids[id(frame)]=self.next
   caller=frame.f_back
   row={'event':event,'frame':self.ids.get(id(frame)),'source':path,'function':name,'definition_line':frame.f_code.co_firstlineno,'line':frame.f_lineno,'position':self.position(frame),'caller':None if caller is None else {'source':self.sources.get(caller.f_code.co_filename,'OUTSIDE-OBSERVED-DOMAIN'),'function':caller.f_code.co_qualname,'position':self.position(caller)},'values':{}}
   names={'Authority.sign':['r','inject','a_id','bound','a','t','raw','p'],'Authority.save':['request','kind','proof','s','new'],'Authority.blob':['raw','ref'],'Authority.get':['ref'],'fault':['point','want'],'tx':['nonce','to','data','gas','key'],'validate':['raw','expected']}[name]
   row['values']={k:typed(frame.f_locals[k]) for k in names if k in frame.f_locals}
   if event=='return':row['result']=typed(arg);row['meaning']='CPython return event; null may indicate exception unwind'
   if event=='exception':row['exception']={'type':type(arg[1]).__name__,'message':str(arg[1])}
   self.events.append(row)
   if event=='return':self.ids.pop(id(frame),None)
  return self.trace
