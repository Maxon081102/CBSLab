#ifndef PriorityQueue_h
#define PriorityQueue_h

#include "Node.h"

#include <stddef.h>
#include <stdbool.h>

typedef struct {
    Node* nodes;
    size_t size;
    size_t capacity;
} PriorityQueue;

PriorityQueue *newQueue(size_t capacity);

bool dequeue(PriorityQueue *q, Node *storage);

void enqueue(PriorityQueue *q, const Node *node);

void deleteQueue(PriorityQueue *q);

#endif /* PriorityQueue_h */
