#!/usr/bin/env python
import os
import cffi


if __name__ == "__main__":
    ffi = cffi.FFI()
    
    with open(os.path.join(os.path.dirname(__file__), "Point.h")) as f:
        ffi.cdef(f.read())
    
    ffi.set_source("_point",
        # Since we are calling a fully built library directly no custom source
        # is necessary. We need to include the .h files, though, because behind
        # the scenes cffi generates a .c file which contains a Python-friendly
        # wrapper around each of the functions.
        '#include "Point.h"',
        # The important thing is to include the pre-built lib in the list of
        # libraries we are linking against:
        libraries=["point"],
        library_dirs=[os.path.dirname(__file__),],
    )

    ffi.compile()
