from __future__ import division

import sys
import os
import pyPROPOSAL as pp
import math
import time
import datetime

from matplotlibconfig import *

try:
    import matplotlib
    matplotlib.use("Agg")

    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm
    from matplotlib.ticker import AutoMinorLocator
    from mpl_toolkits.axes_grid1 import make_axes_locatable

except ImportError:
    print("Matplotlib not installed!")

try:
    import numpy as np
except ImportError:
    print("Numpy not installed!")

try:
    from sklearn.utils import check_random_state
except ImportError:
    print("SkLearn not installed!")


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
            self._bar[:block] = block * [self._bar_full]

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

def propagate_muons():

    mu_def = pp.particle.EPlusDef.get()
    geometry = pp.geometry.Sphere(pp.Vector3D(), 1.e20, 0.0)
    ecut = 500
    vcut = -1

    sector_def = pp.SectorDefinition()
    sector_def.cut_settings = pp.EnergyCutSettings(ecut, vcut)
    sector_def.medium = pp.medium.Air(1.0)
    sector_def.geometry = geometry
    sector_def.scattering_model = pp.scattering.ScatteringModel.NoScattering
    sector_def.crosssection_defs.brems_def.lpm_effect = True
    sector_def.crosssection_defs.epair_def.lpm_effect = True

    sector_def.crosssection_defs.annihilation_def.parametrization = pp.parametrization.annihilation.AnnihilationParametrization.Heitler
    sector_def.crosssection_defs.brems_def.parametrization = pp.parametrization.bremsstrahlung.BremsParametrization.ElectronScreening
    sector_def.crosssection_defs.ioniz_def.parametrization = pp.parametrization.ionization.IonizParametrization.IonizBergerSeltzerBhabha

    detector = geometry

    interpolation_def = pp.InterpolationDef()
    interpolation_def.path_to_tables = "tables/"

    prop = pp.Propagator(mu_def, [sector_def], detector, interpolation_def)

    statistics_log = 5
    statistics = int(10**statistics_log)
    propagation_length = 1e20 # cm
    E_log = 8.0
    pp.RandomGenerator.get().set_seed(1234)

    muon_energies = np.ones(statistics)*10**E_log
    epair_secondary_energy = []
    brems_secondary_energy = []
    ioniz_secondary_energy = []
    photo_secondary_energy = []
    annih_secondary_energy = []

    progress = ProgressBar(statistics, pacman=True)
    progress.start()

    for mu_energy in muon_energies:
        progress.update()

        prop.particle.position = pp.Vector3D(0, 0, 0)
        prop.particle.direction = pp.Vector3D(0, 0, -1)
        prop.particle.propagated_distance = 0
        prop.particle.energy = mu_energy

        secondarys = prop.propagate(propagation_length)

        skip_next = False
        tmp_energy = 0

        for sec in secondarys:

            if(skip_next):
                skip_next = False
                annih_secondary_energy.append(sec_energy + tmp_energy)
                if(sec.particle_def.name!="Gamma"):
                    print("Particle is not a Photon!?")
                continue

            sec_energy = sec.energy

            if(sec_energy <= 0):
                continue 

            if sec.id == pp.particle.Data.Epair:
                epair_secondary_energy.append(sec_energy)
            elif sec.id == pp.particle.Data.Brems:
                brems_secondary_energy.append(sec_energy)
            elif sec.id == pp.particle.Data.DeltaE:
                ioniz_secondary_energy.append(sec_energy)
            elif sec.id == pp.particle.Data.NuclInt:
                photo_secondary_energy.append(sec_energy)
            else:
                tmp_energy = sec_energy
                if(sec.particle_def.name!="Gamma"):
                    print("Particle is not a Photon!?")
                skip_next = True
    #statistics:
    num_all = len(brems_secondary_energy) + len(epair_secondary_energy) + len(photo_secondary_energy) + len(ioniz_secondary_energy) + len(annih_secondary_energy)
    ene_all = sum(brems_secondary_energy) + sum(epair_secondary_energy) + sum(photo_secondary_energy) + sum(ioniz_secondary_energy) + sum(annih_secondary_energy)

    print("Anzahl:")
    print("Brems: ", len(brems_secondary_energy), len(brems_secondary_energy)/num_all)
    print("Epair: ", len(epair_secondary_energy), len(epair_secondary_energy)/num_all)
    print("photo: ", len(photo_secondary_energy), len(photo_secondary_energy)/num_all)
    print("Ioniz: ", len(ioniz_secondary_energy), len(ioniz_secondary_energy)/num_all)
    print("Annih: ", len(annih_secondary_energy), len(annih_secondary_energy)/num_all)
    print("Energie:")

    print("Brems ", sum(brems_secondary_energy), sum(brems_secondary_energy)/ene_all)
    print("Epair: ", sum(epair_secondary_energy), sum(epair_secondary_energy)/ene_all)
    print("photo: ", sum(photo_secondary_energy), sum(photo_secondary_energy)/ene_all)
    print("Ioniz: ", sum(ioniz_secondary_energy), sum(ioniz_secondary_energy)/ene_all)
    print("Annih: ", sum(annih_secondary_energy), sum(annih_secondary_energy)/ene_all)

    plt.rcParams.update(params)

    fig_all = plt.figure(
        figsize=(width, 4)
    )

    x_space = np.logspace(min(np.log10(np.concatenate((ioniz_secondary_energy,brems_secondary_energy,photo_secondary_energy,epair_secondary_energy,annih_secondary_energy)))), E_log, 100)

    ax_all = fig_all.add_subplot(111)
    ax_all.hist(
        [
            ioniz_secondary_energy,
            photo_secondary_energy,
            brems_secondary_energy,
            epair_secondary_energy,
            annih_secondary_energy,
            np.concatenate((
                ioniz_secondary_energy,
                brems_secondary_energy,
                photo_secondary_energy,
                epair_secondary_energy,
                annih_secondary_energy)
            )
        ],
        histtype='step',
        log=True,
        bins=x_space,
        label=['Ionization', 'Photonuclear', 'Bremsstrahlung', r'$e$ pair production', 'Annihilation', 'Sum'],
        color = ['C3', 'C2', 'C1', 'C0', 'C8', 'C7'],
        zorder = 3
    )

    plt.xscale('log')
    #minor_locator = AutoMinorLocator()
    #ax_all.xaxis.set_minor_locator(minor_locator)
    ax_all.legend(loc='best')
    ax_all.set_xlabel(r'$ E \cdot v \,/\, \mathrm{MeV} $')
    ax_all.set_ylabel(r'Frequency')
    #plt.xlim(left=2.5)
    plt.grid(grid_conf)
    fig_all.tight_layout()
    fig_all.savefig("build/spectrum_annihilation.pdf",bbox_inches='tight')



if __name__ == "__main__":
    propagate_muons()

