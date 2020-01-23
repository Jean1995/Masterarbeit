all: build/masterthesis.pdf

build/cont_rand.pdf: Plots/cont_rand.py Plots/matplotlibconfig.py | build 
	python3 Plots/cont_rand.py

build/spectrum.pdf: Plots/spectrum.py Plots/matplotlibconfig.py | build 
	python3 Plots/spectrum.py

build/dEdx.pdf: Plots/dEdx.py Plots/matplotlibconfig.py | build 
	python3 Plots/dEdx.py

build/secondary_number.pdf: Plots/secondary_number.py Plots/matplotlibconfig.py resources/config_ice.json | build
	python3 Plots/secondary_number.py	

build/dEdx_mupair.pdf: Plots/dEdx_mupair.py Plots/matplotlibconfig.py | build
	python3 Plots/dEdx_mupair.py	

build/spectrum_mupair.pdf build/spectrum_mupair_secondary_comparison.pdf build/spectrum_mupair_secondary.pdf: Plots/spectrum_mupair.py Plots/matplotlibconfig.py | build
	python3 Plots/spectrum_mupair.py	

build/mupair_rho.pdf: Plots/mupair_rho.py Plots/matplotlibconfig.py | build
	python3 Plots/mupair_rho.py	

build/dNdx_weak.pdf: Plots/dNdx_weak.py Plots/matplotlibconfig.py | build 
	python3 Plots/dNdx_weak.py

build/dEdx_weak.pdf: Plots/dEdx_weak.py Plots/matplotlibconfig.py | build 
	python3 Plots/dEdx_weak.py

build/dEdx_ionization.pdf: Plots/dEdx_ionization.py Plots/matplotlibconfig.py | build 
	python3 Plots/dEdx_ionization.py

build/dEdx_brems.pdf: Plots/dEdx_brems.py Plots/matplotlibconfig.py | build 
	python3 Plots/dEdx_brems.py	

build/spectrum_annihilation.pdf: Plots/spectrum_annihilation.py Plots/matplotlibconfig.py | build
	python3 Plots/spectrum_annihilation.py		

build/compton.pdf: Plots/compton.py Plots/matplotlibconfig.py | build
	python3 Plots/compton.py	

build/compare_compton.pdf: Plots/compare_compton.py Plots/matplotlibconfig.py | build
	python3 Plots/compare_compton.py	

### shower plots

## 1e5

build/data_1e5_500.txt: shower/shower_prop.py shower/config_electron.json shower/config_positron.json shower/config_photon.json
	python3 shower/shower_prop.py 1e5 500 build/data_1e5_500.txt

build/hex_1e5.png: build/data_1e5_500.txt shower/plot_shower_hexbin.py | build
	python3 shower/plot_shower_hexbin.py build/data_1e5_500.txt build/hex_1e5.png

build/shower_1e5.png: build/data_1e5_500.txt shower/plot_shower.py | build
	python3 shower/plot_shower.py build/data_1e5_500.txt build/shower_1e5.png

build/hist_1e5.pdf: build/data_1e5_500.txt shower/plot_shower_hist.py | build
	python3 shower/plot_shower_hist.py build/data_1e5_500.txt 20 build/hist_1e5.pdf

build/hex_1e5_xy.png: build/data_1e5_500.txt shower/plot_shower_hexbin_xy.py | build
	python3 shower/plot_shower_hexbin_xy.py build/data_1e5_500.txt build/hex_1e5_xy.png

## 1e6

build/data_1e6_500.txt: shower/shower_prop.py shower/config_electron.json shower/config_positron.json shower/config_photon.json
	python3 shower/shower_prop.py 1e6 500 build/data_1e6_500.txt

build/hex_1e6.png: build/data_1e6_500.txt shower/plot_shower_hexbin.py | build
	python3 shower/plot_shower_hexbin.py build/data_1e6_500.txt build/hex_1e6.png

build/shower_1e6.png: build/data_1e6_500.txt shower/plot_shower.py | build
	python3 shower/plot_shower.py build/data_1e6_500.txt build/shower_1e6.png

build/hist_1e6.pdf: build/data_1e6_500.txt shower/plot_shower_hist.py | build
	python3 shower/plot_shower_hist.py build/data_1e6_500.txt 20 build/hist_1e6.pdf

build/hex_1e6_xy.png: build/data_1e6_500.txt shower/plot_shower_hexbin_xy.py | build
	python3 shower/plot_shower_hexbin_xy.py build/data_1e6_500.txt build/hex_1e6_xy.png

## 1e7

build/data_1e7_500.txt: shower/shower_prop.py shower/config_electron.json shower/config_positron.json shower/config_photon.json
	python3 shower/shower_prop.py 1e7 500 build/data_1e7_500.txt

build/hex_1e7.png: build/data_1e7_500.txt shower/plot_shower_hexbin.py | build
	python3 shower/plot_shower_hexbin.py build/data_1e7_500.txt build/hex_1e7.png

#build/shower_1e7.png: build/data_1e7_500.txt shower/plot_shower.py | build
#	python3 shower/plot_shower.py build/data_1e7_500.txt build/shower_1e7.png

build/hist_1e7.pdf: build/data_1e7_500.txt shower/plot_shower_hist.py | build
	python3 shower/plot_shower_hist.py build/data_1e7_500.txt 50 build/hist_1e7.pdf

build/hex_1e7_xy.png: build/data_1e7_500.txt shower/plot_shower_hexbin_xy.py | build
	python3 shower/plot_shower_hexbin_xy.py build/data_1e7_500.txt build/hex_1e7_xy.png	

TeXOptions = -lualatex \
			 -interaction=nonstopmode \
			 -halt-on-error \
			 -output-directory=build
                                                                                
build/masterthesis.pdf: FORCE build/cont_rand.pdf build/spectrum.pdf build/dEdx.pdf build/secondary_number.pdf build/dEdx_mupair.pdf \
							build/spectrum_mupair.pdf build/spectrum_mupair_secondary_comparison.pdf build/spectrum_mupair_secondary.pdf \
						    build/mupair_rho.pdf build/dNdx_weak.pdf build/dEdx_weak.pdf build/dEdx_ionization.pdf build/dEdx_brems.pdf \
							build/spectrum_annihilation.pdf build/compton.pdf build/compare_compton.pdf build/hex_1e5.png build/shower_1e5.png \
							build/hist_1e5.pdf build/hex_1e5_xy.png build/hex_1e6.png build/shower_1e6.png build/hist_1e6.pdf build/hex_1e6_xy.png \
							build/hex_1e7.png build/hist_1e7.pdf build/hex_1e7_xy.png | build
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
