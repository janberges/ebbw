.PHONY: html examples clean

html: ebbw.pdf examples
	sphinx-build -M html . .

ebbw.pdf: ebbw.tex ../logo/ebbw.pdf
	pdflatex --interaction=batchmode $<
	pdflatex --interaction=batchmode $<

../logo/ebbw.pdf: ../logo/ebbw.tex
	$(MAKE) -C ../logo/ ebbw.pdf

examples:
	$(MAKE) -C ../examples/

clean:
	rm -rf doctrees html
