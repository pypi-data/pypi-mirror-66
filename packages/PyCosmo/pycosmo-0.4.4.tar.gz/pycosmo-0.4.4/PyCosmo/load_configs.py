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


# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

if PY2:
    from UserDict import UserDict
else:
    from collections import UserDict

import importlib
import json
import os
import six

from sympy import Rational, Symbol
import sympy


from .config import Parameter
from .symbols import symbols as S
from .v2_config import parse_and_check_v2_config


def loadConfigs(configs):
    """
    Loads key-value configurations from Python modules.

    :param configs: string or list of strings with absolute module declaration
                    e.g. "ivy.config.base_config

    :return config: a :py:class:`Struct` instance with the config attributes
    """
    if configs is None:
        raise AttributeError("Invalid configuration passed")

    if not isinstance(configs, list):
        configs = [configs]

    if len(configs) < 1:
        raise AttributeError("Invalid configuration passed")

    for configName in configs:
        if os.path.exists(configName):
            config = {}
            global_dict = globals().copy()
            global_dict.update({"sp": sympy, "Parameter": Parameter})
            exec(open(configName).read(), global_dict, config)
        else:
            config = importlib.import_module(configName).__dict__

        config["__file__"] = config.get("__file__", os.path.abspath(configName))

        config = parse_and_check_v2_config(config, configName)
        return config


class NBObjects(UserDict):
    def __init__(self, path, dd):
        UserDict.__init__(self, dd)
        self._path = path

    def __setstate__(self, path):
        self._path = path
        dd = extract_code(path)
        self.data = dict()
        self.data.update(dd)

    def __getstate__(self):
        return self._path


def extract_code(path):
    path = os.path.abspath(path)
    cells = json.load(open(path))["cells"]
    all_code = "\n".join(
        "".join(cell["source"])
        for cell in cells
        if (
            cell["cell_type"] == "code"
            and cell["source"]
            and "%%" not in cell["source"][0]
        )
    )

    namespace = globals()["__builtins__"].copy()
    namespace.update(S.__dict__)
    namespace["Rational"] = Rational
    namespace["R"] = Rational
    namespace["Symbol"] = Symbol

    if six.PY3:
        exec(all_code, namespace)
    else:
        exec(all_code) in namespace

    namespace.pop("__builtins__", None)
    return NBObjects(path, namespace)


def check_config_file():
    import sys

    loadConfigs(sys.argv[1:])
