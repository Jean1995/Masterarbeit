
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

    electron = pp.particle.EMinusDef.get()
    positron = pp.particle.EPlusDef.get()
    medium = pp.medium.Air(1.0)  # With densitiy correction
    cuts = pp.EnergyCutSettings(-1, -1)  # ecut, vcut

    dEdx_list = []
    energy = np.logspace(-1, 12, 1000)
    energy = energy[energy > 0.52]

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

    param_defs_electron = [electron, medium, cuts, 1.]

    param_defs_positron = [electron, medium, cuts, 1.]


    params = [
		pp.parametrization.ionization.BetheBlochRossi(*param_defs_electron),
		pp.parametrization.ionization.BergerSeltzerMoller(*param_defs_electron),
		pp.parametrization.ionization.BergerSeltzerBhabha(*param_defs_positron)
    ]

    # =========================================================
    #   Create x sections out of their parametrizations
    # =========================================================

    crosssections = []

    crosssections.append(pp.crosssection.IonizIntegral(
        params[0]
            ))

    crosssections.append(pp.crosssection.IonizIntegral(
        params[1]
    ))

    crosssections.append(pp.crosssection.IonizIntegral(
        params[2]
    ))

    # =========================================================
    #   Calculate DE/dx at the given energies
    # =========================================================

    for cross in crosssections:
        dEdx = []
        for E in energy:
            dEdx.append(cross.calculate_dEdx(E))

        dEdx_list.append(dEdx)

    # =========================================================
    #   Plot
    # =========================================================

    plt.rcParams.update(conf.params)
    fig = plt.figure(figsize=(conf.width,4))
    gs = mpl.gridspec.GridSpec(2, 1, height_ratios=[4, 3], hspace=0.05)

    ax = fig.add_subplot(gs[0])

    labels = [r'Bethe', r'Berger-Seltzer (M{\o}ller)', r'Berger-Seltzer (Bhabha)']
    colors = ['green', 'blue', 'orange']

    for dEdx, param, _label, _color in zip(dEdx_list, params, labels, colors):
        ax.semilogx(
            energy,
            dEdx,
            linestyle='-',
            label=_label,
            color = _color
        )

    ax.set_ylabel(r'$\left\langle\frac{\mathrm{d}E}{\mathrm{d}X}\right\rangle \,\left/\, \left( \rm{MeV} \cdot \rm{g}^{-1} \rm{cm}^2 \right) \right. $')
    ax.xaxis.grid(conf.grid_conf)
    ax.yaxis.grid(conf.grid_conf)
    #ax.set_yscale('log')
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
    ax.semilogx(
        energy[start:],
        np.array(dEdx_list)[1][start:] / np.array(dEdx_list[0][start:]),
        linestyle='-',
        label=r'Berger-Seltzer (M{\o}ller) / Bethe',
        color = colors[1]
    )

    ax.semilogx(
        energy[start:],
        np.array(dEdx_list)[2][start:] / np.array(dEdx_list[0][start:]),
        linestyle='-',
        label=r'Berger-Seltzer (Bhabha) / Bethe',
        color = colors[2]
    )

    ax.xaxis.grid(conf.grid_conf)
    ax.yaxis.grid(conf.grid_conf)

    ax.legend(loc='best')
    ax.set_xlabel(r'$E$ / MeV')
    ax.set_ylabel(r'Ratio')
    plt.tight_layout()
    fig.savefig('build/dEdx_ionization.pdf',bbox_inches='tight')
    plt.show()

