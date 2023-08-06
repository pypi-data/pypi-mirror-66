
# nsb (Night Sky Backgound)

*****************************

This tool was developed during my PhD thesis at the Erlangen Center for Astroparticle Physics (ECAP) and the sky models were fitted to be used for or with the H.E.S.S. collaboration and their observation site in Namibia. For details find and read my thesis online.

Feel free to adapt the models to your own needs and let me know via mail, so we can include it into the package (There are plans to move to github to make those requests easier...)

The tool draws nightsky maps corresponding to KRISCIUNAS Model of the Brightness of Moonlight together with star data obtained from the GAIA public data release catalog. The result is a 2D Pixel array with physical brightness values for each sky position. Or estimate the brightness for a given source over a timespann.
Furthermore there are two advanced models specially fitted for the sky over H.E.S.S. in Namibia

The GAIA Data will we automatically downloaded via an query to the corresponding ESA server. The User has just decide how much to get. For calling sources 'by name' and storing their positions, nsb includes a sub packages 'mypycat'. Therefore a catalog is needed, which is not provided. Only a dummy file will be created and the user is free to add any source coordinates to  ~/.nsb/mypycat.txt

## Usage as commandline tool
```
python -m nsb [--OPTIONS] [--FLAGS]
python -m --help

--h --help prints this help message

--create CONFIGFILE
   writes a standard value configfile

options (can all be set in config):
--version MODEL_VERSION:
   determine which model to use. Choose from "krisciunas", "hess_basic", "hess_advanced"
--use CONFIGFILE:
   use a dedicated (non standard) configfile
--t1 --time DATETIME:
   time and date for which the map should be drawn
   format: 2010/12/24 23:59:59
--t2 --time_end DATETIME:
   needed for plots over a timestamp like --trend and --maxnsb
   format: 2010/12/24 23:59:59
--o --output /OUTPUT/DIRECTORY/
   for saving results in different place than working directory
   filenames will be generated automatically
--s --size IMAGESIZE:
   set the output Imagesize in Pixels
--altaz ALT AZ:
   set the observation position in the sky manually (unit: degrees)
--q --source SOURCENAME:
   set the observation position automatically on a source by name
   i.e.: "crab", "moon"
--l --location LOCATION:
   The observers coordinates (Lon Lat) on earth and elevation (unit: degrees and meters)
   format: 16.5028 -23.27280 1800.0
--hp LEVEL:
   HealPix Level for the gaia catalog to be plotted
   Integer in range [1:12]
--g --gauss KERNELSIZE:
   Gaussian Kernel in pixel to smoothen the model images
   format: 1.5

Flags:
(to steer programs the behaviour)
--verbose
   Do verbose printouts
--skymap
   create the skymap and show it on screen
--savefits
   save the Sky-Brightness Map as *.fits file
--maxnsb VALUE
   creates a plot of nsb vs. gained observation time.
   data points are additionally printed to console with --verbose.
   (NEEDS a --time_end, typically more than a year to be not influenced by the Seasons)
   format: 100.0
--trend
   creates a time trend plot of nsb and source position over the given timespan
   (NEEDS a --time_end)
   Source, Sun and Moon Setting/Rising times are printed to console with --verbose
```

For example plot and save the sky over H.E.S.S. for tonight:
```
python -m --time today 23:30:00 --skymap --savefits --version hess_basic --verbose 
```

Or see if observations of Crab are possible the next days:
```
python -m --t1 2020/01/01 12:00:00 --t2 2020/01/08 12:00:00 --trend --source "Crab" --version hess_currents --verbose
```

*****************************
# Use it as a library

see the following examples:

Creating Allsky and field-of-view map using the basic model, showing them on screen and saving them into FITS

```python
from nsb import config
from nsb.model import nsbModel
from nsb.mypycat import mypycat
from nsb.gaia import Gaia
from nsb.nsbtools import makeDateString, plotMaps
import ephem
import matplotlib.pyplot as plt
import astropy.io.fits as pyfits

con = config.TheConfiguration()
con.readStandardConfig()
# or read a custom config
# con.readConfig("my_config.cfg")

#time_and_date = makeDateString("today now")
time_and_date = ephem.Date("2019-01-26 21:29:07")

mpc = mypycat()
source = mpc.get("Crab Pulsar")

gaiamap = Gaia(level=8, verbose=True)
model = nsbModel(con, gaiamap, time_and_date, version="hess_basic", verbose=True)

# draw what you want
model.drawAllSky(size=800)
# show the results on screen
plotMaps(model.skymap.data, 'Allskymaps for %s' % (model.observer_source.date))

# draw something else:
model.drawFOV_source(source=source, fov=5.0, size=1000)
# show the results on screen
plotMaps(model.skymap.data, 'FOV for %s' % (model.observer_source.date))

# finally call show
plt.show()

# save fits files
hdul = pyfits.HDUList([model.skymap])
hdul.writeto("NSB_of_"+ makeDateString(time_and_date) + "_.fits", 'exception', True)
```



Or get all kind of values like brightness, Alt, Az, Phase, etc. over a timespan from the currents model


```python
from nsb import config
from nsb.model import nsbModel
from nsb.mypycat import mypycat
from nsb.gaia import Gaia
from nsb.nsbtools import plotTimespan
import ephem

con = config.TheConfiguration()
con.readStandardConfig()

time_and_date_1 = ephem.Date("2019/05/10 12:00:00")
time_and_date_2 = time_and_date_1 + 1.0  # plus one day (24h)

mpc = mypycat()
source = mpc.get("Eta Carinae")

gaiamap = Gaia(level=7)
model = nsbModel(con, gaiamap, time_and_date_1, time_and_date_2, version="hess_currents", threshold=400, timeresolution=15, verbose=False)
model.setSource(source=source)
model.calculateTimespan()

# now these arrays are available and filled
t = model.timestamps
b = model.bright
mp = model.moonphase
malt = model.moonalt
salt = model.sourcealt
maz = model.moonaz
saz = model.sourceaz
sunalt = model.sunalt
sunaz = model.sunaz
sep = model.separation

# TODO: anything you like with these values

# the plot from the --trend cmdline tool
plotTimespan(model)
```

*******
If there are questions, feel free to contact me: 

matthias.buechele[at]fau[dot]de

