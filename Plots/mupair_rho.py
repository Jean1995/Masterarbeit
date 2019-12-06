import numpy as np
import pyPROPOSAL as pp
import pyPROPOSAL.parametrization as parametrization

from matplotlibconfig import *

import matplotlib.pyplot as plt


#define defaults and parametrization
mu = pp.particle.MuMinusDef.get()
medium = pp.medium.Ice(1.0)
cuts = pp.EnergyCutSettings(-1, -1) 
interpolation_def = pp.InterpolationDef()
param_defs_mupair = [mu, medium, cuts, 1.0, True, interpolation_def]

plt.rcParams.update(params)

plt.figure(figsize=(width, 3.5))

pp.RandomGenerator.get().set_seed(1234)
param = parametrization.mupairproduction.KelnerKokoulinPetrukhinInterpolant(*param_defs_mupair)

v_list = [0.1, 0.5, 0.8]

rho_list = []


energies = np.ones(1000000)*1e6
for i, v in enumerate(v_list):
	rho_list.append([])
	for E in energies:
		rho_list[i].append(param.Calculaterho(E, v, np.random.rand(), np.random.rand()))



for i, v in enumerate(v_list):
	plt.hist(np.abs(rho_list[i]), bins=40, histtype='step', label=r'$v = {:.2g}$'.format(v), zorder=3)

plt.xlabel(r'$\rho$')
plt.ylabel(r'Frequency',)
plt.legend(loc='upper left')
plt.grid(grid_conf)
plt.tight_layout()
plt.savefig('build/mupair_rho.pdf',bbox_inches='tight')