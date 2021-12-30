import numpy as np

from scipy.interpolate import interp1d
from scipy.optimize import leastsq

from .f_peak import f_peak
from .refactoring import parse
from ..characterizations import characterization

c = 299792458  # speed of light
GHz = 10 ** 9


def quarter_wave(data=None, f_set=None, **kwargs):
    """a closure for calculating the quarter-wave relation of a dataset. Returns
    a function which takes m as input. frequencies used for calculation can be
    acquired using getattr(fn, 'f')"""
    chars = characterization(data=data, f_set=f_set, **kwargs)
    f = np.array(chars["f"])
    ref_index = np.array(chars["ReRefIndx"])
    n = interp1d(f, ref_index, kind="cubic", fill_value="extrapolate")

    def _quarter_wave(m):
        res = ((2 * m - 1) / 4) * (c / (n(f) * (f * GHz)))
        return res * 1000

    _quarter_wave.f = f
    return _quarter_wave


def _fitting_function(x, a, b):
    return a * x ** b


def _residuals(p, d, f):
    return f - _fitting_function(d, *p)


def power_fn(data=None, f_set=None, d_set=None, **kwargs):
    """a closure for generating f(d) = ad^b for band m. returns a function which
    takes m as input. thicknesses used for calculation can be acquired using
    getattr(fn, 'd')"""
    initial_guess = kwargs.get("initial", [1, 1])
    d_set = parse.d_set(d_set)
    data = parse.data(data)

    def _power_fn(m):
        _f_peak = f_peak(data=data, f_set=f_set, d_set=d_set, m_set=[m], **kwargs)
        _data = np.array(_f_peak(m))
        d, f = _data[:, 2], _data[:, 1]
        constants, *_ = leastsq(_residuals, initial_guess, args=(d, f))
        return np.array([_fitting_function(d_i, *constants) for d_i in d_set])

    _power_fn.d = d_set
    return _power_fn
