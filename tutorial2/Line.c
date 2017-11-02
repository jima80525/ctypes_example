#include <stdio.h>
#include <stdlib.h>
#include "Line.h"
#include "Point.h"

void show_line(Line line) {
    printf("Line in C      is (%d, %d)->(%d, %d)\n", line.start.x, line.start.y,
            line.end.x, line.end.y);
}

void move_line_by_ref(Line *line) {
    show_line(*line);
    move_point_by_ref(&line->start);
    move_point_by_ref(&line->end);
    show_line(*line);
}

Line get_line(void) {
    Line l = { get_point(), get_point() };
    return l;
}
