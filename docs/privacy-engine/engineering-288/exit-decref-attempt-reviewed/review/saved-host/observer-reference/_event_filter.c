/* Harness only. CPython 3.12 current-thread profile event filter. No validator code changes. */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <frameobject.h>

typedef struct {PyObject *callback,*target,*protected,*phases,*root,*call,*ret,*validate,*suffix;} State;
static const char *CAP="I164.harness.profile-lease";
static void destroy(PyObject *cap){
 State *s=PyCapsule_GetPointer(cap,CAP);if(!s){PyErr_Clear();return;}
 Py_XDECREF(s->callback);Py_XDECREF(s->target);Py_XDECREF(s->protected);Py_XDECREF(s->phases);Py_XDECREF(s->root);Py_XDECREF(s->call);Py_XDECREF(s->ret);Py_XDECREF(s->validate);Py_XDECREF(s->suffix);PyMem_Free(s);
}
static int selected(State *s,PyCodeObject *c){
 int has=PySet_Contains(s->phases,c->co_name);if(has<=0)return has;
 return PyUnicode_Tailmatch(c->co_filename,s->root,0,PY_SSIZE_T_MAX,-1);
}
static int hook(PyObject *cap,PyFrameObject *frame,int what,PyObject *arg){
 if(what!=PyTrace_CALL && what!=PyTrace_RETURN)return 0;
 State *s=PyCapsule_GetPointer(cap,CAP);if(!s)return -1;
 PyCodeObject *c=PyFrame_GetCode(frame);if(!c)return -1;
 int forward=((PyObject *)c==s->target && what==PyTrace_RETURN);
 if(what==PyTrace_CALL){
  int p=PyDict_Contains(s->protected,c->co_filename);if(p<0){Py_DECREF(c);return -1;}
  if(p && (c->co_flags&2))forward=1; /* Exact original guard predicate; Python checks allowed names. */
  if(!forward){
   int same=PyObject_RichCompareBool(c->co_name,s->validate,Py_EQ);if(same<0){Py_DECREF(c);return -1;}
   if(same){int tail=PyUnicode_Tailmatch(c->co_filename,s->suffix,0,PY_SSIZE_T_MAX,1);if(tail<0){Py_DECREF(c);return -1;}forward=tail;}
  }
 }
 if(!forward){int p=selected(s,c);if(p<0){Py_DECREF(c);return -1;}forward=p;}
 Py_DECREF(c);
 if(!forward)return 0;
 PyObject *v=PyObject_CallFunctionObjArgs(s->callback,(PyObject *)frame,what==PyTrace_CALL?s->call:s->ret,arg?arg:Py_None,NULL);
 if(!v){
  /* Match the Python profile observer's fail-closed exception departure.
     Remove only our exact current lease; preserve the callback error when
     cleanup succeeds. A cleanup error replaces it with the original context. */
  PyObject *original=PyErr_GetRaisedException();
  PyThreadState *t=PyThreadState_Get();
  if(t->c_profilefunc==hook && t->c_profileobj==cap){
   Py_INCREF(cap);PyEval_SetProfile(NULL,NULL);Py_DECREF(cap);
  }
  if(PyErr_Occurred()){
   PyObject *cleanup=PyErr_GetRaisedException();
   PyException_SetContext(cleanup,original);PyErr_SetRaisedException(cleanup);
  }else{PyErr_SetRaisedException(original);}
  return -1;
 }
 Py_DECREF(v);return 0;
}
static PyObject *install(PyObject *self,PyObject *args){
 PyObject *callback,*target,*protected,*phases,*root;
 if(!PyArg_ParseTuple(args,"OOOOO",&callback,&target,&protected,&phases,&root))return NULL;
 if(!PyCallable_Check(callback)||!PyCode_Check(target)||!PyDict_CheckExact(protected)||!PySet_CheckExact(phases)||!PyUnicode_CheckExact(root)){PyErr_SetString(PyExc_TypeError,"FILTER-INPUT-TYPES");return NULL;}
 PyThreadState *t=PyThreadState_Get();
 if(t->c_profilefunc || t->c_tracefunc){PyErr_SetString(PyExc_RuntimeError,"FILTER-OBSERVER-CONTENTION");return NULL;}
 State *s=PyMem_Calloc(1,sizeof(State));if(!s)return PyErr_NoMemory();
 s->callback=Py_NewRef(callback);s->target=Py_NewRef(target);s->protected=Py_NewRef(protected);s->phases=Py_NewRef(phases);s->root=Py_NewRef(root);
 s->call=PyUnicode_FromString("call");s->ret=PyUnicode_FromString("return");s->validate=PyUnicode_FromString("validate");s->suffix=PyUnicode_FromString("/code/correspondence.py");
 PyObject *cap=PyCapsule_New(s,CAP,destroy);
 if(!cap){Py_XDECREF(s->callback);Py_XDECREF(s->target);Py_XDECREF(s->protected);Py_XDECREF(s->phases);Py_XDECREF(s->root);Py_XDECREF(s->call);Py_XDECREF(s->ret);Py_XDECREF(s->validate);Py_XDECREF(s->suffix);PyMem_Free(s);return NULL;}
 if(!s->call||!s->ret||!s->validate||!s->suffix){Py_DECREF(cap);return NULL;}
 PyEval_SetProfile(hook,cap);
 if(PyErr_Occurred()){if(t->c_profilefunc==hook && t->c_profileobj==cap)PyEval_SetProfile(NULL,NULL);Py_DECREF(cap);return NULL;}
 return cap;
}
static PyObject *stop(PyObject *self,PyObject *cap){
 if(!PyCapsule_IsValid(cap,CAP)){PyErr_SetString(PyExc_TypeError,"FILTER-LEASE");return NULL;}
 PyThreadState *t=PyThreadState_Get();
 if(t->c_profilefunc==hook && t->c_profileobj==cap){PyEval_SetProfile(NULL,NULL);Py_RETURN_TRUE;}
 if(!t->c_profilefunc && !t->c_profileobj)Py_RETURN_FALSE;
 PyErr_SetString(PyExc_RuntimeError,"FILTER-FOREIGN-PROFILER-PRESERVED");return NULL;
}
static PyMethodDef methods[]={{"install",install,METH_VARARGS,"Install only on an unused current-thread profiler."},{"stop",stop,METH_O,"Remove only the exact owned native hook/lease."},{NULL,NULL,0,NULL}};
static struct PyModuleDef definition={PyModuleDef_HEAD_INIT,"_event_filter","Harness-only filtered profile observer.",-1,methods,NULL,NULL,NULL,NULL};
PyMODINIT_FUNC PyInit__event_filter(void){return PyModule_Create(&definition);}
