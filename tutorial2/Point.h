#ifndef __POINT_H__
#define __POINT_H__

/* Simple structure for ctypes example */
typedef struct {
    int x;
    int y;
} Point;

void show_point(Point point);
void move_point(Point point);
void move_point_by_ref(Point *point);
Point get_point(void);

#endif /* __POINT_H__ */
