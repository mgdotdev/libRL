import time, cmath
from pandas import DataFrame
from libRL.src.tools import refactoring, quick_graphs
from numpy import(
    array, zeros, float64, sqrt, errstate, pi
)

# constants
j = cmath.sqrt(-1)              # definition of j
c = 299792458                   # speed of light
GHz = 10 ** 9                   # definition of GHz
Z0 = 376.730313461              # intrinsic impedance
e0 = 8.854188 * 10 ** (-12)     # permittivity of free space


def characterization(
        data=None, f_set=None,
        params="all", **kwargs
):
    """

The characterization function takes a set or list of keywords in the 'params'
variable and calculates the character values associated with the parameter. See
10.1016/j.jmat.2019.07.003 for further details and the function comments below
for a full list of :code:`param` arguments.

ref: https://doi.org/10.1016/j.jmat.2019.07.003

::

    :param data:   (data)

Permittivity and Permeability data of Nx5 dimensions.
Can be a string equivalent to the directory and file
name of either a .csv or .xlsx of Nx5 dimensions. Text
above and below data array will be automatically
avoided by the program (most network analysis instruments
report data which is compatible with the required format)

::

    :param f_set:   (start, end, [step])

tuple for frequency values in GHz
- or -
- if given as list of len 3, results are interpolated
- if given as list of len 2, results are data-derived
with the calculation bound by the given start and
end frequencies
- if f_set is None, frequency is bound to input data
- if f_set is of type list, the frequencies calculate
will be only the frequencies represented in the list.

::  
    
    :param params:  list()

A list i.e. [] of text arguments for the parameters the user wants calculated.

The available arguments are:

::

    [
    "tgde",          # dielectric loss tangent
    "tgdu",          # magnetic loss tangent
    "Qe",            # dielectric quality factor
    "Qu",            # magnetic quality factor
    "Qf",            # total quality factor
    "ReRefIndx",     # Refractive Index
    "ExtCoeff",      # Extinction Coeffecient
    "AtnuCnstNm",    # Attenuation Constant (in Np/m)
    "AtnuCnstdB",    # Attenuation Constant (in dB/m)
    "PhsCnst",       # Phase Constant
    "PhsVel",        # Phase Velocity
    "Res",           # Resistance
    "React",         # Reactance
    "Condt",         # Conductivity
    "Skd",           # Skin Depth
    "Eddy"           # Eddy Current Loss
    ]

- if 'all' (default) is passed, calculate everything.

::

    :param kwargs:  override=
                    (None); 'chi zero' 'eps set'

provides response simulation functionality within libRL, common for discerning
which EM parameters are casual for reflection loss. 'chi zero' sets mu =
(1 - j*0). 'eps set' sets epsilon = (avg(e1)-j*0).

::

    :param kwargs:  as_dataframe=
                    (False); True

returns the requested parameters as a pandas dataframe with column names as the
parameter keywords.

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

    :return:        (results)

NxY data set of the requested parameters as columns 1 to Y with the input
frequency values in column zero to N.

- if kwarg as_dataframe is True, returns a pandas dataframe with the requested
  parameters as column headers, and the frequency values as index headers.
    """

    start_time = time.time()
    file_name = 'results'

    overview = {
        'function': 'characterization',
        'date/time': time.strftime('%D %H:%M:%S', time.localtime()),
        'f_set': str(f_set),
        'params': str(params),
        '**kwargs': str(kwargs)
    }

    if 'quick_save' in kwargs and kwargs['quick_save'] is True:
        kwargs['quick_save'], file_name = refactoring.qref(data)
    # data is refactored into a Nx5 numpy array by the file_
    # refactor function in libRL
    data = refactoring.file_refactor(data, **kwargs)

    # acquire the desired interpolating functions from 'refactoring.py'
    e1f, e2f, mu1f, mu2f = refactoring.interpolate(data, **kwargs)

    # ignore for when user inputs simulated data which includes
    # e, mu = (1-j*0) which will throw unnecessary error
    errstate(divide='ignore')

    # if input is an explicit list, keep the list.
    # Otherwise, refactor as usual.
    if isinstance(f_set, list) is True:
        f_set = array(f_set, dtype=float64)
    else:
        f_set = refactoring.f_set_ref(f_set, data)

    # and you thought that first function was ugly
    chars = {
        "TGDE": lambda f: e2f(f) / e1f(f),

        "TGDU": lambda f: mu2f(f) / mu1f(f),

        "QE": lambda f: (e1f(f) / e2f(f)) ** -1,

        "QU": lambda f: (mu1f(f) / mu2f(f)) ** -1,

        "QF": lambda f: ((e1f(f) / e2f(f)) + (mu1f(f) / mu2f(f))) ** -1,

        "REREFINDX": lambda f: sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))
        ).real,

        "EXTCOEFF": lambda f: -1*sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))
        ).imag,

        "ATNUCNSTNM": lambda f: ((2 * pi * f * GHz) * sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))) * (c ** -1)
                                 ).real,

        "ATNUCNSTDB": lambda f: (2 * pi * f * GHz * sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))) * (c ** -1)
                                 ).real * 8.86588,

        "PHSCNST": lambda f: -1*((2 * pi * f * GHz) * sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))) * (c ** -1)
                              ).imag,

        "PHSVEL": lambda f: (2 * pi * f * GHz) / chars["PHSCNST"](f),

        "RES": lambda f: (Z0 * sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))
                          ).real,

        "REACT": lambda f: -1*(Z0 * sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))
                            ).imag,

        "CONDT": lambda f: (2 * pi * f * GHz) * (e0 * e2f(f)),

        "SKD": lambda f: 1000 / ((2 * pi * f * GHz * sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))) * (c ** -1)
                                 ).real,

        "EDDY": lambda f: mu2f(f) / (mu1f(f) ** 2 * f),

    }

    # give user option to just calculate everything without forcing them
    # to type it all. also, don't be case sensitive.
    if params == 'all':
        params = [
            "tgde", "tgdu", "Qe", "Qu", "Qf",
            "ReRefIndx", "ExtCoeff",
            "AtnuCnstNm", "AtnuCnstdB",
            "PhsCnst", "PhsVel", "Res",
            "React", "Condt", "Skd", "Eddy"
        ]

    # results matrix, first column reserved for frequency
    # if output to numpy array
    Matrix = zeros((f_set.shape[0], len(params) + 1), dtype=float64)
    names = ["frequency"]
    Matrix[:, 0] = f_set

    # call the lambda functions from the char dictionary
    for counter, param in enumerate(params, start=1):
        Matrix[:, counter] = chars[param.upper()](f_set[:])
        names.append(param)

    if 'as_dataframe' in kwargs and kwargs['as_dataframe'] is True:
        # whoops, didn't need that first column after all!
        panda_matrix = DataFrame(Matrix[:, 1:])
        panda_matrix.columns = list(names[1:])
        panda_matrix.index = list(f_set)

        if 'quick_save' in kwargs and isinstance(
                kwargs['quick_save'], str
                ) is True:

            overview.update({'calculation time': time.time()-start_time})

            overview = DataFrame.from_dict(overview, orient='index')

            refactoring.save_to_excel(
                data=panda_matrix,
                location=kwargs['quick_save'],
                file_name=file_name,
                parent='characterization',
                overview=overview
            )

        return panda_matrix

    return Matrix, names

