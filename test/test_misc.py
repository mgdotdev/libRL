import libRL

from libRL.tools.f_peak import f_peak
from libRL.tools.quarter_wave import power_fn, quarter_wave

from .utils import Expectation


class TestFPeak:
    def test_f_peak(self, al_tio2_fixture):
        fn = f_peak(al_tio2_fixture.name, f_set=(1, 18, 0.1), d_set=(0, 5, 0.1))

        actual = {str(i): fn(i) for i in range(1, 5)}
        expected = Expectation("al_tio2_fpeak.json")
        for av, ev in zip(actual.values(), expected.read().values()):
            assert av == ev

    def test_quarter_wave(self, al_tio2_fixture):
        fn = quarter_wave(al_tio2_fixture.name, f_set=(1, 18, 0.1),)
        assert len(fn.f) == len(fn(1))

    def test_power_fn(self, al_tio2_fixture):
        fn = power_fn(al_tio2_fixture.name, f_set=(1, 18, 0.1), d_set=(0.1, 5, 0.1))
        assert len(fn.d) == len(fn(1))
