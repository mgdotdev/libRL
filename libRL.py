import cmath

from numpy import(
arange, delete, zeros, abs, array,
float64, argwhere, errstate, pi, sqrt
)

from pandas import(
read_csv, read_excel, DataFrame
)

import warnings
from scipy.interpolate import interp1d
from pathos.multiprocessing import ProcessPool as Pool
from os.path import splitext

'''    
the RL function calculates the Reflection Loss based on the mapping
passed through as the grid variable, done either through multiprocessing 
or through the python built-in map() function. The RL function always
uses the interpolation function, even though as the function passes 
through the points associated with the input data, solving for the 
function at the associated frequencies yields the data point. This
is simply for simplicity.
'''

def RL(Mcalc=None, f_set=None, d_set=None, **kwargs):

    '''
    param Mcalc: Permittivity and Permeability data
    param f_set: (start, end, [step]) tuple for frequency values in GHz
                 - if given as list of len 3, results are interpolated
                 - if given as list of len 2, results are data-derived
                 with the calculation bound by the given start and end
                 frequencies
                 - if f_set is None, frequency is bound to input data
    param d_set: (start, end, step) tuple for thickness values in mm.
                 - or -
                 if d_set is of type list, then the thickness values
                 calculated will only be of the values present in the
                 list.
    param kwargs: interp - set to linear if user wants to linear interp
                  instead of cubic.
                  multiprocessing - set to integer value to use
                  multiprocessing with (int) nodes, set to 0 to use all
                  nodes.
    return: returns Nx3 data set of [RL, freq, thickness]
    '''

    if Mcalc is None:
        ErrorMsg = 'Data must be passed as an array which is mappable to an Nx5 numpy array with columns [freq, e1, e2, mu1, mu2]'
        raise RuntimeError(ErrorMsg)

    # allows for file location to be passed as the data variable.
    if isinstance(Mcalc, str) is True:
        if splitext(Mcalc)[1] == '.csv':
            Mcalc = read_csv(Mcalc, sep=',').to_numpy()

        elif splitext(Mcalc)[1] == '.xlsx':
            Mcalc = read_excel(Mcalc).to_numpy()

        else:
            ErrorMsg = 'Error partitioning input data'
            raise RuntimeError(ErrorMsg)

        # finds all rows in numpy array which aren't a part of the Nx5 data array expected.
        # note, if the file contains more/less than 5 columns this fails as the 6th row is
        # always filled with NaN. That being said, most instruments output a Nx5 data file.
        x = []
        for i in arange(Mcalc.shape[0]):
            for k in arange(Mcalc.shape[1]):
                if isinstance(Mcalc[i, k], (int, float)) is False or Mcalc[i, k] != Mcalc[i, k]:
                    x.append(i)
                    break

        # removes non-data rows from input array to yield the data array
        Mcalc = delete(Mcalc, x, axis=0)

    if d_set is None:
        ErrorMsg = 'd_set must be given as a tuple of length 3 (d_st, d_end, d_step) or a list [] of d values/'
        raise SyntaxError(ErrorMsg)

    if Mcalc[0,0] > f_set[0] or Mcalc[-1,0] < f_set[1]:
        warning = r'You are electing to interpolate outside of the bounds of your experimental data ' \
                  'set. Please be advised that the resulting calculations for points beyond the data' \
                  'set are likely to be in Error.'
        warnings.warn(warning)

    def G(grid):
        f = grid[0]
        d = grid[1]
        y = (20 * cmath.log10((abs(((1 * (cmath.sqrt((mu1f(f) - j * mu2f(f)) /
            (e1f(f) - j * e2f(f)))) * (cmath.tanh(j * (2 * cmath.pi * (f * GHz) * (d * mm) / c) *
            cmath.sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))))) - 1) /
            ((1 * (cmath.sqrt((mu1f(f) - j * mu2f(f)) / (e1f(f) - j * e2f(f)))) *
            (cmath.tanh(j * (2 * cmath.pi * (f * GHz) * (d * mm) / c) * cmath.sqrt(
            (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))))) + 1)))))
        return y.real, f, d

    # constants for later use
    j = cmath.sqrt(-1)
    c = 299792458
    GHz = 10**9
    mm = 10**(-3)

    # pass data to a numpy array
    Mcalc = array(Mcalc)

    # user option to use linear interpolation via a kwarg. Default is cubic spline.
    # (e1, e2, mu1, mu2) = (Real Permittivity, Complex Permittivity, Real Permeability, Complex Permeability)
    if 'interp' in kwargs and kwargs['interp'] is 'linear':

        e1f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 1], dtype=float64),
            kind='linear', fill_value='extrapolate'
        )

        e2f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 2], dtype=float64),
            kind='linear', fill_value='extrapolate'
        )

        mu1f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 3], dtype=float64),
            kind='linear', fill_value='extrapolate'
        )

        mu2f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 4], dtype=float64),
            kind='linear', fill_value='extrapolate'
        )

    else:
        e1f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 1], dtype=float64),
            kind='cubic', fill_value='extrapolate'
        )

        e2f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 2], dtype=float64),
            kind='cubic', fill_value='extrapolate'
        )

        mu1f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 3], dtype=float64),
            kind='cubic', fill_value='extrapolate'
        )

        mu2f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 4], dtype=float64),
            kind='cubic', fill_value='extrapolate'
        )

    if type(d_set) is list:
        pass
    else:
        d_set = arange(d_set[0], d_set[1] + d_set[2], d_set[2])

    # if frequency step value is given, interpolate the results.
    # Otherwise, the grid is tied to the given data as if the function
    # was never interpolated, as interpolating functions pass through
    # all given variables.

    if f_set is None:
        grid=array([(m, n)
                       for n in d_set
                       for m in Mcalc[:, 0]
        ])

    elif len(f_set) is 3:
        grid=array([(m, n)
                       for n in d_set
                       for m in arange(f_set[0], f_set[1]+f_set[2], f_set[2])
        ])

    elif len(f_set) is 2:
        grid=array([(m, n)
                       for n in d_set
                       for m in Mcalc[
                                argwhere(abs(f_set[0]-Mcalc[:,0])<=
                                         Mcalc[1,0]-Mcalc[0,0])[0][0]:
                                argwhere(abs(f_set[1]-Mcalc[:,0])<=
                                         Mcalc[1,0]-Mcalc[0,0])[0][0], 0]
        ])

    else:
        ErrorMsg = 'Error in partitioning frequency values'
        raise SyntaxError(ErrorMsg)

    # if multiprocessing is given and is a non-zero integer, use int value for number of nodes
    # if multiprocessing is given and is the zero integer, use all available nodes

    if 'multiprocessing' in kwargs and isinstance(kwargs['multiprocessing'], int) is True:

        if kwargs['multiprocessing'] is 0:
            res = array(Pool().map(G, grid))
        else:
            res = array(Pool(nodes=kwargs['multiprocessing']).map(G, grid))

    else:
        res = array(list(map(G, grid)))

    # formatting option, sometimes professors like 3 columns for each thickness value
    if 'multicolumn' in kwargs and kwargs['multicolumn'] is True:
        gridInt = int(grid.shape[0] / arange(d_set[0], d_set[1] + d_set[2], d_set[2]).shape[0])
        MCres = zeros(
            (gridInt, arange(d_set[0], d_set[1] + d_set[2], d_set[2]).shape[0] * 3)
        )
        for i in arange(int(MCres.shape[1] / 3)):
            MCres[:, 3*i:3*i+3] = res[i*gridInt:(i+1)*gridInt, 0:3]
        res = MCres

    return res

