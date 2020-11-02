#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 10:43:16 2020

@author: larabreitkreutz
"""

import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
pio.renderers.default = "browser"

import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls

# Read in data from main downsampled CSV

filename = #download and add "main_downsamp.csv"
df = pd.read_csv(filename, encoding='utf-8')

# Convert dataframe index to a column
df.reset_index(inplace=True)
df = df.rename(columns = {'index':'Time'})

# Creates reference bounds for latitudes and longitudes
BBox = ((df.Long.min(),df.Long.max(),      
         df.Lat.min(),df.Lat.max()))

# Creates list of colors, chosen to match color scheme throughout project
colors = ['#7dcbb8', '#9786a0', '#79e788', '#dd7798', '#75ccea', '#3d8198']

# FIGURE 1: EARLY DEPLOYMENTS

# Creates data subsets for early deploylments
is_1 = df[df.ITP == 1]
is_2 = df[df.ITP == 6]
is_3 = df[df.ITP == 8]

# Index Count for rotating through colors
ind=1
# Defines figure traces for each ITP machine
trace1 = go.Scattergeo(
              mode= "markers", 
              name= "ITP 1", 
              lat= is_1['Lat'], 
              lon= is_1['Long'], 
              marker_size=7,
              marker_color=colors[ind],
              opacity=.8,
              text=is_1['Time']
              )
ind+=1
trace2 = go.Scattergeo(
    mode= "markers", 
              name= "ITP 6", 
              lat= is_2['Lat'], 
              lon= is_2['Long'], 
              marker_size=7,
              marker_color=colors[ind],
              opacity=.8,
              text=is_2['Time']
              )
ind+=1
trace3 = go.Scattergeo(
    mode= "markers", 
              name= "ITP 8", 
              lat= is_3['Lat'], 
              lon= is_3['Long'], 
              marker_size=7,
              marker_color=colors[ind],
              opacity=.8,
              text=is_3['Time']
              )

# Creates figure
fig1 = go.Figure(data=[trace1,trace2,trace3])

# Adds title and geo elements
fig1.update_layout(
    geo=dict(
            landcolor= "rgb(212, 212, 212)", 
            showcountries= True,
            countrycolor= "rgb(245, 245, 245)",
           ),
 
    title_text= "Subset of Drift Tracks deployed between 2004-2006",
    title_x=0.5,
    width= 800, 
    height= 700)

# Changes projection and colors
fig1.update_geos(projection_type="orthographic",
                fitbounds="locations",
                showcoastlines=True, coastlinecolor="White",
    showland=True, landcolor="#576b6c",
    showocean=True, oceancolor="#383d3d",
    showlakes=True, lakecolor="#122525",
    showrivers=True, rivercolor="#122525",
    lataxis_showgrid=True, lonaxis_showgrid=True)


# FIGURE 2: MIDDLE DEPLOYMENTS

# Creates data subsets for middle deploylments
is_41 = df[df.ITP == 41]
is_48 = df[df.ITP == 48]
is_49 = df[df.ITP == 49]

ind=2
trace41 = go.Scattergeo(
    mode= "markers", 
              name= "", 
              lat= is_41['Lat'], 
              lon= is_41['Long'], 
              marker_size=7,
              marker_color=colors[ind],
              )
ind+=1
trace48 = go.Scattergeo(
    mode= "markers", 
              name= "", 
              lat= is_48['Lat'], 
              lon= is_48['Long'], 
              marker_size=7,
              marker_color=colors[ind],
              )
ind+=1
trace49 = go.Scattergeo(
    mode= "markers", 
              name= "", 
              lat= is_49['Lat'], 
              lon= is_49['Long'], 
              marker_size=7,
              marker_color=colors[ind],
              )

fig2 = go.Figure(data=[trace41,trace48,trace49])

fig2.update_layout(
    geo=dict(
            landcolor= "rgb(212, 212, 212)", 
            showcountries= True,
            countrycolor= "rgb(245, 245, 245)",
           ),
 
    title_text= "Subset of Drift Tracks deployed between 2011-2014", 
    title_x=0.5,
    width= 800, 
    height= 700)

fig2.update_geos(projection_type="orthographic",
                fitbounds="locations",
                showcoastlines=True, coastlinecolor="White",
    showland=True, landcolor="#576b6c",
    showocean=True, oceancolor="#383d3d",
    showlakes=True, lakecolor="#122525",
    showrivers=True, rivercolor="#122525",
    lataxis_showgrid=True, lonaxis_showgrid=True)

# FIGURE 3: LATE DEPLOYMENTS

# Creates data subsets for late deploylments
is_86 = df[df.ITP == 86]
is_91 = df[df.ITP == 91]
is_92 = df[df.ITP == 92]

ind=3
trace86 = go.Scattergeo(
    mode= "markers", 
              name= "", 
              lat= is_86['Lat'], 
              lon= is_86['Long'], 
              marker_size=7,
              marker_color=colors[ind],
              )
ind+=1
trace91 = go.Scattergeo(
    mode= "markers", 
              name= "", 
              lat= is_91['Lat'], 
              lon= is_91['Long'], 
              marker_size=7,
              marker_color=colors[ind],
              )
ind+=1
trace92 = go.Scattergeo(
    mode= "markers", 
              name= "", 
              lat= is_92['Lat'], 
              lon= is_92['Long'], 
              marker_size=7,
              marker_color=colors[ind],
              )

fig3 = go.Figure(data=[trace86,trace91,trace92])

fig3.update_layout(
    geo=dict(
            landcolor= "rgb(212, 212, 212)", 
            showcountries= True,
            countrycolor= "rgb(245, 245, 245)",
           ),
 
    title_text= "Subset of Drift Tracks deployed between 2014-2016", 
    title_x=0.5,
    width= 800, 
    height= 700)

fig3.update_geos(projection_type="orthographic",
                fitbounds="locations",
                showcoastlines=True, coastlinecolor="White",
    showland=True, landcolor="#576b6c",
    showocean=True, oceancolor="#383d3d",
    showlakes=True, lakecolor="#122525",
    showrivers=True, rivercolor="#122525",
    lataxis_showgrid=True, lonaxis_showgrid=True)



# DROPDOWN MENU added to fig1 (can be modified for each fig)

#From here, make one figure at a time, using the data subsets below. Use '#' to comment out all but one subset at a time.
# DEFAULT is list_of_machines1

list_of_machines1 = [1,6,8]
#list_of_machines2 = [41,48,49]
#list_of_machines3 = [86,91,92]

def getDataByButton(filter_machine):
    global metric
    global df
    # return arg list to set x, y and chart title
    filtered = df[df.ITP == filter_machine]
    return [ {'Lat':[filtered['Lat']], 'Long':[filtered['Long']], 'Time':[filtered['Time']], 'ITP':filter_machine},
             {'Title':filter_machine} ]

buttons = []
#ADD AN "ALL" Button
buttons.append(dict(method='restyle',
                    label='All Machines',
                    visible=True))

# Creates button for each machine
for n in range(len(list_of_machines1)):
    buttons.append(dict(method='restyle',
                        label='ITP Machine' + str(list_of_machines1[n]),
                        visible=True,
                        args=[getDataByButton(n)]
                        )
                  )
    
updatemenu = []
your_menu = dict()
updatemenu.append(your_menu)

updatemenu[0]['buttons'] = buttons
updatemenu[0]['direction'] = 'down'
updatemenu[0]['showactive'] = True

# Adds dropdown to fig1, fig2, or fig3. (DEFAULT is fig1)

fig1.update_layout(showlegend=False, updatemenus=updatemenu)
fig1.update_layout(
    updatemenus=[go.layout.Updatemenu(
        #active=0,
        buttons=list(
            [
            dict(
                method="restyle",
                args= [{'visible': [True, True, True,]}, # the index of True aligns with the indices of plot traces
                          {'title': 'All'}]),
             dict(
                  method = 'restyle',
                  args = [{'visible': [True, False, False]}, # the index of True aligns with the indices of plot traces
                          {'title': 'ITP ' + list_of_machines1[0]}]),
             dict(
                  method = 'restyle',
                  args = [{'visible': [False, True, False]},
                          {'title': 'ITP ' + list_of_machines1[1]}]),
             dict(
                  method = 'restyle',
                  args = [{'visible': [False, False, True]},
                          {'title': 'ITP ' + list_of_machines1[2]}]),
            ])
        )
    ])

fig1.show()


