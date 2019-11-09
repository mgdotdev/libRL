<h1> libRL: A Python library for the characterization of microwave absorption </h1>

---

A Python library for characterizing Microwave Absorption.

This Library is to include all of the functions and methods developed at
the University of Missouri-Kansas City under NSF grant DMR-1609061.

The libRL library can be installed via pip and git

`pip install git+https://github.com/1mikegrn/libRL`

Where the setup file will automatically check dependencies and install
to the main module library. Once installed, simply import the module as
normal via `import libRL`, and query the docstring via libRL? - the
docstring includes a list of the available functions for use.

The library includes the following main-level functions:

    libRL.reflection_loss(
    data=None, f_set=None, d_set=None, **kwargs
    )

[<code>reflection_loss()</code>](__init__.md#reflection_loss) computes the resultants
of Reflection Loss over (f, d) gridspace.

    libRL.characterization(
    data=None, f_set=None, params="all", **kwargs
    )

[<code>characterization()</code>](__init__.md#characterization) yields
the calculated results of common formulations within the Radar Absorbing
Materials field.

    libRL.band_analysis(
    data=None, f_set=None, d_set=None, m_set=None, threshold=-10, **kwargs
    )
    
[<code>band_analysis()</code>](__init__.md#band_analysis) uses given set
of permittivity and permeability data in conjuncture with a requested
band set to determine the set of frequencies whose reflection losses are
below the threshold.