import math

from libRL.__main__ import _fdm_format
from libRL.tools.extensions import gamma, test_extension
from libRL.tools.redundancies import gamma as py_gamma
from libRL.tools.refactoring import parse

from .utils import Expectation


def _is_tolerable(a, b):
    if abs(a - b) < 0.0005:
        return True
    return False


def test_fdm_format():
    actual = _fdm_format(int, "1,2,3")
    assert actual == (1, 2, 3)
    actual = _fdm_format(int, "1,2")
    assert actual == (1, 2)
    actual = _fdm_format(float, "1")
    assert actual == (1.0,)
    actual = _fdm_format(float, "[1,2,3]")
    assert actual == [1.0, 2.0, 3.0]
    actual = _fdm_format(int, "[1,2,3]")
    assert actual == [1, 2, 3]


class TestExtensions:
    def test_extension(self):
        actual = test_extension()
        assert actual in (1, 0)

    def test_gamma(self):
        # RL(0,0,0,0,0,0) converges at -inf
        res = gamma([0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0])
        for (rl, f, d) in res:
            assert math.isnan(rl)
            assert (f, d) == (0, 0)


class TestRedundancies:
    def test_equivalence(self):
        f, d, e1, e2, mu1, mu2 = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]
        expected = py_gamma(f, d, e1, e2, mu1, mu2)
        actual = gamma(f, d, e1, e2, mu1, mu2)
        for ((a, _, _), (b, _, _)) in zip(actual, expected):
            assert _is_tolerable(a, b)

    def test_equivalence_different_thickness_values(self):
        f, d, e1, e2, mu1, mu2 = [
            [1, 1],
            [1, 2, 3, 4, 5],
            [1, 1],
            [1, 1],
            [1, 1],
            [1, 1],
        ]
        expected = py_gamma(f, d, e1, e2, mu1, mu2)
        actual = gamma(f, d, e1, e2, mu1, mu2)
        for ((a, _, _), (b, _, _)) in zip(actual, expected):
            assert _is_tolerable(a, b)


class TestRefactors:
    def test_parse(self, paraffin_fixture):
        actual = parse.file(paraffin_fixture.name)
        expected = Expectation("test_parse.json")
        assert actual == expected.read()
