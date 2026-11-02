"""Source-derived semantic ordering and source positions; no generated catalogue input."""
import ast
from common import identity
ORDER=['handler-type-evaluation','handler-match','handler-selection','handler-entry','caught-error-binding-attempt','caught-error-binding-complete','report-details-evaluation','report-key-evaluation','report-list-resolution','report-method-evaluation','report-item-name','error-type-callable','error-type-argument','error-type-call-attempt','error-type-call-return','error-name-attribute','error-str-callable','error-str-argument','error-str-call-attempt','error-str-call-return','report-item-complete','report-append-attempt','report-append-complete']
def derive(raw):
 t=ast.parse(raw);f=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='_session')
 outer=next(n for n in ast.walk(f) if isinstance(n,ast.ExceptHandler) and n.name=='e')
 assert ast.unparse(outer.type)=='BaseException'
 loop=next(n for n in outer.body if isinstance(n,ast.For));guard=loop.body[0];shared=guard.body[0]
 assert ast.unparse(guard.test)=='obj is not None' and isinstance(shared,ast.Try) and len(shared.handlers)==1 and not shared.orelse and not shared.finalbody
 assert [ast.unparse(n) for n in shared.body]==['obj.close()',"details['cleanup'].append([name, 'close returned'])"]
 handler=shared.handlers[0];assert handler.name=='close_error' and ast.unparse(handler.type)=='BaseException' and len(handler.body)==1
 stmt=handler.body[0];call=stmt.value;assert isinstance(call,ast.Call) and len(call.args)==1 and not call.keywords
 target=call.func;sub=target.value;item=call.args[0];name,typ,string=item.elts
 assert target.attr=='append' and ast.unparse(sub)=="details['cleanup']" and isinstance(item,ast.List)
 assert ast.unparse(name)=='name' and ast.unparse(typ)=='type(close_error).__name__' and ast.unparse(string)=='str(close_error)'
 nodes=[handler.type,handler.type,handler,handler,handler,handler,sub.value,sub.slice,sub,target,name,typ.value.func,typ.value.args[0],typ.value,typ.value,typ,string.func,string.args[0],string,string,item,call,stmt]
 def coord(n):return f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}'
 point=lambda n:{'site':coord(n),'expression':ast.get_source_segment(raw.decode(),n),'source':identity(raw)}
 return {'order':ORDER.copy(),'stages':dict(zip(ORDER,map(point,nodes))),'handler':point(handler),'shared_try':point(shared),'protected_nodes':[point(n) for n in ast.walk(shared) if hasattr(n,'lineno') and n.lineno==171],'dynamic_origins':{'error_name':point(typ),'message':point(string)},'guards':['owner_lock(destination)','except BaseException as e',"for name,obj in [('raw',raw),('managed',managed)]",'obj is not None','except BaseException as close_error'],'boundary':'Semantic acknowledgements only; no runtime/opcode history. Stop before handler exit.'}
