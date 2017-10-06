#ifndef __LINE_H__
#define __LINE_H__
#include "Point.h"

typedef struct {
    Point start;
    Point end;
} Line;

Line getLine(void);
void showLine(Line line);
void moveLineRef(Line *line);

#endif /* __LINE_H__ */
