"""Isolated reviewed CLI execution; reject database and network entry points."""
import runpy, sys

def audit(event,args):
    if event in ('sqlite3.connect','socket.connect','socket.bind'):
        raise RuntimeError('PROHIBITED-OPERATION:'+event)
sys.addaudithook(audit)
sys.argv=sys.argv[1:]
runpy.run_path(sys.argv[0],run_name='__main__')
