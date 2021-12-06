import os.path
import cmath
from numpy import sqrt, pi, array

import libRL

from .utils import LocalFileUtil, Expectation
from .test_tools import _is_tolerable


# constants
j = cmath.sqrt(-1)  # definition of j
c = 299792458  # speed of light
GHz = 10 ** 9  # definition of GHz
Z0 = 376.730313461  # intrinsic impedance
e0 = 8.854188 * 10 ** (-12)  # permittivity of free space


class TestCharacterization:
    def test_chars(self, paraffin_fixture):
        expected = Expectation("characterization.json")
        actual = libRL.characterization(paraffin_fixture.name, f_set=(1, 18, 1))
        assert actual == expected.read()

    def test_chars_chi_zero(self, material_fixture):
        expected = Expectation("characterization_chi_zero.json")
        actual = libRL.characterization(
            material_fixture.name, f_set=(1, 18, 1), override="x0"
        )
        assert actual == expected.read()

    def test_save_chars(self, paraffin_fixture, tempdir):
        filename = "test_save_chars.csv"
        filepath = os.path.join(tempdir.name, filename)
        libRL.characterization(paraffin_fixture.name, save=filepath)
        actual = LocalFileUtil(filepath)
        expected = Expectation(filename)
        assert actual.read() == expected.read()

    def test_al_tio2(self, al_tio2_fixture):
        expected = Expectation("characterization_al.json")
        actual = libRL.characterization(al_tio2_fixture.name, f_set=(1, 18, 1))
        assert actual == expected.read()


class TestParity:
    """test to make sure that new implementation is equivalent to old."""

    def _old_fns(self, e1f, e2f, mu1f, mu2f):
        chars = {
            "TGDE": lambda f: e2f(f) / e1f(f),
            "TGDU": lambda f: mu2f(f) / mu1f(f),
            "QE": lambda f: (e1f(f) / e2f(f)) ** -1,
            "QU": lambda f: (mu1f(f) / mu2f(f)) ** -1,
            "QF": lambda f: ((e1f(f) / e2f(f)) + (mu1f(f) / mu2f(f))) ** -1,
            "REREFINDX": lambda f: sqrt(
                (mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))
            ).real,
            "EXTCOEFF": lambda f: -1
            * sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f))).imag,
            "ATNUCNSTNM": lambda f: (
                (2 * pi * f * GHz)
                * sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))
                * (c ** -1)
            ).real,
            "ATNUCNSTDB": lambda f: (
                2
                * pi
                * f
                * GHz
                * sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))
                * (c ** -1)
            ).real
            * 8.86588,
            "PHSCNST": lambda f: -1
            * (
                (2 * pi * f * GHz)
                * sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))
                * (c ** -1)
            ).imag,
            "PHSVEL": lambda f: (2 * pi * f * GHz) / chars["PHSCNST"](f),
            "RES": lambda f: (
                Z0 * sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))
            ).real,
            "REACT": lambda f: -1
            * (Z0 * sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))).imag,
            "CONDT": lambda f: (2 * pi * f * GHz) * (e0 * e2f(f)),
            "SKD": lambda f: 1000
            / (
                (
                    2
                    * pi
                    * f
                    * GHz
                    * sqrt((mu1f(f) - j * mu2f(f)) * (e1f(f) - j * e2f(f)))
                )
                * (c ** -1)
            ).real,
            "EDDY": lambda f: mu2f(f) / (mu1f(f) ** 2 * f),
        }
        return chars

    def test_chars(self, al_tio2_fixture):

        data = libRL.tools.refactoring.parse.data(al_tio2_fixture.name)
        f, e1, e2, mu1, mu2 = data
        farr = array(f)

        fns = libRL.tools.refactoring.interpolations(f, e1, e2, mu1, mu2, "cubic", None)
        chars = libRL.characterizations.Characterizations(*fns)
        lambdas = self._old_fns(chars.e1f, chars.e2f, chars.mu1f, chars.mu2f)

        for key in chars._CHARACTERIZATION_MAPPING.keys():
            expected = lambdas[key.upper()](farr).tolist()
            actual = chars[key](f)
            assert all(_is_tolerable(e, a) for (e, a) in zip(expected, actual))
