import os.path

import libRL

from .utils import Expectation, LocalFileUtil


class TestBandAnalysis:
    def test_band_analysis(self, material_fixture):
        expected = Expectation("band_analysis.json")
        actual = libRL.band_analysis(
            material_fixture.name,
            f_set=(1, 18, 0.1),
            d_set=(0, 20, 0.1),
            m_set=(1, 5, 1),
        )
        assert all(
            ai == ei
            for ab, eb in zip(actual.values(), expected.read().values())
            for ai, ei in zip(ab.values(), eb.values())
        )

    def test_band_analysis_chi_zero(self, material_fixture):
        expected = Expectation("band_analysis_chi_zero.json")
        actual = libRL.band_analysis(
            material_fixture.name,
            f_set=(1, 18, 0.1),
            d_set=(0, 20, 0.1),
            m_set=(1, 5, 1),
            override="x0",
        )
        assert all(
            ai == ei
            for ab, eb in zip(actual.values(), expected.read().values())
            for ai, ei in zip(ab.values(), eb.values())
        )

    def test_save_band_analysis(self, material_fixture, tempdir):
        filename = "test_save_band_analysis.csv"
        filepath = os.path.join(tempdir.name, filename)
        libRL.band_analysis(
            material_fixture.name,
            f_set=(1, 18, 0.1),
            d_set=(1, 5, 0.1),
            m_set=(1, 5),
            save=filepath,
        )
        actual = LocalFileUtil(filepath)
        expected = Expectation(filename)
        assert actual.read() == expected.read()
