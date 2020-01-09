import pyPROPOSAL as pp
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as c
from matplotlib.pyplot import figure, show, rc

from matplotlibconfig import *

m_e = 0.5109989461 # PROPOSAL electron mass in MeV

def calculate_v(E, angle):
    k = E / ( 1. + (1. - np.cos(angle)) * E / m_e )
    return 1. - k / E

gamma = pp.particle.GammaDef.get()
medium = pp.medium.StandardRock(1.0)
cuts_cont = pp.EnergyCutSettings(-1, -1)

param = pp.parametrization.compton.KleinNishina(gamma, medium, cuts_cont, 1.0)

cross = pp.crosssection.ComptonIntegral(param)

plt.rcParams.update(params)
plt.rcParams["axes.axisbelow"] = False # either the ticktabels are behind the plot (True) or the grid infront of the plot (False)
fig = figure(figsize=(width,width*0.8))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection='polar', facecolor='lightgrey')

energies = [1e-3, 511e-3, 10][:]
sigma_all = []
angle_all = []
sigma_max = 0 # to normalize radial axis

for E in energies:
    sigma_list = []
    angle_list = np.linspace(0, 2*np.pi, 10000)
    for angle in angle_list:
        correct = E * m_e / ( m_e - E * np.cos(angle) + E )**2 # correction factor
        v = calculate_v(E, angle)
        sigma_list.append(param.differential_crosssection(E, v) * correct)
    sigma_list = np.array(sigma_list)
    angle_list = np.array(angle_list)
    sigma_all.append(sigma_list)
    angle_all.append(angle_list)
    sigma_max = max(np.max(sigma_list), sigma_max)

for i, (theta, r) in enumerate(zip(angle_all, sigma_all)):
    ax.plot(theta, r/sigma_max, label= r'$E = $ ' + str(energies[i]) + " MeV")

ax.set_rlabel_position(225)
ax.legend(loc='upper left')

fig.savefig("build/compton.pdf", bbox_inches='tight')