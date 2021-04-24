#!/usr/bin/python

#load libraries
import sys
from datetime import datetime, timedelta
import os.path
from dateutil import rrule

#Get relative path to subroutines
dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
sys.path.append(dirname+'/SubRoutines/')
from lst_cci_read import read_ncdf_variable #Use Karen's reader code as it works well
from lst_cci_read import read_ncdf_variable_units
from lst_cci_plot import plot_on_map_L3 # Subset of my plotting code based on Karen's code

#Hardcoded paths because this is a quick script
  #would normally be in a config file
datadir="/neodc/aast_leicester//data/CST_L3S_V2.1/daily/"
plotdir="/home/users/edodd01/plots/"

################################################################
#Read arguments and other required data

# read dates and site from arguements
if (len(sys.argv) != 2):
  print('run as: python AAST_read_and_plot.py startyr-startmn-startdy:endyr-endmn-enddy')
  exit()
sedate=sys.argv[1]
print(sedate)

#Get start and end date of run
sedates=sedate.split(':')

if len(sedates[0]) != len(sedates[1]):
  print("Length of date string arguements not equal. Something wrong, check command. Stopping.")
  exit()
if len(sedates[0]) != 10: # should only be the daily format
  print("Date format not as expected. Should be startyr-startmn-startdy:endyr-endmn-enddy.")
  exit()

tmp=sedates[0].split('-')
if tmp[2] == "00":
  print('Do not run with 00 in your date string, just run as yr:yr or yr-mn:yr-mn. stopping.')
  exit()
stdate=datetime.strptime(sedates[0],'%Y-%m-%d')
endate=datetime.strptime(sedates[1],'%Y-%m-%d')
interval = rrule.DAILY
info="DAILY"

###################################################################
#loop through data for that date, read and plot

for tmpdate in rrule.rrule(interval, dtstart=stdate, until=endate): #Loop through days/months/years between stdate and endate

  yr = tmpdate.strftime("%Y")
  mn = tmpdate.strftime("%m")
  dy = tmpdate.strftime("%d")

  filepath = datadir + '/' + yr + '/' + mn +'/' + dy +'/'
  fils = os.listdir(filepath)
  for f in fils:
    if "CST" in f: #only use the CST filetype as this has the Surface Temperatures in it

      ff = filepath + f

      #Read data
      lst=read_ncdf_variable(ff, "cst")
      lat=read_ncdf_variable(ff, "lat")
      lon=read_ncdf_variable(ff, "lon")
      lstunits=read_ncdf_variable_units(ff, "cst")

      #Plot
      cmap="seismic" #hopefully a more colourblind friendly map than jet
      ptype="png"
      dpi=300 #lower quality
      cbartitle="Combined Surface Temperature" +' ('+lstunits+')'
      fig = plot_on_map_L3(lst[0,:,:], lat, lon, cmap, cbartitle=cbartitle, title=f) 
      plotname = f.replace(".nc","")
      fig.savefig(plotdir + '/' + plotname+'.'+ptype, format=ptype, dpi=dpi)
      
print("DONE")
