#include "Map.h"

#include <stdlib.h>
#include <stdbool.h>

int pointCmp(Point p1, Point p2) {
    int dx = p1.x - p2.x;
    if (dx != 0) return dx;
    return p1.y - p2.y;
}

/// Order by time, then by x, then by y
static int vConstraintCmp(const void *p1, const void *p2) {
    VConstraint *c1 = (VConstraint*)p1;
    VConstraint *c2 = (VConstraint*)p2;
    
    int dt = c1->time - c2->time;
    if (dt != 0) return dt;
    return pointCmp(c1->p, c2->p);
}

/// Order by time, then by x, then by y of the both points
static int eConstraintCmp(const void *p1, const void *p2) {
    EConstraint *c1 = (EConstraint*)p1;
    EConstraint *c2 = (EConstraint*)p2;
    
    int dt = c1->time - c2->time;
    if (dt != 0) return dt;
    
    int dp1 = pointCmp(c1->e.p1, c2->e.p1);
    if (dp1 != 0) return dp1;
    
    return pointCmp(c1->e.p2, c2->e.p2);
}

Map *newMap(int width, int height, const char *rawBuffer) {
    return newMapWithConstraints(width, height, NULL, NULL, rawBuffer);
}

Map *newMapWithConstraints(int width, int height,
                           vector *vertexConstraints,
                           vector *edgeConstraints,
                           const char *rawBuffer) {
    Map *map = malloc(sizeof(Map));
    map->width = width;
    map->height = height;
    map->vConstraints = vertexConstraints;
    map->eConstraints = edgeConstraints;
    map->data = rawBuffer;
    
    if (map->vConstraints) VectorSort(map->vConstraints, vConstraintCmp);
    if (map->eConstraints) VectorSort(map->eConstraints, eConstraintCmp);
    return map;
}

static void swap(Point *p1, Point *p2) {
    Point temp = *p1;
    *p1 = *p2;
    *p2 = temp;
}

static bool boundsCheck(Map *map, Point p) {
    bool xOk = 0 <= p.x && p.x < map->width;
    bool yOk = 0 <= p.y && p.y < map->height;
    return xOk && yOk;
}

static bool notInVConstraints(Map *map, int time, Point p) {
    VConstraint toFind = {time, p};
    return !map->vConstraints || VectorSearch(map->vConstraints, &toFind, vConstraintCmp, 0, true) == -1;
}
static bool notInEConstraints(Map *map, int time, Point p1, Point p2) {
    if (pointCmp(p1, p2) > 0) // in unsorted order, swap
        swap(&p1, &p2);
    EConstraint toFind = {time - 1, {p1, p2}};
    // the only difference and    ^^^^^^  reason why we can't have one type of constraints
    return !map->eConstraints || VectorSearch(map->eConstraints, &toFind, eConstraintCmp, 0, true) == -1;
}
static bool notInConstraints(Map *map, int time, Point current, Point dest) {
    return notInVConstraints(map, time, dest) && notInEConstraints(map, time, current, dest);
}

int getNeighbors(Map *map, int time, Point p, bool isGoal, Point storage[5]) {
    int k = 0;
    bool atLeastOneIsConstrained = false;
    Point d[] = { {0, 1}, {0, -1}, {1, 0}, {-1, 0} };
    for (int i = 0; i < 4; ++i) {
        Point res = {p.x + d[i].x, p.y + d[i].y};
        if (boundsCheck(map, res) && map->data[res.y * map->width + res.x] == 0) {
            // in bounds and there are no walls in this place
            if (notInConstraints(map, time, p, res))
                // no vertex constraints or edge constraints
                storage[k++] = res;
            else
                atLeastOneIsConstrained = true;
        }
    }
    
    // Respect to Maxim!
    // if not around constriaints then we should definetly move,
    // only otherwise may we stay on the same position, if not constrained
    //
    // ps. If the node is already a goal node (but in lesser time than we want)
    // then we may also not move frome it
    if ((atLeastOneIsConstrained || isGoal) && notInVConstraints(map, time, p))
        storage[k++] = p;
    
    return k;
}

typedef struct {
    Point g;
    int maxSoFar;
} SearchHelper;

static void findMax(void *p, void *acc) {
    VConstraint *vc = (VConstraint*)p;
    SearchHelper *s = (SearchHelper*)acc;
    if (vc->p.x == s->g.x && vc->p.y == s->g.y && vc->time > s->maxSoFar)
        s->maxSoFar = vc->time;
}

int getGoalTimeBoundary(Map *map, Point g) {
    SearchHelper acc = {g, .maxSoFar = -1};
    if (map->vConstraints) VectorMap(map->vConstraints, findMax, &acc);
    return acc.maxSoFar;
}

void deleteMap(Map *map) {
    map->data = NULL;
    free(map);
}
