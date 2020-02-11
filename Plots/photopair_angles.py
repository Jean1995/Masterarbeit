import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate
import pyPROPOSAL as pp
import matplotlibconfig as conf

plt.rcParams.update(conf.params)
plt.figure(figsize=(conf.width, 3.0))

# load photoangle parametrizations

gamma = pp.particle.GammaDef.get()
medium = pp.medium.Air(1.0)

param_tsai = pp.parametrization.photopair.PhotoAngleTsaiIntegral(gamma, medium)

E = 1e2
m_e = 0.5109989461
x = 0.85

# for tsai parametrization
theta = np.geomspace(1e-6, 0.5*np.pi, 100000)
plt.loglog(theta, np.vectorize(param_tsai.FunctionToIntegral)(E, x, theta), label='Tsai')
result = integrate.quad(lambda theta_int: np.vectorize(param_tsai.FunctionToIntegral)(E, x, theta_int), 0, 2*np.pi)

plt.axvline(result[0], label=r'$\left< \theta \right>$ for Tsai', linestyle = 'dashed')

# for egs4 expression

plt.axvline(x = m_e / E, label = 'EGS4 approximation', linestyle = 'dashed', color='red')

plt.xlabel(r'$\theta \,/\, \si{\radian} $')
plt.ylabel(r'Probability')
plt.grid(conf.grid_conf)
plt.legend(loc='best')


plt.tight_layout()
plt.savefig('build/photopair_angles.pdf',bbox_inches='tight')
