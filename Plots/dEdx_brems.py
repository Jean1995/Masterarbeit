
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
    energy = np.logspace(-1, 6, 1000)
    E_min = 3. * np.sqrt(np.e) / 4. * 0.51 * 7.**(1./3.) # limit from v_min = v_max for air 
    energy = energy[energy > E_min]

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

    param_defs = [electron, medium, cuts, 1.0, False]

    params = [
		pp.parametrization.bremsstrahlung.ElectronScreening(*param_defs),
        pp.parametrization.bremsstrahlung.CompleteScreening(*param_defs),
        pp.parametrization.bremsstrahlung.AndreevBezrukovBugaev(*param_defs),
    ]


    # =========================================================
    #   Create x sections out of their parametrizations
    # =========================================================

    crosssections = []

    for param in params:
        crosssections.append(pp.crosssection.BremsIntegral(param))

    # =========================================================
    #   Calculate dE/dX at the given energies
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

    plt.axvline(x = 50, linestyle='--', color='red', linewidth=1)

    labels = [r'Electron Screening', r'Complete Screening', r'Andreev Bezrukov Bugaev']
    colors = ['green', 'blue', 'orange']

    for dEdx, param, _label, _color in zip(dEdx_list, params, labels, colors):
        ax.loglog(
            energy,
            dEdx/energy,
            linestyle='-',
            label=_label,
            color = _color
        )

    ax.set_ylabel(r'$ \frac{1}{E} \cdot \left\langle\frac{\mathrm{d}E}{\mathrm{d}X}\right\rangle \,\left/\, \left(\rm{g}^{-1} \rm{cm}^2 \right) \right. $')
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

    plt.axvline(x = 50, linestyle='--', color='red', linewidth=1)
    
    start = 0
    ax.semilogx(
        energy[start:],
        np.array(dEdx_list)[1][start:] / np.array(dEdx_list[0][start:]),
        linestyle='-',
        label=r'CS / ES',
        color = colors[1]
    )

    ax.semilogx(
        energy[start:],
        np.array(dEdx_list)[2][start:] / np.array(dEdx_list[0][start:]),
        linestyle='-',
        label=r'ABB / ES',
        color = colors[2]
    )   

    ax.xaxis.grid(conf.grid_conf)
    ax.yaxis.grid(conf.grid_conf)

    ax.legend(loc='best')
    ax.set_xlabel(r'$E$ / MeV')
    ax.set_ylabel(r'Ratio')
    plt.tight_layout()
    fig.savefig('build/dEdx_brems.pdf',bbox_inches='tight')
    plt.show()
