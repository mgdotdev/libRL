"""
If you've found your way here, congratulations! Here lies the secrets to making
this run faster. Simply compile the _{}_setup.py files in this tools directory 
to make use of the optional extensions.
"""

from os import path
from libRL.src.tools import(
    quick_graphs,
    refactoring,
)

# if extension not compiled, use python implementations
try:
    from libRL.src.tools import cpfuncs as band_funcs

except:
    from libRL.src.tools import pyfuncs as band_funcs

try:
    from libRL.src.tools import simple as gamma

except:
    from libRL.src.tools import _gamma as gamma
