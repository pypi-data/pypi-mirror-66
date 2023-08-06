#! /usr/bin/env python3
#
#  Copyright 2018 California Institute of Technology
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# ISOFIT: Imaging Spectrometer Optimal FITting
# Author: David R Thompson, david.r.thompson@jpl.nasa.gov
#

import scipy as s
from scipy.linalg import inv
from scipy.optimize import minimize

from ..core.common import emissive_radiance, eps
from .surface_multicomp import MultiComponentSurface


class ThermalSurface(MultiComponentSurface):
    """A model of the surface based on a Mixture of a hot Black Body and 
        Multicomponent cold surfaces."""

    def __init__(self, config):
        """."""

        MultiComponentSurface.__init__(self, config)
        # Handle additional state vector elements
        self.statevec.extend(['SURF_TEMP_K'])
        self.init.extend([300.0])  # This is overwritten below
        self.scale.extend([100.0])
        self.bounds.extend([[250.0, 400.0]])
        self.surf_temp_ind = len(self.statevec)-1
        self.emissive = True
        self.n_state = len(self.init)

        # Value recommended by Glynn Hulley
        self.emissivity_for_surface_T_init = 0.98
        if "emissivity_for_surface_T_init" in config.keys():
            self.emissivity_for_surface_T_init = \
                config['emissivity_for_surface_T_init']

        self.surface_T_prior_sigma_degK = 1.
        if "surface_T_prior_sigma_degK" in config.keys():
            self.surface_T_prior_sigma_degK = \
                config['surface_T_prior_sigma_degK']

    def xa(self, x_surface, geom):
        """Mean of prior distribution, calculated at state x.  We find
        the covariance in a normalized space (normalizing by z) and then un-
        normalize the result for the calling function."""

        mu = MultiComponentSurface.xa(self, x_surface, geom)
        mu[self.surf_temp_ind] = self.init[self.surf_temp_ind]
        return mu

    def Sa(self, x_surface, geom):
        """Covariance of prior distribution, calculated at state x."""

        Cov = MultiComponentSurface.Sa(self, x_surface, geom)
        Cov[self.surf_temp_ind, self.surf_temp_ind] = \
            self.surface_T_prior_sigma_degK**2

        return Cov

    def fit_params(self, rfl_meas, geom, *args):
        """Given a reflectance estimate, find the surface reflectance"""

        x_surface = MultiComponentSurface.fit_params(self, rfl_meas, geom)
        x_surface[self.surf_temp_ind] = self.init[self.surf_temp_ind]

        return x_surface

    def conditional_solrfl(self, rfl_est, geom):
        """Conditions the reflectance on solar-reflected channels."""

        sol_inds = s.logical_and(self.wl > 450, self.wl < 1250)
        if sum(sol_inds) < 1:
            return rfl_est
        x = s.zeros(len(self.statevec))
        x[self.idx_lamb] = rfl_est
        c = self.components[self.component(x, geom)]
        mu_sol = c[0][sol_inds]
        Cov_sol = s.array([c[1][i, sol_inds] for i in s.where(sol_inds)[0]])
        Cinv = inv(Cov_sol)
        diff = rfl_est[sol_inds] - mu_sol
        full = c[0] + c[1][:, sol_inds].dot(Cinv.dot(diff))
        return full

    def calc_rfl(self, x_surface, geom):
        """Reflectance."""

        return self.calc_lamb(x_surface, geom)

    def drfl_dsurface(self, x_surface, geom):
        """Partial derivative of reflectance with respect to state vector, 
        calculated at x_surface."""

        return self.dlamb_dsurface(x_surface, geom)

    def calc_lamb(self, x_surface, geom):
        """Lambertian Reflectance."""

        return MultiComponentSurface.calc_lamb(self, x_surface, geom)

    def dlamb_dsurface(self, x_surface, geom):
        """Partial derivative of Lambertian reflectance with respect to state 
        vector, calculated at x_surface."""

        dlamb = MultiComponentSurface.dlamb_dsurface(self, x_surface, geom)
        dlamb[:, self.surf_temp_ind] = 0
        return dlamb

    def calc_Ls(self, x_surface, geom):
        """Emission of surface, as a radiance."""

        T = x_surface[self.surf_temp_ind]
        rfl = self.calc_rfl(x_surface, geom)
        rfl[rfl > 1.] = 1.
        emissivity = 1 - rfl
        Ls, dLs_dT = emissive_radiance(emissivity, T, self.wl)
        return Ls

    def dLs_dsurface(self, x_surface, geom):
        """Partial derivative of surface emission with respect to state vector, 
        calculated at x_surface."""

        T = x_surface[self.surf_temp_ind]
        rfl = self.calc_rfl(x_surface, geom)
        emissivity = 1 - rfl
        Ls, dLs_dT = emissive_radiance(emissivity, T, self.wl)
        dLs_drfl = s.diag(-1*Ls)
        dLs_dsurface = s.vstack([dLs_drfl, dLs_dT]).T

        return dLs_dsurface

    def summarize(self, x_surface, geom):
        """Summary of state vector."""

        mcm = MultiComponentSurface.summarize(self, x_surface, geom)
        msg = ' Kelvins: %5.1f ' % tuple(x_surface[-1:])
        return msg+mcm
