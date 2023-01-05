#include "hashset.h"
#include <assert.h>
#include <stdlib.h>
#include <string.h>

#define DEFAULT_BUCKET_SIZE 4

void HashSetNew(hashset *h, int elemSize, int numBuckets,
                HashSetHashFunction hashfn, HashSetCompareFunction comparefn, HashSetFreeFunction freefn) {
    assert(elemSize > 0);
    assert(numBuckets > 0);
    assert(hashfn);
    assert(comparefn);
    h->buckets = calloc(numBuckets, sizeof(vector));
    for (int i = 0; i < numBuckets; ++i)
        VectorNew(h->buckets + i, elemSize, freefn, DEFAULT_BUCKET_SIZE);
    h->numBuckets = numBuckets;
    h->elemSize = elemSize;
    h->elemCount = 0;
    h->hashfn = hashfn;
    h->comparefn = comparefn;
}

void HashSetDispose(hashset *h) {
    for (int i = 0; i < h->numBuckets; ++i)
        VectorDispose(h->buckets + i);
    free(h->buckets);
}

int HashSetCount(const hashset *h) {
    return h->elemCount;
}

void HashSetMap(hashset *h, HashSetMapFunction mapfn, void *auxData) {
    assert(mapfn);
    for (int i = 0; i < h->numBuckets; ++i)
        VectorMap(h->buckets + i, mapfn, auxData);
}

void *HashSetEnter(hashset *h, const void *elemAddr) {
    assert(elemAddr);
    int hash = h->hashfn(elemAddr, h->numBuckets);
    assert(hash >= 0);
    assert(hash < h->numBuckets);
    vector *bucket = h->buckets + hash;
    for (int i = 0; i < bucket->logicalLength; ++i) {
        const void *bucketAddr = VectorNth(bucket, i);
        int compare = h->comparefn(elemAddr, bucketAddr);
        if (compare > 0) continue;
        if (compare == 0) VectorReplace(bucket, elemAddr, i);
        else {
            VectorInsert(bucket, elemAddr, i);
            h->elemCount++;
        }
        return VectorNth(bucket, i);
    }
    VectorAppend(bucket, elemAddr);
    h->elemCount++;
    // inserted element is the last
    return VectorNth(bucket, VectorLength(bucket) - 1);
}

void *HashSetLookup(hashset *h, const void *elemAddr) {
    assert(elemAddr);
    int hash = h->hashfn(elemAddr, h->numBuckets);
    assert(hash >= 0);
    assert(hash < h->numBuckets);
    vector *bucket = h->buckets + hash;
    for (int i = 0; i < bucket->logicalLength; ++i) {
        void *bucketAddr = VectorNth(bucket, i);
        if (h->comparefn(elemAddr, bucketAddr) == 0) return bucketAddr;
    }
    return NULL;
}
