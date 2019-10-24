---
title: 'libRL: A Python library for the characterization of microwave absorption'
tags:
  - Python
  - Materials Chemistry
  - Microwave Absorption
  - Permittivity
  - Permeability
authors:
  - name: Michael Green
    orcid: 0000-0002-2525-1274
    affiliation: 1
  - name: Xiaobo Chen
    affiliation: 1
affiliations:
 - name: Department of Chemistry, University of Missouri−Kansas City, MO 64110, U.S.A.
   index: 1
date: 23 October 2019
bibliography: paper.bib
---

# Summary

Ever since the revelation that reflection loss as a parameter of interest was
shown to not be the defining characteristic of radar-absorbing materials (RAM)
[@Green:2019-1; @Green:2019-2; @Green:2019-3], the RAM development community has
been bereft of the tools necessary to determine the parameters desired by the new
RAM performance hierarchy. Elucidating the new parameters of interest, such as the
effective bandwidth, requires non-trivial derivations and calculations that many labs
in the RAM community are simply not prepared to handle, at least not at the scale
necessary for thorough characterization.

In order to best mitigate these difficulties, presented herein is a Python library
for reflection loss characterization, designed for open use by the RAM development
community. The libRL library contains functions and procedures which take
permittivity and permeability data derived from experimentation, and calculates the
various sets of parameters desired for the full characterization of radar-absorbing
materials. Such calculations include the standard reflection loss over
frequency·thickness grid space, the full list of characterization values defined in
the recent literature review, *Recent Progress in Nanomaterials for Microwave Absorption*
[@Green:2019-1], and finally the effective bandwidths for reflection loss. As such, the
library encapsulates the entirety of cutting-edge analyses available for the development
of single plane-wave absorbers [@Naito:1969; @Naito:1971; @Meena:2010]. These functions
have been optimized for both user and computation efficiency, making use of both pythons
built-in functions and the cython library for optimized computation performance.


This library can be installed via pip into the user’s python environment (see README.md
for details) and imported/used similarly to any other library available in the standard
library. libRL includes therein an exhaustive set of methods for customizing the
calculation parameters so to satisfy the broadest of scopes necessary for the RAM
development community - users are encouraged to consult the docstrings therein for a
full description of the customizations available.

# Conflict of interest

Authors declare that there are no conflicts of interest.

# Acknowledgements

M. G. and X. C. appreciate the support from the U.S. National Science Foundation
(DMR-1609061), the School of Biological and Chemical Sciences at the
University of Missouri−Kansas City, and the University of Missouri Research Board.

# References