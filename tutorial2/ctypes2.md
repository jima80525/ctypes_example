The built-in [`ctypes` module](https://docs.python.org/3/library/ctypes.html) is a powerful feature in Python, allowing you to use existing libraries in other languages by writting simple wrappers in Python itself.

In the [first part](https://dbader.org/blog/python-ctypes-tutorial) of this tutorial, we covered the basics of ctypes.  In part two we will dig a little deeper, covering:

* Creating simple Python classes to mirror C structures
* Passing by value versus passing by reference (pointers)
* Expanding our C structure wrappers to hide the complexity from Python code
* Nested structures

Again, let's start by taking a look with the simple C library we will be using and how to build it, and then jump into loading a C library and calling functions in it.

## The C library code

As with the previous tutorial, all of the code to build and test the examples discussed here (as well as the Markdown for this article) are committed to my [GitHub repository](https://github.com/jima80525/ctypes_example).

Let's start with the Point structure and the functions surrounding it.

<from Point.h>
```c
/* Simple structure for ctypes example */
typedef struct {
    int x;
    int y;
} Point;
```

<from Point.c>

```c
/* display a Point value */
void showPoint(Point point) {
    printf("Point in C      is (%d, %d)\n", point.x, point.y);
}

/* Increment a Point which was passed by value */
void movePoint(Point point) {
    showPoint(point);
    point.x++;
    point.y++;
    showPoint(point);
}

/* Increment a Point which was passed by reference */
void movePointRef(Point *point) {
    showPoint(*point);
    point->x++;
    point->y++;
    showPoint(*point);
}

/* Return by value */
Point getPoint(void) {
    static int counter = 0;
    Point point = { counter++, counter++};
    printf("Returning Point    (%d, %d)\n", point.x, point.y);
    return point;
}
```

I won't go into each of these functions in detail as they are fairly simple.  The only interesting bit is the difference between `movePoint` and `movePointRef`.  We'll
talk a bit later about pass-by-value and pass-by-reference semantics.

We'll also be using a Line structure, which is composed of two Points:

<from Line.h>
```c
typedef struct {
    Point start;
    Point end;
} Line;
```

<from Line.c>
```c
void showLine(Line line) {
    printf("Line in C      is (%d, %d)->(%d, %d)\n", line.start.x, line.start.y,
            line.end.x, line.end.y);
}

void moveLineRef(Line *line) {
    showLine(*line);
    movePointRef(&line->start);
    movePointRef(&line->end);
    showLine(*line);
}

Line getLine(void) {
    Line l = { getPoint(), getPoint() };
    return l;
}
```

Again, these functions are hopefully very straightforward.

The Makefile in the repo is set up to completely build and run the demo from
scratch; you only need to run the following command in your shell:

```sh
$ make
```

## creating simple Python classes to mirror C structures

### wrapping CTypes functions
Before we get into the depths of this tutorial, I'll show you a utility function
we'll be using throughout.  This funtion takes a ctypes library and a function name.  It returns as pointer to a function which has the specified `restype` and `argtypes`.
These are concepts covered in the previous tutorial, so if this doesn't make sense, it might be worth reviewing that.

```python
def wrapFunction(lib, funcname, restype, argtypes):
    ''' Simplify wrapping ctypes functions '''
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func
```

### Mirroring C structures

Creating classes which mirror C structures requires little code, but does have a little magic behind the scenes.

```python
class Point(ctypes.Structure):
    _fields_ = [('x', ctypes.c_int), ('y', ctypes.c_int)]

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)
```

As you can see above, we make use of the `_fields_` attribute of the class. (Note the single underscore - this is NOT a `dunder` function.)
This attribute is a list of tuples and allows ctypes to map attributes from Python back to the underlying C structure.  Let's look at how it's used.


```python
    showPoint = wrapFunction(libc, 'showPoint', None, [Point])
    a = Point(1, 2)
    print("Point in Python is", a)
    showPoint(a)
    print()
```

Notice that we can access the `x` and `y` attributes of the Point class in Python in the `__repr__` function.  We can also pass the Point directly to
the showPoint function in the C library.  CTypes uses the `_fields_` map to manage the conversions automatically for you.  Care should be taken
with using the `_fields_` attribute, however.  We'll look at this in a little more detail in the [Nested Structs](#nested-structures) section below.


## passing by value versus passing by reference (pointers)

In Python we get used to referring to things as either 'mutable' or 'immutable'.  This controls what happens when you modify an object you've passed to a function.
For example, `number` objects are immutable.  When you call `myfunc` in the code below, the value of y does not get modified.  The program prints the value 9.

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

list, z, that is passed in to the function *is* modified and the output is `this is z ['more data']`

When interfacing with C, we need to take this concept a step further.  When we pass a parameter to a function, C *always* "passes by value".  What this means
is that, unless you pass in a pointer to an object, the original object is never changed.  Applying this to CTypes, we need to be aware of which values are
being passed as pointers and thus need the `ctypes.POINTER(Point)` type applied to them.

In the example below, we have two versions of the function to move a point: `movePoint`, which passes by value, and `movePointRef` which passes by reference.


```python
###########################################################################
print("Pass by value")
movePoint = wrapFunction(libc, 'movePoint', None, [Point])
a = Point(5, 6)
print("Point in Python is", a)
movePoint(a)
print("Point in Python is", a)
print()

###########################################################################
print("Pass by reference")
movePointRef = wrapFunction(libc, 'movePointRef', None,
                            [ctypes.POINTER(Point)])
a = Point(5, 6)
print("Point in Python is", a)
movePointRef(a)
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

As you can see, when we call movePoint, the C code can change the value of the Point, but that change is not reflected in the Python object.
When we call MovePointRef, however, the change is visible in the Python object.  This is because we passed the address of the memory which holds
that value and the C code took special care (via using the -> accessor) to modify that memory.

When working in cross-language interfaces, memory access and memory management are important aspects to keep in mind.

## Expanding our C structure wrappers to hide the complexity from Python code

We saw above that providing a simple wrapper to a C structure is quite easy using Ctypes.  We can also expand this wrapper to make it behave like a Python class instead of
a C struct.
Here's an example:

```python
class Point(ctypes.Structure):
    _fields_ = [('x', ctypes.c_int), ('y', ctypes.c_int)]

    def __init__(self, lib, x=None, y=None):
        if x:
            self.x = x
            self.y = y
        else:
            getPoint = wrapFunction(lib, 'getPoint', Point, None)
            self = getPoint()

        self.showPointFunc = wrapFunction(lib, 'showPoint', None, [Point])
        self.movePointFunc = wrapFunction(lib, 'movePoint', None, [Point])
        self.movePointRefFunc = wrapFunction(lib, 'movePointRef', None,
                                             [ctypes.POINTER(Point)])

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def showPoint(self):
        self.showPointFunc(self)

    def movePoint(self):
        self.movePointFunc(self)

    def movePointRef(self):
        self.movePointRefFunc(self)

```

You'll see the `_fields_` and `__repr__` attributes are the same as we had in our simple wrapper, but
now we've added a constructor and wrapping functions for each method we'll use.  The interesting code is all in the constructor.
The initial part initializes the `x` and `y` fields.  You can see that we have two methods to achieve this.  If the user passed in
values, we can directly assign those to the fields.  If the default values were used, we call the `getPoint` function in the library
and assign that directly to `self`.

Once we've initialized the fields in our Point class, we then wrap the functions into attributes of our class to allow them to be
accessed in a more _object oriented_ manner.

In the testWrappedPoint.py function, we do the same tests we did with our Point class, but instead of passing the Point class to the
function, `movePointRef(a)`, we call the function on the object `a.movePointRef()`.

## Nested Structures

Finally, we're going to look at how to use nested structures in CTypes.  The obvious next step in our example is to extend a Point to a Line.


```python
class Line(ctypes.Structure):
    _fields_ = [('start', testPoint.Point), ('end', testPoint.Point)]

    def __init__(self, lib):
        getLine = wrapFunction(lib, 'getLine', Line, None)
        a = getLine()
        self.start = a.start
        self.end = a.end
        self.showLineFunc = wrapFunction(lib, 'showLine', None, [Line])
        self.moveLineFunc = wrapFunction(lib, 'moveLineRef', None,
                                         [ctypes.POINTER(Line)])

    def __repr__(self):
        return '{0}->{1}'.format(self.start, self.end)

    def showLine(self):
        self.showLineFunc(self)

    def moveLine(self):
        self.moveLineFunc(self)
```

Most of this class should look fairly familiar if you've been following along.  The one interesting difference is how we initialize the `_fields_` attribute.
You'll remember in the Point class we could assign the returned value from `getPoint()` directly to self.  This doesn't work with our Line wrapper as the entries
in the `_fields_` list are not basic CTypes types, but rather a subclass of one of them.  Assigning these directly tends to mess up how the value is stored so
that the Python attributes you add to the class are inaccessible.

The basic rule I've found in wrapping structures like this is to only add the Python class attributes at the top level and leave the inner structures (i.e. `Point`)
with the simple `_fields_` attribute.


## Conclusion
In this tutorial we covered some more advanced topics in using Ctypes.  I found several resources out there while researching.  The
[ctypesgen project](https://github.com/davidjamesca/ctypesgen) has tools which will auto generate Python wrapping modules for C
header files.  I spent some time playing with this and it looks quite good.

The idea for the `wrapFunction` function was lifted shamelessly from some ctypes tips [here](https://www.cs.unc.edu/~gb/blog/2007/02/11/ctypes-tricks/).

And, finally, if you'd like to see and play with the code I wrote while working on this, please visit my [GitHub repository](https://github.com/jima80525/ctypes_example).  This
tutorial is in the 'tutorial2' directory.
