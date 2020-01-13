import pyPROPOSAL as pp
import numpy as np
import matplotlib.pyplot as plt
from matplotlibconfig import *

plt.rcParams.update(params)
plt.figure(figsize=(width, 3.0))


gamma = pp.particle.GammaDef.get()
medium = pp.medium.Air(1.0)

energy_cut_settings = pp.EnergyCutSettings(1e-10, -1)

param_list_photopair = []
param_list_compton = []
param_list_photangle = []

param_photopair = pp.parametrization.photopair.Tsai(gamma, medium, 1.0)
param_compton = pp.parametrization.compton.KleinNishina(gamma, medium, energy_cut_settings, 1.0 )
param_photoangle = pp.parametrization.photopair.PhotoAngleNoDeflection(gamma, medium)

cross_photopair = pp.crosssection.PhotoPairIntegral(param_photopair, param_photoangle)   
cross_compton = pp.crosssection.ComptonIntegral(param_compton)

energy_list = np.logspace(0, 5, 1000)
sigma_photopair = np.vectorize(cross_photopair.calculate_dNdx)(energy_list)
plt.loglog(energy_list, sigma_photopair, label=r'Pair production')
sigma_compton = np.vectorize(cross_compton.calculate_dNdx)(energy_list)
plt.loglog(energy_list, sigma_compton, label="Compton scattering")
plt.ylabel(r'$ \sigma_{\text{tot}}(E)  \,\left/\, \left( \rm{cm}^2 \rm{g}^{-1} \right) \right. $') #not sure
plt.xlabel(r'$E$ / MeV')
plt.legend(loc='best')
plt.grid(grid_conf)
plt.savefig("build/compare_compton.pdf", bbox_inches='tight')
plt.clf()
    
 
