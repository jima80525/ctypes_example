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
Point get_default_point(void) {
    static int x_counter = 0;
    static int y_counter = 100;
    x_counter++;
    y_counter--;
    return get_point(x_counter, y_counter);
}

Point get_point(int x, int y) {
    Point point = { x, y };
    printf("Returning Point    (%d, %d)\n", point.x, point.y);
    return point;
}
