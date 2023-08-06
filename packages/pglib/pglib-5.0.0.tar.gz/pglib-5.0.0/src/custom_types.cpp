
#include "pglib.h"
#include "byteswap.h"
#include "custom_types.h"

static Oid oidHstore = 0;


Oid GetHstoreOid() {
    return oidHstore;
}

void RegisterHstore(Oid oid)
{
    oidHstore = oid;
}

bool IsHstoreRegistered()
{
    return oidHstore != 0;
}

bool IsHstore(Oid oid)
{
    return oid == oidHstore;
}

PyObject* GetHstore(const char* p)
{
    // Reads an HSTORE off the wire.  The format seems to be:
    //
    // - A 32-bit count of pairs.
    // - Each pair is two consecutive strings.
    //   - each string is a 32-bit byte count
    //   - followed by the bytes

    Object result(PyDict_New());
    if (!result)
        return 0;

    long count = swaps4(*(int32_t*)p);
    p += 4;

    for (long i = 0; i < count; i++)
    {
        long len = swaps4(*(int32_t*)p);
        p += 4;
        Object key(PyUnicode_DecodeUTF8((const char*)p, len, 0));
        p += len;
        if (!key)
            return 0;

        len = swaps4(*(int32_t*)p);
        p += 4;

        Object val;
        if (len == -1)
        {
            val.AttachAndIncrement(Py_None);
        }
        else
        {
            val.Attach(PyUnicode_DecodeUTF8((const char*)p, len, 0));
            p += len;
        }

        if (!val)
            return 0;

        if (PyDict_SetItem(result, key, val) == -1)
            return 0;

        key.Detach();
        val.Detach();
    }

    return result.Detach();
}


static PyObject* Hstore_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    PyObject* dict;
    if (!PyArg_ParseTuple(args, "O", &dict) || !PyDict_Check(dict))
    {
        PyErr_SetString(Error, "hstore constructor requires a single dictionary");
        return 0;
    }

    Hstore* self = (Hstore*)type->tp_alloc(type, 0);
    if (self == 0)
        return 0;

    self->data = dict;
    Py_INCREF(self->data);

    return (PyObject*)self;
}


static void Hstore_dealloc(PyObject* self)
{
    Hstore* hstore = (Hstore*)self;
    Py_XDECREF(hstore->data);
    Py_TYPE(self)->tp_free(self);
}


PyTypeObject HstoreType =
{
    PyVarObject_HEAD_INIT(0, 0)
    .tp_name = "pglib.hstore",
    .tp_basicsize = sizeof(Hstore),
    .tp_dealloc = Hstore_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = Hstore_new
};
