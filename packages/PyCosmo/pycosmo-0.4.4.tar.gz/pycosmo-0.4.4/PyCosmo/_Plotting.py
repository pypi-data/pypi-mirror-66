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

__author__ = 'AR & AA'

import pylab
import numpy as np

def plot_boltz_a(self, k=.01, n_a=1000, lmax=10, damp=False, tca=True, norm='COSMICS', odepar=-1, xvar=0, eins=0, jac=False): # k in [h Mpc^-1]
    """Plot the different Boltzmann perturbation fields as a function of the scale factor a for a given
    value of k
    """
    aa=np.logspace(-6.,0.,num=n_a)    # range of a for boltzmann integration
    f=self.fields_simple(aa,k,lmax,damp,tca,norm,0,odepar,xvar,eins,jac)

    #self, a=1.0, k=0.1, lmax=10, damp=False,tca=True,norm='cosmics',ak=2,odepar=[100000,1e-10,1e-13,1e-20],xvar=0,eins=1,jac=True)

    #y=self.boltz(k,aa,cosmo)

    pylab.clf()

    # plot Phi/Phi(0)
    pylab.subplot(3,2,1)
    pylab.semilogx()
    pylab.plot(aa,f['phi'][0])
    #pylab.plot(aa,f['phi'][:,0]/f['phi'][0,0])
    pylab.xlabel('a')
    pylab.ylabel('Phi')
    # plot densities
    pylab.subplot(3,2,3)
    pylab.loglog()
    pylab.plot(aa,f['delta'][0])
    pylab.plot(aa,f['deltab'][0])
    pylab.plot(aa,f['theta0'][0]*4.)
    pylab.plot(aa,f['n0'][0]*4.)
    pylab.xlabel('a')
    pylab.ylabel('delta_x')

    ## plot velocities
    pylab.subplot(3,2,4)
    pylab.semilogx()
    pylab.plot(aa,-f['u'][0])
    pylab.plot(aa,-f['ub'][0])
    pylab.plot(aa,-f['theta1'][0]*3.)
    pylab.plot(aa,-f['n1'][0]*3.)
    pylab.xlabel('a')
    pylab.ylabel('-u_x')
    # plot Theta0
    #pylab.subplot(3,2,5)
    #pylab.semilogx()
    #pylab.plot(aa,f['theta0'][0])
    #pylab.xlabel('a')
    #pylab.ylabel('Theta0')
    #pylab.plot(aa,f['n0'][0])
    # plot Theta1
    #pylab.subplot(3,2,6)
    #pylab.semilogx()
    #pylab.plot(aa,f['theta1'][0])
    #pylab.xlabel('a')
    #pylab.ylabel('Theta1')
    #pylab.plot(aa,f['n1'][0])

    # plot photon moments
    pylab.subplot(3,2,5)
    pylab.semilogx()
    pylab.plot(aa,f['theta0'][0])
    pylab.plot(aa,f['theta1'][0])
    pylab.plot(aa,f['theta2'][0])
    pylab.xlabel('a')
    pylab.ylabel('Theta_l')

    # plot l=2 moments
    pylab.subplot(3,2,6)
    pylab.semilogx()
    pylab.plot(aa,f['theta2'][0])
    pylab.plot(aa,f['n2'][0])
    pylab.xlabel('a')
    pylab.ylabel('Theta2,N2')

    # plot oscillation damping function if turned on
    if False:
        pylab.subplot(3,2,2)
        pylab.semilogx()
        pylab.xlabel('a')
        pylab.ylabel('Gamma')
        xc_damp=max([1000.,k*self._eta_a([5.*self.params.a_eq])[0]])
        gamma=0.5*(1.-np.tanh((k*np.array(self._eta_a(aa))-xc_damp)/50.))
        pylab.plot(aa,gamma)
    if True:
        ec=self.econ(f)
        pylab.subplot(3,2,2)
        pylab.loglog()
        pylab.xlabel('a')
        pylab.ylabel('econ')
        pylab.plot(aa,np.abs(ec[0,:]))


    #pylab.show()
