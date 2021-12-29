import numpy as np

from scipy.interpolate import interp1d
from scipy.optimize import leastsq

from .f_peak import f_peak
from .refactoring import parse
from ..characterizations import characterization

c = 299792458  # speed of light
GHz = 10**9

def quarter_wave(data=None, f_set=None, **kwargs):
    chars = characterization(data=data, f_set=f_set, **kwargs)
    f = np.array(chars['f'])
    ref_index = np.array(chars['ReRefIndx'])
    n = interp1d(f, ref_index, kind="cubic", fill_value="extrapolate")
    
    def _quarter_wave(m):
        res = ((2*m-1)/4)*(c/(n(f)*(f*GHz)))
        return res*1000
    _quarter_wave.f = f
    return _quarter_wave

def _fitting_function(x, a, b):
    return a * x ** b

def _residuals(p, y, x):
    return y - _fitting_function(x, *p)

def power_fn(data=None, f_set=None, d_set=None, **kwargs):
    initial_guess = kwargs.get("initial", [1,1])
    d_set = parse.d_set(d_set)
    data = parse.data(data)
    def _power_fn(m):
        _f_peak = f_peak(data=data, f_set=f_set, d_set=d_set, m_set=[m], **kwargs)
        x = np.array([i[2] for i in _f_peak[m]])
        y = np.array([i[1] for i in _f_peak[m]])
        constants, *_ = leastsq(
            _residuals, 
            initial_guess, 
            args=(y, x)
        )
        return np.array([_fitting_function(d_i, *constants) for d_i in d_set])
    _power_fn.d = d_set
    return _power_fn


