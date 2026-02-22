all: test

clean:
	rm -f *.o *.so *.html

clib1.so: clib1.o
	gcc -shared -o libclib1.so clib1.o

clib1.o: clib1.c
	cc -c -Wall -Werror -fpic clib1.c -I /usr/include/python3.7

test: clib1.so
	./callclib1.py

doc:
	markdown ctypes.md > ctypes.html
	firefox ctypes.html
