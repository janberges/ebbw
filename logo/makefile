.PHONY: all clean

w = 15
in = 2.54

all: ebbw.png ebbw_square.png ebbw_banner.png

%.pdf: %.tex
	pdflatex --interaction=batchmode $*

ebbw.png: ebbw.pdf
	convert -density `perl -e "print 640 / ($(w) / $(in))"` $< \
        -flatten PNG8:$@

ebbw_square.png: ebbw.pdf
	convert -density `perl -e "print 640 / ($(w) / $(in))"` $< \
        -gravity center -extent 640x640 PNG8:$@

ebbw_banner.png: ebbw.pdf
	convert -density `perl -e "print 1280 / ($(w) / $(in))"` $< \
        -gravity center -extent 1280x640 PNG8:$@

clean:
	rm -f *.aux *.log *.pdf *.png
