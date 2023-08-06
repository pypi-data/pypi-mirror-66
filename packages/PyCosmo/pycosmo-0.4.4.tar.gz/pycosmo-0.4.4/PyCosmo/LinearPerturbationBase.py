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


import numpy as np
import six

from .PerturbationBase import ClassContractMeta, check_protypes, prototype


@six.add_metaclass(ClassContractMeta)
class LinearPerturbationBase(object):

    """
    This class computes the linear matter power spectrum, :math:`P_{lin}(k)`,
    using the fitting functions provided either by the class :class:`PyCosmo.LinearPerturbationApprox`
    or by the :math:`\\textsf{PyCosmo}` Boltzmann Solver. The latter option is still under testing
    and will be available in future releases.
    """

    def __new__(clz, *a, **kw):
        check_protypes(clz)
        return super(LinearPerturbationBase, clz).__new__(clz)

    # todo: sigma_r needs to be speeded up and made robust
    # todo: merge this with sigma8
    def sigma_r(self, r=8., a=1.0):
        """
        Calculates the rms of the density field on a given scale :math:`r`.
        It is a generalization of the function :meth:`sigma8`.

        :param r: scale radius (default set to :math:`8 h^{-1} Mpc`)
        :return: :math:`\\sigma_r` [1]
        """
        r = np.atleast_1d(r)
        # TODO: numpy based vecoriztion !
        res = np.zeros(shape=r.shape)
        for i in range(0, len(r)):
            ri = r[i]
            k = np.logspace(-5., 2., num=5000)  # grid of wavenumber k [Mpc^-1]
            lnk = np.log(k)
            w = (
                3. / (k * ri) ** 2 * (np.sin(k * ri) / (k * ri) - np.cos(k * ri))
            )  # top hat window function
            pk = self.powerspec_a_k(a=1., k=k)
            res[i] = np.trapz(k ** 3 * pk[:, 0] * w ** 2, lnk)

        return np.sqrt(1. / (2. * np.pi ** 2) * res)

    def _sigma_intg(self, lnk, r, a):
        """"Integrand for calculating sigma of the density field"""
        k = np.exp(lnk)
        w = 3. / (k * r) ** 2 * (np.sin(k * r) / (k * r) - np.cos(k * r))
        pk_temp = self.powerspec_a_k(a=a, k=k)
        return k ** 3 * pk_temp[0, :] * w ** 2

    def sigma8(self):
        """
        Computes :math:`\\sigma_8`, the rms density contrast fluctuation smoothed
        with a top hat of radius :math:`8 h^{-1} Mpc`. This specialised routine is
        to be used for the normalisation of the power spectrum.

        :return: :math:`\\sigma_8` [1]
        """

        # TODO: reuse sigma_r ?
        r = 8. / self._params.h  # smoothing radius [Mpc]
        k = np.logspace(-5., 2., num=5000)  # grid of wavenumber k [Mpc^-1]
        lnk = np.log(k)
        w = (
            3. / (k * r) ** 2 * (np.sin(k * r) / (k * r) - np.cos(k * r))
        )  # top hat window function
        pk = self.powerspec_a_k(a=1., k=k)
        res = np.trapz(k ** 3 * pk[:, 0] * w ** 2, lnk)
        return np.sqrt(1. / (2. * np.pi ** 2) * res)

    @prototype
    def growth_a(self, a=1.0, k=None, norm=0, verbose=False):
        pass

    @prototype
    def transfer_k(self, k):
        pass

    def powerspec_a_k(self, a=1.0, k=0.1, diag_only=False):
        """
        Computes the linear matter power spectrum, :math:`P_{lin}(k)`, using a choice of fitting functions.

        :param a: scale factor [1]
        :param k: wavenumber :math:`[Mpc]^{-1}`
        :param diag_only:
        :return: Linear matter power spectrum, :math:`P_{lin}(k)`, in :math:`[Mpc]^3`.

        Example:

        .. code-block:: python

            cosmo.set(pk_type = option)
            cosmo.lin_pert.powerspec_a_k(a,k)

        where ``option`` can be one of the fitting functions described in :class:`PyCosmo.LinearPerturbationApprox`.
        """
        a = np.atleast_1d(a)
        k = np.atleast_1d(k)
        if diag_only:
            assert len(a) == len(k)
        T_k = self.transfer_k(k=k)
        growth = self.growth_a(a, k=1)
        # using equation in section 2.4 of notes
        norm = (
            2.0
            * np.pi ** 2
            * self._params.deltah_norm ** 2
            * (self._params.c / self._params.H0) ** (3.0 + self._params.n)
        )

        if diag_only:
            pk = norm * growth ** 2 * k ** self._params.n * T_k ** 2
        else:
            pk = norm * np.outer(growth.T ** 2, k ** self._params.n * T_k ** 2).T
        return pk
