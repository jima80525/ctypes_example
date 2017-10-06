#!/usr/bin/env python
import ctypes
import testWrappedPoint


def wrapFunction(lib, funcname, restype, argtypes):
    ''' Simplify wrapping ctypes functions '''
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func


class Line(ctypes.Structure):
    _fields_ = [('start', testWrappedPoint.Point),
                ('end', testWrappedPoint.Point)]

    def __init__(self, lib):
        getLine = wrapFunction(lib, 'getLine', Line, None)
        a = getLine()
        self.start = a.start
        self.end = a.end
        self.showLineFunc = wrapFunction(lib, 'showLine', None, [Line])
        self.moveLineFunc = wrapFunction(lib, 'moveLineRef', None,
                                         [ctypes.POINTER(Line)])

    def __repr__(self):
        return '{0}->{1}'.format(self.start, self.end)

    def showLine(self):
        self.showLineFunc(self)

    def moveLine(self):
        self.moveLineFunc(self)

    def moveLineBad(self):
        ''' You might think this would work, but it will not.  start and end
        are NOT of type python class Point.  They are ctype types and don't
        maintain the attributes of the Python class.'''
        # self.start.movePoint()
        # self.end.movePoint()
        pass


class PyLine():
    def __init__(self, lib):
        self.start = testWrappedPoint.Point(lib)
        self.end = testWrappedPoint.Point(lib)

    def __repr__(self):
        return '{0}->{1}'.format(self.start, self.end)

    def showLine(self):
        print("Line in Python is {0}->{1}".format(self.start, self.end))

    def moveLine(self):
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
    l.showLine()
    print()

    ###########################################################################
    print("Move Line in C")
    l = Line(libc)
    print("Line in python is", l)
    l.moveLine()
    print("Line in python is", l)
    print()

    ###########################################################################
    print("Move Line in Python")
    pl = PyLine(libc)
    print("Line in python is", l)
    l.moveLine()
    print("Line in python is", l)
    print()
