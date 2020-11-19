#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 17:41:31 2020

@author: alexandrarivera
"""

import numpy as np
import pathlib
import os
import csv
import pandas as pd

from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show
from bokeh.models import Label, Panel, Tabs

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
         
#%% Creating different tabs of by season

# Winter graphs
p1w = figure(title= itpnumber + "Temperature Profiles, Jan-Mar")
p2w = figure(title= itpnumber + "Salinity Profiles, Jan-Mar")
# Spring graphs
p1sp = figure(title= itpnumber + "Temperature Profiles, Apr-Jun")
p2sp = figure(title= itpnumber + "Salinity Profiles, Apr-Jun")
# Summer Graphs
p1su = figure(title= itpnumber + "Temperature Profiles, Jul-Sep")
p2su = figure(title= itpnumber + "Salinity Profiles, Jul-Sep")
# Fall Graphs
p1f = figure(title= itpnumber + "Temperature Profiles, Oct-Dec")
p2f = figure(title= itpnumber + "Salinity Profiles, Oct-Dec")
# Cumulative
p1c = figure(title= itpnumber + "Temperature Profiles by Season")
p2c = figure(title= itpnumber + "Salinity Profiles by Season")

# Creating axis labels
x_temp = 'Temperature (\N{DEGREE SIGN}C)'
x_sal = 'Salinity (psu)'
y_all = 'Pressure (dbar)'

# Applying the axis labels to each graph
(p1w.xaxis.axis_label, p1sp.xaxis.axis_label, p1su.xaxis.axis_label, p1f.xaxis.axis_label, 
 p1c.xaxis.axis_label) = x_temp, x_temp, x_temp, x_temp, x_temp  

(p2w.xaxis.axis_label, p2sp.xaxis.axis_label, p2su.xaxis.axis_label, p2f.xaxis.axis_label, 
 p2c.xaxis.axis_label) = x_sal, x_sal, x_sal, x_sal, x_sal

(p1w.yaxis.axis_label, p2w.yaxis.axis_label,
 p1sp.yaxis.axis_label, p2sp.yaxis.axis_label,
 p1su.yaxis.axis_label, p2su.yaxis.axis_label,
 p1f.yaxis.axis_label, p2f.yaxis.axis_label,
 p1c.yaxis.axis_label, p2c.yaxis.axis_label) = y_all, y_all, y_all, y_all, y_all, y_all, y_all, y_all, y_all, y_all

# Flipping all y ranges
(p1w.y_range.flipped, p2w.y_range.flipped,
 p1sp.y_range.flipped, p2sp.y_range.flipped,
 p1su.y_range.flipped, p2su.y_range.flipped,
 p1f.y_range.flipped, p2f.y_range.flipped,
 p1c.y_range.flipped, p2c.y_range.flipped) = True, True, True, True, True, True, True, True, True, True

gridw = gridplot([[p1w,p2w]], plot_width=400, plot_height=400)
tabw = Panel(child=gridw, title='Winter')

gridsp = gridplot([[p1sp,p2sp]], plot_width=400, plot_height=400)
tabsp = Panel(child=gridsp, title='Spring')

gridsu = gridplot([[p1su,p2su]], plot_width=400, plot_height=400)
tabsu = Panel(child=gridsu, title='Summer')

gridf = gridplot([[p1f,p2f]], plot_width=400, plot_height=400)
tabf = Panel(child=gridf, title='Fall')

tab1c = Panel(child=p1c, title='All Seasons, Temperature')
tab2c = Panel(child=p2c, title='All Seasons, Salinity')

#%% Plotting
wintertally = 0
springtally = 0
summertally = 0
falltally = 0

specific_t_graph = []
specific_s_graph = []


col_list = ['%pressure(dbar)', 'temperature(C)', 'salinity']
for csvfilename in csvfilelist[0:100]:
    df = pd.read_csv(csvfilename, skiprows=1, usecols = col_list)
    df.columns = ['Pressure', 'Temperature', 'Salinity']
    info = pd.read_csv(csvfilename, nrows=1, names=['Year', 'YearFrac', 'Long', 'Lat', 'Ndepths'])
    yrfr = int(info.YearFrac)
        
    if yrfr in range(0, 92): 
        color = 'steelblue'
        wintertally += 1
        specific_t_graph = p1w
        specific_s_graph = p2w
    elif yrfr in range(92, 183): 
        color = 'palevioletred'
        springtally += 1
        specific_t_graph = p1sp
        specific_s_graph = p2sp
    elif yrfr in range(183, 275):
        color = 'lightgreen'
        summertally += 1
        specific_t_graph = p1su
        specific_s_graph = p2su
    elif yrfr in range(275, 367):
        color = 'skyblue'
        falltally += 1
        specific_t_graph = p1f
        specific_s_graph = p2f

        
    specific_t_graph.line(df['Temperature'], df['Pressure'], color = color, alpha=0.5)
    p1c.line(df['Temperature'], df['Pressure'], color = color, alpha=0.5)
    specific_s_graph.line(df['Salinity'], df['Pressure'], color = color, alpha=0.5)
    p2c.line(df['Salinity'], df['Pressure'], color = color, alpha=0.5)

#%% Formatting and citations for plots
citationw = Label(x=5, y=5, x_units='screen', y_units='screen',
                 text='Amount of Profiles: ' + str(wintertally), text_font_size='10pt')
citationsp = Label(x=5, y=5, x_units='screen', y_units='screen',
                 text='Amount of Profiles: ' + str(springtally), text_font_size='10pt')
citationsu = Label(x=5, y=5, x_units='screen', y_units='screen',
                 text='Amount of Profiles: ' + str(summertally), text_font_size='10pt')
citationf = Label(x=5, y=5, x_units='screen', y_units='screen',
                 text='Amount of Profiles: ' + str(falltally), text_font_size='10pt')
citationc = Label(x=5, y=5, x_units='screen', y_units='screen',
                 text='Winter: Dark Blue' + ',   \n' +
                 "Spring: Green" + ",   \n" +
                 'Summer: Pink' + ',   \n' +
                 'Fall: Light Blue', text_font_size='10pt')

p1w.add_layout(citationw)
p1sp.add_layout(citationsp)
p1su.add_layout(citationsu)
p1f.add_layout(citationf)
p1c.add_layout(citationc)
p2c.add_layout(citationc)

window_size = 30
window = np.ones(window_size)/float(window_size)

output_file(itpnumber + "Final_Colored.html", title= itpnumber + " Final Profiles")

tabs=Tabs(tabs=[ tab1c, tab2c, tabw, tabsp, tabsu, tabf ])
show(tabs)  # open a browser

#%% Delete temporary csv's after running plots
for csvfilename in csvfilelist:
    os.remove(csvfilename)

