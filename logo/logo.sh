#!/bin/bash

w=15
h=6
in=2.54

pdflatex --interaction=batchmode ebbw

convert -density `perl -e "print 640 / ($w / $in)"` ebbw.pdf \
    -flatten PNG8:ebbw.png

convert -density `perl -e "print 640 / ($w / $in)"` ebbw.pdf \
    -background white -gravity center -extent 640x640 PNG8:ebbw_square.png

convert -density `perl -e "print 1280 / ($w / $in)"` ebbw.pdf \
    -background white -gravity center -extent 1280x640 PNG8:ebbw_banner.png
