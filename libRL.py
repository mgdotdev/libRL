import cmath
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from pathos.multiprocessing import ProcessPool as Pool
from os.path import split, splitext

'''    
the RL function caluclates the Reflection Loss based on the mapping
passed through as the grid variable, done either through
multiprocessing or through the python built-in map() function. RL-func always
uses the interpolation function, as the function passes through the input data so
solving for the function at the data point frequency yields the data point.
'''

def RL(Mcalc=None, f_set=None, d_set=None, **kwargs):

    '''
    :param Mcalc: Permittivity and Permeability data
    :param f_set: (start, end, [step]) tuple for frequency values in GHz
                 - if given as list of len 3, results are interpolated
                 - if given as list of len 2, results are data-derived
                 with the calculation bound by the given start and
                 end frequencies
                 - if f_set is None, frequency is bound to input data
    :param d_set: (start, end, step) tuple for thickness values in mm
    :param kwargs: interp - set to linear if user wants to linear interp instead of cubic.
                   multiprocessing - set to integer value to use multiprocessing with (int) nodes,
                   set to 0 to use all nodes.
    :return: returns Nx3 data set of [RL, freq, thickness]
    '''

    if Mcalc is None:
        ErrorMsg = 'Data must be passed as an array which is mappabe to an Nx5 numpy array with columns [freq, e1, e2, mu1, mu2]'
        print(ErrorMsg)
        return ErrorMsg

    # allows for file location to be passed as the data variable.
    if isinstance(Mcalc, str) is True:
        if splitext(Mcalc)[1] == '.csv':
            Mcalc = pd.read_csv(Mcalc, sep=',').to_numpy()

        elif splitext(Mcalc)[1] == '.xlsx':
            Mcalc = pd.read_excel(Mcalc).to_numpy()

        # finds all rows in numpy array which aren't a part of the Nx5 data array expected
        x = []
        for i in np.arange(Mcalc.shape[0]):
            for k in np.arange(Mcalc.shape[1]):
                if isinstance(Mcalc[i, k], (int, float)) is False or Mcalc[i, k] != Mcalc[i, k]:
                    x.append(i)
                    break

        # removes non-data rows from input array to yield the data array
        Mcalc = np.delete(Mcalc, x, axis=0)

    if d_set is None:
        ErrorMsg = 'd_set must be given as a tuple (floats or ints) of length 3 (d_st, d_end, d_step)'
        print(ErrorMsg)
        return ErrorMsg

    def G(grid):
        f = grid[0]
        d = grid[1]
        y = (20 * cmath.log10((np.abs(((1 * (cmath.sqrt((mu1f(f) - j * mu2f(f)) /
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
    Mcalc = np.array(Mcalc)

    # user option to use linear interpolation. Default is cubic spline.
    # (e1, e2, mu1, mu2) = (Real Permittivity, Complex Permittivity, Real Permeability, Complex Permeability)
    if 'interp' in kwargs and kwargs['interp'] is 'linear':

        e1f = interp1d(
            np.array(Mcalc[:, 0], dtype=np.float),
            np.array(Mcalc[:, 1], dtype=np.float),
            kind='linear', fill_value='extrapolate'
        )

        e2f = interp1d(
            np.array(Mcalc[:, 0], dtype=np.float),
            np.array(Mcalc[:, 2], dtype=np.float),
            kind='linear', fill_value='extrapolate'
        )

        mu1f = interp1d(
            np.array(Mcalc[:, 0], dtype=np.float),
            np.array(Mcalc[:, 3], dtype=np.float),
            kind='linear', fill_value='extrapolate'
        )

        mu2f = interp1d(
            np.array(Mcalc[:, 0], dtype=np.float),
            np.array(Mcalc[:, 4], dtype=np.float),
            kind='linear', fill_value='extrapolate'
        )

    else:
        e1f = interp1d(
            np.array(Mcalc[:, 0], dtype=np.float),
            np.array(Mcalc[:, 1], dtype=np.float),
            kind='cubic', fill_value='extrapolate'
        )

        e2f = interp1d(
            np.array(Mcalc[:, 0], dtype=np.float),
            np.array(Mcalc[:, 2], dtype=np.float),
            kind='cubic', fill_value='extrapolate'
        )

        mu1f = interp1d(
            np.array(Mcalc[:, 0], dtype=np.float),
            np.array(Mcalc[:, 3], dtype=np.float),
            kind='cubic', fill_value='extrapolate'
        )

        mu2f = interp1d(
            np.array(Mcalc[:, 0], dtype=np.float),
            np.array(Mcalc[:, 4], dtype=np.float),
            kind='cubic', fill_value='extrapolate'
        )

    # if frequency step value is given, interpolate the results.
    # Otherwise, the grid is tied to the given data as if the function
    # was never interpolated.

    if f_set is None:
        grid=np.array([(m, n)
                       for m in Mcalc[:, 0]
                       for n in np.arange(d_set[0], d_set[1]+d_set[2], d_set[2])
        ])

    elif len(f_set) is 3:
        grid=np.array([(m, n)
                       for m in np.arange(f_set[0], f_set[1]+f_set[2], f_set[2])
                       for n in np.arange(d_set[0], d_set[1]+d_set[2], d_set[2])
        ])

    elif len(f_set) is 2:
        grid=np.array([(m, n)
                       for m in Mcalc[
                                np.argwhere(np.abs(f_set[0]-Mcalc[:,0])<=Mcalc[1,0]-Mcalc[0,0])[0][0]:
                                np.argwhere(np.abs(f_set[1]-Mcalc[:,0])<=Mcalc[1,0]-Mcalc[0,0])[0][0], 0]
                       for n in np.arange(d_set[0], d_set[1]+d_set[2], d_set[2])
        ])

    else:
        ErrorMsg = 'Error in partitioning frequency values'
        print(ErrorMsg)
        return ErrorMsg


    # if multiprocessing is given as a non-zero integer, use int value for number of nodes
    # if multiprocessing is given as a zero integer, use all available nodes

    if 'multiprocessing' in kwargs and isinstance(kwargs['multiprocessing'], int) is True:

        if kwargs['multiprocessing'] is 0:
            res = np.array(Pool().map(G, grid))
        else:
            res = np.array(Pool(nodes=kwargs['multiprocessing']).map(G, grid))

    else:
        res = np.array(list(map(G, grid)))

    # formatting option, sometimes professors like 3 columns for each thickness value
    if 'multicolumn' in kwargs and kwargs['multicolumn'] is True:
        pass

    return res

