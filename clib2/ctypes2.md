The built-in [`ctypes` module](https://docs.python.org/3/library/ctypes.html) is a powerful feature in Python, allowing you to use existing libraries in other languages by writting simple wrappers in Python itself.

In the first part of this tutorial, we covered the basics of ctypes.  In part two we will dig a little deeper, covering:

* creating simple Python classes to mirror C structures
* passing by value versus passing by reference (pointers)
* expanding our C structure wrappers to hide the complexity from Python code
* nested structures


999999999999999999999999999999999999
NOTES
999999999999999999999999999999999999

https://github.com/davidjamesca/ctypesgen
script to create wrapper functions for ctypes in general.  Pretty cool, bit more
than I need to show as far as cross-platform loading.
Doesn't create the class - but automatically generates a modules with the
functions listed in the  .h file with the right types.

https://www.cs.unc.edu/~gb/blog/2007/02/11/ctypes-tricks/
This has the cool wrapper function to wrap functions
it uses something more explicit than the basics, however.
Ahh.  Those are for specifying callback functions.

