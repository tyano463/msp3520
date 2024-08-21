#include <Python.h>

static PyObject* display_init(PyObject* self, PyObject* args) {
    // 初期化処理をここに記述
    Py_RETURN_NONE;
}

static PyObject* display_show(PyObject* self, PyObject* args) {
    const char* text;
    int x, y;

    if (!PyArg_ParseTuple(args, "sii", &text, &x, &y)) {
        return NULL;
    }

    // テキスト表示の処理をここに記述
    Py_RETURN_NONE;
}

static PyMethodDef DisplayMethods[] = {
    {"init", display_init, METH_NOARGS, "Initialize the display"},
    {"show", display_show, METH_VARARGS, "Show text on the display"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef displaymodule = {
    PyModuleDef_HEAD_INIT,
    "msp3520",  // モジュール名を msp3520 に変更
    NULL,
    -1,
    DisplayMethods
};

PyMODINIT_FUNC PyInit_msp3520(void) {
    return PyModule_Create(&displaymodule);
}
