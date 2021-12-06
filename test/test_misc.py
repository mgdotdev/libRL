import libRL

from libRL.tools.f_peak import f_peak

from .utils import Expectation


class TestFPeak:
    def test_f_peak(self, al_tio2_fixture):
        actual = f_peak(
            al_tio2_fixture.name,
            f_set=(1, 18, 0.1),
            d_set=(0, 5, 0.1),
            m_set=(1,5,1)
        )
        expected = Expectation("al_tio2_fpeak.json")
        for av, ev in zip(actual.values(), expected.read().values()):
            assert av == ev
