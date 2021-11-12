from .tools.extensions import gamma

from .tools.refactoring import parse, interpolations


def reflection_loss(data, f_set=None, d_set=None, **kwargs):

    if isinstance(data, str):
        data = parse.file(data)
        f, e1, e2, mu1, mu2 = data

    f_set = parse.f_set(f_set, f)
    d_set = parse.d_set(d_set)

    interpolation_mode = kwargs.get("interp", "cubic")
    fns = interpolations(f, e1, e2, mu1, mu2, interpolation_mode)

    results = gamma(f_set, d_set, *[list(map(fn, f_set)) for fn in fns])

    return results
