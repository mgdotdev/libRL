# Copyright (C) 2019 Michael Green
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, under version 3.0 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

"""
:code:`__init__.py`
===================

libRL is a library of functions used for characterizing Microwave Absorption.

functions include:

::

    libRL.reflection_loss(
    data=None, f_set=None, d_set=None, **kwargs
    )

resultants of Reflection Loss over (f, d) gridspace. Yields the
resulting Reflection Loss results for a given set of permittivity
and permeability data.
see the DocStrings for complete documentation.

::

    libRL.characterization(
    data=None, f_set=None, params="all", **kwargs
    )

characterization of Reflection Loss. Yields the calculated results
of common formulations within the Radar Absorbing Materials field.
see the DocStrings for complete documentation.

::

    libRL.band_analysis(
    data=None, f_set=None, d_set=None, m_set=None, threshold=-10, **kwargs
    )

Band Analysis of Reflection Loss. uses given set of permittivity and
permeability data in conjuncture with a requested band set to determine
the set of frequencies whose reflection losses are below the
threshold.
see the DocStrings for complete documentation.

Developed at the University of Missouri-Kansas City under NSF grant DMR-1609061
by Michael Green and Xiaobo Chen.

full details can be found at https://1mikegrn.github.io/libRL/
"""

from libRL import src, gui
from libRL.src.band_analysis import band_analysis
from libRL.src.characterization import characterization
from libRL.src.reflection_loss import reflection_loss
from libRL.src.profile import Profile