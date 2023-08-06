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

import hashlib
import importlib
import os
import shutil
import sys

from sympy.utilities.autowrap import autowrap

from ._cache_utils import base_cache_folder


def _hash(expr):
    digest = hashlib.sha256()
    digest.update(str(expr).encode('utf-8'))
    return digest.hexdigest()[:20]


def _to_regular_func(c_func, name, is_from_cache=False):
    """we have to introduce an indirection here because we can not set attributes
    on the compiled extension functions
    """
    def wrapped(*a, **kw):
        return c_func(*a, **kw)
    wrapped.is_from_cache = is_from_cache
    wrapped.__name__ = str(name + "__compiled")
    return wrapped


def compile_nbo_eq(nbo, name, *args):
    """
    returns:
        flag:  True if expression was compiled, False if it was already in the cache
        function: compiled function.

        the flag is usually not interesting, except when testing.
    """
    return compile_expression(nbo[name], name, *args)


def compile_expression(expr, name, *args, **kw):
    if not args:
        args = kw.get('args', ())
    h = _hash(expr)
    if "wrappers_folder" in kw:
        wrappers_folder = kw["wrappers_folder"]
    else:
        wrappers_folder = os.path.join(base_cache_folder(), "wrappers")

    folder = os.path.join(wrappers_folder, name + "_" + h)

    def compile_expression():
        print("compile sympy expressions", name, "which is", expr)
        result = autowrap(expr, tempdir=folder, backend='cython', args=args, verbose=True)
        # remove loaded module from cache: module named assigned by sympy else stays in
        # import cache:
        sys.modules.pop(result.__module__, None)
        return result

    if not os.path.exists(folder):
        os.makedirs(folder)
        c_func = compile_expression()
        return _to_regular_func(c_func, name, False)
    else:
        try:
            # sys.modules = {name:m for name, m in sys.modules.items() if not name.startswith("wrapper_module_")}
            sys.path.insert(0, folder)
            wrapper_files = [f for f in os.listdir(folder) if f.startswith("wrapper_module_")]
            shared_libs = [f for f in wrapper_files if f.endswith(".so")]
            if len(shared_libs) != 1:
                print("wrappers folder at {} corrupted, build again"
                      .format(folder))
                raise ImportError()
            mod_name = shared_libs[0].split(".")[0] # without .so and maybe platform postfix
            mod = importlib.import_module(mod_name)
            # remove loaded module from cache: module named assigned by sympy else stays in
            # import cache:
            del sys.modules[mod_name]
            # print("loaded existing compiled code for sympy expression", name)
            return _to_regular_func(mod.autofunc_c, name, True)
        except (ImportError, AttributeError):
            shutil.rmtree(folder)
            c_func = compile_expression()
            return _to_regular_func(c_func, name, False)
        finally:
            del sys.path[0]
