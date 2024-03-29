import itertools

from .tools.extensions import gamma
from .tools.refactoring import parse, interpolations, dfind_half
from .tools.writer import reflection_loss as write


def reflection_loss(data, f_set=None, d_set=None, **kwargs):

    data = parse.data(data)

    f, e1, e2, mu1, mu2 = data

    f_set = parse.f_set(f_set, f)
    d_set = parse.d_set(d_set)

    fns = interpolations(
        f, e1, e2, mu1, mu2, kwargs.get("interp", "cubic"), kwargs.get("override")
    )

    rl_vals = gamma(f_set, d_set, *[list(map(fn, f_set)) for fn in fns])
    result_grid = [
        [rl for (rl, _, _) in grouper]
        for _, grouper in itertools.groupby(rl_vals, key=lambda item: item[2])
    ]
    results = {"f": f_set, "d": d_set, "RL": result_grid}
    filename = kwargs.get("save")
    if filename:
        write(results, filename)
    return results


def band_reflection_loss(data, f_set=None, d_set=None, **kwargs):
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
