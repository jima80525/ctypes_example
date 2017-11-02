#!/usr/bin/env python
""" Simple examples of calling C functions through ctypes module. """
import ctypes
import os


def call_function_with_no_args(libc):
    ''' Calling a function with no arguments is straight forward.  This
        function returns a series of counting values using a static int in C.
    '''
    print("Calling simple C counting function four times:")
    print(libc.simple_function())
    print(libc.simple_function())
    print(libc.simple_function())
    print(libc.simple_function())
    print()


def call_string_modifier(libc):
    ''' python strings are immutable.  The function adds 1 to each value in the
        array. The python string will remain unchanged afterwards.
        Also try with the ctypes string_buffer which is mutable.
    '''
    print("Calling C function which tries to modify Python string")
    original_string = "starting string"
    print("Before:", original_string)
    # this call does not change value, even though it tries!
    libc.add_one_to_string(original_string)
    print("After: ", original_string)

    # The ctypes string buffer IS mutable, however.
    print("Calling C function with mutable buffer this time")
    # need to encode the original to get bytes for string_buffer
    mutable_string = ctypes.create_string_buffer(str.encode(original_string))
    print("Before:", mutable_string.value)
    libc.add_one_to_string(mutable_string)  # works!
    print("After: ", mutable_string.value)
    print()


def call_memory_allocation(libc):
    ''' Call a C function which allocates memory.  Show how to pass that
        memory pointer back to C to be freed.
    '''
    # set up the C function which returns an allocated string.  The memory for
    # this string is allocated in C and so must be freed in C.
    #
    # I found that having the return type be a simple c_char_p caused a
    # conversion to be done on the return.  If I examined the type of the
    # returned object, it was "bytes" which did not contain the original
    # address of the C memory (at least in any usable form).
    #
    # Using a ctypes.POINTER allows us to preserve that information so we can
    # free it later.
    alloc_func = libc.alloc_C_string

    # this is a ctypes.POINTER object which holds the address of the data
    alloc_func.restype = ctypes.POINTER(ctypes.c_char)

    print("Allocating and freeing memory in C")
    c_string_address = alloc_func()
    # now we have the POINTER object.  we should convert that to something we
    # can use on the python side.
    phrase = ctypes.c_char_p.from_buffer(c_string_address)
    print("Python was just handed {0}({1}):{2}".format(
        hex(ctypes.addressof(c_string_address.contents)),
        ctypes.addressof(c_string_address.contents),
        phrase.value))

    # the memory that c_string_address points to was allocated in C, we need to
    # return it there as python's memory manager will NOT free it for us!  This
    # is c_string_address the pointer we have the in c_string_address object is
    # needed.  The POINTER object stores the address of the C memory in the
    # contents attribute.  NOTE: When printing it out, you need the addressof
    # for the contents to tell python NOT to convert it to what the contents
    # pointer is pointing at.
    free_func = libc.free_C_string
    free_func.argtypes = [ctypes.POINTER(ctypes.c_char), ]
    print("Python is sending to C {0}({1}):{2}".format(
        hex(ctypes.addressof(c_string_address.contents)),
        ctypes.addressof(c_string_address.contents),
        phrase.value))
    free_func(c_string_address)  # contents is the actual pointer returned

if __name__ == "__main__":
    # load the shared library into c types.
    libname = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           "libclib1.so"))
    LIBC = ctypes.CDLL(libname)

    call_function_with_no_args(LIBC)
    call_string_modifier(LIBC)
    call_memory_allocation(LIBC)
