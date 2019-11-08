# Copyright (C) 2019 Michael Green
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, under version 3.0 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

"""
libRL
=====

libRL is a library of functions used for characterizing Microwave Absorption.

functions include:

    libRL.reflection_loss(
    data=None, f_set=None, d_set=None, **kwargs
    )
        - resultants of Reflection Loss over (f, d) gridspace. Yields the
        resulting Reflection Loss results for a given set of permittivity
        and permeability data.
        see libRL.reflection_loss? for complete documentation.

    libRL.characterization(
    data=None, f_set=None, params="All", **kwargs
    )
        - characterization of Reflection Loss. Yields the calculated results
        of common formulations within the Radar Absorbing Materials field.
        see libRL.characterization? for complete documentation.

    libRL.band_analysis(
    data=None, f_set=None, d_set=None, m_set=None, threshold=-10, **kwargs
    )
        - Band Analysis of Reflection Loss. Uses given set of permittivity and
        permeability data in conjuncture with a requested band set to determine
        the set of frequencies with are below a threshold.
        see libRL.band_analysis? for complete documentation.

Developed at the University of Missouri-Kansas City under NSF grant DMR-1609061
by Michael Green and Xiaobo Chen.

full details can be found at https://1mikegrn.github.io/DocSite/libRL/
----------------------------------------------
"""

import cmath
from os import path

import pyximport; pyximport.install(
    language_level=3, build_dir=path.abspath(path.dirname(__file__))
)

from libRL import(
    refactoring,
    quick_graphs,
    cpfuncs
)

from numpy import (
    arange, zeros, abs, array,
    float64, errstate, pi, sqrt
)

from pandas import DataFrame
from pathos.multiprocessing import ProcessPool as Pool


