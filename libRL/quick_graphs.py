"""

quick and dirty default graphing protocols for RL and BARF functions.

NOTE:
these functions are *not* going to be meticulously supported. They only exist
to make *my* personal life easier. They'll be updated as necessary for my
personal use without notice. Granted, You're welcome to use them for
your own purposes for as long as they serve them to an acceptable degree,
but if an axis doesn't have the spacing you want or the scale/range doesn't
fit your specific desires, don't expect an update to tailor the library to your
liking - at that point, you're better off just taking the data output and
using matplotlib to generate your own images.

You've been warned... >:D

P.S.

ATM, quick_graphs doesn't support libRL.CARL because of the sheer level
of customization inherent to the function. I may add a feature at a later date
to generate sets of graphs in a directory for each parameter, but it's not too
high on my list of priorities. Jus' sayin'.

"""


from matplotlib import colors
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axis3d as axis3d
from matplotlib import rcParams

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


def qgRL(results, location):
    """

    quick and dirty default graphing protocols for reflection loss.

    :param results:     libRL.RL results of shape Nx3

    :param location:    string directory location of where to save the
                        resulting graphical image.

    :return:            None.
    """

    try:
        fig = plt.figure(dpi=200)
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

        #ax.set_xlim(left=0)
        #ax.set_ylim(bottom=0)
        cbar1.ax.set_ylabel(
            'Reflection Loss / dB',
            fontsize=12, labelpad=15
        )

        cbar1.ax.invert_yaxis()

    except:
        ErrorMsg = 'Error partitioning graphical image'
        raise RuntimeError(ErrorMsg)

    try:
        fig.savefig(location + r'\quick_graph RL.png')

    except:
        ErrorMsg = 'Error partitioning graphical image'
        raise RuntimeError(ErrorMsg)


def qgBARF(bands, d_vals, m_vals, location):
    """

    quick and dirty default graphing protocols for the band analysis.

    :param bands:       band data passed through from the band_results
                        derived from the cython computation.

    :param d_vals:      d_set from libRL.CARL()

    :param m_vals:      m_set from libRL.CARL()

    :param location:    string directory location of where to save the
                        resulting graphical image.


    :return:            None.
    """

    try:
        fig = plt.figure(dpi=200)
        ax = fig.add_subplot(111)

        ax.tick_params(direction='in', pad = 3)
        ax.set_xlabel('Thickness / $mm$', fontsize = 12)
        ax.set_ylabel('Frequency / GHz', fontsize = 12)

        cmap = plt.cm.get_cmap(plt.cm.rainbow, 1)
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

    except:
        ErrorMsg = 'Error partitioning graphical image'
        raise RuntimeError(ErrorMsg)

    try:
        fig.savefig(location + r'\quick_graph BARF.png')

    except:
        ErrorMsg = 'Error partitioning graphical image'
        raise RuntimeError(ErrorMsg)



