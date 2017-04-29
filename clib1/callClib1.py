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

# set up the C function which returns an allocated string.  The memory for this
# string is allocated in C and so must be freed in C.  I found that having the
# return type be a simple c_char_p caused a conversion to be done on the return.
# If I examined the type of the returned object, it was "bytes" which did not
# contain the original address of the C memory.  Using a ctypes.POINTER allows
# us to preserve that information so we can free it later.
f3 = libc.func3_return_string
# f3.restype = c_char_p  # c_char_p is a pointer to a string
f3.restype = POINTER(c_char_p)  # c_char_p is a pointer to a string

cStringAddress = f3()
# now we have the POINTER object.  we should convert that to something we can
# use on the python side.
phrase = c_char_p.from_buffer(cStringAddress)
print("Python was just handed {0}({1}):{2}".format(
    hex(addressof(cStringAddress.contents)), addressof(cStringAddress.contents),
    phrase.value))

# the memory that cStringAddress points to was allocated in C, we need to return
# it there as python's memory manager will NOT free it for us!  This is
# cStringAddress the pointer we have the in cStringAddress object is needed.
# The POINTER object stores the address of the C memory in the contents
# attribute.  NOTE: I'm still not sure why I need addressof for the .contents.
# Ctypes must do the conversion when passing to C that it does not do in python.
f4 = libc.func4_free_string
f4.argtypes = [POINTER(c_char_p), ]
print("Python is sending to C {0}({1}):{2}".format(
    hex(addressof(cStringAddress.contents)), addressof(cStringAddress.contents),
    phrase.value))
f4(cStringAddress.contents) # contents is the actual pointer returned

# The following block of code seems like it should work at first blush, but the
# conversions going on seem to make in not possible to get the correct address
# back to C.
badf3 = libc.func3_return_string
badf3.restype = c_char_p
badPhrase = badf3()
print(badPhrase)
badf4 = libc.func4_free_string
badf4.argtypes = [c_char_p, ]
# This line will core dump as it passes a different address to C
# badf4(badPhrase)
f5 = libc.func5_print_but_do_not_free_string
f5.argtypes = [c_char_p, ]
f5(badPhrase)


