import csv
import cmath

from types import SimpleNamespace

from numpy import sqrt
from scipy.interpolate import interp1d


def _data_generator(f):
    for r in csv.reader(f):
        try:
            yield [float(i) for i in r]
        except ValueError:
            continue


def _parse_file(filepath):
    with open(filepath, "r") as fl:
        return [list(i) for i in zip(*_data_generator(fl))]


def _parse_f_set(f_set, f):
    if f_set is None:
        f_set = f
    elif isinstance(f_set, tuple):
        f_set = list(stepwise(*f_set))
    elif isinstance(f_set, list):
        pass
    else:
        raise ValueError("f_set must be either a tuple, list, or None")
    return f_set


def _parse_d_set(d_set):
    if isinstance(d_set, tuple):
        d_set = list(stepwise(*d_set))
    elif isinstance(d_set, (int, float)):
        d_set = [d_set]
    elif isinstance(d_set, list):
        pass
    else:
        raise ValueError("d_set must be either a value, a tuple, or a list")
    return d_set


def _parse_m_set(m_set):
    if isinstance(m_set, tuple):
        m_set = list(stepwise(*m_set))
    elif isinstance(m_set, (int, float)):
        m_set = [m_set]
    elif isinstance(m_set, list):
        pass
    else:
        raise ValueError("m_set must be either a value, a tuple, or a list")
    return m_set


def stepwise(start, stop, step=None):
    if not step:
        for i in range(int(start), int(stop)):
            yield i
    else:
        _, precision = str(float(step)).split(".")
        for i in range(int((stop - start) / step)):
            yield round(start + (step * i), len(precision))


def interpolations(f, e1, e2, mu1, mu2, mode="cubic", override=None):
    fns = [
        interp1d(f, p, kind=mode, fill_value="extrapolate") for p in (e1, e2, mu1, mu2)
    ]
    if override == "x0":
        fns[2] = lambda f: 1.0
        fns[3] = lambda f: 0.0
    elif override == "es":
        fns[0] = lambda f: sum(e1) / len(e1)
        fns[1] = lambda f: 0.0
    return fns

def dfind_half(e1f, e2f, mu1f, mu2f, f, m):
    mu = mu1f(f) - cmath.sqrt(-1) * mu2f(f)
    e = e1f(f) - cmath.sqrt(-1) * e2f(f)
    msq = 299792458 / (f * 10 ** 9)
    y = (msq * (1.0 / (sqrt(mu * e).real)) * (((2.0 * m) - 2.0) / 4.0)) * 1000
    return y


parse = SimpleNamespace(
    file=_parse_file, f_set=_parse_f_set, d_set=_parse_d_set, m_set=_parse_m_set
)
