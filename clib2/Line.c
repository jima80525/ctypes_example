#include <stdio.h>
#include <stdlib.h>
#include "Line.h"

void showLine(Line line) {
    printf("Line in C      is (%d, %d)->(%d, %d)\n", line.start.x, line.start.y,
            line.end.x, line.end.y);
}
