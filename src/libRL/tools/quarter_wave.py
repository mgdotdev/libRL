import numpy as np
from scipy.interpolate import interp1d

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
    return f, _quarter_wave