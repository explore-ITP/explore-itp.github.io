#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 11:27:00 2020

@author: larabreitkreutz
"""

import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
pio.renderers.default = "browser"
 
# Reads in data from master CSV
filename = "/Users/larabreitkreutz/PythonGIS/rawlocs/mastercsv.csv"
df = pd.read_csv(filename, encoding='utf-8')

# Creates list of colors, chosen to match other visualizations
colors = ['#7dcbb8', '#9786a0', '#79e788', '#dd7798', '#75ccea', '#3d8198']
  
# Defines focal latitute and longitude points
lat_foc = 80
lon_foc = -170        

# Creates three lists that corresppond to subsets of ITP machines
early = [1,6,8]
mid = [41,48,49]
late = [86,91,92]

# Creates data subsets that correspond to early, middle, and late-stage deployments
early_df = df.loc[df['ITP'].isin(early)]
mid_df = df.loc[df['ITP'].isin(mid)]
late_df = df.loc[df['ITP'].isin(late)]

#From here, make one figure at a time, using the data subsets above. Use '#' to comment out all but one dataframe at a time.
fig = go.Figure()
cols = early_df['ITP'].unique()
#cols = mid_df['ITP'].unique()
#cols = late_df['ITP'].unique()

# Iterates through list of columns and creates a dataframe with a column for ITP number
rslt_df=[]
ind=1
for n in cols:
    rslt_df = df.loc[df['ITP'] == n]
    # Creates figure trace for each ITP machine
    fig.add_trace(
    go.Scattergeo(
            mode= "markers", 
              name= str(n), 
              lat= rslt_df['Lat'], 
              lon= rslt_df['Long'], 
              marker_size=5,
              marker_color= colors[ind],
              opacity=.75
              ))
    ind=ind+1
    
# Updates figure layout
fig.update_layout(
    geo=dict(
            landcolor= "rgb(212, 212, 212)", 
            showcountries= True,
            countrycolor= "rgb(245, 245, 245)",
           ),
    width= 800, 
    height= 700)

# Changes projection, updates colors, shows latitutde and longitude grid
fig.update_geos(projection_type="orthographic",
                fitbounds="locations",
                showcoastlines=True, coastlinecolor="White",
    showland=True, landcolor="#576b6c",
    showocean=True, oceancolor="#383d3d",
    showlakes=True, lakecolor="#122525",
    showrivers=True, rivercolor="#122525",
    lataxis_showgrid=True, lonaxis_showgrid=True)

# Adds and styles title and legend. Use '#' to comment out all but one title at a time.
fig.update_layout(
    title="Comparing a Subset of Early Drift Tracks",
    #title="Comparing a Subset of Mid-Stage Drift Tracks",
    #title="Comparing a Subset of Late-Stage Draift Tracks",
    font_size=15,
    legend_title="ITP Machine",
    legend_font_size=15,
    font_color="#383d3d",
    title_x=0.5
)
        
fig.show()