# Ctypes Tutorial Part II

The built-in [`ctypes` module](https://docs.python.org/3/library/ctypes.html) is a powerful feature in Python, allowing you to use existing libraries in other languages by writting simple wrappers in Python itself.

In the [first part](https://dbader.org/blog/python-ctypes-tutorial) of this tutorial, we covered the basics of ctypes.  In part two we will dig a little deeper, covering:

* Creating simple Python classes to mirror C structures
* Passing by value versus passing by reference (pointers)
* Expanding our C structure wrappers to hide the complexity from Python code
* Nested structures

Again, let's start by taking a look with the simple C library we will be using and how to build it, and then jump into loading a C library and calling functions in it.

## The C Library Code

As with the previous tutorial, all of the code to build and test the examples discussed here (as well as the Markdown for this article) are committed to my [GitHub repository](https://github.com/jima80525/ctypes_example). 

The library consists of two data structures; Point and Line.  A Point is a pair of (x,y) coordinates while a Line has a Start and End Point.  There are also a handful of functions which modify each of these types. 

Let's take a closer look at the `Point` structure and the functions surrounding it.

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
/* Display a Point value */
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
Point get_point(void) {
    static int counter = 0;
    Point point = { counter++, counter++ };
    printf("Returning Point    (%d, %d)\n", point.x, point.y);
    return point;
}
```

I won't go into each of these functions in detail as they are fairly simple.  The only interesting bit is the difference between `move_point` and `move_point_by_ref`.  We'll talk a bit later about pass-by-value and pass-by-reference semantics.

We'll also be using a `Line` structure, which is composed of two Points:

<from Line.h>
```c
typedef struct {
    Point start;
    Point end;
} Line;
```

<from Line.c>
    
```c
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
    Line l = { get_point(), get_point() };
    return l;
}
```

The Point structure and its associated functions will allow us to show how to wrap structures and deal with memory references in Ctypes.  The Line structure will allow us to work with nested structures and the complications that arise from that.

The [Makefile](https://github.com/jima80525/ctypes_example/blob/master/clib2/Makefile) in the repo is set up to completely build and run the demo from scratch; you only need to run the following command in your shell:

```sh
$ make
```

The Makefile looks like this:

```Make
all: point wrappedPoint line

clean:
	rm *.o *.so

libpoint.so: Point.o
	gcc -shared $^ -o $@

libline.so: Point.o Line.o
	gcc -shared $^ -o $@

.o: .c
	gcc -c -Wall -Werror -fpic $^

point: libpoint.so
	./testPoint.py

wrappedPoint: libpoint.so
	./testWrappedPoint.py

line: libline.so
	./testLine.py

doc:
	pandoc ctypes2.md > ctypes2.html
	firefox ctypes2.html
```

## Creating Simple Python Classes to Mirror C Structures

Now that we've seen the C code we'll be using, we can start in on Python and Ctypes. We'll start with a quick wrapper function that will simplify the rest of our code, then we'll look at how to wrap C structures.  Finally, we'll discuss the differences between pass-by-value and pass-by-reference.

### Wrapping `ctypes` Functions

Before we get into the depths of this tutorial, I'll show you a utility function we'll be using throughout.  This function takes the object returned from Ctypes.CDLL and the name of a function (as a string).  It returns a Python object which holds the function that has the speicified `restype` and `argtypes`.

These are concepts [covered in the previous tutorial](https://dbader.org/blog/python-ctypes-tutorial), so if this doesn't make sense, it might be worth reviewing that.


> Not entirely sure what this does, it takes a ctypes library and a function name—I guess I'm not clear what a "ctypes library" is in this case. A C "dll" we can load dynamically and use from Python using ctypes? [name=Dan Bader]
> I edited this, but I'm still not thrilled.  Yes, the original "ctypes library" was the object returned from CDLL.  

```python
def wrap_function(lib, funcname, restype, argtypes):
    ''' Simplify wrapping ctypes functions '''
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func
```

### Mirroring C Structures with Python Classes

Creating Python classes which mirror C structs requires little code, but does have a little magic behind the scenes.

```python
class Point(ctypes.Structure):
    _fields_ = [('x', ctypes.c_int), ('y', ctypes.c_int)]

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)
```

As you can see above, we make use of the `_fields_` attribute of the class. (Note the single underscore - this is NOT a `dunder` function.)
This attribute is a list of tuples and allows ctypes to map attributes from Python back to the underlying C structure.  Let's look at how it's used.


```python
show_point = wrap_function(libc, 'show_point', None, [Point])
a = Point(1, 2)
print("Point in Python is", a)
show_point(a)
print()
```

Notice that we can access the `x` and `y` attributes of the Point class in Python in the `__repr__` function.  We can also pass the Point directly to the show_point function in the C library.  CTypes uses the `_fields_` map to manage the conversions automatically for you.  Care should be taken with using the `_fields_` attribute, however.  We'll look at this in a little more detail in the [Nested Structs](#nested-structures) section below.

## Passing by value versus passing by reference (pointers)

In Python we get used to referring to things as either 'mutable' or 'immutable'.  This controls what happens when you modify an object you've passed to a function. For example, `number` objects are immutable.  When you call `myfunc` in the code below, the value of y does not get modified.  The program prints the value 9:

```python
def myfunc(x):
    x = x + 2

y = 9
myfunc(y)
print("this is y", y)
```
Contrarily, list objects *are* mutable.  In a similar function:

```python
def mylistfunc(x):
    x.append("more data")

z = list()
print("this is z", z)
```

As you can see, the list, z, that is passed in to the function *is* modified and the output is `this is z ['more data']`

When interfacing with C, we need to take this concept a step further.  When we pass a parameter to a function, C *always* "passes by value".  What this means is that, unless you pass in a pointer to an object, the original object is never changed.  Applying this to CTypes, we need to be aware of which values are being passed as pointers and thus need the `ctypes.POINTER(Point)` type applied to them.

In the example below, we have two versions of the function to move a point: `move_point`, which passes by value, and `move_point_by_ref` which passes by reference.

```python
###########################################################################
print("Pass by value")
move_point = wrap_function(libc, 'move_point', None, [Point])
a = Point(5, 6)
print("Point in Python is", a)
move_point(a)
print("Point in Python is", a)
print()

###########################################################################
print("Pass by reference")
move_point_by_ref = wrap_function(libc, 'move_point_by_ref', None,
                                  [ctypes.POINTER(Point)])
a = Point(5, 6)
print("Point in Python is", a)
move_point_by_ref(a)
print("Point in Python is", a)
print()
```

The output from these two code sections looks like

```
Pass by value
Point in Python is (5, 6)
Point in C      is (5, 6)
Point in C      is (6, 7)
Point in Python is (5, 6)

Pass by reference
Point in Python is (5, 6)
Point in C      is (5, 6)
Point in C      is (6, 7)
Point in Python is (6, 7)
```

As you can see, when we call move_point, the C code can change the value of the Point, but that change is not reflected in the Python object. When we call move_point_by_ref, however, the change is visible in the Python object.  This is because we passed the address of the memory which holds that value and the C code took special care (via using the -> accessor) to modify that memory.

When working in cross-language interfaces, memory access and memory management are important aspects to keep in mind.

## Expanding our C structure wrappers to hide the complexity from Python code
 We saw above that providing a simple wrapper to a C structure is quite easy using Ctypes.  We can also expand this wrapper to make it behave like a Python class instead of a C struct.
 
Here's an example:

```python
class Point(ctypes.Structure):
    _fields_ = [('x', ctypes.c_int), ('y', ctypes.c_int)]

    def __init__(self, lib, x=None, y=None):
        if x:
            self.x = x
            self.y = y
        else:
            get_point = wrap_function(lib, 'get_point', Point, None)
            self = get_point()

        self.show_point_func = wrap_function(lib, 'show_point', None, [Point])
        self.movePointFunc = wrap_function(lib, 'move_point', None, [Point])
        self.movePointRefFunc = wrap_function(lib, 'move_point_by_ref', None,
                                              [ctypes.POINTER(Point)])

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def show_point(self):
        self.show_point_func(self)

    def move_point(self):
        self.movePointFunc(self)

    def move_point_by_ref(self):
        self.movePointRefFunc(self)

```

You'll see the `_fields_` and `__repr__` attributes are the same as we had in our simple wrapper, but now we've added a constructor and wrapping functions for each method we'll use.  The interesting code is all in the constructor. The initial part initializes the `x` and `y` fields.  You can see that we have two methods to achieve this.  If the user passed in values, we can directly assign those to the fields.  If the default values were used, we call the `get_point` function in the library and assign that directly to `self`.

Once we've initialized the fields in our Point class, we then wrap the functions into attributes of our class to allow them to be accessed in a more _object oriented_ manner.

In the testWrappedPoint module, we do the same tests we did with our Point class but instead of passing the Point class to the function, `move_point_by_ref(a)`, we call the function on the object `a.move_point_by_ref()`.

## Nested Structures

Finally, we're going to look at how to use nested structures in CTypes.  The obvious next step in our example is to extend a Point to a Line.


```python
class Line(ctypes.Structure):
    _fields_ = [('start', testPoint.Point), ('end', testPoint.Point)]

    def __init__(self, lib):
        get_line = wrap_function(lib, 'get_line', Line, None)
        a = get_line()
        self.start = a.start
        self.end = a.end
        self.showLineFunc = wrap_function(lib, 'show_line', None, [Line])
        self.moveLineFunc = wrap_function(lib, 'move_line_by_ref', None,
                                          [ctypes.POINTER(Line)])

    def __repr__(self):
        return '{0}->{1}'.format(self.start, self.end)

    def show_line(self):
        self.showLineFunc(self)

    def moveLine(self):
        self.moveLineFunc(self)
```

Most of this class should look fairly familiar if you've been following along.  The one interesting difference is how we initialize the `_fields_` attribute. You'll remember in the Point class we could assign the returned value from `get_point()` directly to self.  This doesn't work with our Line wrapper as the entries in the `_fields_` list are not basic CTypes types, but rather a subclass of one of them.  Assigning these directly tends to mess up how the value is stored so that the Python attributes you add to the class are inaccessible.

The basic rule I've found in wrapping structures like this is to only add the Python class attributes at the top level and leave the inner structures (i.e. `Point`) with the simple `_fields_` attribute.


## Conclusion
In this tutorial we covered some more advanced topics in using Ctypes.  I found several resources out there while researching.  The [ctypesgen project](https://github.com/davidjamesca/ctypesgen) has tools which will auto generate Python wrapping modules for C header files.  I spent some time playing with this and it looks quite good.

The idea for the `wrap_function` function was lifted shamelessly from some ctypes tips [here](https://www.cs.unc.edu/~gb/blog/2007/02/11/ctypes-tricks/).

And, finally, if you'd like to see and play with the code I wrote while working on this, please visit my [GitHub repository](https://github.com/jima80525/ctypes_example).  This tutorial is in the 'tutorial2' directory.