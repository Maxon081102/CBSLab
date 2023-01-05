#include "Allocator.h"

#include <stdlib.h>
#include <assert.h>

Allocator *newAllocator(size_t capacity, size_t chunkSize) {
    assert(capacity > 0);
    assert(chunkSize > 0);
    Allocator *a = malloc(sizeof(Allocator));
    a->chunks = calloc(capacity, sizeof(Node*));
    a->capacity = (int)capacity;
    a->chunkCount = 0;
    a->chunkSize = (int)chunkSize;
    a->top = 0;
    return a;
}

static void grow(Allocator *a) {
    if (a->chunkCount == a->capacity) {
        Node **reallocated = realloc(a->chunks, 2 * a->capacity * sizeof(Node*));
        assert(reallocated);
        a->chunks = reallocated;
        a->capacity *= 2;
    }
    
    a->chunks[a->chunkCount] = calloc(a->chunkSize, sizeof(Node));
    a->chunkCount++;
}

Node *allocNode(Allocator *a) {
    int chunkIndex = a->top / a->chunkSize;
    int nodeIndex = a->top % a->chunkSize;
    
    if (chunkIndex == a->chunkCount)
        grow(a);
    
    a->top++;
    return a->chunks[chunkIndex] + nodeIndex;
}

void deleteAllocator(Allocator *a) {
    for (int i = 0; i < a->chunkCount; ++i)
        free(a->chunks[i]);
    free(a->chunks);
    a->chunks = NULL;
    free(a);
}
