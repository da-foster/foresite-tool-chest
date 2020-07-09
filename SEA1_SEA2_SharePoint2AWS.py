### RUNS IN PYTHON 3.6 ###

### Title: SEA1_SEA2_SharePoint2AWS
### Description:  This script is the second half of a process that grabs SEA 1 & 2 data from SharePoint,
###               which begins with an automated WinSCP script to upload the data into AWS and land in my FTP folder
###               ('\\fginc-file\GIS\ftp\Foster_FTP\SharePoint_SEA1' AND '\\fginc-file\GIS\ftp\Foster_FTP\SharePoint_SEA2').
###               This Python script moves the data from these locations in the FTP folder to the folder location where
###               'ShareFile_Snatch.py' will commence the movement into the 3GIS SDE connections.
### Company: Foresite Group
### Author: Darren Foster

import os
import zipfile
import time
import shutil
import arcpy
from datetime import datetime

print("Let's party...")

####################################################################################
### SEA1 Input Locations ###
sea1Input = r"\\fginc-file\GIS\ftp\Foster_FTP\SharePoint_SEA1"

#SEA1 Input Variables
s1_InDate = ""
s1_InFolder = ""
s1_InName = ""

#Iterate through the SEA1 input folders to find the most recent data
for root, dirs, files in os.walk(sea1Input):
    for file in files:
        fullPath = os.path.join(root, file)
        baseName = os.path.basename(fullPath)
        modEpoc = os.path.getmtime(fullPath)
        modTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modEpoc))

        if s1_InDate < modTime:

            s1_InDate = modTime
            s1_InFolder = fullPath
            s1_InName = baseName

print('\nThe most recent data in SEA1 input is :  ' + str(s1_InDate))
print('\nThe selected folder in SEA1 input is:  ' + str(s1_InFolder))
print('\nThe basename is: ' + s1_InName)

####################################################################################
### SEA1 Output Locations ###
sea1Output = r"\\fginc-file\GIS\Foster\ShareFile_snatch\3GIS_Data_Exports\Seattle1"

#SEA1 Output Variables
s1_OutDate = ""
s1_OutFolder = ""
s1_OutName = ""

#Iterate through the SEA1 output folders to find the most recent data
for root, dirs, files in os.walk(sea1Output):
    for file in files:
        fullPath = os.path.join(root, file)
        baseName = os.path.basename(fullPath)
        modEpoc = os.path.getmtime(fullPath)
        modTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modEpoc))

        if s1_OutDate < modTime:

            s1_OutDate = modTime
            s1_OutFolder = fullPath
            s1_OutName = baseName

print('\nThe most recent data in SEA1 output is :  ' + str(s1_OutDate))
print('\nThe selected folder in SEA1 output is:  ' + str(s1_OutFolder))
print('\nThe basename is: ' + s1_OutName)


####################################################################################
##### Compare the SEA1 Input data to the Output data #####
if s1_InName == s1_OutName:
    print("\nSEA1 data is the same")
    pass

elif s1_InName != s1_OutName:
    print("\nSEA1 data needs to be updated")
    shutil.copy(s1_InFolder, sea1Output)

####################################################################################
### SEA2 Input Location ###
sea2Input = r"\\fginc-file\GIS\ftp\Foster_FTP\SharePoint_SEA2"

#SEA2 Input Variables
s2_InDate = ""
s2_InFolder = ""
s2_InName = ""

#Iterate through the SEA2 Input folders to find the most recent data
for root, dirs, files in os.walk(sea2Input):
    for file in files:
        fullPath = os.path.join(root, file)
        baseName = os.path.basename(fullPath)
        modEpoc = os.path.getmtime(fullPath)
        modTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modEpoc))

        if s2_InDate < modTime:

            s2_InDate = modTime
            s2_InFolder = fullPath
            s2_InName = baseName

print('\nThe most recent data in SEA2 Input is :  ' + str(s2_InDate))
print('\nThe selected folder in SEA2 Input is:  ' + str(s2_InFolder))
print('\nThe basename is: ' + s2_InName)


####################################################################################
### SEA2 Output Location ###
sea2Output = r"\\fginc-file\GIS\Foster\ShareFile_snatch\3GIS_Data_Exports\Seattle2"

#SEA2 Output Variables
s2_OutDate = ""
s2_OutFolder = ""
s2_OutName = ""

#Iterate through the SEA2 Input folders to find the most recent data
for root, dirs, files in os.walk(sea2Output):
    for file in files:
        fullPath = os.path.join(root, file)
        baseName = os.path.basename(fullPath)
        modEpoc = os.path.getmtime(fullPath)
        modTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modEpoc))

        if s2_OutDate < modTime:

            s2_OutDate = modTime
            s2_OutFolder = fullPath
            s2_OutName = baseName

print('\nThe most recent data in SEA2 output is :  ' + str(s2_OutDate))
print('\nThe selected folder in SEA2 output is:  ' + str(s2_OutFolder))
print('\nThe basename is: ' + s2_OutName)

####################################################################################
##### Compare the SEA2 Input data to the Output data #####
if s2_InName == s2_OutName:
    print("\nSEA2 data is the same")
    pass

elif s2_InName != s2_OutName:
    print("\nSEA2 data needs to be updated")
    shutil.copy(s2_InFolder, sea2Output)
