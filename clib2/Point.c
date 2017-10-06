#include <stdio.h>
#include <stdlib.h>
#include "Point.h"

/* Static counter used for initializing new points */
static int counter = 0;

/* display a Point value */
void showPoint(Point point) {
    printf("Point in C      is (%d, %d)\n", point.x, point.y);
}

/* Increment a Point which was passed by value */
void movePoint(Point point) {
    showPoint(point);
    point.x++;
    point.y++;
    showPoint(point);
}

/* Increment a Point which was passed by reference */
void movePointRef(Point *point) {
    showPoint(*point);
    point->x++;
    point->y++;
    showPoint(*point);
}

/* Return by value */
Point getPoint(void) {
    Point point = { counter++, counter++};
    printf("Returning Point    (%d, %d)\n", point.x, point.y);
    return point;
}
