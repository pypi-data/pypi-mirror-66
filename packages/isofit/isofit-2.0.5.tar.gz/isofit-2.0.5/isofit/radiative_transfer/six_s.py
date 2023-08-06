#
#  Copyright 2019 California Institute of Technology
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

import os
import logging
from datetime import datetime
import scipy as s

from isofit.core.common import resample_spectrum, load_wavelen, VectorInterpolator
from .look_up_tables import TabularRT, FileExistsError
from isofit.core.geometry import Geometry

sixs_names = ['sixs_vswir']

eps = 1e-5  # used for finite difference derivative calculations

sixs_template = '''0 (User defined)
{solzen} {solaz} {viewzen} {viewaz} {month} {day}
8  (User defined H2O, O3)
{H2OSTR}, {O3}
{aermodel}
0
{AOT550}
{elev:.2f} (target level)
-{alt:.2f} (sensor level)
-{H2OSTR}, -{O3}
{AOT550}
-2 
{wlinf}
{wlsup}
0 Homogeneous surface
0 (no directional effects)
0
0
0
-1 No atm. corrections selected
'''


class SixSRT(TabularRT):
    """A model of photon transport including the atmosphere."""

    def __init__(self, config, statevector_names):

        TabularRT.__init__(self, config)
        self.sixs_dir = self.find_basedir(config)
        self.wl, self.fwhm = load_wavelen(config['wavelength_file'])
        self.sixs_grid_init = s.arange(self.wl[0], self.wl[-1]+2.5, 2.5)
        self.sixs_ngrid_init = len(self.sixs_grid_init)
        self.sixs_dir = self.find_basedir(config)
        self.params = {'aermodel': 1,
                       'AOT550': 0.01,
                       'H2OSTR': 0,
                       'O3': 0.40,
                       'day':   config['day'],
                       'month': config['month'],
                       'elev':  config['elev'],
                       'alt':   config['alt'],
                       'atm_file': None,
                       'abscf_data_directory': None,
                       'wlinf': self.sixs_grid_init[0]/1000.0,  # convert to nm
                       'wlsup': self.sixs_grid_init[-1]/1000.0}

        if 'obs_file' in config:
            # A special case where we load the observation geometry
            # from a custom-crafted text file
            g = Geometry(obs=config['obs_file'])
            self.params['solzen'] = g.solar_zenith
            self.params['solaz'] = g.solar_azimuth
            self.params['viewzen'] = g.observer_zenith
            self.params['viewaz'] = g.observer_azimuth
        else:
            # We have to get geometry from somewhere, so we presume it is
            # in the configuration file.
            for f in ['solzen', 'viewzen', 'solaz', 'viewaz']:
                self.params[f] = config[f]

        self.esd = s.loadtxt(config['earth_sun_distance_file'])
        dt = datetime(2000, self.params['month'], self.params['day'])
        self.day_of_year = dt.timetuple().tm_yday
        self.irr_factor = self.esd[self.day_of_year-1, 1]

        irr = s.loadtxt(config['irradiance_file'], comments='#')
        iwl, irr = irr.T
        irr = irr / 10.0  # convert, uW/nm/cm2
        irr = irr / self.irr_factor**2  # consider solar distance
        self.solar_irr = resample_spectrum(irr, iwl,  self.wl, self.fwhm)

        self.angular_lut_keys_degrees = ['OBSZEN','TRUEAZ','viewzen','viewaz',
            'solzen','solaz']

        self.lut_quantities = ['rhoatm', 'transm', 'sphalb', 'transup']
        self.build_lut()

        # This array is used to handle the potential indexing mismatch between
        # the 'global statevector' (which may couple multiple radiative 
        # transform models) and this statevector. It should never be modified
        full_to_local_statevector_position_mapping = []
        for sn in self.statevec:
            ix = statevector_names.index(sn)
            full_to_local_statevector_position_mapping.append(ix)
        self._full_to_local_statevector_position_mapping = \
            s.array(full_to_local_statevector_position_mapping)


    def find_basedir(self, config):
        """Seek out a sixs base directory."""

        if 'sixs_installation' in config:
            return config['sixs_installation']
        if 'SIXS_DIR' in os.getenv():
            return os.getenv('SIXS_DIR')
        return None

    def rebuild_cmd(self, point, fn):
        """."""

        # start with defaults
        vals = self.params.copy()
        for n, v in zip(self.lut_names, point):
            vals[n] = v

        # Translate a couple of special cases
        if 'H2OSTR' in self.lut_names:
            vals['h2o_mm'] = vals['H2OSTR']*10.0
        vals['elev'] = vals['elev']*-1

        # Check rebuild conditions: LUT is missing or from a different config
        sixspath = self.sixs_dir+'/sixsV2.1'
        scriptfilename = 'LUT_'+fn+'.sh'
        scriptfilepath = os.path.join(self.lut_dir, scriptfilename)
        infilename = 'LUT_'+fn+'.inp'
        infilepath = os.path.join(self.lut_dir, infilename)
        outfilename = fn
        outfilepath = os.path.join(self.lut_dir, outfilename)
        if os.path.exists(outfilepath) and os.path.exists(infilepath):
            raise FileExistsError('Files exist')

        if self.sixs_dir is None:
            logging.error('Specify a SixS installation')
            raise KeyError('Specify a SixS installation')

        # write config files
        sixs_config_str = sixs_template.format(**vals)
        with open(infilepath, 'w') as f:
            f.write(sixs_config_str)

        # Write runscript file
        with open(scriptfilepath, 'w') as f:
            f.write('#!/usr/bin/bash\n')
            f.write('%s < %s > %s\n' % (sixspath, infilepath, outfilepath))
            f.write('cd $cwd\n')

        return 'bash '+scriptfilepath

    def load_rt(self, fn):
        """Load the results of a SixS run."""

        with open(os.path.join(self.lut_dir, fn), 'r') as l:
            lines = l.readlines()

        with open(os.path.join(self.lut_dir, 'LUT_'+fn+'.inp'), 'r') as l:
            inlines = l.readlines()
            solzen = float(inlines[1].strip().split()[0])
        self.coszen = s.cos(solzen/360*2.0*s.pi)

        # Strip header
        for i, ln in enumerate(lines):
            if ln.startswith('*        trans  down   up'):
                lines = lines[(i + 1):(i + 1 + self.sixs_ngrid_init)]
                break

        solzens = s.zeros(len(lines))
        sphalbs = s.zeros(len(lines))
        transups = s.zeros(len(lines))
        transms = s.zeros(len(lines))
        rhoatms = s.zeros(len(lines))
        self.grid = s.zeros(len(lines))

        for i, ln in enumerate(lines):
            ln = ln.replace('*', ' ').strip()
            w, gt, scad, scau, salb, rhoa, swl, step, sbor, dsol, toar = \
                ln.split()

            self.grid[i] = float(w) * 1000.0  # convert to nm
            solzens[i] = float(solzen)
            sphalbs[i] = float(salb)
            transups[i] = 0.0  # float(scau)
            transms[i] = float(scau) * float(scad) * float(gt)
            rhoatms[i] = float(rhoa)

        results = {
            "solzen": resample_spectrum(solzens,  self.grid, self.wl, 
                    self.fwhm),
            "rhoatm": resample_spectrum(rhoatms,  self.grid, self.wl, 
                    self.fwhm),
            "transm": resample_spectrum(transms,  self.grid, self.wl, 
                    self.fwhm),
            "sphalb": resample_spectrum(sphalbs,  self.grid, self.wl, 
                    self.fwhm),
            "transup": resample_spectrum(transups, self.grid, self.wl, 
                    self.fwhm)}
        return results

    def ext550_to_vis(self, ext550):
        """."""

        return s.log(50.0) / (ext550 + 0.01159)

    def build_lut(self, rebuild=False):

        TabularRT.build_lut(self, rebuild)

        sixs_outputs = []
        for point, fn in zip(self.points, self.files):
            sixs_outputs.append(self.load_rt(fn))

        self.cache = {}
        dims_aug = self.lut_dims + [self.n_chan]
        for key in self.lut_quantities:
            temp = s.zeros(dims_aug, dtype=float)
            for sixs_output, point in zip(sixs_outputs, self.points):
                ind = [s.where(g == p)[0] for g, p in \
                    zip(self.lut_grids, point)]
                ind = tuple(ind)
                temp[ind] = sixs_output[key]

            self.luts[key] = VectorInterpolator(self.lut_grids, temp, 
                    self.lut_interp_types)

    def _lookup_lut(self, point):
        ret = {}
        for key, lut in self.luts.items():
            ret[key] = s.array(lut(point)).ravel()
        return ret

    def get(self, x_RT, geom):
        point = s.zeros((self.n_point,))
        for point_ind, name in enumerate(self.lut_grid_config):
            if name in self.statevec:
                ix = self.statevec.index(name)
                x_RT_ind = self._full_to_local_statevector_position_mapping[ix]
                point[point_ind] = x_RT[x_RT_ind]
            elif name == "OBSZEN":
                point[point_ind] = geom.OBSZEN
            elif name == "GNDALT":
                point[point_ind] = geom.GNDALT
            elif name == "viewzen":
                point[point_ind] = geom.observer_zenith
            elif name == "viewaz":
                point[point_ind] = geom.observer_azimuth
            elif name == "solaz":
                point[point_ind] = geom.solar_azimuth
            elif name == "solzen":
                point[point_ind] = geom.solar_zenith
            elif name == "TRUEAZ":
                point[point_ind] = geom.TRUEAZ
            elif name == 'phi':
                point[point_ind] = geom.phi
            elif name == 'umu':
                point[point_ind] = geom.umu
            else:
                # If a variable is defined in the lookup table but not
                # specified elsewhere, we will default to the minimum
                point[point_ind] = min(self.lut_grid_config[name])

        return self._lookup_lut(point)

    def get_L_atm(self, x_RT, geom):
        r = self.get(x_RT, geom)
        rho = r['rhoatm']
        rdn = rho / s.pi*(self.solar_irr * self.coszen)
        return rdn

    def get_L_down_transmitted(self, x_RT, geom):
        r = self.get(x_RT, geom)
        rdn = (self.solar_irr * self.coszen) / s.pi * r['transm']
        return rdn

    def get_L_up(self, x_RT, geom):
        """Thermal emission from the ground is provided by the thermal model, so
        this function is a placeholder for future upgrades."""
        return 0
