#!/usr/bin/env python
import ctypes
import testWrappedPoint
import testPoint


def wrap_function(lib, funcname, restype, argtypes):
    ''' Simplify wrapping ctypes functions '''
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func


class Line(ctypes.Structure):
    _fields_ = [('start', testPoint.Point), ('end', testPoint.Point)]

    def __init__(self, lib):
        get_line = wrap_function(lib, 'get_line', Line, None)
        a = get_line()
        self.start = a.start
        self.end = a.end
        self.show_line_func = wrap_function(lib, 'show_line', None, [Line])
        self.move_line_func = wrap_function(lib, 'move_line_by_ref', None,
                                            [ctypes.POINTER(Line)])

    def __repr__(self):
        return '{0}->{1}'.format(self.start, self.end)

    def show_line(self):
        self.show_line_func(self)

    def move_line(self):
        self.move_line_func(self)


class PyLine():
    def __init__(self, lib):
        self.start = testWrappedPoint.Point(lib)
        self.end = testWrappedPoint.Point(lib)

    def __repr__(self):
        return '{0}->{1}'.format(self.start, self.end)

    def show_line(self):
        print("Line in Python is {0}->{1}".format(self.start, self.end))

    def move_line(self):
        self.start.movePoint()
        self.end.movePoint()


if __name__ == '__main__':
    # load the shared library into c types.  NOTE: don't use a hard-coded path
    # in production code, please
    libc = ctypes.CDLL("./libline.so")

    ###########################################################################
    print("Pass a nested struct into C")
    l = Line(libc)
    print("Line in python is", l)
    l.show_line()
    print()

    ###########################################################################
    print("Move Line in C")
    l = Line(libc)
    print("Line in python is", l)
    l.move_line()
    print("Line in python is", l)
    print()

    ###########################################################################
    print("Move Line in Python")
    pl = PyLine(libc)
    print("Line in python is", l)
    l.move_line()
    print("Line in python is", l)
    print()
