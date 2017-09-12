#include <stdio.h>
#include <stdlib.h>
#include "clib2.h"

/* Static counter used for initializing new points */
static int counter = 0;

void showLine(Line line) {
    printf("Line in C      is (%d, %d)->(%d, %d)\n", line.start.x, line.start.y,
            line.end.x, line.end.y);
}
