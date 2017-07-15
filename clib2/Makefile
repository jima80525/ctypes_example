all: test

clean:
	rm *.o *.so

clib2.so: clib2.o
	gcc -shared -o libclib2.so clib2.o

clib2.o: clib2.c
	gcc -c -Wall -Werror -fpic clib2.c

test: clib2.so
	./callClib2.py
