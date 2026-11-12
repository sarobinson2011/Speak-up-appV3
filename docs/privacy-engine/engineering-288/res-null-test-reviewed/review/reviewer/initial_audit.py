from bytes_only import *
p=B/'inputs/I164-res-null-test-public-1-host-evidence.tar.gz'
try:
 a=untar(p,B/'host',{'bytes':23682326,'sha256':'e20093f20368ff130a6c64d6a634fc993b43a05b1e65b01ec6a4e54a58902101'},661,659)
 save(B/'host-archive-audit.json',a);save(B/'host-archive-audit.exit.json',{'exit':0})
except BaseException as e:save(B/'host-archive-audit.exit.json',{'exit':1,'error':repr(e)});raise
