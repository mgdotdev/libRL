"""
:code:`quick_graphs.py`
=======================

quick and dirty default graphing protocols for reflection_loss and
band_analysis functions.

NOTE:
these functions are designed to be *technically* functional.
Users are welcome to use them for as long as they serve them to an acceptable
degree, but please note, bug reports to the contents herein must be of a
'technical' nature, and not artistic. If an axis doesn't have the spacing you
want or the scale/range doesn't fit your specific desires, don't expect an
update to tailor the library to your personal, artistic liking - at that point,
you're better off just taking the data output and using matplotlib to generate
your own images.

P.S.

ATM, quick_graphs doesn't support libRL.characterization because of the sheer 
level of customization inherent to the function. I may add a feature at a 
later date to generate sets of graphs in a directory for each parameter, 
but to be frank, it's not too high on my list of priorities.

"""

from os import path
from matplotlib import colors, pyplot as plt, rcParams
import mpl_toolkits.mplot3d.axis3d as axis3d

rcParams['font.family'] = 'serif'
rcParams['font.sans-serif'] = ['Bookman']
rcParams['font.size'] = 12
rcParams['figure.figsize'] = 4.5, 4
rcParams['axes.labelpad'] = 10
rcParams['mathtext.fontset'] = 'stix'

lw = 1.3
tck = 4
rcParams['axes.linewidth'] = lw
rcParams['ytick.major.width'], rcParams['xtick.major.width'] = lw, lw
rcParams['ytick.major.size'], rcParams['xtick.major.size'] = tck, tck


def quick_graph_reflection_loss(results, location):
    """

    quick and dirty default graphing protocols for the band analysis.

::

    :param bands:       (data)

band data passed through from the band_results derived from the cython
computation.

::

    :param d_vals:      d_set

d_set from libRL.band_analysis()

::

    :param m_vals:      m_set

m_set from libRL.band_analysis()

::

    :param location:    (file directory)

string directory location of where to save the resulting graphical image.

::

    :return:            (None)
    """

    if location == 'show':
        dpi=50
    else:
        dpi=200

    fig = plt.figure(dpi=dpi)
    ax = fig.add_axes([0.1,0.15, 0.7, 0.75], projection='3d')
    cbaxes = fig.add_axes([0.80, 0.352, 0.02, 0.378])

    ax.set_proj_type('ortho')
    ax.zaxis._axinfo['juggled'] = (1, 2, 0)

    ax.dist = 13
    ax.view_init(-153, -130)

    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

    ax.tick_params(labelsize=10, pad=0)
    ax.tick_params(axis='z', pad=3)
    ax.set_xlabel('Frequency / GHz', fontsize=12)
    ax.set_ylabel('Thickness / mm', fontsize=12)

    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.yaxis.set_major_locator(plt.MaxNLocator(5))

    ax.set_zticklabels([0, -10, -20, -30, -40, -50, -60], va='center')
    ax.set_zticks([0, -10, -20, -30, -40, -50, -60])

    ax.set_zlim(-60, 0)

    ccmap = colors.ListedColormap(
        [(0, 0, 0), (0, 0, 255 / 255),
         (0, 255 / 255, 255 / 255), (0, 255 / 255, 0),
         (255 / 255, 255 / 255, 0), (255 / 255, 0, 0)]
    )

    plot1 = ax.plot_trisurf(
        results[:, 1],
        results[:, 2],
        results[:, 0],
        cmap=ccmap,
        linewidth=1,
        alpha=0.95,
        vmin=-60,
        vmax=0
    )

    cbar1 = plt.colorbar(plot1, cax=cbaxes)
    cbar1.ax.tick_params(labelsize=10)

    cbar1.set_ticks(
        [0, -10, -20, -30,
         -40, -50, -60]
    )

    cbar1.ax.set_ylabel(
        'Reflection Loss / dB',
        fontsize=12, labelpad=15
    )

    cbar1.ax.invert_yaxis()

    if location == 'show':
        plt.show()

    else:
        fig.savefig(path.join(location, 'quick_graph RL.png'))

    plt.close()


def quick_graph_band_analysis(bands, d_vals, m_vals, location):
    """

    quick and dirty default graphing protocols for the band analysis.

::

    :param bands:       (data)

band data passed through from the band_results derived from the cython
computation.

::

    :param d_vals:      d_set

d_set from libRL.band_analysis()

::

    :param m_vals:      m_set

m_set from libRL.band_analysis()

::

    :param location:    (file directory)

string directory location of where to save the resulting graphical image.

::

    :return:            (None)
    """

    if location == 'show':
        dpi=50
    else:
        dpi=200

    fig = plt.figure(dpi=dpi)
    ax = fig.add_subplot(111)

    ax.tick_params(direction='in', pad = 3)
    ax.set_xlabel('Thickness / $mm$', fontsize = 12)
    ax.set_ylabel('Frequency / GHz', fontsize = 12)
    
    cmap = plt.cm.get_cmap('rainbow')

    leg_list=[]
    for count, band in enumerate(m_vals):
        ax.plot(
            d_vals,
            bands[:,count],
            c=cmap(count/m_vals.shape[0]),
            )
        leg_list.append('band '+str(band))

    ax.legend(leg_list)

    plt.tight_layout()

    if location == 'show':
        plt.show()

    else:
        fig.savefig(path.join(location, 'quick_graph band_analysis.png'))

    plt.close()