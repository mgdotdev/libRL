import sys
import tempfile

from unittest.mock import patch

import pytest

from libRL.__main__ import main
from .utils import Fixture


@pytest.fixture(scope="session")
def paraffin_fixture():
    yield Fixture("paraffin_data.csv")


@pytest.fixture(scope="session")
def material_fixture():
    yield Fixture("test_data.csv")


@pytest.fixture(scope="session")
def al_tio2_fixture():
    yield Fixture("Al700.csv")


@pytest.fixture(scope="session")
def tempdir():
    tempd = tempfile.TemporaryDirectory()
    yield tempd
    tempd.cleanup()


@pytest.fixture(scope="function")
def catch():
    results = []

    def target(rval):
        def _target(*args, **kwargs):
            results.extend([args, kwargs])
            return rval

        return _target

    return results, target


@pytest.fixture(scope="function")
def run_and_catch():
    def _run_and_catch(args):
        sys.argv = args
        return main()

    return _run_and_catch


@pytest.fixture(scope="function")
def run_patch_and_catch(catch):
    results, target = catch

    def _run_patch_and_catch(fn_name, args, rval=None):
        with patch(fn_name, target(rval)):
            sys.argv = args
            main()
        return results

    return _run_patch_and_catch
