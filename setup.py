# open anaconda prompt, cd to the location of the 'setup.py' file, the run the following:
# python setup.py build_ext --inplace

from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("cpfuncs.pyx")
)