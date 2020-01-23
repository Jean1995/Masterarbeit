
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

def sigma_decay(E, rho):
    c = 2.99792458e10 #speed of light in cm / s
    tau = 2.1969811e-6 # muon life time
    m = 105.6583745 # muon mass in MeV
    gamma = (E - m)/m
    beta = np.sqrt(1 - 1 / gamma**2)
    return 1 / (gamma * beta * tau * c * rho)

if __name__ == "__main__":

    mu = pp.particle.MuMinusDef.get()
    medium = pp.medium.Ice(1.0)  # With densitiy correction
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
            mu,
            medium,
            cuts,
            1.0,
            True,
        ]

    param_defs_ionization = [
            mu,
            medium,
            cuts,
            1.0,
        ]

    param_defs_photo = [
            mu,
            medium,
            cuts,
            1.0,
            pp.parametrization.photonuclear.ShadowButkevichMikhailov()
        ]

    params = [
        parametrization.pairproduction.KelnerKokoulinPetrukhin(
            *param_defs
        ),
        parametrization.bremsstrahlung.KelnerKokoulinPetrukhin(
            *param_defs
        ),
        parametrization.photonuclear.AbramowiczLevinLevyMaor97(
            *param_defs_photo
        ),
        parametrization.ionization.BetheBlochRossi(
            *param_defs_ionization)
    ]

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

    plt.loglog(energy, energy * sigma_decay(energy, medium.mass_density), linestyle='-', label='Decay', c='C5')    

    plt.xlabel(r'$E \,/\, \mathrm{MeV} $')
    plt.ylabel(r'$\left\langle\frac{\mathrm{d}E}{\mathrm{d}X}\right\rangle \,\left/\, \left( \rm{MeV} \cdot \rm{g}^{-1} \rm{cm}^2 \right) \right. $')
    plt.grid(conf.grid_conf)
    plt.legend(loc='best')

    plt.xlim(1e3, 1e12)

    plt.tight_layout()
    plt.savefig('build/dEdx.pdf',bbox_inches='tight')