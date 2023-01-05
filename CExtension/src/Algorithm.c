#include <stdio.h>
#include <stdlib.h>

#include "Allocator.h"
#include "PriorityQueue.h"
#include "hashset.h"

#define NUM_BUCKETS 1337

int manhattan(Point p1, Point p2) {
    return abs(p1.x - p2.x) + abs(p1.y - p2.y);
}

Allocator *a;

bool findPath(Map *map, Point s, Point g, Node *storage) {
    hashset closed;
    HashSetNew(&closed, sizeof(Node*), NUM_BUCKETS, nodePtrHash, nodePtrCmp, NULL);
    PriorityQueue *open = newQueue(map->height * map->width / 2);
    
    int maxConstrainedTime = getGoalTimeBoundary(map, g);
    bool found = false;
    
    Node *node = allocNode(a);
    node->p = s;
    enqueue(open, node);
    
    while (dequeue(open, node)) {
        found = false;
        if (node->p.x == g.x && node->p.y == g.y) {
            found = true;
            if (node->g > maxConstrainedTime) {
                *storage = *node;
                break;
            }
        }
        
        HashSetEnter(&closed, &node);
        
        Point neighbors[5];
        int amount = getNeighbors(map, node->g + 1, node->p, found, neighbors);
        for (int i = 0; i < amount; ++i) {
            Node neighbour = {neighbors[i], .g = node->g + 1};
            Node *ptr = &neighbour;

            if (HashSetLookup(&closed, &ptr) == NULL) {
                neighbour.f = neighbour.g + manhattan(neighbour.p, g);
                neighbour.parent = node;
                enqueue(open, &neighbour);
            }
        }
        node = allocNode(a);
    }
    
    deleteQueue(open);
    HashSetDispose(&closed);
    
    return found;
}

bool testPath(void) {
    // specify actual map
    // 1 - wall, 0 - path
    const char mapArray[] = {
        1, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 1, 1, 0, 1,
        1, 0, 0, 1, 1, 1, 1,
        1, 1, 0, 0, 0, 0, 1,
        1, 1, 1, 1, 1, 1, 1
    };
    
    int mapWidth = 7;
    int mapHeight = 5;
    
    Point start = {1, 0};     // <----- specify start point (x, y)
    Point goal = {1, 1};     // <------- specify goal point (x, y)
    
    a = newAllocator(10, mapWidth * mapHeight / 2);
    
    vector vConstraints, eConstraints;
    
    // specify constraints
    VConstraint vConstraintsArray[] = {
        {1, {1, 0}}, // at t = 1, cannot be at (1, 0)
        {1, {3, 3}}, // at t = 1, cannot also be at (3, 3)
        {2, {3, 1}}, // at t = 2, cannot bet at (3, 1)
        // etc...
    };
    
    // specify constraints
    EConstraint eConstraintsArray[] = {
        {1, { {0, 0}, {0, 1} }}, // at t = 1, cannot go by edge (0, 0) -> (0, 1)
        {0, { {1, 0}, {1, 1} }}, // at t = 0, cannot go (1, 0) -> (1, 1) or (1, 1) -> (1, 0) it is the same
        // etc...
    };
    
    VectorNewFromBuffer(&vConstraints,
                        sizeof(VConstraint),
                        sizeof(vConstraintsArray) / sizeof(VConstraint),
                        vConstraintsArray);
    
    VectorNewFromBuffer(&eConstraints,
                        sizeof(EConstraint),
                        sizeof(eConstraintsArray) / sizeof(EConstraint),
                        eConstraintsArray);
    
    Map *map = newMapWithConstraints(mapWidth, mapHeight, &vConstraints, &eConstraints, mapArray);
    // if vConstraints or eConstraints is empty here ----->^^^^^^^^^^^^^^^^^^^^^^^^^, better pass NULL instead of
    // empty constraints
    // say eConstraints is empty, then
//    Map *map = newMapWithConstraints(mapWidth, mapHeight, &vConstraints, NULL, mapArray);
    // ^^^^^^^^^^ this would be the call                                   ^^^^
    
    Node result;
    bool found = findPath(map, start, goal, &result);
    
    if (!found) {
        deleteAllocator(a);
        return false;
    }

    int l = 0;
    Point path[100] = {0};
    Node *current = &result;
    printf("result.g = %d\n", result.g);
    while (current) {
        path[l++] = current->p;
        printf("(%d, %d) <- ", current->p.x, current->p.y);
        current = current->parent;
    }
    printf("\n");

    deleteAllocator(a);
    deleteMap(map);
    
    return found;
}

int main() { 
    testPath();
    return 0;
}
