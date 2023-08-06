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

import sys

__builtins__["PY2"] = sys.version_info < (3, 0, 0)

import os

# needed for headless mode on ci server
if os.environ.get("CI") is not None:
    import sys

if True:
    # this if is a hack to avoid resorting imports

    import pkg_resources  # part of setuptools

    from . import patches  # installs some hooks
    from .Cosmo import Cosmo
    from .load_configs import loadConfigs
    from .Obs import Obs


# Copyright (C) 2013 ETH Zurich, Institute for Astronomy


version = pkg_resources.require("PyCosmo")[0].version

"""
This is the PyCosmo package.
"""
__all__ = ["Cosmo"]

__version__ = version
__author__ = "Adam Amara, Alexander Refregier, Joel Akeret, Lukas Gamper, Uwe Schmitt"
__credits__ = "Institute for Astronomy ETHZ"
