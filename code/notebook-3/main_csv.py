#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 17:24:49 2020

@author: larabreitkreutz
"""

import pathlib
import os
import pandas as pd
import inspect
src_file_path = inspect.getfile(lambda: None)

#run add_datetime.py and load data here

# Creates an empty list
filelist = []

# Iterates over the files in each folder and appends the file's name to "filelist"
for path in pathlib.Path(os.path.dirname(os.path.abspath('___file___'))).iterdir():
    print(path)
    file_str = str(path)
    if 'datetime.csv' in file_str:
        folder = os.path.basename(file_str)
        filelist.append(folder)

# Creates a main empty dataframe
main_df = pd.DataFrame(columns=['Long', 'Lat', 'Time', 'ITP'])

# Creates an empty list and reads each file as a CSV, appending it to the main dataframe
info = []
for filename in filelist:
    info = pd.read_csv(filename)
        
    main_df = main_df.append(info)
    
# Sorts by ITP
main_df = main_df.sort_values(by=['ITP'])

# Puts time stamp in first column
main_df = main_df[['Time', 'ITP', 'Long', 'Lat']]
    
# Creates a CSV file from the main dataframe
main_df.to_csv('main.csv', index=False)

# Reads in data from main CSV 
df = pd.read_csv("/Users/larabreitkreutz/PythonGIS/rawlocs/main.csv", parse_dates=['Time'], index_col=0)

# Downsamples data, one mean observation per day
downsamp = df.resample('D').agg({'ITP':'last','Long':'mean', 'Lat':'mean'})

# Saves downsampled data as CSV
downsamp.to_csv('main_downsamp.csv', index=False)
