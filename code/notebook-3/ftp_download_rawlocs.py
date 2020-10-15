#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 19:12:42 2020
@author: alexandrarivera
"""

import ftplib
import os
import fnmatch

ASCII_LASTLINE='\033[F'

# ==================== CONFIG =================== #

# FTP server credentials
FTP_HOST = 'ftp.whoi.edu'
FTP_USER = 'anonymous'
FTP_PASS = ''
# Local save folder
SAVE_FOLDER = 'allraw_loc'
# Temporary suffix for downloaded files before hashing has completed
PREHASH_FILENAME_SUFFIX = '_tmp'

# =============================================== #

# Initialize ftp session over TLS
ftp = ftplib.FTP_TLS(host=FTP_HOST, user=FTP_USER, passwd=FTP_PASS)
ftp.encoding = 'utf-8'
# Change to secure connection 
ftp.prot_p()
# Print FTP welcome message
print(ftp.getwelcome())

# Change the remote working directory to ITP folder
ftp.cwd('/whoinet/itpdata')
# Create the local save folder if necessary
savedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), SAVE_FOLDER)
if not os.path.exists(savedir):
	os.makedirs(savedir)
# Change the local working directory to the save folder
os.chdir(savedir)

# Empty structure to hold all FTP data
ls = []
ftp.retrlines('LIST', ls.append)

# Get only files ending in "final.zip"
filematch = '*rawlocs.dat'
filtered = fnmatch.filter(ls, filematch)

# For each profiler, append most updated zip file (final or grddata)
final = {}
all_machines = []

for old in filtered:
    if "itw" not in old:
        if "itm" not in old:
            o = old.split()[-1][:-11]
            final[o] = old

mach_nums = range(1,120)
for num in mach_nums:
    all_machines.append(final.get("itp" + str(num)))


# Download and unzip all files
for entry in all_machines:
    if entry is None:
        continue
    
    filename = entry.split()[-1][:-4]
    print("Processing %s.dat..." % filename)

    # If a local file exists with the same name as a remote zip file
    if(os.path.exists('%s.dat' % filename)):
        continue

	# Download/retrieve the dat file
    with open('%s.dat' % filename ,'wb') as fp:
        print(ASCII_LASTLINE + "Retrieving %s.dat..." % filename)
        ftp.retrbinary('RETR %s.dat' % filename, fp.write)
        fp.close()
    print(ASCII_LASTLINE + "Retrieved %s.dat    " % filename)