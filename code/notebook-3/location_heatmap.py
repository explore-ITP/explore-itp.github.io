#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 09:46:36 2020

@author: larabreitkreutz
"""

#1 LAT by 1 LON grid
import pandas as pd
import math
import numpy as np

 
filename = "/Users/larabreitkreutz/PythonGIS/rawlocs/mastercsv.csv"
df = pd.read_csv(filename, encoding='utf-8')
df_short = df.head(100)

#this import works!
import plotly.io as pio
pio.renderers.default = "browser"


BBox = (-180, 180, 60, 90)

#create matrix with lat/lon bounds appropriate for Arctic Ocean
df_zero = pd.DataFrame(0, index=np.arange(BBox[2], BBox[3]+1), columns=np.arange(BBox[0],BBox[1]+1))

#change parameters here
BBox = (-180, 180, 60, 90)
latmin = float(BBox[2])
latmax = float(BBox[3])
latbins = (int(latmax-latmin))

lonmin = float(BBox[0])
lonmax = float(BBox[1])
lonbins = (int(lonmax-lonmin))

#create filelist, where files will be opened and analyzed
import pathlib
import os

filelist = []
for path in pathlib.Path(os.path.dirname(os.path.abspath('___file___'))).iterdir():
    print(path)
    folder_str = str(path)
    if not folder_str.endswith('.zip'):
         if not folder_str.endswith('.csv'):
             if not folder_str.endswith('.py'):
                 if not folder_str.endswith('.ipynb'):
                     if not folder_str.endswith('.DS_Store'):
                         if not folder_str.endswith('checkpoints'):
                             if 'rawlocs' in folder_str:
                                 folder = os.path.basename(folder_str)
                                 filelist.append(folder)                  

for filename in filelist:
    find_data = os.path.dirname(os.path.abspath('__file__'))
    find_data_two= os.path.join(find_data, filename)
     
    original_data = [i.strip().split() for i in open(find_data_two).readlines()]
    obs_data = original_data[1:-1]
    

    #round the lat/lon values within the data, so that they can be easily placed in matrix
    #find location and add count to grid cell
    for obs in obs_data:
        if obs[2] != 'NaN' and obs[3] != 'NaN': 
            year = obs[0]
            lon = obs[2]
            lat = obs[3]
            lon_r = math.ceil(float(lon))
            lat_r = math.ceil(float(lat))
            if BBox[2] <= lat_r <= BBox[3] and BBox[0] <= lon_r <= BBox[1]:
                current = df_zero.loc[lat_r, lon_r]
                updated = current+1
                df_zero.at[lat_r, lon_r] = updated
            else:
                continue
          
    
#make heatmap
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(dpi=3000)
ax=sns.heatmap(df_zero, fmt='d', cmap="Blues", cbar_kws={'label': 'Number of Observations in Coordinate Gridspace'}, xticklabels = 15, yticklabels = 2)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Location Density of All ITP Machines')
ax.invert_yaxis()





#ALTERNATIVE METHOD, takes a lot longer to run

#get bins into lists, to make DataFrame
df_zero_lat = np.linspace(latmin,latmax,latbins,endpoint=False)
rows = df_zero_lat.tolist()
df_zero_lon = np.linspace(lonmin,lonmax,lonbins,endpoint=False)
cols = df_zero_lon.tolist()

#append last column to each row
rows.append(90.0)
cols.append(180.0)

#create DataFrame with bins constructed above
matrix_dens  = pd.DataFrame(0, index=rows, columns=cols)
#reverse the latitudes
matrix_dens = matrix_dens.reindex(index=matrix_dens.index[::-1])

lat_list = []
lon_list = []

for filename in filelist:
    find_data = os.path.dirname(os.path.abspath('__file__'))
    find_data_two= os.path.join(find_data, filename)
     
    #reconstruct data into pandas dataframe
    original_data = [i.strip().split() for i in open(find_data_two).readlines()]
    obs_data = original_data[1:-1]
    obs_dataframe = pd.DataFrame(obs_data, columns=('Year', 'YearFrac', 'Lon', 'Lat'))

    for obs in obs_data:
        lat_list.append(float(obs[3]))
        lon_list.append(float(obs[2]))

lat_list2 = [y for y in lat_list if str(y) != 'NaN']
lon_list2 = [x for x in lon_list if str(x) != 'NaN']

for x, y in zip(lon_list2, lat_list2):

    if latmin <= y <= latmax and lonmin <= x <= lonmax:
        x_ind = float(np.floor(x))
        y_ind = float(np.floor(y))
        matrix_dens[x_ind][y_ind] += 1
    else:
        continue


#BELOW I tried to add a basemap to this heatmap, which would mean the grids would need to change shape...didnt work
#trying out https://medium.com/@tiofaizintio/how-to-visualize-spatial-point-based-data-and-its-density-with-python-basemap-bfe6d9da76df
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap



#declare basemap parameters
bmap = Basemap(projection='ortho',lat_0=90,lon_0=0,resolution='l') 
#Kernel restarts HERE
fig=plt.figure(figsize=(20,15))
bmap.drawcoastlines(linewidth=1)
bmap.drawstates()
bmap.drawcountries()
parallels = np.arange(-15,15,10)
bmap.drawparallels(parallels,labels=[False,True,True,False],fontsize=16)
meridians = np.arange(90,150,10)
bmap.drawmeridians(meridians,labels=[True,False,False,True],fontsize=16)

#trying out another tutorial
#https://towardsdatascience.com/mapping-with-matplotlib-pandas-geopandas-and-basemap-in-python-d11b57ab5dac

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd

fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='ortho', resolution='h', 
            lat_0=90, lon_0=0,
            width=1.05E6, height=1.2E6)
m.shadedrelief()
    
