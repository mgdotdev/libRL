from .utils import Expectation, Fixture


class TestMain:
    def test_reflection_loss(self, paraffin_fixture, run_and_catch):
        expected = Expectation("reflection_loss.csv")
        actual = run_and_catch(
            ["libRL", "rl", paraffin_fixture.name, "-f", "1,18,1", "-d", "0,20,1"]
        )
        assert expected.read() == actual

    def test_band_analysis(self, material_fixture, run_and_catch):
        expected = Expectation("band_analysis.csv")
        actual = run_and_catch(
            [
                "libRL",
                "ba",
                material_fixture.name,
                "-f",
                "1,18,0.1",
                "-d",
                "0,20,0.1",
                "-m",
                "1,5",
            ]
        )
        assert actual == expected.read()

    def test_characterization(self, paraffin_fixture, run_and_catch):
        expected = Expectation("characterization.csv")
        actual = run_and_catch(["libRL", "c", paraffin_fixture.name, "-f", "1,18,1"])
        assert actual == expected.read()
