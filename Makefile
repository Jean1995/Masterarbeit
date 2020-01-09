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

build/mupair_rho.pdf: Plots/mupair_rho.py Plots/matplotlibconfig.py | build
	python Plots/mupair_rho.py	

build/dNdx_weak.pdf: Plots/dNdx_weak.py Plots/matplotlibconfig.py | build 
	python Plots/dNdx_weak.py

build/dEdx_ionization.pdf: Plots/dEdx_ionization.py Plots/matplotlibconfig.py | build 
	python Plots/dEdx_ionization.py

build/dEdx_brems.pdf: Plots/dEdx_brems.py Plots/matplotlibconfig.py | build 
	python Plots/dEdx_brems.py	

build/spectrum_annihilation.pdf: Plots/spectrum_annihilation.py Plots/matplotlibconfig.py | build
	python Plots/spectrum_annihilation.py		

build/compton.pdf: Plots/compton.py Plots/matplotlibconfig.py | build
	python Plots/compton.py	

TeXOptions = -lualatex \
			 -interaction=nonstopmode \
			 -halt-on-error \
			 -output-directory=build
                                                                                
build/masterthesis.pdf: FORCE build/cont_rand.pdf build/spectrum.pdf build/dEdx.pdf build/secondary_number.pdf build/dEdx_mupair.pdf build/spectrum_mupair.pdf build/mupair_rho.pdf build/dNdx_weak.pdf build/dEdx_ionization.pdf build/dEdx_brems.pdf build/spectrum_annihilation.pdf build/compton.pdf| build
	latexmk $(TeXOptions) masterthesis.tex

preview: FORCE | build
	latexmk $(TeXOptions) -pvc masterthesis.tex	
	
FORCE:

build:
	mkdir -p build/
	mkdir -p build/numbers/

clean:
	rm -rf build

bibclean:
	rm build/masterthesis.aux
	rm build/masterthesis.bbl
	rm build/masterthesis.blg
