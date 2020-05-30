from os import path
from libRL.src.tools import(
    quick_graphs,
    refactoring
)

try:

    from libRL.src.tools import cpfuncs as band_funcs

except:
    from libRL.src.tools import pyfuncs as band_funcs