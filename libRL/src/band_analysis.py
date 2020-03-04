import time, cmath
from os import path
from pandas import DataFrame
from libRL.src.tools import refactoring, quick_graphs, band_funcs
from pathos.multiprocessing import ProcessPool as Pool
from numpy import(
    array, zeros, float64, sqrt, errstate, pi
)

# some users having issues with pyximport compiling if they don't have
# a compiler installed to the OS path. So, try the install, if it doesn't work,
# fall back to a python implementation

# try:
    
#     import pyximport; pyximport.install(
#         language_level=3,
#         build_dir=path.join(path.abspath(path.dirname(__file__)),'tools')
#     )

#     from libRL.src.tools import cpfuncs
#     print(1)

# except:
#     from libRL.src.tools import pyfuncs as cpfuncs
#     print(0)


def band_analysis(
        data=None, f_set=None,
        d_set=None, m_set=None,
        thrs=-10, **kwargs
        ):
    """

The Band Analysis for ReFlection loss (BARF) function uses Permittivity
and Permeability data of materials so to determine the effective bandwidth
of Reflection Loss. The effective bandwidth is the span of frequencies
where the reflection loss is below some proficiency threshold (standard
threshold is -10 dB). Program is computationally taxing; thus, efforts
were made to push most of the computation to the C-level for faster run
times - the blueprints for such are included in the cpfuncs.pyx file which
is passed through pyximport()

    :*and yes, I love you 3000*:

ref: https://doi.org/10.1016/j.jmat.2018.12.005

ref: https://doi.org/10.1016/j.jmat.2019.07.003

::

    :param data:    (data)

Permittivity and Permeability data of Nx5 dimensions. Can be a string
equivalent to the directory and file name of either a .csv or .xlsx of Nx5
dimensions. Text above and below data array will be automatically avoided by
the program (most network analysis instruments report data which is compatible
with the required format)

::

    :param f_set:   (start, end, [step])

tuple for frequency values in GHz

- if given as tuple of len 3, results are interpolated

- if given as tuple of len 2, results are data-derived with the calculation
  bound by the given start and end frequencies from the tuple

- if given as int or float of len 1, results are interpolated over the entire
  data set with a step size of the given tuple value.

- if f_set is None (default), frequency is bound to input data.

::

    :param d_set:   (start, end, [step])

tuple for thickness values in mm.

- if d_set is of type list, then the thickness values calculated will only be
  of the values present in the list. (is weird, but whatever.)

::

    :param m_set:   (start, end, [step])

tuple of ints which define the bands to be calculated.

- if m_set is given as a list [], the explicitly listed band integers will be
  calculated.

::

    :param thrs:    -10

Threshold for evaluation. If RL values are below this threshold value, the
point is counted for the band. Default value is -10.

::

    :param kwargs:  override=
                    (None); 'chi zero',  'eps set'

provides response simulation functionality within libRL, common for discerning
which EM parameters are casual for reflection loss. 'chi zero' sets mu =
(1 - j*0). 'eps set' sets epsilon = (avg(e1)-j*0).

::

    :param kwargs:  interp=
                    ('cubic'); 'linear'

Method for interpolation. Set to linear if user wants to linear interp instead
of cubic spline.

::

    :param kwargs:  quick_graph=
                    (False); True, 'show', str()

saves a `.png` graphical image to a specified location. If set to True, the
quick_graph function saves the resulting graphical image to the location of the
input data as defined by the data input (assuming that the data was input via a
location string. If not, True throws an assertion error). The raw string of a
file location can also be passed as the str() argument, if utilized then the
function will save the graph at the specified location. Optionally, this kwarg
can be set to 'show' to simply display the generated image to either a 
matplotlib window on the desktop or within a jupyter notebook if the function
is run on google colab.

::

    :param kwargs:  as_dataframe=
                    (False); True

Formats results into a pandas dataframe with the index labels as the thickness
values, the column labels as the band numbers, and the dataframe as the
resulting effective bandwidths.

::

    :param kwargs:  quick_save=
                    (False); True, str()

Saves the results to an excel file for external reference. If set to True, the
quick_save function saves the resulting excel file to the location of the
input data as defined by the data input (assuming that the data was input via a
location string. If not, True throws an assertion error). The raw string of a
file location can also be passed as the str() argument, if utilized then the
function will save the excel file at the specified location.

::

    :return:        (d_set, band_results, m_set)

returns len(3) tuple of (d_set, band_results, m_set). the rows of the
band_results correspond with the d_set and the columns of the band_results
correspond with the m_set.

- if kwarg as_dataframe is True, returns the requested dataframe with the
  band values as column headers and the thickness values as row headers.
    """

    start_time = time.time()
    file_name = 'results'

    overview = {
        'function': 'band_analysis',
        'date/time': time.strftime('%D %H:%M:%S', time.localtime()),
        'f_set': str(f_set),
        'd_set': str(d_set),
        'm_set': str(m_set),
        'threshold': thrs,
        '**kwargs': str(kwargs)
    }

    # data is refactored into a Nx5 numpy array by the file_refactor
    # function from 'refactoring.py'
    if 'quick_save' in kwargs and kwargs['quick_save'] is True:
        kwargs['as_dataframe'] = True
        kwargs['quick_save'], file_name = refactoring.qref(data)
    
    if 'quick_graph' in kwargs and kwargs['quick_graph'] is True:
        kwargs['quick_graph'], file_name = refactoring.qref(data)

    # data is refactored into a Nx5 numpy array by the file_
    # refactor function in libRL
    data = refactoring.file_refactor(data, **kwargs)

    # refactor the data sets in accordance to
    # refactoring protocols in 'refactoring.py'
    f_set = refactoring.f_set_ref(f_set, data)
    d_set = refactoring.d_set_ref(d_set)
    m_set = refactoring.m_set_ref(m_set)

    # acquire the desired interpolating functions from 'refactoring.py'
    e1f, e2f, mu1f, mu2f = refactoring.interpolate(data, **kwargs)

    # ignore for when user inputs simulated data which includes
    # e, mu = (1-j*0) which will throw unnecessary error
    errstate(divide='ignore')

    # this time make the permittivity and permeability grid first
    # so we can push the core of the calculation down to the C-layer
    # via cython
    PnPGrid = array([
        f_set[:],
        e1f(f_set[:]),
        e2f(f_set[:]),
        mu1f(f_set[:]),
        mu2f(f_set[:])
        ]).transpose()

    # make another grid for the band edges
    mGrid = zeros((f_set.shape[0], m_set.shape[0] * 2), dtype=float64)

    # use the 1/2 integer function to populate it
    for i, m in enumerate(m_set):
        mGrid[:, 2 * i] = refactoring.dfind_half(
            e1f, e2f, mu1f, mu2f, f_set[:], m
            )

        mGrid[:, 2 * i + 1] = refactoring.dfind_half(
            e1f, e2f, mu1f, mu2f, f_set[:], m + 1
            )

    # push the calculation to cython for increased computation performance
    # see included file titled 'cpfuncs.pyx' for build blueprint

    band_results = band_funcs.band_analysis_cython(
        PnPGrid, mGrid, m_set, d_set, thrs
    )

    # takes data derived from computation and the file directory string and
    # generates a graphical image at the at location.
    if 'quick_graph' in kwargs and isinstance(
            kwargs['quick_graph'], str
            ) is True:
        quick_graphs.quick_graph_band_analysis(
            bands=band_results,
            d_vals = d_set,
            m_vals = m_set,
            location=kwargs['quick_graph']
        )

    if 'as_dataframe' in kwargs and kwargs['as_dataframe'] is True:
        res = DataFrame(band_results)
        res.columns = list(m_set)
        res.index = list(d_set)

        if 'quick_save' in kwargs and isinstance(
                kwargs['quick_save'], str
                ) is True:

            overview.update({'calculation time': time.time()-start_time})

            overview = DataFrame.from_dict(overview, orient='index')

            refactoring.save_to_excel(
                data=res,
                location=kwargs['quick_save'],
                file_name=file_name,
                parent='band_analysis',
                overview=overview
            )

    else:
        res = (d_set, band_results, m_set)

    return res
