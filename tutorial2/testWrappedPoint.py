#!/usr/bin/env python
import ctypes


def wrapFunction(lib, funcname, restype, argtypes):
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
            getPoint = wrapFunction(lib, 'getPoint', Point, None)
            self = getPoint()

        self.showPointFunc = wrapFunction(lib, 'showPoint', None, [Point])
        self.movePointFunc = wrapFunction(lib, 'movePoint', None, [Point])
        self.movePointRefFunc = wrapFunction(lib, 'movePointRef', None,
                                             [ctypes.POINTER(Point)])

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def showPoint(self):
        self.showPointFunc(self)

    def movePoint(self):
        self.movePointFunc(self)

    def movePointRef(self):
        self.movePointRefFunc(self)


if __name__ == '__main__':
    ###########################################################################
    libc = ctypes.CDLL("./libpoint.so")
    print("Pass a struct into C")
    a = Point(libc, 1, 2)
    print("Point in python is", a)
    a.showPoint()
    print()

    ###########################################################################
    print("Pass by value")
    a = Point(libc, 5, 6)
    print("Point in python is", a)
    a.movePoint()
    print("Point in python is", a)
    print()

    ###########################################################################
    print("Pass by reference")
    a = Point(libc, 5, 6)
    print("Point in python is", a)
    a.movePointRef()
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
