#ifndef Map_h
#define Map_h

#include "vector.h"

typedef struct {
    int x, y;
} Point;

/// performs similar to `strcmp`
/// compare points by `x`, if equal, compare by `y`
/// returns:
///     negative number if `p1 < p2`
///     0 if `p1 == p2`
///     positive number if `p1 > p2`
int pointCmp(Point p1, Point p2);

typedef struct {
    Point p1, p2;
} Edge;

typedef struct {
    int time;
    Point p;
} VConstraint;

typedef struct {
    int time;
    Edge e;
} EConstraint;

typedef struct {
    int width, height;
    vector *vConstraints;
    vector *eConstraints;
    const char *data;
} Map;

/// creates map with given `width` and `height`
/// put your ndarray's data into `rawBuffer` pointer
/// it will be used as an array of bools indicating wheter cell is traversable
Map *newMap(int width, int height, const char *rawBuffer);

/// creates map similar to `newMap` function, but created map will also have vertex and/or edge constraints
/// all of which will be checked for in the `getNeighbors` function
Map *newMapWithConstraints(int width, int height,
                           vector *vertexConstraints,
                           vector *edgeConstraints,
                           const char *rawBuffer);

/// find neighbors to the point `p` at `time` on the 4-connected grid
/// returns the amount of neighbors it found, max is 5 (4 directoins + stay put),
/// found neighbors positions are stored in `storage`
int getNeighbors(Map *map, int time, Point p, bool isGoal, Point storage[5]);

/// returns the last time when point `g` is constraint
/// if `g` is not constrainded at any time, returns `-1`
/// this is so A* algorithm *would not exit when found goal node
/// if it is constrained later in the future
int getGoalTimeBoundary(Map *map, Point g);

void deleteMap(Map *map);

#endif /* Map_h */
