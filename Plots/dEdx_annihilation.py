
import pyPROPOSAL as pp
import pyPROPOSAL.parametrization as parametrization

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

import matplotlibconfig as conf


if __name__ == "__main__":

    eplus = pp.particle.EPlusDef.get()
    medium = pp.medium.Air(1.0)  # With densitiy correction
    cuts = pp.EnergyCutSettings(-1, -1)  # ecut, vcut

    dEdx_photo = []
    energy = np.logspace(3, 12, 2000)

    interpolation_def = pp.InterpolationDef()

    # =========================================================
    # 	Constructor args for parametrizations
    #
    #   - particle
    #   - medium
    #   - cut
    #   - multiplier
    #   - lpm effect
    #   - interpolation definition
    # =========================================================

    param_defs = [
            eplus,
            medium,
            cuts,
            1.0,
            True,
        ]

    param_defs_ionization = [
            eplus,
            medium,
            cuts,
            1.0,
        ]

    param_defs_photo = [
            eplus,
            medium,
            cuts,
            1.0,
            pp.parametrization.photonuclear.ShadowButkevichMikhailov()
        ]

    param_defs_annihilation = [
            eplus,
            medium,
            1.0]

    params = [
        parametrization.pairproduction.KelnerKokoulinPetrukhin(
            *param_defs
        ),
        parametrization.bremsstrahlung.ElectronScreening(
            *param_defs
        ),
        parametrization.photonuclear.AbramowiczLevinLevyMaor97(
            *param_defs_photo
        ),
        parametrization.ionization.BergerSeltzerBhabha(
            *param_defs_ionization
        ),

    ]

    param_annihilation = parametrization.annihilation.Heitler(*param_defs_annihilation)

    # =========================================================
    # 	Create x sections out of their parametrizations
    # =========================================================

    crosssections = []

    crosssections.append(pp.crosssection.EpairIntegral(
        params[0]
            ))

    crosssections.append(pp.crosssection.BremsIntegral(
        params[1]
    ))

    crosssections.append(pp.crosssection.PhotoIntegral(
        params[2]
    ))    

    crosssections.append(pp.crosssection.IonizIntegral(
        params[3]
    ))  


    cross_annihilation = pp.crosssection.AnnihilationIntegral(param_annihilation)

    # =========================================================
    # 	Calculate DE/dx at the given energies
    # =========================================================

    for cross in crosssections:
        dEdx = []
        for E in energy:
            dEdx.append(cross.calculate_dEdx(E))

        dEdx_photo.append(dEdx)

    # =========================================================
    # 	Plot
    # =========================================================

    plt.rcParams.update(conf.params)
    plt.figure(figsize=(conf.width,3.2))

    labels = [r'$e$ pair production', 'Bremsstrahlung', 'Photonuclear', 'Ionization']
    colors = ['C0', 'C1', 'C2', 'C3']

    for dEdx, param, _label, color in zip(dEdx_photo, params, labels, colors):
        plt.loglog(
            energy,
            dEdx,
            linestyle='-',
            label=_label,
            c = color
        )

    def dEdx_annihilation(E):
        ''' calculate dEdx value for Annihilation '''
        return E * np.vectorize(cross_annihilation.calculate_dNdx)(E)

    plt.loglog(energy, dEdx_annihilation(energy), linestyle='-', label='Annihilation', c = 'C8')

    plt.xlabel(r'$E \,/\, \mathrm{MeV} $')
    plt.ylabel(r'$\left\langle\frac{\mathrm{d}E}{\mathrm{d}X}\right\rangle \,\left/\, \left( \rm{MeV} \cdot \rm{g}^{-1} \rm{cm}^2 \right) \right. $')
    plt.grid(conf.grid_conf)
    plt.legend(loc='best')

    plt.xlim(1e3, 1e12)

    plt.tight_layout()
    plt.savefig('build/dEdx_annihilation.pdf',bbox_inches='tight')