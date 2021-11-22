import itertools

from .tools.extensions import gamma
from .tools.refactoring import parse, interpolations, dfind_half
from .tools.writer import band_analysis as write


def band_analysis(data, f_set=None, d_set=None, m_set=None, threshold=-10, **kwargs):

    if isinstance(data, str):
        data = parse.file(data)
        f, e1, e2, mu1, mu2 = data

    f_set = parse.f_set(f_set, f)
    d_set = parse.d_set(d_set)
    m_set = parse.m_set(m_set)

    f_step = (f_set[-1] - f_set[0]) / (len(f_set) - 1)
    f_precision = max(
        set(ids := [len(str(x).split(".")[1]) for x in f_set]), key=ids.count
    )

    interpolation_mode = kwargs.get("interp", "cubic")
    e1f, e2f, mu1f, mu2f = interpolations(f, e1, e2, mu1, mu2, interpolation_mode)
    fns = [e1f, e2f, mu1f, mu2f]

    band_results = {}
    for m in m_set:
        results = []
        for f in f_set:
            d_min = dfind_half(e1f, e2f, mu1f, mu2f, f, m)
            d_max = dfind_half(e1f, e2f, mu1f, mu2f, f, m + 1)
            d_vals = [d for d in d_set if d_min <= d <= d_max]
            reflection_loss_values = gamma(
                [f], d_vals, *[list(map(fn, [f])) for fn in fns]
            )

            results.extend([x for x in reflection_loss_values if x[0] <= threshold])
        results.sort(key=lambda item: item[2])

        for key, grouper in itertools.groupby(results, key=lambda item: item[2]):
            values = list(grouper)
            band_results.setdefault(m, {})[key] = round(
                len(values) * f_step, f_precision
            )

    if filename := kwargs.get("save"):
        return write(d_set, band_results, filename)
    return band_results
