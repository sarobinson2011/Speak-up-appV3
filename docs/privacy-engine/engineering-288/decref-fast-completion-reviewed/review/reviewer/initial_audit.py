from bytes_only import *
r=untar(B/'inputs/I164-decref-fast-completion-public-1-host-evidence.tar.gz',B/'host',{'bytes':17223047,'sha256':'0eba64a9a1b94b7d471c5cf42770f4df49a6f28b24e3cb1d305906549ef94a91'},677,675);save(B/'host-archive-audit.json',r);save(B/'initial-audit.exit.json',{'exit':0});print({k:v for k,v in r.items() if k!='members'})
