import itertools

import numpy as np

from ..reflection_loss import reflection_loss
from .extensions import gamma
from .refactoring import parse, interpolations, dfind_half


def _neighbors(d_i, f_i):
    return (
        (d_i+1, f_i),
        (d_i-1, f_i),
        (d_i, f_i-1),
        (d_i, f_i+1),
    )

def f_peak(data, f_set=None, d_set=None, m_set=None, **kwargs):

    data = parse.data(data)

    f, e1, e2, mu1, mu2 = data

    f_set = parse.f_set(f_set, f)
    d_set = parse.d_set(d_set)
    m_set = parse.m_set(m_set)

    fns = interpolations(
        f, e1, e2, mu1, mu2, kwargs.get("interp", "cubic"), kwargs.get("override")
    )

    peak_results = {}
    for m in m_set:
        results = []
        for f in f_set:
            d_min = dfind_half(*fns, f, m)
            d_max = dfind_half(*fns, f, m + 1)
            d_vals = [d for d in d_set if d_min <= d <= d_max]
            reflection_loss_values = gamma(
                [f], d_vals, *[list(map(fn, [f])) for fn in fns]
            )

            results.extend(reflection_loss_values)
        results.sort(key=lambda item: item[2])

        rl_vals = []
        for _, grouper in itertools.groupby(results, key=lambda item: item[2]):
            rl_vals.append([v[0] for v in grouper])
        f_peaks = []
        for d_i, d in enumerate(d_set):
            for f_i, f in enumerate(f_set):
                try:
                    rl_val = rl_vals[f_i][d_i]
                    subarr = (rl_vals[j][i] for (i, j) in _neighbors(d_i, f_i))
                    if all(rl_val < i for i in subarr):
                        f_peaks.append([rl_val, f, d])
                except IndexError:
                    continue
        peak_results[m] = f_peaks
    return peak_results
