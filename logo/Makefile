.PHONY: all clean

all: ebbw.pdf ebbw.png ebbw_square.png ebbw_banner.png

%.pdf: %.tex
	pdflatex --interaction=batchmode $*

ebbw.png: ebbw.svg
	inkscape -w 600 -b white -o $@ $<
	python3 optimize.py $@ $@

ebbw_square.png: ebbw.png
	convert $< -gravity center -extent 600x600 $@

ebbw_banner.png: ebbw.png
	convert $< -gravity center -extent 1280x640 $@

clean:
	rm -f *.aux *.log *.pdf *_*.png
