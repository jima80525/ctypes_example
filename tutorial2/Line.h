#ifndef __LINE_H__
#define __LINE_H__
#include "Point.h"

typedef struct {
    Point start;
    Point end;
} Line;

Line get_line(void);
void show_line(Line line);
void move_line_by_ref(Line *line);

#endif /* __LINE_H__ */
