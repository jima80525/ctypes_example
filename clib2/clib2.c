#include <stdio.h>
#include <stdlib.h>
#include "clib2.h"

/* Static counter used for initializing new points */
static int counter = 0;

/* display a Point value */
void showPoint(Point point) {
    printf("Point in C      is (%d, %d)\n", point.x, point.y);
}
void showPointRef(Point *point) {
    printf("Point in C      is (%d, %d)\n", point->x, point->y);
}

void showLine(Line line) {
    printf("Line in C      is (%d, %d)->(%d, %d)\n", line.start.x, line.start.y,
            line.end.x, line.end.y);
}

/* Increment a Point which was passed by value */
void movePoint(Point point) {
    printf("Point in C      is (%d, %d)\n", point.x, point.y);
    point.x++;
    point.y++;
    printf("Point in C      is (%d, %d)\n", point.x, point.y);
    /* return point; */
}

/* Increment a Point which was passed by reference */
void movePointRef(Point *point) {
    printf("Point in C      is (%d, %d)\n", point->x, point->y);
    point->x++;
    point->y++;
    printf("Point in C      is (%d, %d)\n", point->x, point->y);
    /* return point; */
}

/* Return by value */
Point getPoint(void) {
    Point point = { counter++, counter++};
    printf("Returning Point (%d, %d)\n", point.x, point.y);
    return point;
}

/* Return by reference */
Point* getPointPointer(void) {
    Point* point = malloc(sizeof(Point));
    point->x = counter++;
    point->y = counter++;

    printf("Returning Point (%d, %d)\n", point->x, point->y);
    return point;
}
