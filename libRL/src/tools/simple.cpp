#define _USE_MATH_DEFINES

#include <Python.h>
#include <cmath>
#include <iostream>
#include <complex>

using namespace std;

double reflection_loss(
    double f, double d, double e1, double e2, double mu1, double mu2
    ){

    complex<double> er(e1, -1*e2);
    complex<double> mur(mu1, -1*mu2);
    complex<double> j(0.0, 1.0);
    complex<double> cnsts(
        2.0*M_PI*(f*pow(10.0,9.0))*(d*pow(10.0,-3.0))/299792458.0, 0.0
    );
    complex<double> rl = 20.0 * log10(
        abs(
           ((pow(mur/er, 0.5) * tanh(j*cnsts*pow(er*mur,0.5)))-1.0)
           /((pow(mur/er,0.5) * tanh(j*cnsts*pow(er*mur,0.5)))+1.0) 
        )
    );
    return rl.real();
};


static PyObject *Cgamma(
        PyObject *f, PyObject *d, PyObject *e1, 
        PyObject *e2, PyObject *mu1, PyObject *mu2
    ) {

    int f_length = PyObject_Length(f);
    int d_length = PyObject_Length(d);

    double *d_cpp, *f_cpp, *e1_cpp, *e2_cpp, *mu1_cpp, *mu2_cpp;
    double *NA[5] = {f_cpp, e1_cpp, e2_cpp, mu1_cpp, mu2_cpp};
    PyObject *NA_py[5] = {f, e1, e2, mu1, mu2};

    for (int i=0; i<sizeof(NA)/sizeof(*NA); i++){
        NA[i] = new double[f_length];
    };

    d_cpp = new double[d_length];

    for (int i=0; i<sizeof(NA)/sizeof(*NA); i++) {
        for (int index = 0; index < f_length; index++) {
            PyObject *item;
            item = PyList_GetItem(NA_py[i], index);
            NA[i][index] = PyFloat_AsDouble(item);
        };
    };

    for (int index = 0; index < d_length; index++) {
        PyObject *item;
        item = PyList_GetItem(d, index);
        d_cpp[index] = PyFloat_AsDouble(item);
    };

    PyObject *outer = PyList_New(d_length*f_length);

    int count = 0;
    for (int i = 0; i < d_length; i++){
        for (int j = 0; j < f_length; j++){

            PyObject* single_res = Py_BuildValue(
                "[f, f, f]", reflection_loss(
                    NA[0][j], d_cpp[i], NA[1][j], 
                    NA[2][j], NA[3][j], NA[4][j]
                ), NA[0][j], d_cpp[i]
            );
            PyList_SetItem(outer, count, single_res);
            count += 1;
        };
    };

    for (int i=0; i<sizeof(NA)/sizeof(*NA); i++){
        delete[] NA[i];
    };

    delete[] d_cpp;

    return outer;
};

static PyObject *gamma(PyObject *self, PyObject *args) {

    PyObject *f, *d, *e1, *e2, *mu1, *mu2;

    if (!PyArg_ParseTuple(args, "OOOOOO", &f, &d, &e1, &e2, &mu1, &mu2)){
        return NULL;
    };

    return Py_BuildValue("O", Cgamma(f, d, e1, e2, mu1, mu2));
};

static PyObject *test_Cgamma(PyObject *self) {
    return Py_BuildValue("i", 1);
};

static char gamma_docs[] = 
    "A C++ extension for calculating the reflection loss. Accepts *only* 6 "
    "lists of f, d, e1, e2, mu1, and mu2. lists 0 and 2-5 must be same length \n";

static PyMethodDef gamma_func[] = {
    {"gamma", (PyCFunction) gamma, METH_VARARGS, gamma_docs},
    {"test_Cgamma", (PyCFunction) test_Cgamma, METH_NOARGS, "test C extension"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef array_gamma = {
    PyModuleDef_HEAD_INIT,
    "gamma",
    NULL,
    -1,
    gamma_func
};

PyMODINIT_FUNC PyInit_simple(void){
    return PyModule_Create(&array_gamma);
};