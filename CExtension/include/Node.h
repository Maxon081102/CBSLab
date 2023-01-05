#ifndef Node_h
#define Node_h

#include "Map.h"

typedef struct Node {
    Point p;
    int g, f;
    struct Node* parent;
} Node;

int nodeHash(const void *p, int numBuckets);
int nodeCmp(const void *p1, const void *p2);

int nodePtrHash(const void *p, int numBuckets);
int nodePtrCmp(const void *p1, const void *p2);

#endif /* Node_h */
