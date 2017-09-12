all: test

clean:
	rm *.o *.so

libclib2.so: Point.o Line.o
	gcc -shared $^ -o $@

.o: .c
	gcc -c -Wall -Werror -fpic $^

test: libclib2.so
	./callClib2.py
