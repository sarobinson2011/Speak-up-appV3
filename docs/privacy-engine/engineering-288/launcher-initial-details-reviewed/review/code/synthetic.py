"""Reviewer-created predecessor fixtures: monitoring plumbing, never source authentication."""
import types,copy,sys

def fixture(m,mode='normal',error=None,on_validate=None):
 counts={'public':0,'basis':0};p=types.SimpleNamespace();basis={'fresh':{'fixture':'FL6-LD01'},'payload':{'roles':['one','two']}};saved=m.enc({'fixture':'FL6-LD01','roles':['one','two']})
 def _basis():counts['basis']+=1;return copy.deepcopy(basis)
 def _rows(b):return copy.deepcopy(b['payload']['roles'])
 def _assemble(fresh,rows,b):return {'fixture':fresh['fixture'],'roles':rows} if mode!='wrong-basis' else {'wrong':True}
 def validate(root,raw):
  counts['public']+=1
  if on_validate:on_validate()
  if mode=='before':raise error
  if mode!='missing':_basis()
  if mode=='extra':_basis()
  if mode=='after':raise error
  return {'result':'FAIL' if mode=='wrong-result' else 'PASS','contexts':list(m.CONTEXTS),'receipt':dict(m.PREDECESSOR_RECEIPT),'nested':{'values':[1,2]}}
 p._basis=_basis;p._rows=_rows;p._assemble=_assemble;p.validate=validate;p.enc=m.enc
 return {'prior_module':p,'prior_root':'FL6-SYNTHETIC-NOT-AUTHENTICATED','prior_saved':saved},counts

def release_fixture(p,owner):
 sm=sys.monitoring
 assert sm.get_tool(2) is owner
 sm.set_events(2,0);sm.set_local_events(2,p._basis.__code__,0);sm.register_callback(2,sm.events.PY_RETURN,None);sm.free_tool_id(2)
