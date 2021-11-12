import libRL

from .utils import Expectation, Fixture


class TestCharacterization:
    def test_chars(self):
        fixture = Fixture("paraffin_data.csv")
        expected = Expectation("characterization.json")
        actual = libRL.characterization(fixture.name, f_set=(1, 18, 1))
        assert actual == expected.read()
