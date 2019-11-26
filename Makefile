all: build/masterthesis.pdf

build/cont_rand.pdf: Plots/cont_rand.py Plots/matplotlibconfig.py | build 
	python Plots/cont_rand.py

TeXOptions = -lualatex \
			 -interaction=nonstopmode \
			 -halt-on-error \
			 -output-directory=build
                                                                                
build/masterthesis.pdf: FORCE build/cont_rand.pdf | build
	latexmk $(TeXOptions) masterthesis.tex

preview: FORCE | build
	latexmk $(TeXOptions) -pvc masterthesis.tex	
	
FORCE:

build:
	mkdir -p build/

clean:
	rm -rf build
