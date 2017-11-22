#!/usr/bin/env python
import ctypes
import testWrappedPoint
import testPoint


class Line(ctypes.Structure):
    _fields_ = [('start', testPoint.Point), ('end', testPoint.Point)]
    _libc = ctypes.CDLL("./libline.so")

    def __init__(self):
        a = self.get_line()
        self.start = a.start
        self.end = a.end

    def __repr__(self):
        return '{0}->{1}'.format(self.start, self.end)

    def show_line(self):
        self.show_line_func(self)

    def move_line(self):
        self.move_line_func(self)

    @staticmethod
    def wrap_function(funcname, restype, argtypes):
        ''' Simplify wrapping ctypes functions '''
        func = Line._libc.__getattr__(funcname)
        func.restype = restype
        func.argtypes = argtypes
        return func


Line.get_line = Line.wrap_function('get_line', Line, None)
Line.show_line_func = Line.wrap_function('show_line', None, [Line])
Line.move_line_func = Line.wrap_function('move_line_by_ref', None,
                                         [ctypes.POINTER(Line)])


class PyLine():
    def __init__(self):
        self.start = testWrappedPoint.Point()
        self.end = testWrappedPoint.Point()

    def __repr__(self):
        return '{0}->{1}'.format(self.start, self.end)

    def show_line(self):
        print("Line in Python is {0}->{1}".format(self.start, self.end))

    def move_line(self):
        self.start.movePoint()
        self.end.movePoint()


if __name__ == '__main__':
    ###########################################################################
    print("Pass a nested struct into C")
    l = Line()
    print("Line in python is", l)
    l.show_line()
    print()

    ###########################################################################
    print("Move Line in C")
    l = Line()
    print("Line in python is", l)
    l.move_line()
    print("Line in python is", l)
    print()

    ###########################################################################
    print("Move Line in Python")
    pl = PyLine()
    print("Line in python is", l)
    l.move_line()
    print("Line in python is", l)
    print()
