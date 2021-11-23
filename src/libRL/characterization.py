import io
import cmath


from numpy import sqrt, pi, array

from .tools.refactoring import parse, interpolations, _data_generator
from .tools.writer import characterization as write

# constants
j = cmath.sqrt(-1)  # definition of j
c = 299792458  # speed of light
GHz = 10 ** 9  # definition of GHz
Z0 = 376.730313461  # intrinsic impedance
e0 = 8.854188 * 10 ** (-12)  # permittivity of free space


def characterization(data=None, f_set=None, params=None, **kwargs):
    if params is None:
        params = ["all"]

    data = parse.data(data)

    f, e1, e2, mu1, mu2 = data

    fns = interpolations(f, e1, e2, mu1, mu2, kwargs.get("interp", "cubic"), kwargs.get("override"))
    chars = Characterizations(*fns)

    if params == ["all"]:
        params = list(chars._CHARACTERIZATION_MAPPING.keys())

    if type(params) != list:
        raise TypeError("params arg must be 'all' or a list of params")

    f_set = parse.f_set(f_set, f)
    results = {"f": f_set, **{param: chars[param](f_set).tolist() for param in params}}

    filename = kwargs.get("save")
    if filename:
        return write(results, filename)
    return results


class Characterizations:
    _CHARACTERIZATION_MAPPING = {
        "tgde": "tgde",
        "tgdu": "tgdu",
        "Qe": "qe",
        "Qu": "qu",
        "Qf": "qf",
        "ReRefIndx": "real_refractive_index",
        "ExtCoeff": "extinction_coefficient",
        "AtnuCnstNm": "attenuation_constant_per_nm",
        "AtnuCnstdB": "attenuation_constant_per_db",
        "PhsCnst": "phase_constant",
        "PhsVel": "phase_velocity",
        "Res": "resistance",
        "React": "reactance",
        "Condt": "conductance",
        "Skd": "skin_depth",
        "Eddy": "eddy_current",
    }

    def __init__(self, e1f, e2f, mu1f, mu2f):
        self.e1f = e1f
        self.e2f = e2f
        self.mu1f = mu1f
        self.mu2f = mu2f

    def __getitem__(self, attr):
        return self.__getattribute__(self._CHARACTERIZATION_MAPPING[attr])

    def _attenuation_and_phase(self, f):
        return self._angular_frequency(f) * self._refractive_index(f) * (c ** -1)

    def _refractive_index(self, f):
        return sqrt((self.mu1f(f) - j * self.mu2f(f)) * (self.e1f(f) - j * self.e2f(f)))

    def _angular_frequency(self, f):
        return 2 * pi * array(f) * GHz

    def tgde(self, f):
        return self.e2f(f) / self.e1f(f)

    def tgdu(self, f):
        return self.mu2f(f) / self.mu1f(f)

    def qe(self, f):
        return (self.e1f(f) / self.e2f(f)) ** -1

    def qu(self, f):
        return (self.mu1f(f) / self.mu2f(f)) ** -1

    def qf(self, f):
        return ((self.e1f(f) / self.e2f(f)) + (self.mu1f(f) / self.mu2f(f))) ** -1

    def real_refractive_index(self, f):
        return self._refractive_index(f).real

    def extinction_coefficient(self, f):
        return -1 * self._refractive_index(f).imag

    def attenuation_constant_per_nm(self, f):
        return self._attenuation_and_phase(f).real

    def attenuation_constant_per_db(self, f):
        return self._attenuation_and_phase(f).real * 8.86588

    def phase_constant(self, f):
        return -1 * self._attenuation_and_phase(f).imag

    def phase_velocity(self, f):
        return self._angular_frequency(f) / self.phase_constant(f)

    def resistance(self, f):
        return Z0 * self.real_refractive_index(f)

    def reactance(self, f):
        return -1 * (Z0 * self._refractive_index(f)).imag

    def conductance(self, f):
        return self._angular_frequency(f) * (e0 * self.e2f(f))

    def skin_depth(self, f):
        return 1000 / self.attenuation_constant_per_nm(f)

    def eddy_current(self, f):
        return self.mu2f(f) / (self.mu1f(f) ** 2 * f)
