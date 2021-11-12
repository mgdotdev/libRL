import libRL

from .utils import Expectation, Fixture


class TestReflectionLoss:
    def test_reflection_loss(self):
        fixture = Fixture("paraffin_data.csv")
        expected = Expectation("reflection_loss.json")
        actual = libRL.reflection_loss(fixture.name, f_set=(1, 18, 1), d_set=(0, 20, 1))
        assert actual == expected.read()
