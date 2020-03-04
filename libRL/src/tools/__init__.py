from os import path
from libRL.src.tools import(
    quick_graphs,
    refactoring
)

try:
    import pyximport; pyximport.install(
        language_level=3,
        build_dir=path.join(path.abspath(path.dirname(__file__)),'cython')
    )

    from libRL.src.tools import cpfuncs as band_funcs

except:
    from libRL.src.tools import pyfuncs as band_funcs