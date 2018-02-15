#!/usr/bin/env python
import _line


class Line():
    def __init__(self):
        self.line = _line.lib.get_line()

    def __repr__(self):
        return '({0}, {1})->({2}, {3})'.format(
            self.line.start.x, self.line.start.y, 
            self.line.end.x, self.line.end.y)

    def show_line(self):
        _line.lib.show_line(self.line)

    def move_line(self):
        pline = _line.ffi.new("Line*", self.line)
        _line.lib.move_line_by_ref(pline)
        self.line = pline


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

