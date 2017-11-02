#include <stdio.h>
#include <stdlib.h>
#include "Point.h"

/* display a Point value */
void show_point(Point point) {
    printf("Point in C      is (%d, %d)\n", point.x, point.y);
}

/* Increment a Point which was passed by value */
void move_point(Point point) {
    show_point(point);
    point.x++;
    point.y++;
    show_point(point);
}

/* Increment a Point which was passed by reference */
void move_point_by_ref(Point *point) {
    show_point(*point);
    point->x++;
    point->y++;
    show_point(*point);
}

/* Return by value */
Point get_point(void) {
    static int counter = 0;
    Point point = { counter++, counter++};
    printf("Returning Point    (%d, %d)\n", point.x, point.y);
    return point;
}