def reflection_loss(data=None, f_set=None, d_set=None, **kwargs):
    """

    the reflection_loss (RL) function calculates the RL based on the mapping
    passed through as the grid variable, done either through multiprocessing
    or through the python built-in map() function. The RL function always
    uses the interpolation function, even though as the function passes
    through the points associated with the input data, solving for the
    function at the associated frequencies yields the data point. This
    is simply for simplicity.

    ref: https://doi.org/10.1016/j.jmat.2019.07.003

    :param data:   (data)

                    Permittivity and Permeability data of Nx5 dimensions.
                    Can be a string equivalent to the directory and file
                    name of either a .csv or .xlsx of Nx5 dimensions. Text
                    above and below data array will be automatically
                    avoided by the program (most network analysis instruments
                    report data which is compatible with the required format)

    :param f_set:   (start, end, [step])

                    tuple for frequency values in GHz
                    - if given as list of len 3, results are interpolated
                    - if given as list of len 2, results are data-derived
                    with the calculation bound by the given start and end
                    frequencies
                    - if f_set is None, frequency is bound to input data

    :param d_set:   (start, end, step)

                    tuple for thickness values in mm.
                    - or -
                    if d_set is of type list, then the thickness values
                    calculated will only be of the values present in the
                    list.
                    ------------------------------

    :param kwargs:  :interp=:
                    ('cubic'); 'linear'

                    Method for interpolation. Set to linear if user wants to
                    linear interp instead of cubic spline. Default action
                    uses cubic spline.
                    ------------------------------

                    :override=:
                    (None); 'chi zero'; 'eps set'

                    provides response simulation functionality within libRL,
                    common for discerning which EM parameters are casual for
                    reflection loss. 'chi zero' sets mu = (1 - j*0). 'eps set'
                    sets epsilon = (avg(e1)-j*0).
                    ------------------------------

                    :multiprocessing=:
                    (False); True; 0; 1; 2; ...

                    Method for activating multiprocessing functionality for
                    faster run times. This **kwarg takes integers and booleans.
                    Set variable to True or 0 to use all available nodes. Pass
                    an integer value to use (int) nodes. Will properly handle
                    'False' as an input though it's equivalent to not even
                    designating the particular **kwarg.

                    NOTE: if you use the multiprocessing functionality herein
                    while on a Windows computer you ***MUST MUST MUST MUST***
                    provide main module protection via the
                    if __name__ == "__main__":
                    conditional so to negate infinite spawns.
                    ------------------------------

                    :quick_graph=:
                    (False); True, str()

                    saves a *.png graphical image to a specified location. If
                    set to True, the quick_graph function saves the resulting
                    graphical image to the location of the input data as
                    defined by the data input (assuming that the data was
                    input via a location string. If not, True throws an
                    assertion error). The raw string of a file location can
                    also be passed as the str() argument, if utilized then the
                    function will save the graph at the specified location.
                    ------------------------------

                    :as_dataframe=:
                    (False); True

                    returns data in a pandas dataframe. This is particularly
                    useful if multicolumn is also set to true.
                    ------------------------------

                    :multicolumn=:
                    (False); True

                    outputs data in multicolumn form with  a numpy array of
                    [RL, f, d] iterated over each of the three columns.
                    - or -
                    if as_dataframe is used, then return value will be a pandas
                    dataframe with columns of name d and indexes of name f.
                    ------------------------------


    :return:        returns Nx3 data set of [RL, f, d] by default
                    - or -
                    if multicolumn=True, an NxM dataframe with N rows for the
                    input frequency values and M columns for the input
                    thickness values, with pandas dataframe headers/indexes
                    of value f/d respectively.


    ----------------------------------------------
    """
    # data is refactored into a Nx5 numpy array by the file_refactor
    # function from 'refactoring.py'

    if 'quick_graph' in kwargs and kwargs['quick_graph'] is True:
        kwargs['quick_graph'] = refactoring.qgref(data)

    data = refactoring.file_refactor(data)

    # acquire the desired interpolating functions from 'refactoring.py'
    e1f, e2f, mu1f, mu2f = refactoring.interpolate(data, **kwargs)

    # refactor the data sets in accordance to refactoring protocols
    # in 'refactoring.py'
    f_set = refactoring.f_set_ref(f_set, data)
    d_set = refactoring.d_set_ref(d_set)

    # construct a data grid for mapping from refactored data sets
    # d *must* be first as list comprehension cycles through f_set
    # for each d value, and this is deterministic of the structure
    # of the resultant.
    grid = array([(m, n)
                  for n in d_set
                  for m in f_set
                  ], dtype=float64)

    # just a constant
    j = cmath.sqrt(-1)

    def gamma(grid):
        f = grid[0]
        d = grid[1]

        # I know, it's super ugly.
        y = (20 * cmath.log10((abs(((1 * (cmath.sqrt((mu1f(f) - j * mu2f(f)) /
            (e1f(f) - cmath.sqrt(-1) * e2f(f)))) * (cmath.tanh(j *
            (2 * cmath.pi * (f * 10**9) * (d * 0.001) / 299792458) *
            cmath.sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j *
            e2f(f)))))) - 1) / ((1 * (cmath.sqrt((mu1f(f) - j * mu2f(f)) /
            (e1f(f) - j * e2f(f)))) * (cmath.tanh(j * (2 *
            cmath.pi * (f * 10**9) * (d * 0.001) / 299792458) * cmath.sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j *
            e2f(f)))))) + 1)))))

        # return inputted data for documentation and return
        # the real portion of y to drop complex portion
        # of form j*0
        return y.real, f, d

    # if multiprocessing is given as True or as
    # a zero integer, use all available nodes
    # if multiprocessing is given and is a non-zero
    # integer, use int value for number of nodes
    # if multiprocessing is given as False (for some
    # reason?), or anything else, ignore it.
    # returns res of Zx3 data where Z is the product
    # of len(f_set) and len(d_set)
    if 'multiprocessing' in kwargs and isinstance(
            kwargs['multiprocessing'], int) is True:

        if kwargs['multiprocessing'] is True or kwargs['multiprocessing'] == 0:
            res = array(Pool().map(gamma, grid))
        elif kwargs['multiprocessing'] > 0:
            res = array(Pool(nodes=kwargs['multiprocessing']).map(gamma, grid))
        else:
            res = array(list(map(gamma, grid)))
    else:
        res = array(list(map(gamma, grid)))

    # takes data derived from computation and the file directory string and
    # generates a graphical image at the at location.
    if 'quick_graph' in kwargs and isinstance(
            kwargs['quick_graph'], str
            ) is True:

        quick_graphs.quick_graph_reflection_loss(
            results=res, location=kwargs['quick_graph']
            )

    # formatting option, sometimes professors
    # like 3 columns for each thickness value
    if 'multicolumn' in kwargs and kwargs['multicolumn'] is True:

        # get frequency values from grid so
        # to normalize the procedure due to the
        # various frequency input methods
        gridInt = int(grid.shape[0] / d_set.shape[0])

        # zero-array of NxM where N is the frequency
        # values and M is 3 times the
        # number of thickness values
        MCres = zeros(
            (gridInt, d_set.shape[0] * 3)
        )

        # map the Zx3 result array to the NxM array
        for i in arange(int(MCres.shape[1] / 3)):
            MCres[:, 3 * i:3 * i + 3] = res[
                                        i * gridInt:(i + 1) * gridInt, 0:3
                                        ]

        # stick the MultiColumn Array in the place of the results array
        res = MCres

    if 'as_dataframe' in kwargs and kwargs['as_dataframe'] is True:

        if 'multicolumn' in kwargs and kwargs['multicolumn'] is True:
            res = DataFrame(res[:, ::3])
            res.columns = list(d_set)
            res.index = list(f_set)

        else:
            res = DataFrame(res)
            res.columns = ['RL', 'f', 'd']

    return res


