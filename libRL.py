import cmath
import cpfuncs

from numpy import(
arange, delete, zeros, abs, array,
argmin, float64, errstate, pi, sqrt
)

from pandas import(
read_csv, read_excel, DataFrame
)

from scipy.interpolate import interp1d
from pathos.multiprocessing import ProcessPool as Pool
from os.path import splitext


def help():
    q1 = RL(Mcalc='?')
    q2 = CARL(Mcalc='?')
    q3 = BARF(Mcalc='?')
    return q1, q2, q3


def RL(Mcalc=None, f_set=None, d_set=None, **kwargs):

    init='''
    
    RL(Mcalc=None, f_set=None, d_set=None, **kwargs)
    
    the RL function calculates the Reflection Loss based on the mapping
    passed through as the grid variable, done either through multiprocessing 
    or through the python built-in map() function. The RL function always
    uses the interpolation function, even though as the function passes 
    through the points associated with the input data, solving for the 
    function at the associated frequencies yields the data point. This
    is simply for simplicity.

    ref: https://doi.org/10.1016/j.jmat.2019.07.003
    
    :param Mcalc:   Permittivity and Permeability data of Nx5 dimensions.
                    Can be a string equivalent to the directory and file
                    name of either a .csv or .xlsx of Nx5 dimensions. Text
                    above and below data array will be automatically 
                    avoided by the program (most network analysis instruments
                    report data which is compatible with the required format)
    
    :param f_set:   (start, end, [step]) tuple for frequency values in GHz
                    - if given as list of len 3, results are interpolated
                    - if given as list of len 2, results are data-derived
                    with the calculation bound by the given start and end
                    frequencies
                    - if f_set is None, frequency is bound to input data
    
    :param d_set:   (start, end, step) tuple for thickness values in mm.
                    - or -
                    if d_set is of type list, then the thickness values
                    calculated will only be of the values present in the
                    list.
    
    :param kwargs:  interp='linear' - set to linear if user wants to linear 
                    interp instead of cubic.
                    multiprocessing=(int) - set to integer value to use
                    multiprocessing with (int) nodes; set to 0 to use all
                    nodes.
                    'multicolumn'=True - outputs data in multicolumn form with
                    either a numpy array of [RL, f, d] iterated over each three
                    columns, or, if as_dataframe is used, then as a pandas 
                    dataframe with columns of name d and indexes of name f
                    as_dataframe=True - returns data in a pandas dataframe.
    
    
    :return:        returns Nx3 data set of [RL, f, d] by default or an
                    NxM dataframe where N rows for the input frequency values
    
    -------------------------------------
    '''

    if Mcalc is '?':
        return init

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
        d_set = array(d_set)
    else:
        d_set = arange(d_set[0], d_set[1] + d_set[2], d_set[2])

    # if frequency step value is given, interpolate the results.
    # Otherwise, the grid is tied to the given data as if the function
    # was never interpolated, as interpolating functions pass through
    # all given variables.

    if f_set is None:
        f_set = Mcalc[:, 0]
        grid = array([(m, n)
                      for n in d_set
                      for m in f_set
        ])

    elif f_set is float or int and not tuple:
        f_set = arange(Mcalc[0,0],Mcalc[-1,0]+f_set, f_set)
        grid = array([(m, n)
                      for n in d_set
                      for m in f_set
        ])

    elif len(f_set) is 2:
        f_set = Mcalc[argmin(abs(f_set[0]-Mcalc[:,0])):argmin(abs(f_set[1]-Mcalc[:,0])),0]
        grid = array([(m, n)
                      for n in d_set
                      for m in f_set
        ])

    elif len(f_set) is 3:
        f_set = arange(f_set[0], f_set[1]+f_set[2], f_set[2])
        grid = array([(m, n)
                      for n in d_set
                      for m in f_set
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

        # get frequency values from grid so to normalize the procedure due to the
        # various frequency input methods
        gridInt = int(grid.shape[0] / d_set.shape[0])

        # zero-array of NxM where N is the frequency values and M is 3 times the
        # number of thickness values
        MCres = zeros(
            (gridInt, d_set.shape[0] * 3)
        )

        # map the Zx3 result array to the NxM array
        for i in arange(int(MCres.shape[1] / 3)):
            MCres[:, 3*i:3*i+3] = res[i*gridInt:(i+1)*gridInt, 0:3]

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


def CARL(Mcalc=None, f_set=None, params="All", **kwargs):

    init='''
    
    CARL(Mcalc=None, f_set=None, params="All", **kwargs)
    
    the CARL (ChAracterization of Reflection Loss) function takes
    a set or list of keywords in the 'params' variable and calculates 
    the character values associated with the parameter. See  
    10.1016/j.jmat.2019.07.003 for further details and the
    function comments below for a full list of keywords.
    
    ref: https://doi.org/10.1016/j.jmat.2019.07.003
    
    :param Mcalc:   Permittivity and Permeability data of Nx5 dimensions.
                    Can be a string equivalent to the directory and file
                    name of either a .csv or .xlsx of Nx5 dimensions. Text
                    above and below data array will be automatically 
                    avoided by the program (most network analysis instruments
                    report data which is compatible with the required format)
    
    :param f_set:   (start, end, [step]) tuple for frequency values in GHz
                    - if given as list of len 3, results are interpolated
                    - if given as list of len 2, results are data-derived
                    with the calculation bound by the given start and
                    end frequencies
                    - if f_set is None, frequency is bound to input data
                    or:
                    - if f_set is of type list, the frequencies calculate
                    will be only the frequencies represented in the list.
    
    :param params:  A list i.e. [] of text arguments for the parameters
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

    :param kwargs:  as_dataframe=True - returns the requested parameters as
                    a pandas dataframe with column names as the parameter keywords

    
    :return:        NxY data set of the requested parameters as columns 1 to Y with the input
                    frequency values in column zero to N.
    
    -------------------------------------
    '''

    if Mcalc is '?':
        return init

    if Mcalc is None:
        ErrorMsg = 'Data must be passed as an array which is mappable to an Nx5 ' \
                   'numpy array with columns [freq, e1, e2, mu1, mu2]'
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
    Z0 = 376.730313461
    e0 = 8.854188 * 10 ** (-12)

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

    errstate(divide='ignore')

    # if frequency step value is given, interpolate the results.
    # Otherwise, the grid is tied to the given data as if the function
    # was never interpolated, as interpolating functions pass through
    # all given variables.

    if f_set is None:
        f_vals = array([
            m for m in Mcalc[:, 0]
        ])

    elif f_set is float or int and not tuple:
        f_vals = array([
            m for m in arange(Mcalc[0,0],Mcalc[-1,0]+f_set, f_set)
        ])

    elif len(f_set) is 2:
        f_vals = array([
            m for m in Mcalc[
                        argmin(abs(f_set[0]-Mcalc[:,0])):
                        argmin(abs(f_set[1]-Mcalc[:,0])),
                        0]
        ])

    elif len(f_set) is 3:
        f_vals = array([
            m for m in arange(f_set[0], f_set[1]+f_set[2], f_set[2])
        ])

    else:
        ErrorMsg = 'Error in partitioning frequency values'
        raise SyntaxError(ErrorMsg)

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
        "PhsVel": lambda f: ((2 * pi * f * GHz) /
                            ((2*pi*f*GHz*sqrt((mu1f(f) - j * mu2f(f)) *
                            (e1f(f) - j * e2f(f))))*(c**-1))).imag,
        "Res": lambda f: (Z0 * sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))).real,
        "React": lambda f: (Z0 * sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))).imag,
        "Condt": lambda f: (2 *pi * f * GHz) * (e0 * e2f(f)),
        "Skd": lambda f: 1000 / ((2*pi*f*GHz*sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))))*(c**-1)).real,
        "Eddy": lambda f: mu2f(f) / (mu1f(f) ** 2 * f)
    }

    if params is 'All' or 'all' or params[0] is 'All' or params[0] is 'all':
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
        panda_matrix = DataFrame(Matrix[:, 1:])
        panda_matrix.columns = list(names[1:])
        panda_matrix.index = list(f_vals)
        return panda_matrix

    return Matrix, names

