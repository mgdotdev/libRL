import os.path

import pytest

import libRL
from .utils import LocalFileUtil, Expectation


class TestReflectionLoss:
    def test_reflection_loss(self, paraffin_fixture):
        expected = Expectation("reflection_loss.json")
        actual = libRL.reflection_loss(
            paraffin_fixture.name, f_set=(1, 18, 1), d_set=(0, 20, 1)
        )
        assert actual == expected.read()

    def test_reflection_loss_lists(self, paraffin_fixture):
        expected = Expectation("reflection_loss_lists.json")
        actual = libRL.reflection_loss(
            paraffin_fixture.name, f_set=[1, 2, 3, 4, 5], d_set=[1]
        )
        assert actual == expected.read()

    def test_reflection_loss_single_thickness(self, paraffin_fixture):
        expected = Expectation("reflection_loss_lists.json")
        actual = libRL.reflection_loss(
            paraffin_fixture.name, f_set=[1, 2, 3, 4, 5], d_set=1
        )
        assert actual == expected.read()

    def test_reflection_loss_chi_zero(self, material_fixture):
        expected = Expectation("reflection_loss_chi_zero.json")
        actual = libRL.reflection_loss(
            material_fixture.name, f_set=[1, 2, 3, 4, 5], d_set=[1,2,3,4,5], override="x0"
        )
        assert actual == expected.read()
        
    def test_reflection_loss_eps_set(self, material_fixture):
        expected = Expectation("reflection_loss_eps_set.json")
        actual = libRL.reflection_loss(
            material_fixture.name, f_set=[1, 2, 3, 4, 5], d_set=[1,2,3,4,5], override="es"
        )
        assert actual == expected.read()

    def test_reflection_loss_thickness_only(self, paraffin_fixture):
        expected = Expectation("reflection_loss_thickness_only.json")
        actual = libRL.reflection_loss(paraffin_fixture.name, d_set=1)
        assert actual == expected.read()

    def test_save_reflection_loss(self, paraffin_fixture, tempdir):
        filename = "test_save_reflection_loss.csv"
        filepath = os.path.join(tempdir.name, filename)
        libRL.reflection_loss(
            paraffin_fixture.name, f_set=[1, 2, 3, 4, 5], d_set=1, save=filepath,
        )
        actual = LocalFileUtil(filepath)
        expected = Expectation(filename)
        assert actual.read() == expected.read()
