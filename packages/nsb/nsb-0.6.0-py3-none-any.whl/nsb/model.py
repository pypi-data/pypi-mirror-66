"""
allskymaps python package.

Draws Allsky Nightsky Images with stars from the GAIA catalog

    This work has made use of data from the European Space Agency (ESA)
    mission {\\it Gaia} (\\url{https://www.cosmos.esa.int/gaia}), processed by
    the {\\it Gaia} Data Processing and Analysis Consortium (DPAC,
    \\url{https://www.cosmos.esa.int/web/gaia/dpac/consortium}). Funding
    for the DPAC has been provided by national institutions, in particular
    the institutions participating in the {\\it Gaia} Multilateral Agreement.

and draws moonlight corresponding to the Model from Krisciunas et al.

   author = {{Krisciunas}, K. and {Schaefer}, B.~E.},
    title = "{A model of the brightness of moonlight}",
  journal = {\pasp},
     year = 1991,
    month = sep,
   volume = 103,
    pages = {1033-1039},
      doi = {10.1086/132921},
   adsurl = {http://adsabs.harvard.edu/abs/1991PASP..103.1033K},


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

Created and maintained by Matthias Buechele [FAU].

"""

import numpy as np
import astropy.io.fits as pyfits
from astropy import units as u
from astropy.coordinates import SkyCoord
import ephem
import math
from scipy.ndimage import gaussian_filter, median_filter
from tqdm import tqdm
from . import nsbtools