def characterization(data=None, f_set=None, params="all", **kwargs):
    """

    the characterization function takes
    a set or list of keywords in the 'params' variable and calculates
    the character values associated with the parameter. See
    10.1016/j.jmat.2019.07.003 for further details and the
    function comments below for a full list of keywords.

    ref: https://doi.org/10.1016/j.jmat.2019.07.003

    :param data:   (data)

                    Permittivity and Permeability data of Nx5 dimensions.
                    Can be a string equivalent to the directory and file
                    name of either a .csv or .xlsx of Nx5 dimensions. Text
                    above and below data array will be automatically
                    avoided by the program (most network analysis instruments
                    report data which is compatible with the required format)

    :param f_set:   (start, end, [step])

                    tuple for frequency values in GHz
                    - if given as list of len 3, results are interpolated
                    - if given as list of len 2, results are data-derived
                    with the calculation bound by the given start and
                    end frequencies
                    - if f_set is None, frequency is bound to input data
                    - if f_set is of type list, the frequencies calculate
                    will be only the frequencies represented in the list.

    :param params:  A list i.e. [] of text arguments for the parameters
                    the user wants calculated.

                    The available arguments are:
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

                    ------------------------------
    :param kwargs:  :override=:
                    (None); 'chi zero'; 'edp zero'; 'eps set'

                    provides response simulation functionality within libRL,
                    common for discerning which EM parameters are casual for
                    reflection loss. 'chi zero' sets mu = (1 - j*0). 'eps set'
                    sets epsilon = (avg(e1)-j*0).
                    ------------------------------

                    :as_dataframe=:
                    (False); True

                    returns the requested parameters as a pandas dataframe with
                    column names as the parameter keywords.
                    ------------------------------


    :return:        NxY data set of the requested
                    parameters as columns 1 to Y with the input
                    frequency values in column zero to N.
                    - or -
                    returns a pandas dataframe with the requested parameters
                    as column headers, and the frequency
                    values as index headers.

    ----------------------------------------------
    """

    # data is refactored into a Nx5 numpy array by the file_
    # refactor function in libRL
    data = refactoring.file_refactor(data)

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

    # constants
    j = cmath.sqrt(-1)              # definition of j
    c = 299792458                   # speed of light
    GHz = 10 ** 9                   # definition of GHz
    Z0 = 376.730313461              # intrinsic impedance
    e0 = 8.854188 * 10 ** (-12)     # permittivity of free space

    # and you thought that first function was ugly
    chars = {
        "TGDE": lambda f: e1f(f) / e2f(f),

        "TGDU": lambda f: mu1f(f) / mu2f(f),

        "QE": lambda f: (e1f(f) / e2f(f)) ** -1,

        "QU": lambda f: (mu1f(f) / mu2f(f)) ** -1,

        "QF": lambda f: ((e1f(f) / e2f(f)) + (mu1f(f) / mu2f(f))) ** -1,

        "REREFINDX": lambda f: sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))
        ).real,

        "EXTCOEFF": lambda f: sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))
        ).imag,

        "ATNUCNSTNM": lambda f: ((2 * pi * f * GHz) * sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))) * (c ** -1)
                                 ).real,

        "ATNUCNSTDB": lambda f: (2 * pi * f * GHz * sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))) * (c ** -1)
                                 ).real * 8.86588,

        "PHSCNST": lambda f: ((2 * pi * f * GHz) * sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))) * (c ** -1)
                              ).imag,

        "PHSVEL": lambda f: ((2 * pi * f * GHz) / (
            ((2 * pi * f * GHz) * sqrt(
                (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))
            ) * (c ** -1))
            ).imag),

        "RES": lambda f: (Z0 * sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))
                          ).real,

        "REACT": lambda f: (Z0 * sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))
                            ).imag,

        "CONDT": lambda f: (2 * pi * f * GHz) * (e0 * e2f(f)),

        "SKD": lambda f: 1000 / ((2 * pi * f * GHz * sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))) * (c ** -1)
                                 ).real,

        "EDDY": lambda f: mu2f(f) / (mu1f(f) ** 2 * f)
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
        return panda_matrix

    return Matrix, names


