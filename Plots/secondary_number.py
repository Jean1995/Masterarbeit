import sys
import pyPROPOSAL
import math
import time
import datetime

from matplotlibconfig import *

try:
    import matplotlib
    matplotlib.use("Agg")

    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm
    from mpl_toolkits.axes_grid1 import make_axes_locatable

except ImportError:
    print("Matplotlib not installed!")

import numpy as np
# np.set_printoptions(threshold='nan')


class ProgressBar(object):

    def __init__(self, loops, bar_lenght=50, start=0, **keywords):

        self._bar_lenght = bar_lenght
        self._bar = []
        self._loops = loops
        self._start = float(start)
        self._current_loop = start

        self._started_process = False
        self._start_time = None

        self._pacman = False

        self._status = ""
        self._text = "\rPercent: [{0}] {1}% Time: {2} Iteration: {3}/{4} {5}"

        self._bar_full = "="
        self._bar_empty = " "

        for key, value in keywords.items():
            if key is "pacman":
                assert type(value) is bool
                self._pacman = value

        if self._pacman:
            self._bar_full = "-"
            self._bar_empty = "o"

            current = self._bar_empty
            for i in range(self._bar_lenght):
                if current is self._bar_empty:
                    current = " "
                    self._bar.append(current)
                else:
                    current = self._bar_empty
                    self._bar.append(current)
        else:
            for i in range(self._bar_lenght):
                self._bar.append(self._bar_empty)

        self._current_pac_state = "C"
        self._current_pac_block = 0

    def reset(self):
        self._current_loop = self._start
        self._status = ""
        self._started_process = False

    def start(self):
        self._started_process = True
        self._start_time = time.time()

    def update(self):
        if self._started_process is False:
            print("Pleas start ProgressBar before updating it!")
            return

        self._current_loop += 1.0
        progress = self._current_loop / self._loops

        if progress >= 1.0:
            self._status = "Done...\n"

        if self._pacman:
            block = int((self._bar_lenght - 1) * progress)

            if self._current_pac_block < block:
                self._current_pac_block = block
                if self._current_pac_state is "c":
                    self._current_pac_state = "C"
                else:
                    self._current_pac_state = "c"
            else:
                pass

            self._bar[block] = '\033[1m' + "\033[93m" + \
                               self._current_pac_state + '\033[0m'
            self._bar[:block] = block * [self._bar_full]
        else:
            block = int(self._bar_lenght * progress)
            self._bar[:block] = baxislock * [self._bar_full]

        text = self._text.format(
            "".join(self._bar),
            progress*100,
            str(datetime.timedelta(seconds=(time.time() - self._start_time))),
            int(self._current_loop),
            self._loops,
            self._status
        )

        sys.stdout.write(text)
        sys.stdout.flush()


def plot_hist(ax, prim, sec, label):

    x_space = np.logspace(  2, 14, 100)
    y_space = np.logspace( -2, 14, 100)

    hist = ax.hist2d(prim, sec, bins=(x_space, y_space), norm=LogNorm())

    textstr = label
    
    props = dict(facecolor='white', alpha=0.8, edgecolor='none')
    ax.text(0.1, 0.9, textstr,
            verticalalignment='top', horizontalalignment='left',
            transform=ax.transAxes, fontsize=font_size, bbox=props)

    ax.set_xscale("log", nonposx='clip')
    ax.set_yscale("log", nonposy='clip')

    ax.grid(ls=":", lw=0.2)

    count = sum([sum(x) for x in hist[0]])
    esum = sum(sec)

    return (ax, hist, count, esum)

if __name__ == "__main__":

    import sys

    # =========================================================
    # 	Commandline args
    # =========================================================

    statistics = 10
    config_file = "resources/config_ice.json"

    if len(sys.argv) == 2:
        statistics = int(sys.argv[1])
    elif len(sys.argv) == 3:
        statistics = int(sys.argv[1])
        config_file = sys.argv[2]

    # =========================================================
    #   PROPOSAL
    # =========================================================

    prop = pyPROPOSAL.Propagator(
        particle_def=pyPROPOSAL.particle.MuMinusDef.get(),
        config_file=config_file
    )

    mu = prop.particle

    E_max_log = 14

    epair_primary_energy = []
    epair_secondary_energy = []

    brems_primary_energy = []
    brems_secondary_energy = []

    ioniz_primary_energy = []
    ioniz_secondary_energy = []

    photo_primary_energy = []
    photo_secondary_energy = []

    length = []
    n_secondarys = []

    progress = ProgressBar(statistics, pacman=True)
    progress.start()

    for i in range(statistics):
        progress.update()

        mu.position = pyPROPOSAL.Vector3D(0, 0, 0)
        mu.direction = pyPROPOSAL.Vector3D(0, 0, -1)
        mu.energy = math.pow(10, E_max_log)
        mu.propagated_distance = 0

        secondarys = prop.propagate()

        length.append(mu.propagated_distance / 100)
        n_secondarys.append(len(secondarys))

        for sec in secondarys:
            sec_energy = sec.energy
            energy = sec.parent_particle_energy

            if sec.id == pyPROPOSAL.particle.Data.Epair:
                epair_primary_energy.append(energy)
                epair_secondary_energy.append(sec_energy)
            if sec.id == pyPROPOSAL.particle.Data.Brems:
                brems_primary_energy.append(energy)
                brems_secondary_energy.append(sec_energy)
            if sec.id == pyPROPOSAL.particle.Data.DeltaE:
                ioniz_primary_energy.append(energy)
                ioniz_secondary_energy.append(sec_energy)
            if sec.id == pyPROPOSAL.particle.Data.NuclInt:
                photo_primary_energy.append(energy)
                photo_secondary_energy.append(sec_energy)

    # =========================================================
    #   Plot
    # =========================================================

    plt.rcParams.update(params)


    fig, axes = plt.subplots(nrows=2, ncols=2, 
        figsize=(width , 0.7*width), sharex=True, sharey=True
    )

    hists = []
    counts = []
    esums = []
    primary_energies = [epair_primary_energy, brems_primary_energy, photo_primary_energy, ioniz_primary_energy]
    secondary_energies = [epair_secondary_energy, brems_secondary_energy, photo_secondary_energy, ioniz_secondary_energy]
    labels = [r'$e$ pair production', "Bremsstrahlung", "Photonuclear", "Ionization"]

    for ax, primary_energy, secondary_energy, label in zip(axes.flat, primary_energies, secondary_energies, labels):
    	ax, hist_tmp, count, esum = plot_hist(ax, primary_energy, secondary_energy, label)
    	hists.append(hist_tmp[3])
    	counts.append(count)
    	esums.append(esums)
    fig.tight_layout(rect=(0.02, 0.02, 1, 1)) # rect = (0,0,1,1) is the default option

    fig.subplots_adjust(wspace=0.15, hspace=0.1, right=0.88)
    cbar_ax = fig.add_axes([0.91, 0.15, 0.03, 0.7])
    fig.colorbar(hists[3], cax=cbar_ax)

    fig.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.xlabel(r'$  E_{\textrm{primary}}\,/\, \mathrm{MeV} $')
    plt.ylabel(r'$  E_{\textrm{primary}} \cdot v \,/\, \mathrm{MeV} $', labelpad=10)

    fig.savefig("build/secondary_number.pdf")