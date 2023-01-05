#define PY_SSIZE_T_CLEAN
#include <Python.h>

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>

#include "Map.h"
#include "vector.h"
#include "Allocator.h"
#include "Algorithm.h"


/// Uncomment if you want to debug `A*`
// #define DebugMode


extern Allocator *a;

static PyObject *
fromPython(PyObject *self, PyObject *args, PyObject *keywords)
{
    PyArrayObject *grid = NULL, *vConstraints = NULL, *eConstraints = NULL;
    int sx, sy, gx, gy;
    bool returnAll = false;
    static char *keylist[] = {"map", "start", "goal", "v_constraints", "e_constraints", "return_all", NULL};

    if (!PyArg_ParseTupleAndKeywords(
        args, keywords, "O!(ii)(ii)|O!O!i", keylist, 
        &PyArray_Type, &grid, 
        &sx, &sy, &gx, &gy, 
        &PyArray_Type, &vConstraints, 
        &PyArray_Type, &eConstraints,
        &returnAll
    ))
        return NULL;

    int vConstraintsCount = 0;
    if (vConstraints) vConstraintsCount = (int)PyArray_DIM(vConstraints, 0);

    int eConstraintsCount = 0;
    if (eConstraints) eConstraintsCount = (int)PyArray_DIM(eConstraints, 0);

    Map *map;
    int w = (int)PyArray_DIM(grid, 1);
    int h = (int)PyArray_DIM(grid, 0);
    char *mapBytes = PyArray_BYTES(grid);

    if (vConstraintsCount > 0 || eConstraintsCount > 0) {
        vector constraints[2] = {0};
        vector *vc = NULL, *ec = NULL;
        if (vConstraintsCount > 0) { 
            VectorNewFromBuffer(constraints, sizeof(VConstraint), vConstraintsCount, PyArray_DATA(vConstraints));
            vc = constraints;
        }
        if (eConstraintsCount > 0)  {
            VectorNewFromBuffer(constraints + 1, sizeof(EConstraint), eConstraintsCount, PyArray_DATA(eConstraints));
            ec = constraints + 1;
        }
        map = newMapWithConstraints(w, h, vc, ec, mapBytes);
    } else { 
        map = newMap(w, h, mapBytes);
    }

#ifdef DebugMode
    puts("\n----------------------------------------------");
    printf("Calculating path from (%d, %d) to (%d, %d)\n\n", sx, sy, gx, gy);
    
    printf("VertexConstraints: len = %d ", vConstraintsCount);
    puts("in format: t, (x, y)");

    VConstraint *vcs = (VConstraint*)PyArray_DATA(vConstraints);
    for (int i = 0; i < vConstraintsCount; ++i)
        printf("[%d] = %d, (%d, %d)\n", i, vcs[i].time, vcs[i].p.x, vcs[i].p.y);
    
    printf("\nEdgeConstraints: len = %d ", eConstraintsCount);
    puts("in format: t, (x1, y1) -> (x2, y2)");
    
    EConstraint *ecs = (EConstraint*)PyArray_DATA(eConstraints);
    for (int i = 0; i < eConstraintsCount; ++i)
        printf("[%d] = %d, (%d, %d) -> (%d, %d)\n",
               i, ecs[i].time, ecs[i].e.p1.x, ecs[i].e.p1.y, ecs[i].e.p2.x, ecs[i].e.p2.y);
    
    printf("\n");
#endif
    
    Point s = {sx, sy}, g = {gx, gy};
    
#ifdef DebugMode
    printf("minimum path lenght with respect to constraints = %d\n", getGoalTimeBoundary(map, g));
#endif

    a = newAllocator(10, map->width * map->height / 2);
    
    // actual A* here
    Node result;
    bool found = findPath(map, s, g, &result);
    
    if (!found) {
        deleteAllocator(a);
#ifdef DebugMode
        puts("Path not found this time!");
        puts("Calculating is done");
        puts("----------------------------------------------\n");
#endif
        Py_RETURN_NONE;
    }

    // create the return array
    npy_intp shape[] = {result.g + 1, 2};
    PyArrayObject *path = (PyArrayObject*)PyArray_SimpleNew(2, shape, NPY_INT);

    // fill the array by unwinding the path by traveling through `parent`
    Point *p = PyArray_DATA(path);
    p += result.g;
    Node *current = &result;
#ifdef DebugMode
    printf("found path with length = %d\n", result.g);
#endif
    while (current) {
        *p = current->p;
        --p;
#ifdef DebugMode
        printf("(%d, %d) <- ", current->p.x, current->p.y);
#endif
        current = current->parent;
    }
#ifdef DebugMode
    printf("\n\n");
#endif

    deleteMap(map);
    deleteAllocator(a);

    if (returnAll) {
#ifdef DebugMode
        puts("Returning all paths");
        puts("Calculating is done"); // for now
        puts("----------------------------------------------\n");
#endif
        PyErr_SetString(PyExc_NotImplementedError, "return all paths is not implemented yet!");
        return NULL;
    }

#ifdef DebugMode
    puts("Calculating is done");
    puts("----------------------------------------------\n");
#endif

    return (PyObject*)path;
}

static PyMethodDef methods[] = {
    {"find_path", (PyCFunction)(void(*)(void))fromPython, METH_VARARGS | METH_KEYWORDS,
     "Do some stuff"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef lightspeed = {
    PyModuleDef_HEAD_INIT,
    "lightspeed",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    methods
};

PyMODINIT_FUNC
PyInit_lightspeed(void)
{
    PyObject* mod = PyModule_Create(&lightspeed);
    import_array();
    return mod;
}
