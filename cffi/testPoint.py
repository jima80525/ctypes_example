#!/usr/bin/env python
import _point

class Point():
    def __init__(self, x=None, y=None):
        if x:
            self.p = _point.lib.get_point(x, y)
        else:
            self.p = _point.lib.get_default_point()
        
    def __repr__(self):
        return '({0}, {1})'.format(self.p.x, self.p.y)

    def show_point(self):
        _point.lib.show_point(self.p)

    def move_point(self):
        _point.lib.move_point(self.p)

    def move_point_by_ref(self):
        ppoint = _point.ffi.new("Point*", self.p)
        _point.lib.move_point_by_ref(ppoint)
        self.p = ppoint


if __name__ == '__main__':
    ###########################################################################
    print("Pass a struct into C")
    a = Point(1, 2)
    print("Point in python is", a)
    a.show_point()
    print()

    ###########################################################################
    print("Pass by value")
    a = Point(5, 6)
    print("Point in python is", a)
    a.move_point()
    print("Point in python is", a)
    print()

    ###########################################################################
    print("Pass by reference")
    a = Point(5, 6)
    print("Point in python is", a)
    a.move_point_by_ref()
    print("Point in python is", a)
    print()

    ###########################################################################
    print("Get Struct from C")
    a = Point()
    print("New Point in python (from C) is", a)
    a = Point()
    print("New Point in python (from C) is", a)
    a = Point()
    print("New Point in python (from C) is", a)
    a = Point()
    print("New Point in python (from C) is", a)
