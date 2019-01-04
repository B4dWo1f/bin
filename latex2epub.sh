#!/bin/bash

#
# Will only work for very basic tex files
#

latexml --dest=$1.xml $1.tex
latexmlpost -dest=$1.html $1.xml
ebook-convert $1.html $1.epub --language en --no-default-epub-cover
