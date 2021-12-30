import csv
import cmath
import io

import numpy as np

from types import SimpleNamespace

from numpy import sqrt
from scipy.interpolate import interp1d


def _data_generator(f):
    for r in csv.reader(f):
        try:
            yield [float(i) for i in r]
        except ValueError:
            continue


def _parse_file(_input):
    if isinstance(_input, list):
        return _input
    if isinstance(_input, io.StringIO):
        return [list(i) for i in zip(*_data_generator(_input))]
    if isinstance(_input, str):
        with open(_input, "r") as fl:
            return [list(i) for i in zip(*_data_generator(fl))]
    raise ValueError("unable to parse data input, should be filepath or io.StringIO")


def _parse_f_set(f_set, f):
    if f_set is None:
        return f
    if isinstance(f_set, list):
        return f_set
    if isinstance(f_set, tuple):
        return list(stepwise(*f_set))
    raise ValueError("f_set must be either a tuple, list, or None")


def _parse_d_set(d_set):
    if isinstance(d_set, list):
        return d_set
    if isinstance(d_set, tuple):
        return list(stepwise(*d_set))
    if isinstance(d_set, (int, float)):
        return [d_set]
    raise ValueError("d_set must be either a value, a tuple, or a list")


def _parse_m_set(m_set):
    if isinstance(m_set, list):
        return m_set
    if isinstance(m_set, tuple):
        return list(stepwise(*m_set))
    if isinstance(m_set, (int, float)):
        return [m_set]
    raise ValueError("m_set must be either a value, a tuple, or a list")


def stepwise(start, stop, step=None):
    if not step:
        return range(int(start), int(stop))
    _, precision = str(float(step)).split(".")
    return (
        round(start + (step * i), len(precision))
        for i in range(int((stop - start) / step))
    )


def interpolations(f, e1, e2, mu1, mu2, mode="cubic", override=None):
    fns = [
        interp1d(f, p, kind=mode, fill_value="extrapolate") for p in (e1, e2, mu1, mu2)
    ]
    if override == "x0":
        fns[2] = lambda f: 0 * np.array(f) + 1
        fns[3] = lambda f: 0 * np.array(f)
    elif override == "es":
        fns[0] = lambda f: np.average(np.array(f))
        fns[1] = lambda f: 0 * np.array(f)
    return fns


def dfind_half(e1f, e2f, mu1f, mu2f, f, m):
    mu = mu1f(f) - cmath.sqrt(-1) * mu2f(f)
    e = e1f(f) - cmath.sqrt(-1) * e2f(f)
    msq = 299792458 / (f * 10 ** 9)
    y = (msq * (1.0 / (sqrt(mu * e).real)) * (((2.0 * m) - 2.0) / 4.0)) * 1000
    return y


parse = SimpleNamespace(
    data=_parse_file, f_set=_parse_f_set, d_set=_parse_d_set, m_set=_parse_m_set
)
