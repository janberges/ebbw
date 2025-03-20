.PHONY: all clean

all: $(patsubst %.py, %.png, $(filter-out test.py, $(wildcard *.py)))

clean:
	rm -f *.png

%.png: %.py
	python3 $^
