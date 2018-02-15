/* Simple structure for ctypes example */
typedef struct {
    int x;
    int y;
} Point;

void show_point(Point point);
void move_point(Point point);
void move_point_by_ref(Point *point);
Point get_default_point(void);
Point get_point(int x, int y);

