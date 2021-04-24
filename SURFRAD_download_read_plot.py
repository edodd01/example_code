#!/usr/bin/python

#load libraries

import sys
import os
import os.path
from dateutil import rrule
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

#Hardcoded paths because this is a quick script
  #would normally be in a config file
datadir="/home/users/edodd01/example_data/"
plotdir="/home/users/edodd01/plots/"
ftp="ftp://aftp.cmdl.noaa.gov/data/radiation/surfrad/"

################################################################
#Read arguments and other required data

# read dates and site from arguements

if (len(sys.argv) != 4):
  print('run as: python run_pipeline.py site_code startyr-startmn-startdy:endyr-endmn-enddy youremail_for_wget')
  exit()
site=sys.argv[1]
sedate=sys.argv[2]
email=sys.argv[3] #This would also go into a config file normally, but this is a public repo...

# check that the site code is valid, set paths and emissivity
surfradsites = ["bnd","tbl","dra","fpk","gwn","psu","sxf","sgp"]
ftp_name = ["Bondville_IL","Boulder_CO","Desert_Rock_NV","Fort_Peck_MT","Goodwin_Creek_MS","Penn_State_PA","Sioux_Falls_SD",""]
if site.lower() not in surfradsites: #make sure it copes with upper case input
  print("Site code not recognised. Possible site codes are: ")
  print(surfradsites)
  exit()
else:
  #So for SGP you need to go to the ARM site...
  if site.lower()=="sgp":
    print("Bad luck, you need to download this data manually from https://www.arm.gov/data.")
    exit()
  print("Running for site "+site.lower())
  #get index to get the correct ftp_name
  ind = surfradsites.index(site.lower())
  ftp_dir=ftp_name[ind]
  #According to the website, the BND site has filenames starting with bon...
  if site.lower() == "bnd":
    site = "bon" 

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
#download file if not present, read/process a day of data and plot it

for tmpdate in rrule.rrule(interval, dtstart=stdate, until=endate): #Loop through days/months/years between stdate and endate

  yr = tmpdate.strftime("%Y")
  mn = tmpdate.strftime("%m")
  dy = tmpdate.strftime("%d")
  doy = tmpdate.strftime("%j")

  #make the expected datafile name to be downloaded if not already in data folder
  infil = datadir + '/' + site.lower() + yr[2:4]+doy+".dat"
  if not os.path.isfile(infil): #if file not downloaded get the file
    print("downloading "+ site.lower() + yr[2:4]+doy+".dat") 
    #get file using wget and os
    os.system("wget -r -np -nH --cut-dirs=6 -nc -c --ftp-user=anonymous --ftp-password="+email+" "+ftp+'/'+ftp_dir+'/'+yr+'/'+site.lower() + yr[2:4]+doy+".dat -P "+datadir)
  
  #ok lets read the file using readlines() and get the data in BT format
  fil = open(infil,'r')
  lines = fil.readlines()
  count = 0 #because I know we have a header
  time=[]
  bt=[]
  bt_sky=[]
  sat=[]
  const_sigma = float(0.00000005670373)
  for line in lines:
    if count < 2: #ignore header
      count += 1
      continue
    words = line.split()

    #cast fill values to NAN, otherwise convert to a brightness temperature using the inverse of the Stefan-Boltzmann law
    if words[16] == "-9999.9":
      bt_sky.append(float('NaN'))
    else:
      bt_sky.append(float((float(words[16]) / const_sigma)**0.25)) #downwelling radiation

    if words[22] == "-9999.9":
      bt.append(float('NaN'))
    else:
      bt.append(float((float(words[22]) / const_sigma)**0.25)) #upwelling radiation

    #get the surface air temperature for comparison
    if words[38] == "-9999.9":
      sat.append(float('NaN'))
    else:
      sat.append(float(words[38]) + 273.15) #convert celcius to kelvin

    #get time in string format HH:MM for plotting
    time.append(words[4].zfill(2)+":"+words[5].zfill(2))
    count += 1

  #plot the daily data####################################
  print('plot')
  fig = plt.figure()
  ax = plt.axes()
  plt.plot(bt, 'g', label="Ground Brightness Temperature")
  plt.plot(bt_sky, 'b', label="Sky Brightness Temperature")
  plt.plot(sat, 'r', label="10m Air Temperature")
  plt.xlim([0, len(bt)]) #I assume bt and bt_sky should be the same size
  plt.title(site.lower() + " " + yr + '/' + mn + '/' + dy)
  plt.xlabel("Time (HH:MM)")
  plt.ylabel("Temperature (K)");
  plt.legend()
  #I want the x axis labels to be every 3 hours e.g. 00:00, 03:00...
  locs = []
  labels = []
  for i,t in enumerate(time):
    if t[3:] == "00":
      if int(t[0:2])%3 == 0:
        locs.append(i)
        labels.append(t)
  plt.xticks(locs, labels)
  locs, labels = plt.xticks() #lets make the x axis labels nicer
  plt.savefig(plotdir+site.lower() + yr[2:4]+doy+'.png')

print("DONE")
