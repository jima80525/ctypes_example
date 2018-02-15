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
	pandoc cffi.md > cffi.html
	firefox cffi.html
