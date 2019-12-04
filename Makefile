all: build/masterthesis.pdf

build/cont_rand.pdf: Plots/cont_rand.py Plots/matplotlibconfig.py | build 
	python Plots/cont_rand.py

build/spectrum.pdf: Plots/spectrum.py Plots/matplotlibconfig.py | build 
	python Plots/spectrum.py

build/dEdx.pdf: Plots/dEdx.py Plots/matplotlibconfig.py | build 
	python Plots/dEdx.py

build/secondary_number.pdf: Plots/secondary_number.py Plots/matplotlibconfig.py resources/config_ice.json | build
	python Plots/secondary_number.py	

build/dEdx_mupair.pdf: Plots/dEdx_mupair.py Plots/matplotlibconfig.py | build
	python Plots/dEdx_mupair.py	

build/spectrum_mupair.pdf: Plots/spectrum_mupair.py Plots/matplotlibconfig.py | build
	python Plots/spectrum_mupair.py	

TeXOptions = -lualatex \
			 -interaction=nonstopmode \
			 -halt-on-error \
			 -output-directory=build
                                                                                
build/masterthesis.pdf: FORCE build/cont_rand.pdf build/spectrum.pdf build/dEdx.pdf build/secondary_number.pdf build/dEdx_mupair.pdf build/spectrum_mupair.pdf | build
	latexmk $(TeXOptions) masterthesis.tex

preview: FORCE | build
	latexmk $(TeXOptions) -pvc masterthesis.tex	
	
FORCE:

build:
	mkdir -p build/
	mkdir -p build/numbers/

clean:
	rm -rf build
