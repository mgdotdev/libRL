"""
to build C/C++ files, cd to this folder and pass:

python _c_setup.py build_ext --inplace clean --all
"""

import glob
from setuptools import setup, Extension, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
# files = [path.split(x)[1] for x in glob.glob(path.join(here, '**.cpp'))]

files = [glob.glob(e) for e in ['*.c', '*.cpp']] 

extensions = [Extension(
    path.splitext(x[0])[0], [x[0]]
) for x in files]

setup(
    ext_modules = extensions,
)