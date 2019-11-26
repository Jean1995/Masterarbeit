#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import matplotlib as mpl
    import matplotlib.pyplot as plt
except ImportError:
    raise ImportError("Matplotlib not installed!")

try:
    import numpy as np
except ImportError:
    raise ImportError("Numpy not installed!")

try:
    import pyPROPOSAL as pp
except ImportError:
    raise ImportError("pyPROPOSAL not installed!")

from timeit import default_timer as timer

def muons(energy, statistics, vcut, do_continuous_randomization, dist):

    sec_def = pp.SectorDefinition()
    sec_def.medium = pp.medium.StandardRock(1.0)
    sec_def.geometry = pp.geometry.Sphere(pp.Vector3D(), 1e20, 0)
    sec_def.particle_location = pp.ParticleLocation.inside_detector

    sec_def.scattering_model = pp.scattering.ScatteringModel.Moliere
    sec_def.do_continuous_randomization = do_continuous_randomization

    sec_def.cut_settings.ecut = 0
    sec_def.cut_settings.vcut = vcut

    interpolation_def = pp.InterpolationDef()
    interpolation_def.path_to_tables = "tables/"

    prop = pp.Propagator(
            particle_def=pp.particle.MuMinusDef.get(),
            sector_defs=[sec_def],
            detector=pp.geometry.Sphere(pp.Vector3D(), 1e20, 0),
            interpolation_def=interpolation_def
    )

    mu = prop.particle

    mu_energies = []

    start = timer()


    for i in range(statistics):

        mu.position = pp.Vector3D(0, 0, 0)
        mu.direction = pp.Vector3D(0, 0, -1)
        mu.energy = energy
        mu.propagated_distance = 0

        d = prop.propagate(dist * 100)

        mu_energies.append(mu.energy)

    end = timer()


    return (mu_energies, statistics/(end-start) )


if __name__ == "__main__":

    # =========================================================
    # 	Save energies
    # =========================================================

    energy = 1e8
    statistics = int(1e5)
    dist = 300
    binning = 100


    energies_1, time1 = muons(energy, statistics, 0.05, False, dist)
    energies_2, time2 = muons(energy, statistics, 0.0001, False, dist)
    energies_3, time3 = muons(energy, statistics, 0.05, True, dist)

    from matplotlibconfig import *

    plt.rcParams.update(params)

    # =========================================================
    # 	Plot energies
    # =========================================================

    binning = 100

    fig = plt.figure(figsize=(5.5,3))
    ax = fig.add_subplot(111)

    ax.hist(
        energies_1,
        histtype="step",
        log=True,
        bins=binning,
        label=r"$v_\text{{cut}} = 0.05$"
    )

    ax.hist(
        energies_2,
        histtype="step",
        log=True,
        bins=binning,
        label=r"$v_\text{{cut}} = 10^{-4}$"
    )


    ax.hist(
        energies_3,
        histtype="step",
        log=True,
        bins=binning,
        label=r"$v_\text{{cut}} = 0.05, $ with randomization"
    )

    ax.set_xlabel(r'Final muon energy / $\si{\mega\electronvolt}$')
    ax.set_ylabel(r'Frequency')
    fig.tight_layout()
    ax.legend(loc='upper left')

    fig.savefig("build/cont_rand.pdf")



