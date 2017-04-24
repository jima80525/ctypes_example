#!/usr/bin/env python
from ctypes import *

libc = CDLL("./libclib1.so")
libc
print(libc.func1_no_args())
print(libc.func1_no_args())
print(libc.func1_no_args())
print(libc.func1_no_args())

# python strings are immutable.
x = "staring string"
print(x)
libc.func2_string_add_one(x)  # should fail
print(x)

y = create_string_buffer(str.encode(x)) # need to encode this to get bytes
print(y.value)
libc.func2_string_add_one(y)  # should fail
print(y.value)

libc.func3_return_string.restype = c_char_p  # c_char_p is a pointer to a string
where = libc.func3_return_string()
print(where)
