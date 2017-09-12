#ifndef __LINE_H__
#define __LINE_H__
#include "Point.h"

typedef struct {
    Point start;
    Point end;
} Line;

void showLine(Line line);

#endif /* __LINE_H__ */
