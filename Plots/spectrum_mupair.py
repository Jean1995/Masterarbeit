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

    mu_def = pp.particle.MuMinusDef.get()
    geometry = pp.geometry.Sphere(pp.Vector3D(), 1.e20, 0.0)
    ecut = 500
    vcut = -1

    sector_def = pp.SectorDefinition()
    sector_def.cut_settings = pp.EnergyCutSettings(ecut, vcut)
    sector_def.medium = pp.medium.Ice(1.0)
    sector_def.geometry = geometry
    sector_def.scattering_model = pp.scattering.ScatteringModel.NoScattering
    sector_def.crosssection_defs.brems_def.lpm_effect = True
    sector_def.crosssection_defs.epair_def.lpm_effect = True

    detector = geometry

    interpolation_def = pp.InterpolationDef()
    interpolation_def.path_to_tables = "tables/"

    #initialize propagator without mupairproduction
    prop_nomupair = pp.Propagator(mu_def, [sector_def], detector, interpolation_def)

    #initialize propagator with mupairproduction
    sector_def.crosssection_defs.mupair_def.parametrization = pp.parametrization.mupairproduction.MupairParametrization.KelnerKokoulinPetrukhin
    sector_def.crosssection_defs.mupair_def.particle_output = False
    prop = pp.Propagator(mu_def, [sector_def], detector, interpolation_def)


    # for rho sampling
    param_defs_mupair = [mu_def, sector_def.medium, sector_def.cut_settings, 1.0, True, interpolation_def]
    param_mupair = pp.parametrization.mupairproduction.KelnerKokoulinPetrukhinInterpolant(*param_defs_mupair)

    statistics_log = 4
    statistics = int(10**statistics_log)
    propagation_length = 1e20 # cm
    E_log = 8.0
    pp.RandomGenerator.get().set_seed(1234)

    ### PRIMARY MUON PROPAGATION ###

    muon_energies = np.ones(statistics)*10**E_log
    epair_secondary_energy = []
    brems_secondary_energy = []
    ioniz_secondary_energy = []
    photo_secondary_energy = []

    mpair_secondary_energy = []
    mpair_primary_energy = []

    print("Propagate primary muons...")
    progress = ProgressBar(statistics, pacman=True)
    progress.start()

    for mu_energy in muon_energies:
        progress.update()

        prop.particle.position = pp.Vector3D(0, 0, 0)
        prop.particle.direction = pp.Vector3D(0, 0, -1)
        prop.particle.propagated_distance = 0
        prop.particle.energy = mu_energy

        secondarys = prop.propagate(propagation_length)

        for sec in secondarys:
            sec_energy = sec.energy

            if sec.id == pp.particle.Data.Epair:
                epair_secondary_energy.append(sec_energy)
            elif sec.id == pp.particle.Data.Brems:
                brems_secondary_energy.append(sec_energy)
            elif sec.id == pp.particle.Data.DeltaE:
                ioniz_secondary_energy.append(sec_energy)
            elif sec.id == pp.particle.Data.NuclInt:
                photo_secondary_energy.append(sec_energy)
            elif sec.id == pp.particle.Data.MuPair:
                mpair_secondary_energy.append(sec_energy)
                mpair_primary_energy.append(sec.parent_particle_energy)
    #statistics:
    num_all = len(brems_secondary_energy) + len(epair_secondary_energy) + len(photo_secondary_energy) + len(ioniz_secondary_energy) + len(mpair_secondary_energy)
    ene_all = sum(brems_secondary_energy) + sum(epair_secondary_energy) + sum(photo_secondary_energy) + sum(ioniz_secondary_energy) + sum(mpair_secondary_energy)

    print("Number:")
    print("Brems: ", len(brems_secondary_energy), len(brems_secondary_energy)/num_all)
    print("Epair: ", len(epair_secondary_energy), len(epair_secondary_energy)/num_all)
    print("photo: ", len(photo_secondary_energy), len(photo_secondary_energy)/num_all)
    print("Ioniz: ", len(ioniz_secondary_energy), len(ioniz_secondary_energy)/num_all)
    print("MPair: ", len(mpair_secondary_energy), len(mpair_secondary_energy)/num_all)
    print("Energies:")

    print("Brems ", sum(brems_secondary_energy), sum(brems_secondary_energy)/ene_all)
    print("Epair: ", sum(epair_secondary_energy), sum(epair_secondary_energy)/ene_all)
    print("photo: ", sum(photo_secondary_energy), sum(photo_secondary_energy)/ene_all)
    print("Ioniz: ", sum(ioniz_secondary_energy), sum(ioniz_secondary_energy)/ene_all)
    print("MPair: ", sum(mpair_secondary_energy), sum(mpair_secondary_energy)/ene_all)

    plt.rcParams.update(params)

    fig_all = plt.figure(
        figsize=(width, 4)
    )

    x_space = np.logspace(min(np.log10(np.concatenate((ioniz_secondary_energy,brems_secondary_energy,photo_secondary_energy,epair_secondary_energy,mpair_secondary_energy)))), E_log, 100)

    ax_all = fig_all.add_subplot(111)
    ax_all.hist(
        [
            ioniz_secondary_energy,
            photo_secondary_energy,
            brems_secondary_energy,
            epair_secondary_energy,
            mpair_secondary_energy,
            np.concatenate((
                ioniz_secondary_energy,
                brems_secondary_energy,
                photo_secondary_energy,
                epair_secondary_energy,
                mpair_secondary_energy)
            )
        ],
        histtype='step',
        log=True,
        bins=x_space,
        label=['Ionization', 'Photonuclear', 'Bremsstrahlung', r'$e$ pair production', r'$\mu$ pair production', 'Sum'],
        color = ['C3', 'C2', 'C1', 'C0', 'C4', 'C7'],
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
    fig_all.savefig("build/spectrum_mupair.pdf",bbox_inches='tight')
    plt.clf()

    epair_old = epair_secondary_energy
    brems_old = brems_secondary_energy
    ioniz_old = ioniz_secondary_energy
    photo_old = photo_secondary_energy
    mpair_old = mpair_secondary_energy

    ### SECONDARY MUON PROPAGATION ###
    secondary_muon_energy = []

    for E, nu in zip(mpair_primary_energy, mpair_secondary_energy):
        rho = param_mupair.Calculaterho(E, nu/E, np.random.rand(), np.random.rand())
        secondary_muon_energy.append( 0.5 * nu * (1. + rho) )
        secondary_muon_energy.append( 0.5 * nu * (1. - rho) )


    epair_secondary_energy = []
    brems_secondary_energy = []
    ioniz_secondary_energy = []
    photo_secondary_energy = []
    mpair_secondary_energy = []

    print("Propagate secondary muons...")
    progress = ProgressBar(len(secondary_muon_energy), pacman=True)
    progress.start()

    for mu_energy in secondary_muon_energy:
        progress.update()

        prop.particle.position = pp.Vector3D(0, 0, 0)
        prop.particle.direction = pp.Vector3D(0, 0, -1)
        prop.particle.propagated_distance = 0
        prop.particle.energy = mu_energy

        secondarys = prop.propagate(propagation_length)

        for sec in secondarys:
            sec_energy = sec.energy

            if sec.id == pp.particle.Data.Epair:
                epair_secondary_energy.append(sec_energy)
            elif sec.id == pp.particle.Data.Brems:
                brems_secondary_energy.append(sec_energy)
            elif sec.id == pp.particle.Data.DeltaE:
                ioniz_secondary_energy.append(sec_energy)
            elif sec.id == pp.particle.Data.NuclInt:
                photo_secondary_energy.append(sec_energy)
            elif sec.id == pp.particle.Data.MuPair:
                mpair_secondary_energy.append(sec_energy)

    print("Number:")
    print("Brems: ", len(brems_secondary_energy), len(brems_secondary_energy)/num_all)
    print("Epair: ", len(epair_secondary_energy), len(epair_secondary_energy)/num_all)
    print("photo: ", len(photo_secondary_energy), len(photo_secondary_energy)/num_all)
    print("Ioniz: ", len(ioniz_secondary_energy), len(ioniz_secondary_energy)/num_all)
    print("MPair: ", len(mpair_secondary_energy), len(mpair_secondary_energy)/num_all)
    print("Energies:")

    print("Brems ", sum(brems_secondary_energy), sum(brems_secondary_energy)/ene_all)
    print("Epair: ", sum(epair_secondary_energy), sum(epair_secondary_energy)/ene_all)
    print("photo: ", sum(photo_secondary_energy), sum(photo_secondary_energy)/ene_all)
    print("Ioniz: ", sum(ioniz_secondary_energy), sum(ioniz_secondary_energy)/ene_all)
    print("MPair: ", sum(mpair_secondary_energy), sum(mpair_secondary_energy)/ene_all)


    ### PROPAGATION WITHOUT MUPAIRPRODUCTION

    muon_energies = np.ones(statistics)*10**E_log
    epair_secondary_energy_nomupair = []
    brems_secondary_energy_nomupair = []
    ioniz_secondary_energy_nomupair = []
    photo_secondary_energy_nomupair = []

    print("Propagate muons without MuPairProduction...")
    progress = ProgressBar(statistics, pacman=True)
    progress.start()

    for mu_energy in muon_energies:
        progress.update()

        prop_nomupair.particle.position = pp.Vector3D(0, 0, 0)
        prop_nomupair.particle.direction = pp.Vector3D(0, 0, -1)
        prop_nomupair.particle.propagated_distance = 0
        prop_nomupair.particle.energy = mu_energy

        secondarys = prop_nomupair.propagate(propagation_length)

        for sec in secondarys:
            sec_energy = sec.energy

            if sec.id == pp.particle.Data.Epair:
                epair_secondary_energy_nomupair.append(sec_energy)
            elif sec.id == pp.particle.Data.Brems:
                brems_secondary_energy_nomupair.append(sec_energy)
            elif sec.id == pp.particle.Data.DeltaE:
                ioniz_secondary_energy_nomupair.append(sec_energy)
            elif sec.id == pp.particle.Data.NuclInt:
                photo_secondary_energy_nomupair.append(sec_energy)
            elif sec.id == pp.particle.Data.MuPair:
                print("Something went wrong")


    # Comparison plot

    plt.rcParams.update(params)

    fig_all = plt.figure(
        figsize=(width, 4)
    )

    gs = matplotlib.gridspec.GridSpec(2, 1, height_ratios=[4, 1], hspace=0.05)


    x_space = np.logspace(min(np.log10(np.concatenate((ioniz_secondary_energy_nomupair,photo_secondary_energy_nomupair,brems_secondary_energy_nomupair,epair_secondary_energy_nomupair)))), E_log, 100)
    
    ax_all = fig_all.add_subplot(gs[0])
    ax_all.hist(
        [
            ioniz_secondary_energy,
            photo_secondary_energy,
            brems_secondary_energy,
            epair_secondary_energy,
            mpair_secondary_energy
        ],
        histtype='step',
        color = ['C3', 'C2', 'C1', 'C0', 'C4'],
        log=True,
        bins=x_space,
        zorder = 3,
        linestyle = 'dashed',
    )

    ax_all.hist(
        [
            ioniz_secondary_energy_nomupair,
            photo_secondary_energy_nomupair,
            brems_secondary_energy_nomupair,
            epair_secondary_energy_nomupair,
            np.concatenate((
                ioniz_secondary_energy_nomupair,
                brems_secondary_energy_nomupair,
                photo_secondary_energy_nomupair,
                epair_secondary_energy_nomupair)
            )
        ],
        color = ['C3', 'C2', 'C1', 'C0','C7'],
        label=['Ionization', 'Photonuclear', 'Bremsstrahlung', r'$e$ pair production', 'Sum'],
        histtype='step',
        log=True,
        bins=x_space,
        zorder = 4,
    )    

    plt.xscale('log')
    #minor_locator = AutoMinorLocator()
    #ax_all.xaxis.set_minor_locator(minor_locator)
    ax_all.legend(loc='best')
    ax_all.set_ylabel(r'Frequency')
    #plt.xlim(left=2.5)
    plt.grid(grid_conf)
    plt.setp(ax_all.get_xticklabels(), visible=False)
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False
    ) # labels along the bottom edge are off

    ax_all = fig_all.add_subplot(gs[1], sharex=ax_all)

    hist_1, bin_edges_1 = np.histogram(np.concatenate((ioniz_secondary_energy_nomupair,brems_secondary_energy_nomupair,photo_secondary_energy_nomupair,epair_secondary_energy_nomupair)),
                                        bins = x_space)

    hist_2, bin_edges_2 = np.histogram(np.concatenate((epair_old, ioniz_old, brems_old, photo_old, ioniz_secondary_energy,photo_secondary_energy,brems_secondary_energy,epair_secondary_energy,mpair_secondary_energy)),
                                        bins = x_space)    

    print(np.shape(x_space))

    print(np.shape(hist_1))

    ax_all.step(x_space[1:], hist_1/hist_2, where='pre', color='C4')
    #ax_all.bar(x_space[:-1], hist_1/hist_2, width=np.diff(x_space), align='edge', fill=False)

    ax_all.set_xlabel(r'$ E \cdot v \,/\, \mathrm{MeV} $')
    ax_all.set_ylabel(r'ratio')
    plt.grid(grid_conf)
    ax_all.axhline(y=1, linewidth=0.5, zorder=0, C = 'C7')

    fig_all.tight_layout()
    fig_all.savefig("build/spectrum_mupair_secondary_comparison.pdf",bbox_inches='tight')
    plt.clf()


    # Plot particles from secondary spectrum

    plt.rcParams.update(params)

    fig_all = plt.figure(
        figsize=(width, 4)
    )

    x_space = np.logspace(min(np.log10(np.concatenate((ioniz_secondary_energy,brems_secondary_energy,photo_secondary_energy,epair_secondary_energy,mpair_secondary_energy)))), E_log, 100)

    ax_all = fig_all.add_subplot(111)
    ax_all.hist(
        [
            ioniz_secondary_energy,
            photo_secondary_energy,
            brems_secondary_energy,
            epair_secondary_energy,
            mpair_secondary_energy,
            np.concatenate((
                ioniz_secondary_energy,
                brems_secondary_energy,
                photo_secondary_energy,
                epair_secondary_energy,
                mpair_secondary_energy)
            )
        ],
        histtype='step',
        log=True,
        bins=x_space,
        label=['Ionization', 'Photonuclear', 'Bremsstrahlung', r'$e$ pair production', r'$\mu$ pair production', 'Sum'],
        color = ['C3', 'C2', 'C1', 'C0', 'C4', 'C7'],
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
    fig_all.savefig("build/spectrum_mupair_secondary.pdf",bbox_inches='tight')
    plt.clf()


if __name__ == "__main__":
    propagate_muons()

