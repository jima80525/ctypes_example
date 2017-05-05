#!/usr/bin/env python
from ctypes import *

# load the shared library into c types.  NOTE: don't use a hard-coded path in
# production code, please
libc = CDLL("./libclib1.so")

###############################################################################
# Calling a function with no arguments is straight forward.  This function
# returns a series of counting values using a static int in C.
print("Calling simple C counting function four times:")
print(libc.func1_no_args())
print(libc.func1_no_args())
print(libc.func1_no_args())
print(libc.func1_no_args())
print()

###############################################################################
# python strings are immutable.  The function adds 1 to each value in the array.
# The python string will remain unchanged afterwards.
print("Calling C function which tries to modify python string")
x = "staring string"
print("Before:", x)
libc.func2_string_add_one(x)  # does not change value, even though it tries!
print("After:", x)

# The ctypes string buffer IS mutable, however.
print("Calling C function with mutable buffer this time")
y = create_string_buffer(str.encode(x)) # need to encode this to get bytes
print("Before:", y.value)
libc.func2_string_add_one(y)  # should fail
print("After:", y.value)
print()

###############################################################################
# set up the C function which returns an allocated string.  The memory for this
# string is allocated in C and so must be freed in C.
#
# I found that having the return type be a simple c_char_p caused a conversion
# to be done on the return.  If I examined the type of the returned object, it
# was "bytes" which did not contain the original address of the C memory (at
# least in any usable form).
#
# Using a ctypes.POINTER allows us to preserve that information so we can free
# it later.
alloc_func = libc.func3_return_string
# alloc_func.restype = c_char_p  # c_char_p is a pointer to a string
alloc_func.restype = POINTER(c_char) # this is a ctypes.POINTER object which
                                     # holds the address of the data

print("Allocating and freeing memory in C")
cStringAddress = alloc_func()
# now we have the POINTER object.  we should convert that to something we can
# use on the python side.
phrase = c_char_p.from_buffer(cStringAddress)
print("Python was just handed {0}({1}):{2}".format(
    hex(addressof(cStringAddress.contents)),
    addressof(cStringAddress.contents),
    phrase.value))

# the memory that cStringAddress points to was allocated in C, we need to return
# it there as python's memory manager will NOT free it for us!  This is
# cStringAddress the pointer we have the in cStringAddress object is needed.
# The POINTER object stores the address of the C memory in the contents
# attribute.  NOTE: When printing it out, you need the addressof for the
# contents to tell python NOT to convert it to what the contents pointer is
# pointing at.
free_func = libc.func4_free_string
free_func.argtypes = [POINTER(c_char), ]
print("Python is sending to C {0}({1}):{2}".format(
    hex(addressof(cStringAddress.contents)), addressof(cStringAddress.contents),
    phrase.value))
free_func(cStringAddress) # contents is the actual pointer returned

