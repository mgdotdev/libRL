import argparse
import functools
import sys

import libRL
from .tools.refactoring import parse


def _fdm_format(_type, string):
    if string.startswith("[") and string.endswith("]"):
        return list(map(_type, string[1:-1].split(",")))
    return tuple(map(_type, string.split(",")))


def param_format(string):
    return string.split(",")


def _f_set(parser):
    parser.add_argument(
        "-f",
        "--f_set",
        type=functools.partial(_fdm_format, float),
        metavar="",
        help="frequencies for analysis, three numbers separated by ','",
        default=None,
    )


def _d_set(parser):
    parser.add_argument(
        "-d",
        "--d_set",
        type=functools.partial(_fdm_format, float),
        metavar="",
        help="thicknesses for analysis, three numbers separated by ','",
        default=(0, 5, 0.1),
    )


def _m_set(parser):
    parser.add_argument(
        "-m",
        "--m_set",
        type=functools.partial(_fdm_format, int),
        metavar="",
        help="band numbers for analysis, three numbers separated by ','",
        default=[1],
    )


def _saver(parser):
    parser.add_argument(
        "-s",
        "--save",
        type=str,
        help="filepath to save data at. Directory must exist.",
        default=None,
    )


def _reflection_loss_cli(filepath, args):
    parser = argparse.ArgumentParser(description="libRL reflection loss")
    _f_set(parser)
    _d_set(parser)
    _saver(parser)
    parser.add_argument(
        "--override",
        type=str,
        metavar="",
        help=(
            "data override, options are ['x0', 'es'] for ",
            "chi-zero and epsilon-set, respectively",
        ),
        default=None,
    )
    ns = parser.parse_args(args)
    results = libRL.reflection_loss(filepath, **vars(ns))
    vals = zip(results["f"], *results["RL"])
    return "\n".join(
        (
            "," + ",".join([str(i) for i in results["d"]]),
            *(",".join((str(i) for i in v)) for v in vals),
        )
    )


def _bandwidth_analysis_cli(filepath, args):
    parser = argparse.ArgumentParser(description="libRL band analysis")
    _d_set(parser)
    _m_set(parser)
    _f_set(parser)
    _saver(parser)

    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        metavar="",
        help="threshold value, default is -10",
        default=-10,
    )
    ns = parser.parse_args(args)
    results = libRL.band_analysis(filepath, **vars(ns))

    m_set = parse.m_set(ns.m_set)
    d_set = parse.d_set(ns.d_set)

    return "\n".join(
        (
            ",".join(["d", *(str(m) for m in m_set)]),
            *(
                ",".join([str(results.get(m, {}).get(d, 0)) for m in m_set])
                for d in d_set
            ),
        )
    )


def _characterization_cli(filepath, args):
    parser = argparse.ArgumentParser(description="libRL characterizations")
    _f_set(parser)
    _saver(parser)
    parser.add_argument(
        "-p",
        "--params",
        type=param_format,
        metavar="",
        help="parameters to calculate, separated by comma. Default is 'all'",
        default=["all"],
    )
    ns = parser.parse_args(args)
    results = libRL.characterization(filepath, **vars(ns))
    keys = results.keys()
    vals = [list(i) for i in zip(*(results[i] for i in keys))]
    return "\n".join((",".join(keys), *(",".join((str(i) for i in v)) for v in vals)))


def _print_help():
    _help = "libRL"
    print(_help)


def main():
    _, cmd, filepath, *args = sys.argv
    if cmd in ("rl", "reflection_loss"):
        return _reflection_loss_cli(filepath, args)
    elif cmd in ("ba", "band_analysis"):
        return _bandwidth_analysis_cli(filepath, args)
    elif cmd in ("c", "char", "characterization"):
        return _characterization_cli(filepath, args)
    elif cmd in ("-h", "--help"):
        return _print_help()
    else:
        raise RuntimeError("cmd did not match any of the available cmd options")


if __name__ == "__main__":
    main()
