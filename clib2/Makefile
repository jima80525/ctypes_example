all: test

clean:
	rm *.o *.so

libclib2.so: clib2.o Point.o
	gcc -shared $^ -o $@

.o: .c
	gcc -c -Wall -Werror -fpic $^

test: libclib2.so
	./callClib2.py
