all: point wrappedPoint line

clean:
	rm -f *.o *.so *.html

libpoint.so: Point.o
	gcc -shared $^ -o $@

libline.so: Point.o Line.o
	gcc -shared $^ -o $@

%.o: %.c
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
