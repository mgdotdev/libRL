This site is a docstring repository for the libRL library, written by
Michael Green at the University of Missouri-Kansas City.

Use the tabs on the left-hand side of the page to navigate to the
various document sections.

Research was supported by the National Science Foundation under grant
NSF-1609061.

**Connect:**

Michael Green
`@Github <https://github.com/1mikegrn>`_
`@StackOverflow <https://stackoverflow.com/users/10881573/michael-green?tab=profile>`_

Getting Started
===============

If you're new to Python, the easiest way to get started is through the
`Anaconda <https://www.anaconda.com/distribution/>`_ distribution.
Installation instructions for the three major operating systems can be found
in the JCE-Supplemental for `pyGC <https://github.com/1mikegrn/pyGC>`_

From your command prompt, the libRL library can be installed via pip and git

:code:`pip install git+https://github.com/1mikegrn/libRL`

Where the setup file will automatically check dependencies and install
to the main module library. Once installed, simply import the module as
normal via :code:`import libRL`, and query the docstring via libRL? - the
docstring includes a list of the available functions for use.

The library includes the following main-level functions:

::

    libRL.reflection_loss(
    data=None, f_set=None, d_set=None, **kwargs
    )

:func:`libRL.__init__.reflection_loss` computes the resultants of Reflection Loss
over (f, d) gridspace.

::

    libRL.characterization(
    data=None, f_set=None, params="all", **kwargs
    )

:func:`libRL.__init__.characterization` yields the calculated results of common
formulations within the Radar Absorbing Materials field.

::

    libRL.band_analysis(
    data=None, f_set=None, d_set=None, m_set=None, threshold=-10, **kwargs
    )

:func:`libRL.__init__.band_analysis` uses given set of permittivity and permeability data
in conjuncture with a requested band set to determine the set of frequencies
whose reflection losses are below the threshold.

Library Structure
=================

::

    libRL/
        __init__.py         # initial executable
        cpfunc.pyx          # cython protocols
        refactoring.py      # Data processing protocols
        quick_graphs.py     # data visualization protocols

the main libRL functions are all accessible via the modules
:code:`__init__.py` method, which are called directly from libRL.