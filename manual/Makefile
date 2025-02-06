.PHONY: clean html

html: ebbw.pdf
	sphinx-build -M html . .

ebbw.pdf: ebbw.tex ../logo/ebbw.pdf
	pdflatex --interaction=batchmode $<
	pdflatex --interaction=batchmode $<

../logo/ebbw.pdf: ../logo/ebbw.tex
	$(MAKE) -C ../logo/ ebbw.pdf

clean:
	rm -rf doctrees html
