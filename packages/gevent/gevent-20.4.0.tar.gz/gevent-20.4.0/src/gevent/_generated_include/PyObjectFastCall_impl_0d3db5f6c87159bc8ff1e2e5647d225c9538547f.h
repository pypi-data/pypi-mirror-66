static CYTHON_INLINE PyObject* __Pyx_PyObject_FastCall_fallback(PyObject *func, PyObject **args, Py_ssize_t nargs) {
    PyObject *argstuple;
    PyObject *result;
    Py_ssize_t i;
    argstuple = PyTuple_New(nargs);
    if (unlikely(!argstuple)) return NULL;
    for (i = 0; i < nargs; i++) {
        Py_INCREF(args[i]);
        PyTuple_SET_ITEM(argstuple, i, args[i]);
    }
    result = __Pyx_PyObject_Call(func, argstuple, NULL);
    Py_DECREF(argstuple);
    return result;
}
static CYTHON_INLINE PyObject* __Pyx_PyObject_FastCall(PyObject *func, PyObject **args, Py_ssize_t nargs) {
#if CYTHON_COMPILING_IN_CPYTHON
    if (nargs == 0) {
#ifdef __Pyx_CyFunction_USED
        if (PyCFunction_Check(func) || __Pyx_CyFunction_Check(func))
#else
        if (PyCFunction_Check(func))
#endif
        {
            if (likely(PyCFunction_GET_FLAGS(func) & METH_NOARGS)) {
                return __Pyx_PyObject_CallMethO(func, NULL);
            }
        }
    }
    else if (nargs == 1) {
        if (PyCFunction_Check(func))
        {
            if (likely(PyCFunction_GET_FLAGS(func) & METH_O)) {
                return __Pyx_PyObject_CallMethO(func, args[0]);
            }
        }
    }
#endif
    #if PY_VERSION_HEX < 0x030800B1
    #if CYTHON_FAST_PYCCALL && PY_VERSION_HEX >= 0x030700A1
    if (PyCFunction_Check(func)) {
        return _PyCFunction_FastCallKeywords(func, args, nargs, NULL);
    }
    if (__Pyx_IS_TYPE(func, &PyMethodDescr_Type)) {
        return _PyMethodDescr_FastCallKeywords(func, args, nargs, NULL);
    }
    #elif CYTHON_FAST_PYCCALL
    if (PyCFunction_Check(func)) {
        return _PyCFunction_FastCallDict(func, args, nargs, NULL);
    }
    #endif
    #if CYTHON_FAST_PYCALL
    if (PyFunction_Check(func)) {
        return __Pyx_PyFunction_FastCall(func, args, nargs);
    }
    #endif
    #endif
    #if CYTHON_VECTORCALL
    vectorcallfunc f = _PyVectorcall_Function(func);
    if (f) {
        return f(func, args, nargs, NULL);
    }
    #elif __Pyx_CyFunction_USED && CYTHON_BACKPORT_VECTORCALL
    if (__Pyx_IS_TYPE(func, __pyx_CyFunctionType)) {
        __pyx_vectorcallfunc f = __Pyx_CyFunction_func_vectorcall(func);
        if (f) return f(func, args, nargs, NULL);
    }
    #endif
    if (nargs == 0) {
        return __Pyx_PyObject_Call(func, __pyx_empty_tuple, NULL);
    }
    return __Pyx_PyObject_FastCall_fallback(func, args, nargs);
}

