"""
creates a skymap in healpix representation with data from GAIA.


    This work has made use of data from the European Space Agency (ESA)
    mission {\\it Gaia} (\\url{https://www.cosmos.esa.int/gaia}), processed by
    the {\\it Gaia} Data Processing and Analysis Consortium (DPAC,
    \\url{https://www.cosmos.esa.int/web/gaia/dpac/consortium}). Funding
    for the DPAC has been provided by national institutions, in particular
    the institutions participating in the {\\it Gaia} Multilateral Agreement..


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


import os.path
import healpy as hp
from ..gaia import create
from tqdm import tqdm
import numpy as np


class Gaia(object):
    """docstring for gaia"""
    def __init__(self, level, verbose=False):
        self.level = level
        self.verbose = verbose
        try:
            catalogname = 'healpixmap_level' + str(self.level) + '.txt'
            home = os.path.join(os.path.expanduser("~"), ".nsb/")
            filepath = os.path.join(home, catalogname)
            self.loadMap(filepath)
        except Exception as e:
            print('GAIA: ' + str(e))
            print('GAIA: Seems there is no gaia healpixmap with level %i.\n'
                  'GAIA: We will create a new one and try again.\n'
                  'GAIA: This might take a while...' % level)
            create.createMap(self.level)
            self.loadMap(filepath)
            # raise SystemExit

    def loadMap(self, filepath):
        if self.verbose:
            print('GAIA: Opening gaia catalog map...\t(reduce heaplix level if slow)')
        f = open(filepath)
        self.map = []
        for line in tqdm(f.readlines(), mininterval=0., disable=not self.verbose):
            if not line.startswith("#"):
                self.map.append([float(x) for x in line.split(',')])
            else:
                if "max_mag" in line:
                    max_mag = float(line.split("=")[1].strip())
                    if max_mag < 12:
                        message = "\nWARNING: This map was created from gaia star data with max Magnitude %.2f \n" % max_mag
                        print('\x1b[0;30;41m' + len(message) * '#')
                        print(message)
                        print("  -> consider deleting gaiamap.txt and healpixmap_level*.txt")
                        print("     in your HOME/.nsb/ directoy to download more next time")
                        print(len(message) * '#' + '\x1b[0m')
                    else:
                        print("GAIA: This map was created from star data with max Magnitude %.2f" % max_mag)
        f.close()
        self.map = np.array(self.map)
        self.hpmap = self.map[:, 4]

    def healpix(self, ra, dec):
        return hp.ang2pix(2**self.level, ra, dec, nest=True, lonlat=True) # DEGREES !!!

    def getBrightness(self, healpixid):
        return self.map[healpixid][4]

    def getFlux(self, healpixid):
        return self.map[healpixid][3]

    def getRa(self, healpixid):
        return self.map[healpixid][1]

    def getDec(self, healpixid):
        return self.map[healpixid][2]

    def getArcsec2(self, healpixid):
        return self.map[healpixid][5]

    def getNumber(self, healpixid):
        return self.map[healpixid][6]

    def getBrightness_FOV(self, ra, dec):
        healpixid = self.healpix(ra, dec)
        return self.map[tuple([healpixid])][:,4]