'''
the CARL (ChAracterization of Reflection Loss) function takes
a set or list of keywords in the 'params' variable and calculates 
the character values associated with the parameter. See  
10.1016/j.jmat.2019.07.003 for further details and the
function comments below for a full list of keywords.
'''

def CARL(Mcalc=None, f_set=None, params="All", **kwargs):

    '''
    :param Mcalc: Permittivity and Permeability data
    :param f_set: (start, end, [step]) tuple for frequency values in GHz
                 - if given as list of len 3, results are interpolated
                 - if given as list of len 2, results are data-derived
                 with the calculation bound by the given start and
                 end frequencies
                 - if f_set is None, frequency is bound to input data
                 or
                 - if f_set is of type list, the frequencies calculate
                 will be only the frequencies represented in the list.
    :param params: A list i.e. [] of text arguments for the parameters
                   the user wants calculated. The available arguments
                   are: {
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
                   }
                   If no list is passed, the default is to calculate everything.

    :return: returns NxY data set of the requested parameters as columns 1 to Y with the input
                  frequency values in column zero of length N.
    '''

    if Mcalc is None:
        ErrorMsg = 'Data must be passed as an array which is mappable to an Nx5 numpy array with columns [freq, e1, e2, mu1, mu2]'
        raise RuntimeError(ErrorMsg)

    # allows for file location to be passed as the data variable.
    if isinstance(Mcalc, str) is True:
        if splitext(Mcalc)[1] == '.csv':
            Mcalc = read_csv(Mcalc, sep=',').to_numpy()

        elif splitext(Mcalc)[1] == '.xlsx':
            Mcalc = read_excel(Mcalc).to_numpy()

        # finds all rows in numpy array which aren't a part of the Nx5 data array expected.
        # note, if the file contains more/less than 5 columns this fails as the 6th row is
        # always filled with NaN. That being said, most instruments output a Nx5 data file.
        x = []
        for i in arange(Mcalc.shape[0]):
            for k in arange(Mcalc.shape[1]):
                if isinstance(Mcalc[i, k], (int, float)) is False or Mcalc[i, k] != Mcalc[i, k]:
                    x.append(i)
                    break

        # removes non-data rows from input array to yield the data array
        Mcalc = delete(Mcalc, x, axis=0)

    # constants for later use
    j = cmath.sqrt(-1)
    c = 299792458
    GHz = 10**9
    mm = 10**(-3)
    Z0 = 376.730313461
    e0 = 8.854188 * 10 ** (-12)

    # pass data to a numpy array
    Mcalc = array(Mcalc)

    if Mcalc[0,0] > f_set[0] or Mcalc[-1,0] < f_set[1]:
        warning = r'You are electing to interpolate outside of the bounds of your experimental data ' \
                  'set. Please be advised that the resulting calculations for points beyond the data ' \
                  'set are likely to be in Error.'
        warnings.warn(warning)

    # user option to use linear interpolation via a kwarg. Default is cubic spline.
    # (e1, e2, mu1, mu2) = (Real Permittivity, Complex Permittivity, Real Permeability, Complex Permeability)
    if 'interp' in kwargs and kwargs['interp'] is 'linear':

        e1f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 1], dtype=float64),
            kind='linear', fill_value='extrapolate'
        )

        e2f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 2], dtype=float64),
            kind='linear', fill_value='extrapolate'
        )

        mu1f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 3], dtype=float64),
            kind='linear', fill_value='extrapolate'
        )

        mu2f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 4], dtype=float64),
            kind='linear', fill_value='extrapolate'
        )

    else:
        e1f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 1], dtype=float64),
            kind='cubic', fill_value='extrapolate'
        )

        e2f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 2], dtype=float64),
            kind='cubic', fill_value='extrapolate'
        )

        mu1f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 3], dtype=float64),
            kind='cubic', fill_value='extrapolate'
        )

        mu2f = interp1d(
            array(Mcalc[:, 0], dtype=float64),
            array(Mcalc[:, 4], dtype=float64),
            kind='cubic', fill_value='extrapolate'
        )

    errstate(divide='ignore')

    if f_set is None:
        f_vals=array([
            m for m in Mcalc[:, 0]
        ])

    elif type(f_set) is list:
        f_vals=array(f_set)

    elif len(f_set) is 3:
        f_vals=array([
            m for m in arange(f_set[0], f_set[1]+f_set[2], f_set[2])
        ])

    elif len(f_set) is 2:
        f_vals=array([
            m for m in Mcalc[argwhere(abs(f_set[0]-Mcalc[:,0])<=Mcalc[1,0]-Mcalc[0,0])[0][0]:
                             argwhere(abs(f_set[1]-Mcalc[:,0])<=Mcalc[1,0]-Mcalc[0,0])[0][0], 0]
        ])

    else:
        ErrorMsg = 'Error in partitioning frequency values'
        raise RuntimeError(ErrorMsg)

    chars = {
        "tgde": lambda f: e1f(f) / e2f(f),
        "tgdu": lambda f: mu1f(f) / mu2f(f),
        "Qe": lambda f: (e1f(f) / e2f(f))**-1,
        "Qu": lambda f: (mu1f(f) / mu2f(f))**-1,
        "Qf": lambda f: ((e1f(f) / e2f(f))+(mu1f(f) / mu2f(f)))**-1,
        "ReRefIndx": lambda f: sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))).real,
        "ExtCoeff": lambda f:  sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))).imag,
        "AtnuCnstNm": lambda f: ((2*pi*f*GHz*sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))))*(c**-1)).real,
        "AtnuCnstdB": lambda f: ((2*pi*f*GHz*sqrt((mu1f(f) - j * mu2f(f)) *
                                (e1f(f) - j * e2f(f))))*(c**-1)).real * 8.86588,
        "PhsCnst": lambda f: ((2*pi*f*GHz*sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))))*(c**-1)).imag,
        "PhsVel": lambda f: ((2 * pi * i * GHz) /
                            ((2*pi*f*GHz*sqrt((mu1f(f) - j * mu2f(f)) *
                            (e1f(f) - j * e2f(f))))*(c**-1))).imag,
        "Res": lambda f: (Z0 * sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))).real,
        "React": lambda f: (Z0 * sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))).imag,
        "Condt": lambda f: (2 *pi * f * GHz) * (e0 * e2f(f)),
        "Skd": lambda f: 1000 / ((2*pi*f*GHz*sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))))*(c**-1)).real,
        "Eddy": lambda f: mu2f(f) / (mu1f(f) ** 2 * f)
    }

    if params is "All" or params[0] is "All":
        params = [
            "tgde","tgdu","Qe","Qu","Qf",
            "ReRefIndx","ExtCoeff",
            "AtnuCnstNm","AtnuCnstdB",
            "PhsCnst","PhsVel","Res",
            "React","Condt","Skd","Eddy"
        ]

    Matrix, names = zeros((f_vals.shape[0],len(params)+1), dtype=float64), ["frequency"]
    Matrix[:,0] = f_vals[:]

    for counter, param in enumerate(params, start=1):
        Matrix[:, counter] = chars[param](f_vals[:])
        names.append(param)

    if 'as_dataframe' in kwargs and kwargs['as_dataframe'] is True:
        panda_matrix = DataFrame(Matrix)
        panda_matrix.columns = names
        return panda_matrix

    return Matrix, names