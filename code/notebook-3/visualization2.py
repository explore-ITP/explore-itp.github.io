#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 09:46:36 2020

@author: larabreitkreutz
"""

import pathlib
import os
import pandas as pd
import math
import numpy as np
import plotly.io as pio
pio.renderers.default = "browser"

 
filename = #download and add "ALL_main_downsamp.csv"
df = pd.read_csv(filename, encoding='utf-8')

# Identifies coordinate bounds
BBox = (-180, 180, 60, 90)

# Creates empty dataframe with rows and columns representing lat/lon values appropriate for Arctic Ocean
df_zero = pd.DataFrame(0, index=np.arange(BBox[2], BBox[3]+1), columns=np.arange(BBox[0],BBox[1]+1))

# Identifies necessary variables for bounds
BBox = (-180, 180, 60, 90)
latmin = float(BBox[2])
latmax = float(BBox[3])
latbins = (int(latmax-latmin))

lonmin = float(BBox[0])
lonmax = float(BBox[1])
lonbins = (int(lonmax-lonmin))

# Creates filelist, where files will be opened and analyzed
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

# Iterates through rawlocs files and reads data
for filename in filelist:
    find_data = os.path.dirname(os.path.abspath('__file__'))
    find_data_two= os.path.join(find_data, filename)
     
    original_data = [i.strip().split() for i in open(find_data_two).readlines()]
    obs_data = original_data[1:-1]
    

    # Rounds the lat/lon values within the data, so that they can be easily placed in matrix
    # Finds location and adds 1 count to grid cell
    for obs in obs_data:
        if obs[2] != 'NaN' and obs[3] != 'NaN': 
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
          
# Make heatmap
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(dpi=3000)
ax=sns.heatmap(df_zero, fmt='d', cmap="RdYlBu_r", cbar_kws={'label': 'Number of Observations in Coordinate Gridspace'}, xticklabels = 15, yticklabels = 2)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Location Density of All ITP Machines')
ax.invert_yaxis()
    

 # Change colormap of plot by inserting one of the following into cmap: [‘Accent’, ‘Accent_r’, ‘Blues’, ‘Blues_r’, ‘BrBG’, ‘BrBG_r’, ‘BuGn’, ‘BuGn_r’, ‘BuPu’, ‘BuPu_r’, 
 # ‘CMRmap’, ‘CMRmap_r’, ‘Dark2’, ‘Dark2_r’, ‘GnBu’, ‘GnBu_r’, ‘Greens’, ‘Greens_r’, ‘Greys’, ‘Greys_r’, ‘OrRd’, 
 # ‘OrRd_r’, ‘Oranges’, ‘Oranges_r’, ‘PRGn’, ‘PRGn_r’, ‘Paired’, ‘Paired_r’, ‘Pastel1’, 
 # ‘Pastel1_r’, ‘Pastel2’, ‘Pastel2_r’, ‘PiYG’, ‘PiYG_r’, ‘PuBu’, ‘PuBuGn’, ‘PuBuGn_r’, 
 # ‘PuBu_r’, ‘PuOr’, ‘PuOr_r’, ‘PuRd’, ‘PuRd_r’, ‘Purples’, ‘Purples_r’, ‘RdBu’, ‘RdBu_r’, 
 # ‘RdGy’, ‘RdGy_r’, ‘RdPu’, ‘RdPu_r’, ‘RdYlBu’, ‘RdYlBu_r’, ‘RdYlGn’, ‘RdYlGn_r’, ‘Reds’, 
 # ‘Reds_r’, ‘Set1’, ‘Set1_r’, ‘Set2’, ‘Set2_r’, ‘Set3’, ‘Set3_r’, ‘Spectral’, ‘Spectral_r’, 
 # ‘Wistia’, ‘Wistia_r’, ‘YlGn’, ‘YlGnBu’, ‘YlGnBu_r’, ‘YlGn_r’, ‘YlOrBr’, ‘YlOrBr_r’, ‘YlOrRd’, 
 # ‘YlOrRd_r’, ‘afmhot’, ‘afmhot_r’, ‘autumn’, ‘autumn_r’, ‘binary’, ‘binary_r’, ‘bone’, 
 # ‘bone_r’, ‘brg’, ‘brg_r’, ‘bwr’, ‘bwr_r’, ‘cividis’, ‘cividis_r’, ‘cool’, ‘cool_r’, ‘coolwarm’, ‘coolwarm_r’, ‘copper’, ‘copper_r’,
 # ‘cubehelix’, ‘cubehelix_r’, ‘flag’, ‘flag_r’, ‘gist_earth’, ‘gist_earth_r’, ‘gist_gray’, ‘gist_gray_r’, ‘gist_heat’, ‘gist_heat_r’, ‘gist_ncar’, ‘gist_ncar_r’,
 # ‘gist_rainbow’, ‘gist_rainbow_r’, ‘gist_stern’, ‘gist_stern_r’, ‘gist_yarg’, 
 # ‘gist_yarg_r’, ‘gnuplot’, ‘gnuplot2’, ‘gnuplot2_r’, ‘gnuplot_r’, ‘gray’, ‘gray_r’,
 # ‘hot’, ‘hot_r’, ‘hsv’, ‘hsv_r’, ‘icefire’, ‘icefire_r’, ‘inferno’, 
 # ‘inferno_r’, ‘magma’, ‘magma_r’, ‘mako’, ‘mako_r’, 
 # ‘nipy_spectral’, ‘nipy_spectral_r’, ‘ocean’, ‘ocean_r’, ‘pink’, ‘pink_r’,
 # ‘plasma’, ‘plasma_r’, ‘prism’, ‘prism_r’, ‘rainbow’, ‘rainbow_r’,
 # ‘rocket’, ‘rocket_r’, ‘seismic’, ‘seismic_r’, ‘spring’, ‘spring_r’,
 # ‘summer’, ‘summer_r’, ‘tab10’, ‘tab10_r’, ‘tab20’, ‘tab20_r’, ‘tab20b’,
 # ‘tab20b_r’, ‘tab20c’, ‘tab20c_r’, ‘terrain’, ‘terrain_r’, ‘twilight’,
 # ‘twilight_r’, ‘twilight_shifted’, ‘twilight_shifted_r’, ‘viridis’, ‘viridis_r’, ‘vlag’, ‘vlag_r’, ‘winter’, ‘winter_r’]
