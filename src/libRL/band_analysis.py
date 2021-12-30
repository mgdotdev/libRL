import io
import itertools

from .tools.extensions import gamma
from .tools.refactoring import parse, interpolations, dfind_half
from .tools.writer import band_analysis as write


def band_analysis(data, f_set=None, d_set=None, m_set=None, threshold=-10, **kwargs):

    m_set = parse.m_set(m_set)
    _analysis = _band_analysis(data=data, f_set=f_set, d_set=d_set, threshold=threshold, **kwargs)

    band_results = {}
    for m in m_set:
        band_results[m] = _analysis(m)
    filename = kwargs.get("save")
    if filename:
        d_set = parse.d_set(d_set)
        return write(d_set, band_results, filename)
    return band_results


def _band_reflection_loss(data, f_set=None, d_set=None, **kwargs):
    data = parse.data(data)

    f, e1, e2, mu1, mu2 = data

    f_set = parse.f_set(f_set, f)
    d_set = parse.d_set(d_set)

    fns = interpolations(
        f, e1, e2, mu1, mu2, kwargs.get("interp", "cubic"), kwargs.get("override")
    )
    def _results(m):
        results = []
        for f in f_set:
            d_min = dfind_half(*fns, f, m)
            d_max = dfind_half(*fns, f, m + 1)
            d_vals = [d for d in d_set if d_min <= d <= d_max]
            reflection_loss_values = gamma(
                [f], d_vals, *[list(map(fn, [f])) for fn in fns]
            )
            results.extend(reflection_loss_values)
        return results
    return _results


def _band_analysis(data, f_set=None, d_set=None, threshold=-10, **kwargs):
    data = parse.data(data)
    f, *_ = data

    f_set = parse.f_set(f_set, f)
    f_step = (f_set[-1] - f_set[0]) / (len(f_set) - 1)

    precisions = [len(str(x).split(".")[1]) for x in f_set]
    f_precision = max(set(precisions), key=precisions.count)

    _band_rl = _band_reflection_loss(
        data, f_set=f_set, d_set=d_set, **kwargs
    )

    def _analysis(m):
        results = list(filter(lambda x: x[0] <= threshold, _band_rl(m)))
        results.sort(key=lambda item: item[2])
        band_results = {}
        for key, grouper in itertools.groupby(results, key=lambda item: item[2]):
            values = list(grouper)
            band_results[key] = round(
                len(values) * f_step, f_precision
            )
        return band_results
    return _analysis
