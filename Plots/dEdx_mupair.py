
import pyPROPOSAL as pp
import pyPROPOSAL.parametrization as parametrization

import matplotlibconfig as conf

try:
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
except ImportError:
    raise ImportError("Matplotlib not installed!")

try:
    import numpy as np
except ImportError:
    raise ImportError(
        "Numpy not installed! Needed to calculate the detector cylinder"
    )

import math


if __name__ == "__main__":

    mu = pp.particle.MuMinusDef.get()
    medium = pp.medium.Ice(1.0)  # With densitiy correction
    cuts = pp.EnergyCutSettings(-1, -1)  # ecut, vcut

    dEdx_photo = []
    energy = np.logspace(2, 9, 100)

    interpolation_def = pp.InterpolationDef()

    # =========================================================
    #   Constructor args for parametrizations
    #
    #   - particle
    #   - medium
    #   - cut
    #   - multiplier
    #   - lpm effect
    #   - interpolation definition
    # =========================================================

    param_defs = [
            mu,
            medium,
            cuts,
            1.0,
            True,
        ]

    param_defs_mupair = [
            mu,
            medium,
            cuts,
            1.0,
            False,
        ]

    params = [
        parametrization.pairproduction.KelnerKokoulinPetrukhin(
            *param_defs
        ),
        parametrization.mupairproduction.KelnerKokoulinPetrukhin(
            *param_defs_mupair
        )
    ]

    # =========================================================
    #   Create x sections out of their parametrizations
    # =========================================================

    crosssections = []

    crosssections.append(pp.crosssection.EpairIntegral(
        params[0]
            ))

    crosssections.append(pp.crosssection.MupairIntegral(
        params[1]
    ))

    # =========================================================
    #   Calculate DE/dx at the given energies
    # =========================================================

    for cross in crosssections:
        dEdx = []
        for E in energy:
            dEdx.append(cross.calculate_dEdx(E))

        dEdx_photo.append(dEdx)

    # =========================================================
    #   Plot
    # =========================================================

    plt.rcParams.update(conf.params)
    fig = plt.figure(figsize=(conf.width,4))
    gs = mpl.gridspec.GridSpec(2, 1, height_ratios=[3, 2], hspace=0.05)

    ax = fig.add_subplot(gs[0])

    labels = [r'$e$-Paarproduktion', r'$\mu$-Paarproduktion']

    for dEdx, param, _label in zip(dEdx_photo, params, labels):
        ax.loglog(
            energy,
            dEdx,
            linestyle='-',
            label=_label
        )

    ax.set_ylabel(r'$\left\langle\frac{\mathrm{d}E}{\mathrm{d}X}\right\rangle \,\left/\, \left( \rm{MeV} \cdot \rm{g}^{-1} \rm{cm}^2 \right) \right. $')
    ax.xaxis.grid(conf.grid_conf)
    ax.yaxis.grid(conf.grid_conf)
    ax.legend(loc='best')
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False
    ) # labels along the bottom edge are off

    # ====[ ratio ]============================================

    ax = fig.add_subplot(gs[1], sharex=ax)

    start = 0
    ax.loglog(
        energy[start:],
        np.array(dEdx_photo)[1][start:] / np.array(dEdx_photo[0][start:]),
        linestyle='-',
        label=""
    )

    ax.xaxis.grid(conf.grid_conf)
    ax.yaxis.grid(conf.grid_conf)

    ax.set_ylim(8e-7, 1e-2)
    ax.set_xlabel(r'$E$ / MeV')
    ax.set_ylabel(r'$\left\langle\frac{\mathrm{d}E}{\mathrm{d}X}\right\rangle_\mu \,\left/\, \left\langle\frac{\mathrm{d}E}{\mathrm{d}X}\right\rangle_e \right.$')
    plt.tight_layout()
    fig.savefig('build/dEdx_mupair.pdf',bbox_inches='tight')
    plt.show()
