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

# Creates an empty list
filelist = []

# Iterates over the files in each folder and appends the file's name to "filelist"
for path in pathlib.Path(os.path.dirname(os.path.abspath('___file___'))).iterdir():
    print(path)
    file_str = str(path)
    if 'datetime.csv' in file_str:
        folder = os.path.basename(file_str)
        filelist.append(folder)

# Creates a master empty dataframe
master_df = pd.DataFrame(columns=['Long', 'Lat', 'Time', 'ITP'])

# Creates an empty list and reads each file as a CSV, appending it to the master dataframe
info = []
for filename in filelist:
    info = pd.read_csv(filename)
        
    master_df = master_df.append(info)
    
#sort by ITP
master_df = master_df.sort_values(by=['ITP'])
    
# Creates a CSV file from the master dataframe
master_df.to_csv('mastercsv.csv', index=False)
