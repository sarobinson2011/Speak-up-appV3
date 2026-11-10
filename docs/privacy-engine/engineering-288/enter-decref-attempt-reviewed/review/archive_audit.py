from bytes_only import *
try:
 a=untar(B/'inputs/I164-enter-decref-attempt-public-1-host-evidence.tar.gz',B/'host',{'bytes':14159284,'sha256':'e05ba364b756c887fbf2092b2bb98eb93c9de673869831a764b48b5838499000'})
 save(B/'host-archive-audit.json',a)
 for name,dest in [('I164-helper-open-persistent-host-launcher-review-2.zip','launcher'),('I164-enter-return-res-1-independent-review.zip','prior-review')]:
  save(B/(dest+'-archive-audit.json'),unzip(B/'inputs'/name,B/dest))
 for name,dest,sz,sha in [('I164-enter-decref-attempt-1-source.zip','source',2825074,'e17a9925333e36a81fa1167ab080c1f9e7538b05dcd811df499f0e7f3d75d96d'),('I164-enter-decref-attempt-1-results.zip','focused',2556368,'a9f068829b7feccb670bdde4c56e3f093beb95fd1215ff8b9eaf69f87a9f1d6b')]:
  save(B/(dest+'-archive-audit.json'),unzip(B/'host/inputs'/name,B/dest,{'bytes':sz,'sha256':sha}))
 save(B/'archive-audit.exit.json',{'exit':0});print('archive audit PASS')
except BaseException as e:
 save(B/'archive-audit.exit.json',{'exit':1,'failure':repr(e)});raise