def band_analysis(
        data=None, f_set=None,
        d_set=None, m_set=None,
        thrs=-10, **kwargs
        ):
    """

    the Band Analysis for ReFlection loss (BARF) function uses Permittivity
    and Permeability data of materials so to determine the effective bandwidth
    of Reflection Loss. The effective bandwidth is the span of frequencies
    where the reflection loss is below some proficiency threshold (standard
    threshold is -10 dB). Program is computationally taxing; thus, efforts
    were made to push most of the computation to the C-level for faster run
    times - the blueprints for such are included in the cpfuncs.pyx file which
    is passed through pyximport()

    [and yes, I love you 3000]

    ref: https://doi.org/10.1016/j.jmat.2018.12.005
         https://doi.org/10.1016/j.jmat.2019.07.003

    :param data:   (data)

                    Permittivity and Permeability data of Nx5 dimensions.
                    Can be a string equivalent to the directory and file
                    name of either a .csv or .xlsx of Nx5 dimensions. Text
                    above and below data array will be automatically
                    avoided by the program (most network analysis instruments
                    report data which is compatible with the required format)

    :param f_set:   (start, end, [step])

                    tuple for frequency values in GHz
                    - or -
                    - if given as tuple of len 3, results are interpolated
                    - if given as tuple of len 2, results are data-derived
                    with the calculation bound by the given start and end
                    frequencies from the tuple
                    - is given as int or float of len 1, results are
                    interpolated over the entire data set with a step size
                    of the given tuple value.
                    - if f_set is None (default), frequency is bound to
                    input data.

    :param d_set:   (start, end, [step])

                    tuple for thickness values in mm.
                    - or -
                    - if d_set is of type list, then the thickness values
                    calculated will only be of the values present in the
                    list. (is weird, but whatever.)

    :param m_set:   (start, end, [step])

                    tuple of ints which define the bands to be calculated.
                    - or -
                    - if m_set is given as a list [], the explicitly listed
                    band integers will be calculated.

    :param thrs:    -10

                    Threshold for evaluation. If RL values are below this
                    threshold value, the point is counted for the band.
                    Default value is -10.

                    ------------------------------
    :param kwargs:  :override=:
                    (None); 'chi zero'; 'edp zero'; 'eps set'

                    provides response simulation functionality within libRL,
                    common for discerning which EM parameters are casual for
                    reflection loss. 'chi zero' sets mu = (1 - j*0). 'eps set'
                    sets epsilon = (avg(e1)-j*0).
                    ------------------------------

                    :interp=:
                    'linear'; 'cubic'

                    Method for interpolation. Set to linear if user wants to
                    linear interp instead of cubic spline.
                    ------------------------------

                    :quick_graph=:
                    (False); True, str()

                    saves a *.png graphical image to a specified location. If
                    set to True, the quick_graph function saves the resulting
                    graphical image to the location of the input data as
                    defined by the data input (assuming that the data was
                    input via a location string. If not, True throws an
                    assertion error). The raw string of a file location can
                    also be passed as the str() argument, if utilized then the
                    function will save the graph at the specified location.
                    ------------------------------

                    :as_dataframe=:
                    (False); True

                    Formats results into a pandas
                    dataframe with the index labels as the thickness
                    values, the column labels as the band numbers, and
                    the dataframe as the resulting effective bandwidths.
                    ------------------------------


    :return:        returns len(3) tuple with [d_set, band_results, m_set].
                    the rows of the band_results correspond with the d_set and
                    the columns of the band_results correspond with the m_set.
                    - or -
                    returns the requested dataframe with the band values as
                    column headers and the thickness values as row headers.

    ----------------------------------------------
    """

    # data is refactored into a Nx5 numpy array by the file_refactor
    # function from 'refactoring.py'
    if 'quick_graph' in kwargs and kwargs['quick_graph'] is True:
        kwargs['quick_graph'] = refactoring.qgref(data)

    # data is refactored into a Nx5 numpy array by the file_
    # refactor function in libRL
    data = refactoring.file_refactor(data)

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
    PnPGrid = zeros((f_set.shape[0], 5), dtype=float64)

    # populate grid accordingly
    PnPGrid[:, 0] = f_set[:]
    PnPGrid[:, 1] = e1f(f_set[:])
    PnPGrid[:, 2] = e2f(f_set[:])
    PnPGrid[:, 3] = mu1f(f_set[:])
    PnPGrid[:, 4] = mu2f(f_set[:])

    # to find the 1/2th integer wavelength, NOT quarter.
    def dfind(f, m):
        y = ((299792458 / (f * 10**9)) * (1.0 / (
            sqrt((mu1f(f) - cmath.sqrt(-1) * mu2f(f)) *
            (e1f(f) - cmath.sqrt(-1) * e2f(f))).real)) * (
                ((2.0 * m) - 2.0) / 4.0)) * 1000
        return y

    # make another grid for the band edges
    mGrid = zeros((f_set.shape[0], m_set.shape[0] * 2), dtype=float64)

    # use the 1/2 integer function to populate it
    for i, m in enumerate(m_set):
        mGrid[:, 2 * i] = dfind(f_set[:], m)
        mGrid[:, 2 * i + 1] = dfind(f_set[:], m + 1)

    # push the calculation to cython for increased computation performance
    # see included file titled 'cpfuncs.pyx' for build blueprint

    band_results = cpfuncs.band_analysis_cython(
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

    else:
        res = (d_set, band_results, m_set)

    return res
