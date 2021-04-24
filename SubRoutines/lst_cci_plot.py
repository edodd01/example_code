## Plotting routines for LST CCI project
## Date: 11 July 2019
## Authors: K L Veal and E Dodd

###############################################################################

## plot 2D array on map

def plot_on_map_L3(data, lat, lon, cmapt, cbartitle=None, title=None, centrelon = None):

   import numpy as np
   import numpy.ma as ma
   import matplotlib.pyplot as plt
   plt.switch_backend('agg')
   import matplotlib.ticker as mticker
   import cartopy.crs as ccrs
   from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
   from cartopy.feature import LAND
   #Get relative path to subroutines
   import os
   import sys
   dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
   os.environ["CARTOPY_USER_BACKGROUNDS"] =  dirname+'/Blue_marble_data/BlueMarbleNG-TB/'

   proj = ccrs.Stereographic(central_latitude=90.0)
   ax = plt.axes(projection=proj)
   ax.coastlines()

   gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
   gl.top_labels = False
   gl.left_labels = False
   gl.xlocator = mticker.FixedLocator([-180, -120, -60, 0, 60, 120, 180])
   gl.ylocator = mticker.FixedLocator([-90, -60, -30, 0, 30, 60, 90])
   gl.xformatter = LONGITUDE_FORMATTER
   gl.yformatter = LATITUDE_FORMATTER
  
   mi=data.min()
   ma=data.max()

   mapped = plt.pcolormesh(lon, lat, data, cmap=cmapt, vmin=mi, vmax=ma, transform=ccrs.PlateCarree())
   cbar = plt.colorbar(mapped, ax=ax, orientation='horizontal', pad=0.05, extend='both')

   if cbartitle is not None:
      cbar.set_label(cbartitle)

   #Maximize and save PNG file
   if title is not None:
      plt.title(title)
      ax.xaxis.labelpad = 20
      plt.gcf().subplots_adjust(bottom=0.00)

   fig = plt.gcf()
   return fig

###############################################################################
