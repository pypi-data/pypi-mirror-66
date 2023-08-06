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



from PyCosmo._structs import Struct
from sympy import Symbol, Rational

_syms = """a H_0 k Phi delta delta_b u u_b
           taudot_interp c_s_interp eta_interp
           omega_r omega_m omega_k omega_l omega_b omega_gamma omega_neu
           omega_dm """.split()


class SymbolArray:

    def __init__(self, base_symbol):
        self.base_symbol = base_symbol

    def __getitem__(self, idx):
        from sympy import Symbol  # hack to make notebook work
        return Symbol("{}_{}".format(self.base_symbol, idx))


symbols = Struct({
                  "R": Rational,
                  "Theta": SymbolArray("Theta"),
                  "Theta_P": SymbolArray("Theta_P"),
                  "N": SymbolArray("N"),
                 }
                 )

for _name in _syms:
    _name = _name.strip()
    symbols[_name] = Symbol(_name)


try:
    del _syms
    del _name
    del Symbol
    del Rational
    del Struct
except Exception as e:
    print(e)
