test: library.so test_it.py
	python3 test_it.py

library.so: Makefile library.c
	gcc -std=c99 -Wall -shared library.c -o library.so

.PHONY: test

