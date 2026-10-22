"""Executable local framing interpretation; not an added runtime record."""
from common import *
def framing(value,key=None,present=True):
 boolean(present);need(key is None or type(key) is str,'KEY-TYPE')
 if not present:return {'presence':False,'availability':'INAPPLICABLE-ONLY-WITH-VALIDATED-GUARD','encoding_length':0,'member_count':None,'exact_bytes':'','type_tag':'ABSENT','key_encoding':None,'separator_encoding':'','opening_delimiter':'','closing_delimiter':''}
 raw=enc(value);container=type(value) in [dict,list];tag={dict:'OBJECT',list:'ARRAY',str:'STRING',int:'INTEGER',float:'NUMBER',bool:'BOOLEAN',type(None):'NULL'}[type(value)]
 return {'presence':True,'availability':'PRESENT','encoding_length':len(raw),'member_count':len(value) if container else None,'exact_bytes':raw.hex(),'type_tag':tag,'key_encoding':enc(key)[:-1].hex() if key is not None else None,'separator_encoding':','.encode().hex() if container and len(value)>1 else '', 'opening_delimiter':('{' if type(value) is dict else '[' if type(value) is list else '').encode().hex(),'closing_delimiter':('}' if type(value) is dict else ']' if type(value) is list else '').encode().hex()}
