"""
refactoring.py provides the data refactoring protocols for the
libRL module.

functions include:

    refactoring.file_refactor(Mcalc=None):
        - resultant is the processed Nx5 data array of
        [frequency, e1, e2, mu1, mu2]. Gives the user
        options for inputting data, from a file location
        string to the data array already formatted.

    refactoring.interpolate(Mcalc, **kwargs):
        - resultant is the four scipy-derived interpolating
        functions for e1, e2, mu1, and mu2. Default is
        cubic spline interpolation (piece-wise 3rd order
        polynomials) but user has the option to override
        with linear interpolation.

    refactoring.f_set_ref(f_set, Mcalc):
        - resultant is the Nx1 array of frequency values
        determined from user inputs.
        see refactoring.f_set_ref? for complete documentation

    refactoring.d_set_ref(f_set):
        - resultant is the Nx1 array of thickness values
        determined from user inputs.
        see refactoring.d_set_ref? for complete documentation

    refactoring.m_set_ref(m_set):
        - resultant is the Nx1 array of band values
        determined from user inputs.
        see refactoring.m_set_ref? for complete documentation

---------------------------------------------
"""

from numpy import (
    arange, delete, abs, array,
    argmin, float64, average
)

from pandas import (
    read_csv, read_excel
)

from scipy.interpolate import interp1d

from os.path import splitext, split


def file_refactor(Mcalc=None, **kwargs):
    """

    refactors the given user data into actionable permittivity and
    permeability data.

    :param Mcalc:   (data)

                    Permittivity and Permeability data of Nx5 dimensions.
                    Can be a string equivalent to the directory and file
                    name of either a .csv or .xlsx of Nx5 dimensions. Text
                    above and below data array will be automatically
                    avoided by the program (most network analysis instruments
                    report data which is compatible with the required format)

    :param kwargs:  :override=:
                    (None); 'chi zero'; 'eps set'

                    provides response simulation functionality within libRL,
                    common for discerning which EM parameters are casual for
                    reflection loss. 'chi zero' sets mu = (1 - j*0). 'eps set'
                    sets epsilon = (avg(e1)-j*0).
                    ------------------------------


    :return:        refactored Mcalc data of Nx5 dimensionality in numpy array

    ---------------------------------------------
    """
    if Mcalc is None:
        ErrorMsg = 'Data must be passed as an array which is mappable ' \
                   'to an Nx5 numpy array with columns ' \
                   '[freq, e1, e2, mu1, mu2]'
        raise RuntimeError(ErrorMsg)

    # allows for file location to be passed as the data variable.
    if isinstance(Mcalc, str) is True:

        if splitext(Mcalc)[1] == '.csv':
            Mcalc = read_csv(Mcalc, sep=',').to_numpy()

            # check each position in numpy array
            # if it can be a number, make it a number
            for row in range(Mcalc.shape[0]):
                for col in range(Mcalc.shape[1]):
                    try:
                        Mcalc[row, col] = float64(Mcalc[row, col])
                    except:
                        pass

        elif splitext(Mcalc)[1] == '.xlsx':
            Mcalc = read_excel(Mcalc).to_numpy()

        else:
            ErrorMsg = 'Error partitioning input data from string'
            raise RuntimeError(ErrorMsg)

    # finds all rows in numpy array which aren't
    # a part of the Nx5 data array expected.
    #
    # NOTE:
    # if the file contains more/less than
    # 5 columns this fails as the 6th row is
    # always filled with NaN. That being said,
    # most instruments output a Nx5 data file.

    x = []
    for row in arange(Mcalc.shape[0]):
        for col in arange(Mcalc.shape[1]):
            if isinstance(
                    Mcalc[row, col], (int, float)
                    ) is False or Mcalc[row, col] != Mcalc[row, col]:
                x.append(row)
                break

    # removes non-data rows from input array to yield the data array
    Mcalc = delete(Mcalc, x, axis=0)

    if 'override' in kwargs and kwargs['override'] == 'chi zero':
        Mcalc[:, 3:5] = array([1, 0])

    elif 'override' in kwargs and kwargs['override'] == 'eps set':
        avg = average(Mcalc[:,1])
        Mcalc[:, 1:3] = array([avg, 0])

    return Mcalc


def qgref(Mcalc):
    assert isinstance(Mcalc, str) is True, \
        'To use the True assertion for this **kwarg the user must ' \
        'pass a valid data file string as the data argument. The user may ' \
        'also pass a directory location instead.'

    if splitext(split(Mcalc)[1])[1] == '':
        ErrorMsg = "error parsing out data file."
        raise SyntaxError(ErrorMsg)

    else:
        output_location = split(Mcalc)[0]

    return output_location


