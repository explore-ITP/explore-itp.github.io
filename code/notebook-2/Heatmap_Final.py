#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 17:37:46 2020

@author: alexandrarivera
"""

import pathlib
import os
import csv
import pandas as pd

from bokeh.io import output_file, show
from bokeh.models import (ColorBar, LinearColorMapper, LinearAxis,
                          PrintfTickFormatter, HoverTool, BasicTicker, SingleIntervalTicker)
from bokeh.plotting import figure
from bokeh.palettes import mpl

from datetime import datetime, timedelta
import math

itpnumber = 'ITP1 '

#%% To iterate over files in the folder and create individual csvs
filelist = []
filelist_csv = {}

for path in pathlib.Path(os.path.dirname(os.path.abspath(__file__))).iterdir():
    full_str = str(path)
    if full_str.endswith('.dat'):
        if '._' not in full_str:
            dat_str = os.path.basename(full_str)
            filelist.append(dat_str)

for dat_str in filelist: 
    filelist_csv[dat_str] = dat_str[:-4] + '.csv'
    
for filename in filelist:
    find_data = os.path.dirname(os.path.abspath(__file__))
    find_data_two= os.path.join(find_data, filename)
     
    original_data = [i.strip().split() for i in open(find_data_two).readlines()]
    
    with open(filelist_csv.get(filename), 'w') as csv_file1:
        csv_writer1 = csv.writer(csv_file1)
        csv_writer1.writerows(original_data[1:2] + original_data[2:-1])    

#%% To iterate over csv files
csvfilelist = []

for path in pathlib.Path(os.path.dirname(os.path.abspath(__file__))).iterdir():
    full_str2 = str(path)
    if full_str2.endswith('.csv'): 
        if 'urls' not in full_str2:
            if '._' not in full_str2:
                dat_str2 = os.path.basename(full_str2)
                csvfilelist.append(dat_str2)
           
#%% Creating dataframe for heatmap
master_df = pd.DataFrame(columns=['Temperature', 'Pressure', 'Time'])

col_list = ['%pressure(dbar)', 'temperature(C)']

for csvfilename in csvfilelist[0:100]:
    df = pd.read_csv(csvfilename, skiprows=1, usecols = col_list)
    df.columns = ['Pressure', 'Temperature']
    info = pd.read_csv(csvfilename, nrows=1, names=['Year', 'YearFrac', 'Long', 'Lat', 'Ndepths'])
       
    tyr = str(info['Year'])
    tyrfr = str(info['YearFrac'])    
    year_start = datetime(int(tyr[5:9]), 1, 1) 
    itp_yearfraction = float(tyrfr[5:-31])    
    itp_day_whole=math.floor(itp_yearfraction)
    final_date = year_start + timedelta(days=itp_day_whole)     
    final_date_str = final_date.strftime('%Y-%m-%d')
          
    df["Time"] = final_date_str
    target_df = df[['Temperature','Pressure', 'Time']]
    master_df = master_df.append(target_df)

master_df = master_df.reset_index(drop=True)
#%% Plotting heatmap 

TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

colors = mpl['Plasma'][11]
mapper = LinearColorMapper(
    palette=colors, low=master_df.Temperature.min(), high=master_df.Temperature.max())

time_list = list(master_df.Time)
time_list = list(sorted(time_list))
simplified_tl = []
[simplified_tl.append(x) for x in time_list if x not in simplified_tl]

hm = figure(title= 'Temperature Heatmap: ' + master_df.Time.min() + ' to ' + master_df.Time.max() + ', ' + itpnumber,
           x_range= simplified_tl, y_range=list(reversed((0,760))),
           x_axis_type=None, plot_width=1000, plot_height=400,
           tools=TOOLS, toolbar_location='above')


hm.rect(x="Time", y="Pressure",width=1,height=1,source = master_df, fill_color={'field': 'Temperature', 'transform': mapper},
       line_color=None)  
#%% Creating colorbar
color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="11px",
                     ticker=BasicTicker(desired_num_ticks=13),
                     formatter=PrintfTickFormatter(format='%1.2f' '\N{DEGREE SIGN}C'),
                     label_standoff=12, border_line_color=None, location=(0, 0))

hm.add_layout(color_bar, 'right')

#%% Other formatting for plot
ticker = SingleIntervalTicker(interval=10, num_minor_ticks=5)
xaxis = LinearAxis(ticker=ticker)
hm.add_layout(xaxis, 'below')
hm.xaxis.axis_label = 'Time (days)'
hm.xaxis.major_label_orientation = math.pi / 3

hm.yaxis.axis_label = 'Pressure (dbar)'
hm.select_one(HoverTool).tooltips = [('Time', '@Time'),('Pressure', '@Pressure'), ('Temperature', '@Temperature')]

hm.background_fill_color = "black"

output_file(itpnumber + "HeatMap.html", title= itpnumber + "Heatmap")

show(hm)  #open a browser

#%% Delete temperary csv's after creating plots
for csvfilename in csvfilelist:
    os.remove(csvfilename)

        