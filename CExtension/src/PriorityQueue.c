#include "PriorityQueue.h"

#include <stdlib.h>
#include <string.h>
#include <assert.h>

PriorityQueue *newQueue(size_t capacity) {
    assert(capacity > 0);
    PriorityQueue *q = malloc(sizeof(PriorityQueue));
    q->size = 0;
    q->nodes = calloc(capacity, sizeof(Node));
    q->capacity = capacity;
    return q;
}

bool dequeue(PriorityQueue *q, Node *storage) {
    if (q->size == 0) return false;
    *storage = q->nodes[--q->size];
    return true;
}

static void grow(PriorityQueue *q) {
    void *reallocated = realloc(q->nodes, sizeof(Node) * q->capacity * 2);
    assert(reallocated);
    q->capacity *= 2;
    q->nodes = reallocated;
}

static int binarySearch(int a, int b, Node* nodes, int f) {
    int m;
    do {
        m = (a + b) / 2;
        if (nodes[m].f > f) a = m + 1;
        else if (f > nodes[m].f) b = m;
        else break;
        m = a;
    } while (a != b);
    
    // we want to insert equal value to the rightmost index
    while (m < b && nodes[m].f == f) ++m;
    
    return m;
}

void enqueue(PriorityQueue *q, const Node *node) {
    if (q->size == q->capacity) grow(q);
    
    if (q->size == 0) {
        q->nodes[q->size++] = *node;
        return;
    }
    
    int paste = binarySearch(0, (int)q->size, q->nodes, node->f);
    
    memmove(q->nodes + paste + 1, q->nodes + paste, sizeof(Node) * (q->size - paste));
    q->nodes[paste] = *node;
    
    q->size++;
}

void deleteQueue(PriorityQueue *q) {
    free(q->nodes);
    free(q);
}