class nsbModel():
    def __init__(self, conf, gaiamap, time1, time2=None, version="hess_basic", threshold=400, timeresolution=15, verbose=False):
        # create an PyEphem Observer and set the pressure to 0 -> No atmospheric corrections near the horizon
        self.observer_sun = ephem.Observer()
        self.observer_sun.pressure = 0
        self.observer_sun.horizon = conf.config['sun_below_horizon']
        self.observer_sun.lon, self.observer_sun.lat = conf.config['Lon'], conf.config['Lat']
        self.observer_sun.elevation = float(conf.config['elevation'])

        self.observer_moon = ephem.Observer()
        self.observer_moon.pressure = 0
        self.observer_moon.horizon = conf.config['moon_above_horizon']
        self.observer_moon.lon, self.observer_moon.lat = conf.config['Lon'], conf.config['Lat']
        self.observer_moon.elevation = float(conf.config['elevation'])

        self.observer_source = ephem.Observer()
        self.observer_source.pressure = 0
        self.observer_source.horizon = conf.config['source_above_horizon']
        self.observer_source.lon, self.observer_source.lat = conf.config['Lon'], conf.config['Lat']
        self.observer_source.elevation = float(conf.config['elevation'])

        self.moon = ephem.Moon()
        self.sun = ephem.Sun()
        self.source = None  # will be set later if needed

        # all the other stuff
        self.verbose = verbose
        self.offset = ephem.Date('0001/01/01 00:00:00')

        self.time_start = time1
        self.time_end = time2
        self.threshold = threshold
        self.timeresolution = timeresolution
        self.version = version
        if self.version == "hess_advanced":
            self.units = 'MHz'
        else:
            self.units = 'nLb'
        self.gaiamap = gaiamap

        self.setDate(self.time_start)

    def setSource(self, source, ra_offset=0.0, dec_offset=0.0):
        if source is None:
            raise SystemExit("No source given! Check your arguments!")
        else:
            self.pointing = source.name
            if source.name.lower().strip() == 'moon':
                self.source = self.moon
            else:
                self.source = ephem.FixedBody()
                if type(source.ra) is str:
                    self.source._ra, self.source._dec = source.ra, source.dec
                else:
                    self.source._ra, self.source._dec = ephem.hours(math.radians(source.ra)), ephem.degrees(math.radians(source.dec))

                self.source._ra += np.deg2rad(ra_offset)
                self.source._dec += np.deg2rad(dec_offset)
                self.source.name = source.name
                self.setDate(self.time_start)
                self.recomputeAll()
                coord = SkyCoord(ra=self.source._ra * u.rad, dec=self.source._dec* u.rad, frame='icrs')
                self.source_lon, self.source_lat = coord.galactic.l.value, coord.galactic.b.value
                healpixid = self.gaiamap.healpix(np.rad2deg(self.source._ra), np.rad2deg(self.source._dec))
                if self.verbose: print('* %s at \tzen %.2f\taz %.2f (healpix %i)' % (self.source.name, np.rad2deg(np.pi / 2 - self.source.alt), np.rad2deg(self.source.az), healpixid))

    def writeFitsHeader(self, fov):
        self.skymap.header['sunalt'] = (np.rad2deg(self.sun.alt), 'Degrees')
        self.skymap.header['sunaz'] = (np.rad2deg(self.sun.az), 'Degrees')
        self.skymap.header['moonalt'] = (np.rad2deg(self.moon.alt), 'Degrees')
        self.skymap.header['moonaz'] = (np.rad2deg(self.moon.az), 'Degrees')
        self.skymap.header['moonph'] = (self.moon.moon_phase, 'Moon Phase as Fraction of illuminated Surface')
        if self.source is not None:
            self.skymap.header['alt'] = (np.rad2deg(self.source.alt), 'Degrees (Pointing)')
            self.skymap.header['az'] = (np.rad2deg(self.source.az), 'Degrees (Pointing)')
            self.skymap.header['source'] = (self.pointing, 'Name of pointed source (if available)')
        # self.skymap.header['extinc'] = (self.k, 'Extincion Coefficient used')
        self.skymap.header['bzero'] = (0, " ")
        self.skymap.header['date'] = (str(self.time_start), ' ')
        self.skymap.header['lat'] = (str(self.observer_source.lat), 'Observer GPS Position')
        self.skymap.header['lon'] = (str(self.observer_source.lon), 'Observer GPS Position')
        self.skymap.header['elev'] = (self.observer_source.elevation, 'Observer Elevation [m above NN]')
        self.skymap.header['units'] = (self.units)
        self.skymap.header['model'] = (self.version, 'Name of NSB model')
        self.skymap.header['fov'] = (str(fov), 'Degrees')

    def drawAllSky(self, size=400):
        a = np.empty((size, size))
        a.fill(np.nan)
        self.skymap = pyfits.PrimaryHDU(a)
        self.writeFitsHeader(fov=180.0)
        self.skymap.data = self.getAllSky(size)

    def getAllSky(self, size):
        resolution = math.radians(180) / size
        offset_zen = 0
        offset_az = 0
        offset_x = 0
        offset_y = -offset_zen * (1 / resolution)
        return self.getMapData(size, offset_x, offset_y, offset_az, offset_zen, resolution, silent=not self.verbose)

    def drawFOV_source(self, source, fov=5.0, size=10, ra_offset=0.0, dec_offset=0.0):
        self.setSource(source, ra_offset=ra_offset, dec_offset=dec_offset)
        a = np.empty((size, size))
        a.fill(np.nan)
        self.skymap = pyfits.PrimaryHDU(a)
        self.writeFitsHeader(fov=fov)
        self.skymap.data = self.getFOV_source(fov=fov, size=size)

    def drawFOV_altaz(self, alt, az, fov=5.0, size=10):
        a = np.empty((size, size))
        a.fill(np.nan)
        self.skymap = pyfits.PrimaryHDU(a)
        self.writeFitsHeader(fov=fov)
        self.skymap.data = self.getFOV_altaz(alt, az, fov=fov, size=size)

    def getFOV_altaz(self, pointing_alt, pointing_az, fov, size):
        off_x = 6
        off_y = 3

        resolution = math.radians(fov) / size
        offset_zen = float(np.pi/2 - pointing_alt)
        offset_az = float(pointing_az) - np.deg2rad(1.83)
        offset_x = 0 - off_x
        offset_y = -offset_zen * (1 / resolution) - off_y
        return self.getMapData(size, offset_x, offset_y, offset_az, offset_zen, resolution, silent=not self.verbose)

    def getFOV_source(self, fov, size):
        resolution = math.radians(fov) / size
        offset_zen = float(np.pi/2 - self.source.alt)
        offset_az = float(self.source.az)
        offset_x = 0
        offset_y = -offset_zen * (1 / resolution)
        return self.getMapData(size, offset_x, offset_y, offset_az, offset_zen, resolution, silent=not self.verbose)

    def getMapData(self, size, offset_x, offset_y, offset_az, offset_zen, resolution, silent=True):
        sunalt = float(self.sun.alt)
        if sunalt > 0:
            sunset = self.observer_source.next_setting(self.sun)
            # print fancy red error message
            if not silent:
                message = 5 * '#' + ' Sun still up! Next sunset at %s ' % sunset + 5 * '#'
                print('\x1b[0;30;41m' + len(message) * '#')
                print(message)
                print(len(message) * '#' + '\x1b[0m')

            return np.zeros((size, size))

        elif sunalt < 0 and sunalt > math.radians(-18.0):
            # print fancy red error message
            if not silent:
                message = 5 * '#' + ' Sunlight might have influence! sun alt= %.2f deg ' % np.rad2deg(sunalt) + 5 * '#'
                print('\x1b[0;30;41m' + len(message) * '#')
                print(message)
                print(len(message) * '#' + '\x1b[0m')

            return np.zeros((size, size))

        else:
            # Model drawing starts here:
            data = np.empty((size, size))
            data.fill(np.nan)
            for x in tqdm(range(size), disable=silent):
                for y in range(size):
                    az = (math.atan2((x - size / 2. - offset_x),
                                     (y - size / 2. - offset_y)) + offset_az)
                    zen = math.hypot((x - size / 2. - offset_x),
                                     (y - size / 2. - offset_y)) * resolution
                    if (zen > math.radians(90.0)):
                        continue
                    else:
                        moondist = nsbtools.greatCircle(zen, az, np.pi / 2. - self.moon.alt, self.moon.az)
                        if moondist > math.radians(20.0) and nsbtools.greatCircle(zen, az, offset_zen, offset_az) < resolution*size / 2:
                            data[y, x] = self.model(zen=zen, az=az, version=self.version)
            return data

    def model(self, zen, az, version="hess_currents"):
        def X(Z):
            if Z <= math.pi/2:
                return (1 - 0.96 * (math.sin(Z))**2)**(-0.5)
            else:
                return (1 - 0.96 * 1)**(-0.5)
        """
        def X(Z):
            if Z <= math.pi/2:
                return 0.4 + 0.6 * (1 - 0.96 * (math.sin(Z))**2)**(-0.5)
            else:
                return 0.4 + 0.6 * (1 - 0.96 * 1)**(-0.5)

        def X(Z):
            # Rozenberg 1996
            return 1 / (np.cos(Z) + 0.025 * np.exp(-11 * np.cos(Z)))
        """

        def f(rho, A, B, C):
            r = np.rad2deg(rho)
            return 10**A * (1.06 + (math.cos(rho))**2) + 10**(B - r / 40) + C * (10**7) * rho**(-2)

        def I_moon(moon_alpha):
            a = np.rad2deg(moon_alpha)
            return 10**(-0.4 * (3.84 + 0.026 * math.fabs(a) + 4 * 10**(-9) * a**4))

        def B_sky(Zen, phi, B_zero, k):
            """
            Krisciunas et. al Sky-only-Model
            Brightness of the Sky at certain position without moon
            """
            if Zen < np.pi / 2:
                return B_zero * X(Zen) * 10**(-0.4 * k * (X(Zen) - 1))
            else:
                return 0

        def B_moon(Zen, phi, Zen_moon, phi_moon, k, moon_alpha, A, B, C, version="basic"):
            """
            Moon-Model from Krisciunas et. al  and altered versions of it
            only valid for moon above horizon. it gives values for negative moon alt,
            but they have no physical meaning.
            --> so in that case better return 0
            """
            if version == "basic":
                if Zen_moon < np.pi / 2:
                    rho = nsbtools.greatCircle(Zen, phi, Zen_moon, phi_moon)
                    return f(rho, A, B, C) * I_moon(moon_alpha) * 10 ** (-0.4 * k * X(Zen_moon)) * (1 - 10 ** (-0.4 * k * X(Zen)))
                else:
                    return 0

            elif version == "advanced":
                # cheat a little with the moon altitude to get a more realistic moon rise
                moon_horizon = -4.346
                Zm = Zen_moon + float(np.deg2rad(moon_horizon))

                if Zm < np.pi / 2:
                    rho = nsbtools.greatCircle(Zen, phi, Zm, phi_moon)
                    return f(rho, A, B, C) * I_moon(moon_alpha) * (1 - 10 ** (-0.4 * k * X(Zen))) * (10 ** (-0.4 * k * X(Zm)) - 10 ** (-0.4 * k * X(np.pi / 2)))
                else:
                    return 0

            else:
                raise NotImplementedError("wrong or no model version given!")


        ra, dec = self.observer_source.radec_of(az, math.pi / 2 - zen)
        healpixid = self.gaiamap.healpix(np.rad2deg(ra), np.rad2deg(dec))

        if version == "krisciunas":
            A = 5.36
            B = 6.15
            C = 0
            B_0 = 79.0
            k = 0.172
            return (B_moon(zen, az, np.pi / 2. - self.moon.alt, self.moon.az, k, self.moon_alpha, A, B, C, "basic") +
                    B_sky(zen, az, B_0, k))

        elif version == "hess_basic":
            A = 5.1276
            B = 5.9596
            C = 0.0
            B_0 = 52
            k = 0.479
            return (B_moon(zen, az, np.pi / 2. - self.moon.alt, self.moon.az, k, self.moon_alpha, A, B, C, "basic") +
                    B_sky(zen, az, B_0, k) +
                    nsbtools.MagnLb(self.gaiamap.getBrightness(healpixid)))

        elif version == "hess_currents":
            A = 5.1276
            B = 5.9596
            k = 0.293
            p_0 = 49.204
            p_1 = 0.952
            p_2 = 1.520
            return (p_1*B_moon(zen, az, np.pi / 2. - self.moon.alt, self.moon.az, k, self.moon_alpha, A, B, 0, "advanced") +
                    B_sky(zen, az, p_0, k) +
                    p_2*nsbtools.MagnLb(self.gaiamap.getBrightness(healpixid)))
        else:
            raise NotImplementedError("wrong or no model version given!")

    def smooth_gauss(self, sigma):
        self.skymap.data = gaussian_filter(self.skymap.data, sigma=sigma)

    def median_filter(self, size):
        self.skymap.data = median_filter(self.skymap.data, size=int(size))

    def getStatistics(self):
        median_sky_brightness, mean_sky_brightness = np.nanmedian(self.skymap.data), np.nanmean(self.skymap.data)
        if not np.isnan(median_sky_brightness) and not np.isnan(mean_sky_brightness):
            self.skymap.header['median'] = (median_sky_brightness, 'Median Image Brightness')
            self.skymap.header['mean'] = (mean_sky_brightness, 'Mean Image Brightness')

        return median_sky_brightness, mean_sky_brightness

    def setDate(self, date):
        self.observer_source.date = date
        self.observer_moon.date = date
        self.observer_sun.date = date
        self.recomputeAll()

    def recomputeAll(self):
        if self.source is not None:
            self.source.compute(self.observer_source)
        self.moon.compute(self.observer_moon)
        self.moon_alpha = math.acos(self.moon.moon_phase * 2 - 1)
        self.sun.compute(self.observer_sun)

    def calculateTimespan_fast(self, moonallowed=True):
        self.setDate(self.time_start)
        self.bright = []
        self.moonphase = []
        self.moonalt = []
        self.sourcealt = []
        self.moonaz = []
        self.sourceaz = []
        self.separation = []

        t = self.time_start
        self.setDate(t)

        while t < self.time_end:

            if self.sun.alt > self.observer_sun.horizon:
                t = self.observer_sun.next_setting(self.sun)
                self.setDate(t)

            elif self.source.alt > self.observer_source.horizon and moonallowed:
                self.bright.append(self.model(zen=np.pi / 2 - self.source.alt, az=self.source.az, version=self.version))
                self.moonphase.append(self.moon.moon_phase)
                self.moonalt.append(np.rad2deg(self.moon.alt))
                self.moonaz.append(np.rad2deg(self.moon.az))
                self.sourcealt.append(np.rad2deg(self.source.alt))
                self.sourceaz.append(np.rad2deg(self.source.az))

                self.separation.append(np.rad2deg(nsbtools.greatCircle(np.pi / 2. - self.source.alt,
                                                                         self.source.az,
                                                                         np.pi / 2. - self.moon.alt,
                                                                         self.moon.az)))

            elif not moonallowed and self.source.alt > self.observer_source.horizon and self.moon.alt < self.observer_moon.horizon:
                self.bright.append(self.model(zen=np.pi / 2 - self.source.alt, az=self.source.az, version=self.version))
            else:
                pass

            t += 1.0 / (24 * (60 / self.timeresolution))
            self.setDate(t)

    def calculateTimespan(self):
        self.setDate(self.time_start)
        self.timestamps = []
        self.bright = []
        self.moonphase = []
        self.moonalt = []
        self.sourcealt = []
        self.moonaz = []
        self.sourceaz = []
        self.sunalt = []
        self.sunaz = []
        self.separation = []

        t = self.time_start
        while t < self.time_end:
            self.setDate(t)
            self.timestamps.append(t - self.time_start)
            if self.source.alt > self.observer_source.horizon and self.sun.alt < self.observer_sun.horizon:
                self.bright.append(self.model(zen=np.pi / 2 - self.source.alt, az=self.source.az, version=self.version))
            else:
                self.bright.append(np.nan)

            self.moonphase.append(self.moon.moon_phase * 100)
            self.moonalt.append(np.rad2deg(self.moon.alt))
            self.moonaz.append(np.rad2deg(self.moon.az))
            self.sourcealt.append(np.rad2deg(self.source.alt))
            self.sourceaz.append(np.rad2deg(self.source.az))
            self.sunalt.append(np.rad2deg(self.sun.alt))
            self.sunaz.append(np.rad2deg(self.sun.az))

            if self.source.alt > self.observer_source.horizon and self.moon.alt > self.observer_moon.horizon:
                self.separation.append(np.rad2deg(nsbtools.greatCircle(np.pi / 2. - self.source.alt,
                                                                         self.source.az,
                                                                         np.pi / 2. - self.moon.alt,
                                                                         self.moon.az)))
            else:
                self.separation.append(np.nan)

            t += 1.0 / (24 * (60 / self.timeresolution))

        t = self.time_start - 1
        self.setDate(self.time_start)
        #self.recomputeAll()
        self.sunset = []
        self.sunrise = []
        while t < self.time_end:
            self.observer_sun.date = t
            sr = self.observer_sun.next_rising(self.sun)
            ss = self.observer_sun.next_setting(self.sun)

            t = ss + 0.25
            self.sunrise.append([float(sr - self.time_start), str(sr) + ' \tSunrise'])
            self.sunset.append([float(ss - self.time_start), str(ss) + ' \tSunset'])

        t = self.time_start - 1
        self.setDate(self.time_start)
        #self.recomputeAll()
        self.moonset = []
        self.moonrise = []
        while t < self.time_end:
            self.observer_moon.date = t
            mr = self.observer_moon.next_rising(self.moon)
            ms = self.observer_moon.next_setting(self.moon)
            t = ms + 0.25
            self.moonrise.append([float(mr - self.time_start), str(mr) + ' \tMoonrise'])
            self.moonset.append([float(ms - self.time_start), str(ms) + ' \tMoonset'])

        t = self.time_start
        self.setDate(self.time_start)
        #self.recomputeAll()
        self.sourceset = []
        self.sourcerise = []
        while t < self.time_end:
            self.observer_source.date = t
            sor = self.observer_source.next_rising(self.source)
            sos = self.observer_source.next_setting(self.source)
            t = sos + 0.25
            self.sourceset.append([float(sos - self.time_start), str(sos) + ' \tSet of ' + self.source.name])
            self.sourcerise.append([float(sor - self.time_start), str(sor) + ' \tRise of ' + self.source.name])
