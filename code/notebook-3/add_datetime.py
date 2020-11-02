#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 13:43:06 2020

@author: alexandrarivera, larabreitkreutz
"""

import pathlib
import os
import csv
import pandas as pd
from datetime import datetime, timedelta
import math
import inspect
src_file_path = inspect.getfile(lambda: None)

#download rawlocs data and load here

folderlist = []

# Iterates through directory and appends only unmodified rawlocs.dat files to folderlist
for path in pathlib.Path(os.path.dirname(os.path.abspath('___file___'))).iterdir():
    folder_str = str(path)
    if not folder_str.endswith('.zip'):
         if not folder_str.endswith('.csv'):
             if not folder_str.endswith('.py'):
                 if not folder_str.endswith('.ipynb'):
                     if not folder_str.endswith('.DS_Store'):
                         if not folder_str.endswith('checkpoints'):
                             if 'rawlocs' in folder_str:
                                 folder = os.path.basename(folder_str)
                                 folderlist.append(folder)
         
# Iterates through folderlist to create CSV for folder
for folders in folderlist:
    path = os.path.dirname(os.path.abspath('___file___'))
    
    tempfilelist = []
    tempfilelist_csv = {}
    csvfilelist = []
    
    # Iterates through each file and appends rawlocs.dat files to to temporary filelist
    for r,d,f in os.walk(path):
        for file in f:
            if file.endswith('rawlocs.dat'):
                tempfilelist.append(file)
        
    # Creates .csv file for each .dat file and appends to tempfilelist_csv   
    for dat_str in tempfilelist:
        tempfilelist_csv[dat_str] = dat_str[:-4] + '.csv'
    
    # Finds full path for file
    for filename in tempfilelist:
        find_data= os.path.join(path, filename)
     
        original_data = [i.strip().split() for i in open(find_data).readlines()]
    
        # opens and writes each file as CSV
        with open(tempfilelist_csv.get(filename), 'w') as csv_file1:
            csv_writer1 = csv.writer(csv_file1)
            csv_writer1.writerows(original_data[:-1])
    
    # Itereates again through each file and appends rawlocs.csv files to csvfilelist
    for r2, d2, f2 in os.walk(path):
        for file2 in f2:     
            if file2.endswith('locs.csv'):
                csvfilelist.append(file2)

    #names the columns of interest
    col_list = ['longitude(E+)', 'latitude(N+)']
    
    # Iterates through each csv file, opens and reads data
    for csvfilename in csvfilelist:
        df = pd.read_csv(csvfilename, usecols=col_list)
        df.columns = ['Long', 'Lat']
        info = pd.read_csv(csvfilename, skiprows=1, names=['Year', 'YearFrac', 'Long', 'Lat'])
    
        final_times = []
    
        # Iterates through each row of data to create datetime
        for row in info.itertuples():
            
            tyr = row[1]
            tyrfr = str(row[2])   
            year_start = datetime(int(tyr), 1, 1) 
            itp_yearfraction = float(tyrfr)    
            #extract day    
            itp_day_whole=math.floor(itp_yearfraction)
            itp_day_decimal= itp_yearfraction - itp_day_whole
            #extract hour
            itp_hour_whole = itp_day_decimal * 24.0
            itp_hour_decimal = math.floor(itp_hour_whole)
            #extract minute
            itp_minute_whole = (itp_hour_whole - itp_hour_decimal) * 60.0
            itp_minute_decimal = math.floor(itp_minute_whole)
            #extract second
            itp_second_whole = (itp_minute_whole - itp_minute_decimal) * 60.0
            itp_second_decimal = math.floor(itp_second_whole)
            
            final_date = year_start + timedelta(days=itp_day_whole, 
                                           hours=itp_hour_decimal,
                                           minutes=itp_minute_decimal,
                                           seconds=itp_second_decimal)     
            final_date_str = final_date.strftime('%Y-%m-%d %H:%M:%S')
            final_times.append(final_date_str)
        
        # Appends final_times to the dataframe containing row information    
        df['Time'] = final_times
        # Locates ITP machine number based on index and adds column with this number
        start_i = csvfilename.index('i')
        end_i = csvfilename.index('r')
        itp_number = csvfilename[start_i+3:end_i]
        df['ITP'] = itp_number
        
        # Save file as a new CSV, now with datetime info
        savepath = os.path.dirname(os.path.abspath('__file__'))
        os.chdir(savepath)
        df.to_csv(csvfilename[:-4] + '_datetime' + '.csv', index=False)