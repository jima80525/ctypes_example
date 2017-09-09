#!/usr/bin/env python
from ctypes import *

# struct Point { }
class Point(Structure):
    _fields_ = [('x', c_int), ('y', c_int)]

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)

class Line(Structure):
    _fields_ = [('start', Point), ('end', Point)]

    def __repr__(self):
        return '{0}->{1}'.format(self.start, self.end)


# load the shared library into c types.  NOTE: don't use a hard-coded path in
# production code, please
libc = CDLL("./libclib2.so")

###############################################################################
print("Pass a struct into C")
showPoint = libc.showPoint
showPoint.argtypes = [Point]
a = Point(1, 2)
print("Point in python is", a)
showPoint(a)
print()

###############################################################################
print("Pass a nested struct into C")
showLine = libc.showLine
showLine.argtypes = [Line]
a = Point(1, 2)
b = Point(3, 4)
l = Line(a, b)
print("Line in python is", l)
showLine(l)
print()


###############################################################################
print("Pass by value")
movePoint = libc.movePoint
movePoint.argtypes = [Point]
a = Point(5, 6)
print("Point in python is", a)
movePoint(a)
print("Point in python is", a)
print()

###############################################################################
print("Pass by reference")
movePointRef = libc.movePointRef
movePointRef.argtypes = [POINTER(Point)]
a = Point(5, 6)
print("Point in python is", a)
movePointRef(a)
print("Point in python is", a)
print()

###############################################################################
print("Return struct")
getPoint = libc.getPoint
getPoint.restype = Point
a = getPoint()
print("Point in python is", a)
print()

###############################################################################
print("Return struct pointer")
getPointPointer = libc.getPointPointer
getPointPointer.restype = POINTER(Point)
a = getPointPointer()
print("Point in python is", a)
print()
