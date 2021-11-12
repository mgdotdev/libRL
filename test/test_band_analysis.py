import libRL

from .utils import Expectation, Fixture


class TestBandAnalysis:
    def test_band_analysis(self):
        fixture = Fixture("test_data.csv")
        expected = Expectation("band_analysis.json")
        actual = libRL.band_analysis(
            fixture.name, f_set=(1, 18, 0.1), d_set=(0, 20, 0.1), m_set=(1, 5, 1)
        )
        assert all(
            ai == ei
            for ab, eb in zip(actual.values(), expected.read().values())
            for ai, ei in zip(ab.values(), eb.values())
        )
