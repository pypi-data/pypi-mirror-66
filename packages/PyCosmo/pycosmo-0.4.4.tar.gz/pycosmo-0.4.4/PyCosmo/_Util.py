# This file is part of PyCosmo, a multipurpose cosmology calculation tool in Python.
#
# Copyright (C) 2013-2020 ETH Zurich, Institute for Particle and Astrophysics and SIS
# ID.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import print_function, division, absolute_import

import functools
import hashlib
import types

import numpy as np


def _check_a_ode(a=1.0, tilltoday=False):
    """
    Checks that the a vector used in for the Boltz integrator statisfies some basic condition:
    (i) a is listed in increasing order,
    (ii) that the first value of a is early enough

    :param a:
    :param tilltoday:
    """
    aa = np.atleast_1d(a)
    ind_sort = aa.argsort()
    ind_unsort = ind_sort.argsort()
    a_sort = aa[ind_sort]
    return a_sort, ind_unsort


def relative_differences(a=1., b=1.):
    a = np.atleast_1d(a)
    b = np.atleast_1d(b)
    return np.absolute((a - b) / a)
