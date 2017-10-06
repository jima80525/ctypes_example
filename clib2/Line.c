#include <stdio.h>
#include <stdlib.h>
#include "Line.h"
#include "Point.h"

Line getLine(void) {
    Line l = { getPoint(), getPoint() };
    return l;
}

void showLine(Line line) {
    printf("Line in C      is (%d, %d)->(%d, %d)\n", line.start.x, line.start.y,
            line.end.x, line.end.y);
}

void moveLineRef(Line *line) {
    showLine(*line);
    movePointRef(&line->start);
    movePointRef(&line->end);
    showLine(*line);
}
