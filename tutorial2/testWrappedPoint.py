#!/usr/bin/env python
import ctypes


def wrap_function(lib, funcname, restype, argtypes):
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func


class Point(ctypes.Structure):
    _fields_ = [('x', ctypes.c_int), ('y', ctypes.c_int)]

    def __init__(self, lib, x=None, y=None):
        if x:
            self.x = x
            self.y = y
        else:
            get_point = wrap_function(lib, 'get_point', Point, None)
            point = get_point()
            self.x = point.x
            self.y = point.y

        self.show_point_func = wrap_function(lib, 'show_point', None, [Point])
        self.move_point_func = wrap_function(lib, 'move_point', None, [Point])
        self.move_point_by_ref_func = wrap_function(lib, 'move_point_by_ref',
                                                    None,
                                                    [ctypes.POINTER(Point)])

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def show_point(self):
        self.show_point_func(self)

    def move_point(self):
        self.move_point_func(self)

    def move_point_by_ref(self):
        self.move_point_by_ref_func(self)


if __name__ == '__main__':
    ###########################################################################
    libc = ctypes.CDLL("./libpoint.so")
    print("Pass a struct into C")
    a = Point(libc, 1, 2)
    print("Point in python is", a)
    a.show_point()
    print()

    ###########################################################################
    print("Pass by value")
    a = Point(libc, 5, 6)
    print("Point in python is", a)
    a.move_point()
    print("Point in python is", a)
    print()

    ###########################################################################
    print("Pass by reference")
    a = Point(libc, 5, 6)
    print("Point in python is", a)
    a.move_point_by_ref()
    print("Point in python is", a)
    print()

    ###########################################################################
    print("Get Struct from C")
    a = Point(libc)
    print("New Point in python (from C) is", a)
    a = Point(libc)
    print("New Point in python (from C) is", a)
    a = Point(libc)
    print("New Point in python (from C) is", a)
    a = Point(libc)
    print("New Point in python (from C) is", a)