def BARF(Mcalc=None, f_set=None, d_set=None, m_set=None, threshold=-10, **kwargs):

    init='''
    
    BARF(Mcalc=None, f_set=None, d_set=None, m_set=None, threshold=-10, **kwargs)
    
    the BARF (Band Analysis for ReFlection loss) function uses Permittivity 
    and Permeability data of materials so to determine the effective bandwidth 
    of Reflection Loss. The effective bandwidth is the span of frequencies where 
    the reflection loss is below some proficiency threshold (standard threshold
    is -10 dB). Program is computationally taxing; thus, efforts were made to push 
    most of the computation to the C-level for faster run times - the blueprints
    for such are included in the cpfuncs.pyx file, which was compiled via Cython 
    and the cython_setup.py file. [and yes, I love you 3000]
    
    ref: https://doi.org/10.1016/j.jmat.2018.12.005 
         https://doi.org/10.1016/j.jmat.2019.07.003
    
    :param Mcalc:   Permittivity and Permeability data of Nx5 dimensions.
                    Can be a string equivalent to the directory and file
                    name of either a .csv or .xlsx of Nx5 dimensions. Text
                    above and below data array will be automatically 
                    avoided by the program (most network analysis instruments
                    report data which is compatible with the required format)
    
    :param f_set:   (start, end, [step]) tuple for frequency values in GHz
                    or:
                    - if given as tuple of len 3, results are interpolated
                    - if given as tuple of len 2, results are data-derived
                    with the calculation bound by the given start and end
                    frequencies from the tuple
                    - is given as int or float of len 1, results are 
                    interpolated over the entire data set with a step size
                    of the given tuple value.
                    - if f_set is None (default), frequency is bound to 
                    input data.
    
    :param d_set:   (start, end, [step]) tuple for thickness values in mm.
                    or:
                    if d_set is of type list, then the thickness values
                    calculated will only be of the values present in the
                    list. (is weird, but whatever.)
    
    :param m_set:   (start, end, [step]) tuple of ints which define the
                    bands to be calculated.
                    or:
                    if m_set is given as a list [], the explicitly listed
                    band integers will be calculated.                                                            
    
    :param kwargs:  interp='linear' - set to linear if user wants to 
                    linear interp instead of cubic.
                    as_dataframe=True - formats results into a pandas 
                    dataframe with the index labels as the thickness 
                    values, the column labels as the band numbers, and 
                    the dataframe as the resulting effective bandwidths.
                  
    
    :return:        returns len(3) tuple with [d_set, band_results, m_set]
                    or the requested dataframe
    
    -------------------------------------
    '''

    if Mcalc is '?':
        return init

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
        ErrorMsg = 'd_set must be given as a tuple of length 3 (d_st, d_end, d_step) or a list [] of d values.'
        raise SyntaxError(ErrorMsg)

    # constants for later use
    j = cmath.sqrt(-1)
    c = 299792458
    GHz = 10**9

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

    errstate(divide='ignore')

    if type(d_set) is list:
        d_set = array(d_set)
    else:
        try:
            d_set = arange(d_set[0], d_set[1] + d_set[2], d_set[2])
        except:
            ErrorMsg = 'd_set must be a tuple type int or float of structure (start, end, step) ' \
                       'or a list [] of type int or float values.'
            raise SyntaxError(ErrorMsg)

    # paritition band values
    if type(m_set) is list:
        m_set = array(m_set)

    else:
        try:
            m_set = arange(m_set[0], m_set[1] + m_set[2], m_set[2])
        except:
            ErrorMsg = 'm_set must be a tuple of positive integers of structure (start, end, step) ' \
                       'or a list [] of integer values.'
            raise SyntaxError(ErrorMsg)

    # if frequency step value is given, interpolate the results.
    # Otherwise, the grid is tied to the given data as if the function
    # was never interpolated, as interpolating functions pass through
    # all given variables.

    if f_set is None:
        f_set=array([
            m for m in Mcalc[:, 0]
        ])

    elif f_set is float or int and not tuple:
        f_set=array([
            m for m in arange(Mcalc[0,0],Mcalc[-1,0]+f_set, f_set)
        ])

    elif len(f_set) is 2:
        f_set=array([
            m for m in Mcalc[
                        argmin(abs(f_set[0]-Mcalc[:,0])):
                        argmin(abs(f_set[1]-Mcalc[:,0])),
                        0]
        ])

    elif len(f_set) is 3:
        f_set=array([
            m for m in arange(f_set[0], f_set[1]+f_set[2], f_set[2])
        ])

    else:
        ErrorMsg = 'Error in partitioning frequency values'
        raise SyntaxError(ErrorMsg)

    PnPGrid = zeros((f_set.shape[0],5))

    PnPGrid[:,0] = f_set[:]
    PnPGrid[:,1] = e1f(f_set[:])
    PnPGrid[:,2] = e2f(f_set[:])
    PnPGrid[:,3] = mu1f(f_set[:])
    PnPGrid[:,4] = mu2f(f_set[:])

    mGrid = zeros((f_set.shape[0], m_set.shape[0]*2))

    # to find the 1/2th integer wavelength, NOT quarter.
    def dfind(f, m):
        return ((c/(f*GHz))*(1.0/(sqrt((mu1f(f) - j*mu2f(f)) * (e1f(f) - j*e2f(f))).real))*(((2.0*m)-2.0)/4.0))*1000

    for i, m in enumerate(m_set):
        mGrid[:,2*i] = dfind(f_set[:], m)
        mGrid[:,2*i+1] = dfind(f_set[:], m+1)

    # pushes calculation to the C-level for increased computation performance.
    # see included file titled 'cpfuncs.pyx' for build blueprint
    band_results = cpfuncs.BARC(PnPGrid, mGrid, m_set, d_set, threshold)

    if 'as_dataframe' in kwargs and kwargs['as_dataframe'] is True:
        res = DataFrame(band_results)
        res.columns = list(m_set)
        res.index = list(d_set)

    else:
        res = (d_set, band_results, m_set)

    return res
