import numpy as np
import pyPROPOSAL as pp
import pyPROPOSAL.parametrization as parametrization

from matplotlibconfig import *

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


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
colors = ['tab:blue', 'tab:orange', 'tab:green']


E_list = [1e4, 1e9]
linestyles = ['--', '-']

statistics = int(1e6)

for E_init, linestyle in zip(E_list, linestyles):
	rho_list = []
	energies = np.ones(statistics)*E_init
	for i, v in enumerate(v_list):
		rho_list.append([])
		for E in energies:
			rho_list[i].append(param.Calculaterho(E, v, np.random.rand(), np.random.rand()))

	for i, (v, c) in enumerate(zip(v_list, colors)):
		plt.hist(np.abs(rho_list[i]), color=c, bins=40, histtype='step', zorder=3, ls=linestyle)

plt.xlabel(r'$\lvert \rho \rvert$')
plt.ylabel(r'Frequency',)

# automatic legend
plt.legend(loc='upper left')
custom_lines = []
legends = []
for v, c in zip(v_list, colors):
	custom_lines.append(Line2D([0], [0], color=c, lw=2))
	legends.append(r'$v = {:.2g}$'.format(v))

plt.legend(custom_lines, legends, loc='upper left')

plt.grid(grid_conf)
plt.tight_layout()
plt.savefig('build/mupair_rho.pdf',bbox_inches='tight')