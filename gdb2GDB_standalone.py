### Title: gdb2GDB
### Description: This script truncates all the data in the 3GIS SDE GDB,
###              and appends new data from an exported FGDB(s).
### Company: Foresite Group
### Author: Darren Foster

### RUNS IN PYTHON 3.6 ###

import arcpy
import os

### INPUT GDB ###
inputGDB = r"S:\Shared Folders\Verizon\3GIS Exports\AWS_Imports\Nashville_Import\Mastec_NashvilleTN_Bulk_2019-12-25_20-54-22.gdb"

### CORRESPONDING 3GISDB ###
threeGIS_DB = r"\\fginc-file\gis\dbConnections\3GIS\NASH_3GIS as GISADMIN.sde"


### For the truncate, set the workspace environment to the 3GIS database ###
arcpy.env.workspace = threeGIS_DB


### Truncate Tables ###
truncateTableList = arcpy.ListTables()
print("Truncating Tables:")

for data in truncateTableList:
    arcpy.TruncateTable_management(data)
    print(data)


### Truncate Feature Classes ###
truncateFeatureList = arcpy.ListFeatureClasses()
print("\n Truncating Feature Classes:")

for data in truncateFeatureList:
    if data == 'NASH_3GIS.DBO.PERMIT_ACTIVITY_POINT' or \
       data == 'NASH_3GIS.DBO.PERMIT_ACTIVITY_LINE' or \
       data == 'NASH_3GIS.DBO.ASBUILT_POLYGONS':
        print("Not truncating: " + str(data))
        pass
    
    else:
        arcpy.TruncateTable_management(data)
        print(data)


### For the append, set the workspace environment and list the feature classes/tables in the Input GDB ###
arcpy.env.workspace = inputGDB


### Loop through and append tables into GDB ###
appendTableList = arcpy.ListTables()
print("\n Appending Tables:")

for table in appendTableList:
    try:
        arcpy.Append_management(table, threeGIS_DB + "\\" + table, 'NO_TEST')
        print(table)
    except:
        print("Unable to append " + str(table))
        print(arcpy.GetMessages())


### Loop through and append feature classes into GDB ###
appendFeatureList = arcpy.ListFeatureClasses()
print("\n Appending Feature Classes:")

for fc in appendFeatureList:
    try:
        arcpy.Append_management(fc, threeGIS_DB + "\\" + fc, 'NO_TEST')
        print(fc)
    except:
        print("Unable to append " + str(fc))
        print(arcpy.GetMessages())
        

print("\n Process Complete!")

