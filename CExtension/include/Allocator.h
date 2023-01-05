#ifndef Allocator_h
#define Allocator_h

#include "Node.h"
#include <stddef.h>

typedef struct {
    Node **chunks;
    int capacity;
    int chunkCount;
    int chunkSize;
    int top;
} Allocator;

Allocator *newAllocator(size_t capacity, size_t chunkSize);

Node *allocNode(Allocator *a);

void deleteAllocator(Allocator *a);


#endif /* Allocator_h */
