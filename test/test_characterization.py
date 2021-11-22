import os.path

import libRL

from .utils import LocalFileUtil, Expectation, Fixture


class TestCharacterization:
    def test_chars(self, paraffin_fixture):
        expected = Expectation("characterization.json")
        actual = libRL.characterization(paraffin_fixture.name, f_set=(1, 18, 1))
        assert actual == expected.read()

    def test_save_chars(self, paraffin_fixture, tempdir):
        filename = "test_save_chars.csv"
        filepath = os.path.join(tempdir.name, filename)
        libRL.characterization(paraffin_fixture.name, save=filepath)
        actual = LocalFileUtil(filepath)
        expected = Expectation(filename)
        assert actual.read() == expected.read()
