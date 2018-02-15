#include "Point.h"

typedef struct {
    Point start;
    Point end;
} Line;

Line get_line(void);
void show_line(Line line);
void move_line_by_ref(Line *line);

