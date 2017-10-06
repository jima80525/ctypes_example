#ifndef __POINT_H__
#define __POINT_H__

/* Simple structure for ctypes example */
typedef struct {
    int x;
    int y;
} Point;

void showPoint(Point point);
void movePoint(Point point);
void movePointRef(Point *point);
Point getPoint(void);

#endif /* __POINT_H__ */
