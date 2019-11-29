tex_preamble = [
    r"\usepackage{amsmath}",
    r"\usepackage[utf8]{inputenc}",
    r"\usepackage[T1]{fontenc}",
    r"\usepackage{siunitx}",
]

font_size = 11
tick_size = 9
width = 5.45

params = {
    'backend': 'pdf',
    'font.family': 'serif',
    'font.size': font_size,
    'text.usetex': True,
    'text.latex.preamble': tex_preamble,
    'axes.labelsize': font_size,
    'legend.numpoints': 1,
    'legend.shadow': False,
    'legend.fontsize': font_size,
    'xtick.labelsize': tick_size,
    'ytick.labelsize': tick_size,
    'axes.unicode_minus': True
}

grid_conf = 'ls=":", lw=0.2, zorder=0'
