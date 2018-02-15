# Interfacing Python and C: the CFFI module

Learn use the CFFI module for interfacing Python with native libraries.

[cool picture goes here :) ]

In previous tutorials, we covered the basics of CTypes and some advanced CTypes usage.  This tutorial will cover 
the [`CFFI` module](https://cffi.readthedocs.io/en/latest/index.html).   CFFI is a richer environment than Ctypes, allowing several different options 
for how you want to interface with a native library. 

In this tutorial we will be covering:

* 'Out-of-line' vs 'in-line' interfaces
* Building and running CFFI-based scripts on Linux
* Creating simple Python classes to mirror C structures
* Passing structures by reference
* Working around some CFFI limitations

As with previous tutorials, let's start by taking a look with the simple C library we will be using and how to build it, and then jump into loading a C library and calling functions in it.

## The C Library Code

As with the previous tutorials, all of the code to build and test the examples discussed here (as well as the Markdown for this article) are committed to my [GitHub repository](https://github.com/jima80525/ctypes_example). 

The library consists of two data structures; Point and Line.  A Point is a pair of (x,y) coordinates while a Line has a Start and End Point.  There are also a handful of functions which modify each of these types. 

Let's take a closer look at the `Point` structure (skipping the functions surrounding it.

```c
/* Point.h */
/* Simple structure for ctypes example */
typedef struct {
    int x;
    int y;
} Point;
```

```c
/* Point.c */
/* display a Point value */
void show_point(Point point) {
    printf("Point in C      is (%d, %d)\n", point.x, point.y);
}

/* Increment a Point which was passed by value */
void move_point(Point point) {
    show_point(point);
    point.x++;
    point.y++;
    show_point(point);
}

/* Increment a Point which was passed by reference */
void move_point_by_ref(Point *point) {
    show_point(*point);
    point->x++;
    point->y++;
    show_point(*point);
}

/* Return by value */
Point get_default_point(void) {
    static int x_counter = 0;
    static int y_counter = 100;
    x_counter++;
    y_counter--;
    return get_point(x_counter, y_counter);
}

Point get_point(int x, int y) {
    Point point = { x, y };
    printf("Returning Point    (%d, %d)\n", point.x, point.y);
    return point;
}
```

I won't go into each of these functions in detail as they are fairly simple.  The only interesting bit is the difference between `move_point` and `move_point_by_ref`.  We'll talk a bit later about pass-by-value and pass-by-reference semantics.

We'll also be using a `Line` structure, which is composed of two Points:

```c
/* Line.h */
typedef struct {
    Point start;
    Point end;
} Line;
```

```c
/* Line.c */
void show_line(Line line) {
    printf("Line in C      is (%d, %d)->(%d, %d)\n", line.start.x, line.start.y,
            line.end.x, line.end.y);
}

void move_line_by_ref(Line *line) {
    show_line(*line);
    move_point_by_ref(&line->start);
    move_point_by_ref(&line->end);
    show_line(*line);
}

Line get_line(void) {
    Line l = { get_default_point(), get_default_point() };
    return l;
}
```

The Point structure and its associated functions will allow us to show how to set up and build this example and how to 
deal with memory references in Ctypes.  The Line structure will allow us to work with nested structures and the complications that arise from that.

The [Makefile](https://github.com/jima80525/ctypes_example/blob/master/cffi/Makefile) in the repo is set up to completely build and run the demo from scratch:

```Make
all: point line

clean:
	rm -f *.o *.so *.html _point.c _line.c Line.h.preprocessed

libpoint.so: Point.o
	gcc -shared $^ -o $@

libline.so: Point.o Line.o
	gcc -shared $^ -o $@

%.o: %.c
	gcc -c -Wall -Werror -fpic $^

point: export LD_LIBRARY_PATH = $(shell pwd)
point: libpoint.so
	./build_point.py
	./testPoint.py

line: export LD_LIBRARY_PATH = $(shell pwd)
line: libline.so
	# hack to get around cffi not supporting #include directives
	gcc -E Line.h > Line.h.preprocessed
	./build_line.py
	./testLine.py

doc:
	pandoc ctypes2.md > ctypes2.html
	firefox ctypes2.html
```

To build and run the demo you only need to run the following command in your shell:

```sh
$ make
```

## 'Out-of-line' vs 'in-line' interfaces
Before we dive into what the code looks like, let's step back and discuss what CFFI does and some of the options you have using it.

CFFI is a Python module which will read C function prototypes automatically generate some of the marshalling to and from these C functions. 

I'm going to quote the [CFFI docs](https://cffi.readthedocs.io/en/latest/overview.html#overview), as they describe the options much better than I could:


>    
>    CFFI can be used in one of four modes: “ABI” versus “API” level, each with
>    “in-line” or “out-of-line” preparation (or compilation).
>    
>    The ABI mode accesses libraries at the binary level, whereas the faster API
>    mode accesses them with a C compiler. This is described in detail below.
>    
>    In the in-line mode, everything is set up every time you import your Python
>    code. In the out-of-line mode, you have a separate step of preparation (and
>    possibly C compilation) that produces a module which your main program
>    can then import.
>    

In this tutorial we'll be writing an API level, out-of-line system.  This means we will have to talk about some system requirements 
before we dive into the Python code.  

## Building and running CFFI-based scripts on Linux

The examples in this tutorial have been worked through on Linux Mint 18.3.  They should work on most Linux systems.  Windows and Mac users 
will need to solve similar problems, but with obviously different solutions.

To start, your system will need to have:

* a C compiler (this is fairly standard on Linux distros)
* make (again, this is fairly standard)
* Python (the examples here were tested on 3.5.2)
* CFFI module (pip install cffi)

Now, if we look at the section of the Makefile that builds and runs the tests for the Point class, we see:


```Make
point: export LD_LIBRARY_PATH = $(shell pwd)
point: libpoint.so
	./build_point.py
	./testPoint.py
```

There's a lot going on here.  The LD_LIBRARY_PATH is needed because the CFFI module is 
going to be loading a library we have built in the local directory.  Linux will not, by default, 
search the current directory for shared libraries so we need to tell it to do so.

Next, we're making `point` dependent on libpoint.so, which causes make to go build that library. 

Once the library is built, we need to do our 'out-of-line' processing to build the C code to 
interface to our library.  We'll dive into that code in a minute.

Finally, we run our Python script which actually talks to the library and does the real work (in our case, runs tests).

### Building the C Interface
As we just saw, 'out-of-line' processing is done to allow CFFI to use the header file from C to build an interface module. 

That code looks like this:

```Python
    ffi = cffi.FFI()
    
    with open(os.path.join(os.path.dirname(__file__), "Point.h")) as f:
        ffi.cdef(f.read())
    
    ffi.set_source("_point",
        '#include "Point.h"',
        libraries=["point"],
        library_dirs=[os.path.dirname(__file__),],
    )

    ffi.compile()
```
This code reads in the header file and passes it to a CFFI FFI module to parse.  (NOTE: FFI is a library on top of which CFFI was written)

Once the FFI has the header information, we then set the source information.  The first parameter to the set_source function is the name of 
the .c file you want it to generate.  Next is the custom C source you want to insert.  In our case, this custom code is simply including the 
Point.h file from the library we are talking to.  Finally you need to tell it some information about which libraries you want it to link against.

After we've read in and processed the headers and set up the source file, we tell CFFI to call the compiler and build the interface module.  On
my system, this step produces three files:
    _point.c
    _point.o
    _point.cpython-35m-x86_64-linux-gnu.so

The \_point.c file is over 700 lines long and, like most generated code, can be difficult to read.  The .o file is the output from the compiler and the 
.so file is the interface module we want.

Now that we've got the interface module, we can go ahead and write some Python to talk to our C library!

## Creating simple Python classes to mirror C structures

We can build a simple Python class to wrap around the C struct we use in this library.  Like our CTypes tutorials, this
is fairly simple as CFFI does the data marshalling for us.  To use the generated code we must first import the module 
that CFFI generated for us:

```Python
import _point
```

Then we define our class, `__init__` method of which simply calls the C library to get us a point object:

```Python
class Point():
    def __init__(self, x=None, y=None):
        if x:
            self.p = _point.lib.get_point(x, y)
        else:
            self.p = _point.lib.get_default_point()
```

You can see that the CFFI library allows us to access the functions in the C library directly and allows us to store the
`struct Point` that is returned.   If you add a `print(self.p)` line to the end of the __init__ function, you'll
see that it stores this in a named cdata object:

```
<cdata 'Point' owning 8 bytes>
```

However, that `cdata 'Point'` still has the x and y data members, so you can get and set those values quite easily, as  you can see in the 
__repr__ function for our class:

```Python
    def __repr__(self):
        return '({0}, {1})'.format(self.p.x, self.p.y)
```

We can quite easily wrap the `show_point` and `move_point` methods in our library in class methods as well:

```Python
    def show_point(self):
        _point.lib.show_point(self.p)

    def move_point(self):
        _point.lib.move_point(self.p)
```

## Passing structures by reference

When we pass values by reference in the `move_point_by_ref` function, we need to do a little 
extra work to help CFFI create an object so it can take the address of it and pass that.  This requires a little 
code, but not much.  The prototype for the C function we're trying to call is:

```C
void move_point_by_ref(Point *point);
```

To call that, we need to call the ffi.new() function with two parameters.  The first is a string indicating the type 
of the object to be created.  This type has to match a "known" type in that FFI instance.  In our case, it knows about 
the `Point` type because of the call to cffi.cdef we did during our out-of-line processing.  The second parameter to ffi.new() is 
an initial value for the object.  In this case we want the created object to start with our self.p Point.

```Python
    def move_point_by_ref(self):
        ppoint = _point.ffi.new("Point*", self.p)
        _point.lib.move_point_by_ref(ppoint)
        self.p = ppoint
```

The memory created by ffi.new() will be garbaged collected for us unless we need to do something special with it (see the ffi.gc() function
if you need that).  We end by simply copying the new value from the Point\* back to our self.p cdata member.


## Working around some CFFI limitations

As in our previous tutorials, there is also a Line struct, which holds two Points.  This struct, while quite simple, 
shows a limitation in CFFI that's worth discussing.  In the out-of-line processing script for the Point library, build_point.py, we simply read the Point.h header file 
directly and handed that to cffi.cdef().  This model breaks down when we get to the build_line.py script due to a limitation of CFFI.   CFFI, for some quite good reasons
I won't go into here, does not allow preprocessor directives (i.e. 'lines starting with #').  This prevents us from passing it Line.h directly as the very first line is:

```C
#include "Point.h"
```

There are a couple of common solutions that I saw while researching this tutorial.  One is to custom write the C header information, possibly directly into the build_line.py 
file.  Another, which I think respects the DRY principle, is to use the C preprocessor to generate the file we read in.  This shows up in the Makefile as:

```Make
	# hack to get around cffi not supporting #include directives
	gcc -E Line.h > Line.h.preprocessed
```
The `gcc` line runs the preprocessor on Line.h and we store the output in Line.h.preprocessed.  In the build_line.py script, instead of reading from Line.h we read Line.h.preprocessed
and pass that to the cffi.cdef() function instead.  

NOTE: this trick will not always work, there are many cases where compiler-specific extensions are used in the standard headers (like "stdio.h") which 
will cause cffi to fail.

The rest of the Line example follows the concepts we learned in the Point code above.

## Conclusion
In this tutorial we covered some of the basics about the CFFI module and how to use it to interface native C libraries.  I found
several resources out there while researching.  The 
[python-cffi-example](https://github.com/wolever/python-cffi-example) is a full on code example of using CFFI.  It creates custom function prototypes rather than 
calling the preprocessor as we did in the last section.

If you're interested in passing pointers through the CFFI interface, you should start by reading 
[this section](https://cffi.readthedocs.io/en/latest/using.html#working) of the documentation carefully.  I found it quite worthwhile.

If you're dying to read more about why C preprocessor directives are not supported, I'd recommend starting with 
[this thread](https://groups.google.com/forum/#!topic/python-cffi/vDAw37NHRSg).  The description there covers the 
issue in some detail.

And, finally, if you'd like to see and play with the code I wrote while working
on this, please visit my [GitHub repository](https://github.com/jima80525/ctypes_example).  This tutorial is in
the 'cffi' directory.

