## File reading routines for LST CCI project
## Date: 11 July 2019
## Authors: K L Veal

###############################################################################
## read variable from netcdf: opens file reads variable into numpy array and 
## closes file.

from netCDF4 import Dataset
import numpy

def read_ncdf_variable(filepath, varname, start=None, end=None):

   fid = Dataset(filepath, 'r')

   if start is None or end is None:
      values = fid.variables[varname][:]
   else:
      ndims = fid.variables[varname].ndim
      slices = [slice(start[i], end[i]) for i in range(ndims)]
      values = fid.variables[varname][slices]

   return values


###############################################################################

###############################################################################
## read variable from netcdf: opens file reads variable into numpy array and 
## closes file.

from netCDF4 import Dataset
import numpy

def read_ncdf_variable_units(filepath, varname):

   fid = Dataset(filepath, 'r')
   units = fid.variables[varname].units

   return units

#The below is used to read bit masks such as to find cloud data
#Author: Emma Dodd
def is_set(x, n):
    # a more bitwise- and performance-friendly version:
    return x & 1 << n != 0

