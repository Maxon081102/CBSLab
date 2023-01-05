#include "vector.h"
#include <stdlib.h>
#include <assert.h>
#include <string.h>

#define DEFAULT_INITIAL_ALLOCATION 10

#define vectorElem(v, index) (((char*)(v->elems)) + (index) * (v->elemSize))

void VectorNewFromBuffer(vector *v, int elemSize, int length, void *rawBytes) {
    assert(elemSize > 0);
    assert(length >= 0);
    v->elems = rawBytes;
    v->logicalLength = length;
    v->allocatedLength = length;
    v->allocationChunk = length;
    v->elemSize = elemSize;
    v->freeFn = NULL;
}

void VectorNew(vector *v, int elemSize, VectorFreeFunction freefn, int initialAllocation) {
    assert(elemSize > 0);
    assert(initialAllocation >= 0);
    if (initialAllocation == 0) initialAllocation = DEFAULT_INITIAL_ALLOCATION;
    v->elems = calloc(initialAllocation, elemSize);
    v->logicalLength = 0;
    v->allocatedLength = initialAllocation;
    v->allocationChunk = initialAllocation;
    v->elemSize = elemSize;
    v->freeFn = freefn;
}

void VectorDispose(vector *v) {
    if (v->freeFn)
        for (int i = 0; i < v->logicalLength; ++i)
            v->freeFn(vectorElem(v, i));
    free(v->elems);
}

int VectorLength(const vector *v) {
    return v->logicalLength;
}

void *VectorNth(const vector *v, int position) {
    assert(position >= 0);
    assert(position < v->logicalLength);
    return vectorElem(v, position);
}

static void VectorGrow(vector* v) {
    void *reallocated = realloc(v->elems, (v->allocatedLength + v->allocationChunk) * v->elemSize);
    assert(reallocated);
    v->allocatedLength += v->allocationChunk;
    v->elems = reallocated;
}

void VectorInsert(vector *v, const void *elemAddr, int position) {
    assert(position >= 0);
    assert(position <= v->logicalLength);
    if (v->logicalLength >= v->allocatedLength) VectorGrow(v);
    memmove(vectorElem(v, position + 1), vectorElem(v, position), (v->logicalLength - position) * v->elemSize);
    memcpy(vectorElem(v, position), elemAddr, v->elemSize);
    v->logicalLength++;
}

void VectorAppend(vector *v, const void *elemAddr) {
    if (v->logicalLength >= v->allocatedLength) VectorGrow(v);
    memcpy(vectorElem(v, v->logicalLength), elemAddr, v->elemSize);
    v->logicalLength++;
}

void VectorReplace(vector *v, const void *elemAddr, int position) {
    assert(position >= 0);
    assert(position < v->logicalLength);
    if (v->freeFn) v->freeFn(vectorElem(v, position));
    memcpy(vectorElem(v, position), elemAddr, v->elemSize);
}

void VectorDelete(vector *v, int position) {
    assert(position >= 0);
    assert(position < v->logicalLength);
    if (v->freeFn) v->freeFn(vectorElem(v, position));
    memmove(vectorElem(v, position), vectorElem(v, position + 1), (v->logicalLength - position - 1) * v->elemSize);
    v->logicalLength--;
}

static void *lsearch(const void *key, void *base, int count, int width, VectorCompareFunction searchfn) {
    for (int i = 0; i < count; ++i)
        if (searchfn((char*)base + i * width, key) == 0)
            return base + i * width;
    return NULL;
}

int VectorSearch(const vector *v, const void *key, VectorCompareFunction searchfn, int startIndex, bool isSorted) {
    assert(startIndex >= 0);
    assert(startIndex <= v->logicalLength);
    assert(key);
    assert(searchfn);
    char *found;
    void *base = vectorElem(v, startIndex);
    int count = v->logicalLength - startIndex;
    if (isSorted)
        found = bsearch(key, base, count, v->elemSize, searchfn);
    else
        found = lsearch(key, base, count, v->elemSize, searchfn);
    if (found)
        return (int)(found - (char*)v->elems) / v->elemSize;
    return -1;
}

void VectorSort(vector *v, VectorCompareFunction comparefn) {
    assert(comparefn);
    qsort(v->elems, v->logicalLength, v->elemSize, comparefn);
}

void VectorMap(vector *v, VectorMapFunction mapfn, void *auxData) {
    assert(mapfn);
    for (int i = 0; i < v->logicalLength; ++i)
        mapfn(vectorElem(v, i), auxData);
}
