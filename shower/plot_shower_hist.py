import numpy as np
import matplotlib.pyplot as plt
import sys

from matplotlibconfig import *

plt.rcParams.update(params)

def binning(upper, lower, x_up, x_low):
    if(upper < lower):
        upper, lower = lower, upper
    condition =  (x_up >= lower) & (x_low <= lower) | (x_up >= upper) & (x_low <= upper) | (x_up <= upper) & (x_low >= lower) | (x_up >= upper) & (x_low <= lower) 
    return np.sum(condition)

x, y, z, x_pre, y_pre, z_pre, ID, E_i = np.genfromtxt(sys.argv[1], unpack=True)

conversion_z = 100 # cm in m
x /= conversion_z
y /= conversion_z
z /= conversion_z
x_pre /= conversion_z
y_pre /= conversion_z
z_pre /= conversion_z


if(len(sys.argv)<2):
	bin_num = 100
else:
	bin_num = sys.argv[2]

		
binning=np.vectorize(binning, excluded = ['x_up', 'x_low'])
bin_borders = np.linspace(min( np.min(z), np.min(z_pre) ), max( np.max(z), np.max(z_pre) ), int(bin_num))

bin_vals = binning(bin_borders[:-1], bin_borders[1:], x_up = z_pre, x_low = z)

plt.figure(figsize=(width, 2.7))

plt.step(bin_borders[:-1], bin_vals, where='post')
plt.ylabel("Particle number")
plt.xlabel(r'$z \,/\, \si{\metre}$')
plt.xlim(0, 1000000/conversion_z)
plt.grid()

if(len(sys.argv)<=3):
	plt.show()
else:
	plt.savefig(sys.argv[3], bbox_inches='tight')
