#!/usr/bin/env python
import ctypes


def wrapFunction(lib, funcname, restype, argtypes):
    ''' Simplify wrapping ctypes functions '''
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func


# struct Point { }
class Point(ctypes.Structure):
    _fields_ = [('x', ctypes.c_int), ('y', ctypes.c_int)]

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)


if __name__ == '__main__':
    # load the shared library into c types.  NOTE: don't use a hard-coded path
    # in production code, please
    libc = ctypes.CDLL("./libpoint.so")

    ###########################################################################
    print("Pass a struct into C")
    showPoint = wrapFunction(libc, 'showPoint', None, [Point])
    a = Point(1, 2)
    print("Point in python is", a)
    showPoint(a)
    print()

    ###########################################################################
    print("Pass by value")
    movePoint = wrapFunction(libc, 'movePoint', None, [Point])
    a = Point(5, 6)
    print("Point in python is", a)
    movePoint(a)
    print("Point in python is", a)
    print()

    ###########################################################################
    print("Pass by reference")
    movePointRef = wrapFunction(libc, 'movePointRef', None,
                                [ctypes.POINTER(Point)])
    a = Point(5, 6)
    print("Point in python is", a)
    movePointRef(a)
    print("Point in python is", a)
    print()