def interpolate(Mcalc, **kwargs):
    """

    uses SciPy's interpolation module to generate interpolating functions
    over the input data. Interpolate also handles the override **kwargs
    for response simulation

    :param Mcalc:   Permittivity data of Nx5 form where N rows are
                    [frequency, e1, e2, mu1, mu2]

                    ------------------------------
    :param kwargs:  :interp=:
                    ('cubic'); 'linear'

                    Method for interpolation. Set to linear if user wants to
                    linear interp instead of cubic spline.
                    ------------------------------


    :return:        e1f, e2f, mu1f, mu2f

                    returns four functions for Real Permittivity,
                    Complex Permittivity, Real Permeability, and
                    Complex Permeability respectively

    ----------------------------------------------
    """

    params = ['e1f', 'e2f', 'mu1f', 'mu2f']

    if 'interp' in kwargs and kwargs['interp'] is 'linear':

        funcs = {param: interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, count], dtype=float64),
            kind='linear', fill_value='extrapolate'
        ) for count, param in enumerate(params, start=1)
        }

    else:
        funcs = {param: interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, count], dtype=float64),
            kind='cubic', fill_value='extrapolate'
        ) for count, param in enumerate(params, start=1)
        }

    return funcs['e1f'], funcs['e2f'], funcs['mu1f'], funcs['mu2f']


def f_set_ref(f_set, Mcalc):
    """

    refactors the input f_set to the corresponding
    Nx1 numpy array.

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

    :param Mcalc:   (data)

                    uses Mcalc as reference as frequencies are
                    experimentally determined.


    :return:        refactored f_set of Nx1 numpy array

    ----------------------------------------------
    """
    if f_set is None:
        f_set = array([
            m for m in Mcalc[:, 0]
        ], dtype=float64)

    elif f_set is float or int and isinstance(f_set, tuple) is False:
        f_set = array([
            m for m in arange(Mcalc[0, 0], Mcalc[-1, 0] + f_set, f_set)
        ], dtype=float64)

    elif len(f_set) is 2:

        if f_set[0] > f_set[1]:
            ErrorMsg = "f_set must be of order (start, stop) where 'start' " \
                       "is a value smaller than 'stop'"
            raise SyntaxError(ErrorMsg)

        f_set = array([
            m for m in Mcalc[
                       argmin(abs(f_set[0] - Mcalc[:, 0])):
                       argmin(abs(f_set[1] - Mcalc[:, 0])) + 1,
                       0]
        ], dtype=float64)

    elif len(f_set) is 3:

        if f_set[0] > f_set[1]:
            ErrorMsg = "f_set must be of order (start, stop, [step]) where " \
                       "'start' is a value smaller than 'stop'"
            raise SyntaxError(ErrorMsg)

        f_set = array([
            m for m in arange(f_set[0], f_set[1] + f_set[2], f_set[2])
        ], dtype=float64)

    else:
        ErrorMsg = 'Error in partitioning frequency values'
        raise SyntaxError(ErrorMsg)

    return f_set


def d_set_ref(d_set):

    """

    refactors the input d_set to the corresponding
    Nx1 numpy array.

    :param d_set:   (start, end, [step])

                    tuple for thickness values in mm.
                    - or -
                    if d_set is of type list, then the thickness values
                    calculated will only be of the values present in the
                    list.


    :return:        refactored d_set of Nx1 numpy array

    ----------------------------------------------
    """
    if d_set is None:
        ErrorMsg = 'd_set must be given as a tuple of length 3 ' \
                   '(d_st, d_end, d_step) or a list [] of d values.'
        raise SyntaxError(ErrorMsg)

    elif type(d_set) is list:
        d_set = array(d_set, dtype=float64)
    else:
        try:
            d_set = arange(d_set[0], d_set[1] + d_set[2], d_set[2], dtype=float64)
        except:
            ErrorMsg = 'd_set must be a tuple type int or float of ' \
                       'structure (start, end, step) ' \
                       'or a list [] of type int or float values.'
            raise SyntaxError(ErrorMsg)

    return d_set


def m_set_ref(m_set):

    """

    refactors the input m_set to the corresponding
    Nx1 numpy array.

    :param m_set:   (start, end, [step])

                    tuple of ints which define the bands to be calculated.
                    - or -
                    if m_set is given as a list [], the explicitly listed
                    band integers will be calculated.


    :return:        refactored m_set of Nx1 numpy array

    ----------------------------------------------
    """
    # partition band values
    if type(m_set) is list:
        m_set = array(m_set, dtype=int)

    else:
        try:
            m_set = arange(m_set[0], m_set[1] + m_set[2], m_set[2], dtype=int)
        except:
            ErrorMsg = 'm_set must be a tuple of positive integers of ' \
                       'structure (start, end, step) ' \
                       'or a list [] of integer values.'
            raise SyntaxError(ErrorMsg)

    return m_set
