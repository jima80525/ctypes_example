#!/usr/bin/env python
from ctypes import *

libc = CDLL("./libclib1.so")
libc
print(libc.func1_no_args())
print(libc.func1_no_args())
print(libc.func1_no_args())
print(libc.func1_no_args())
