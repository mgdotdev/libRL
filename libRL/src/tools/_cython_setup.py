"""
to build Cython files, cd to this folder and pass:

python _cython_setup.py build_ext --inplace clean --all

once built, see _c_setup.py to compile C/C++ files
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize('**/*.pyx'),
)