from __future__ import print_function, division, absolute_import
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


import os
import sys

if sys.version_info[0] == 3:
    basestring = str


def base_cache_folder():
    home = os.path.expanduser("~")
    if sys.platform.startswith("darwin"):
        base_folder = os.path.join(home, "Library", "Cache")
    else:
        base_folder = os.path.join(home, "_cache")
    return os.path.join(base_folder, "PyCosmo")
