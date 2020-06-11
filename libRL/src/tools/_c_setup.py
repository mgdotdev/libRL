"""
to build C files, cd to this folder and pass:

python _c_setup.py build_ext --inplace clean --all
"""

import glob
from setuptools import setup, Extension, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
files = [path.split(x)[1] for x in glob.glob(path.join(here, '**.cpp'))]

extensions = [Extension(
    path.splitext(x)[0], [x]
) for x in files]

setup(
    ext_modules = extensions,
)