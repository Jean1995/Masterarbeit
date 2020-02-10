import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import matplotlib
import matplotlib.cm as cm
from matplotlib.lines import Line2D

from matplotlibconfig import *

scale = 12 # point density (lower scale means smaller distance means more points)

def make_point_path(start, end):
	''' Input: Two arrays of vectors corresponding to starting and ending points of tracks
		Returns: List of points along the tracks '''
	distances = np.linalg.norm(end-start, axis=-1) # distance between start and end
	num_points = np.rint(distances / scale).astype(int) # calculate number of points for each bath
	indices = np.cumsum(num_points) # list of indices
	needed_points = np.sum(num_points)
	point_list = np.zeros((needed_points, np.size(start, 1))) # allocate memory
	for points, index, first, last in zip(num_points, indices, start, end):
		tmp = first + (last - first) * np.vstack((np.linspace(0,1,points), np.linspace(0,1,points))).T
		point_list[ index-points : index] = tmp
	return point_list

x_i_list, y_i_list, z_i_list, x_f_list, y_f_list, z_f_list, ID_list, energy_i_list = np.genfromtxt(sys.argv[1], unpack=True)

# sort input data

particle_data_i = []
particle_data_f = []
count = 0

for x_i, y_i, z_i, x_f, y_f, z_f, ID, energy_i in zip(x_i_list, y_i_list, z_i_list, x_f_list, y_f_list, z_f_list, ID_list, energy_i_list):
	if(energy_i < 50):
		continue

	count += 1
	particle_data_i.append( [x_i, y_i, z_i] )
	particle_data_f.append( [x_f, y_f, z_f] )

## choose projection plane here
projection_vec_1 = np.array([1,0,0])
projection_vec_2 = np.array([0,1,0])

particle_data_i_proj_1 = np.matmul(np.array(particle_data_i), projection_vec_1)
particle_data_i_proj_2 = np.matmul(np.array(particle_data_i), projection_vec_2)

particle_data_f_proj_1 = np.matmul(np.array(particle_data_f), projection_vec_1)
particle_data_f_proj_2 = np.matmul(np.array(particle_data_f), projection_vec_2)



particle_proj_i = np.vstack((particle_data_i_proj_1, particle_data_i_proj_2)).T # starting point list, shape: (number_points, 2)
particle_proj_f = np.vstack((particle_data_f_proj_1, particle_data_f_proj_2)).T # stopping point list, shape: (number_points, 2)


particle_point_path = make_point_path(particle_proj_i, particle_proj_f)

#plt.rcParams['axes.axisbelow'] = True
plt.figure(figsize=(2.7, 2.7))
plt.rcParams.update(params)

conversion_y = 100

y_min = -10000
y_max = 10000

num_bins_y = 750

scale_factor = (y_max - y_min) / (num_bins_y * scale) # L / (num_bins * scale) where L is y_max-y_min and num_bins number of bins in y

plt.hist2d(particle_point_path.T[0]/conversion_y, particle_point_path.T[1]/conversion_y, bins=(num_bins_y, 750), weights = np.ones(len(particle_point_path)) / scale_factor, cmap='Reds', alpha=1, norm=matplotlib.colors.LogNorm(), range=[[-10000/conversion_y, 10000/conversion_y], [-10000/conversion_y, 10000/conversion_y]])

## custom legend

print("Showing " + str(count) + " Particles.")

#plt.grid(True, ls='--') Do we need a grid?
plt.xlabel(r'$x \,/\, \si{\metre}$')
plt.ylabel(r'$y \,/\, \si{\metre}$', labelpad=-10)
plt.xlim(-10000/conversion_y, 10000/conversion_y)
plt.ylim(y_min/conversion_y, y_max/conversion_y)

cb = plt.colorbar(aspect=30)

plt.tight_layout()

if(len(sys.argv)==2):
	plt.show()
else:
	plt.savefig(sys.argv[2], bbox_inches='tight', dpi=500, progressive = True)

