### RUNS IN PYTHON 3.6 ###

### Title: ShareFile / 3GIS Append
### Description: This Python tool accesses our Network Design ShareFile account via  
###              the ShareFile Windows desktop application. It looks at each of the folder's contents, 
###              determines if there is new data to download (based on the most recent modification date),
###              unzips the data into a corresponding folder in the 'AWS_Imports' folder, and appends the 
###              data into the SDE databases in AWS.
### Company: Foresite Group
### Author: Darren Foster

### Import Statements ###
import os
import zipfile
import time
import arcpy
from datetime import datetime

now = datetime.now()
lastRun = r"\\fginc-file\GIS\Foster\ShareFile_snatch\ShareFileSnatch_TXTs\DO NOT TOUCH THESE TXTs.txt"

with open(lastRun, 'r+') as textFile:
    textFile.write(str(now))

### Paths to most where updated GDB are stored ###
cleveFolder = r"\\fginc-file\GIS\Foster\ShareFile_snatch\3GIS_Data_Exports\Cleveland"
knoxFolder = r"\\fginc-file\GIS\Foster\ShareFile_snatch\3GIS_Data_Exports\Knoxville"
nashFolder = r"\\fginc-file\GIS\Foster\ShareFile_snatch\3GIS_Data_Exports\Nashville"
seaFolder = r"\\fginc-file\GIS\Foster\ShareFile_snatch\3GIS_Data_Exports\Seattle2"
sea1Folder = r"\\fginc-file\GIS\Foster\ShareFile_snatch\3GIS_Data_Exports\Seattle1"

### Paths to the unpacking area ###
cleveImport = r"\\fginc-file\GIS\Foster\ShareFile_snatch\3GIS_Data_Exports\Cleveland_unpack"
knoxImport = r"\\fginc-file\GIS\Foster\ShareFile_snatch\3GIS_Data_Exports\Knoxville_unpack"
nashImport = r"\\fginc-file\GIS\Foster\ShareFile_snatch\3GIS_Data_Exports\Nashville_unpack"
seaImport = r"\\fginc-file\GIS\Foster\ShareFile_snatch\3GIS_Data_Exports\Seattle2_unpack"
sea1Import = r"\\fginc-file\GIS\Foster\ShareFile_snatch\3GIS_Data_Exports\Seattle1_unpack"

### TXT paths ###
cleveTXT = r"\\fginc-file\GIS\Foster\ShareFile_snatch\ShareFileSnatch_TXTs\Cleveland.txt"
knoxTXT = r"\\fginc-file\GIS\Foster\ShareFile_snatch\ShareFileSnatch_TXTs\Knoxville.txt"
nashTXT = r"\\fginc-file\GIS\Foster\ShareFile_snatch\ShareFileSnatch_TXTs\Nashville.txt"
seaTXT = r"\\fginc-file\GIS\Foster\ShareFile_snatch\ShareFileSnatch_TXTs\Seattle2.txt"
sea1TXT = r"\\fginc-file\GIS\Foster\ShareFile_snatch\ShareFileSnatch_TXTs\Seattle1.txt"

### 3GIS SDE Databases ###
cle3GIS = r"\\fginc-file\gis\dbConnections\3GIS\CLE_3GIS as GISADMIN.sde"
knox3GIS = r"\\fginc-file\gis\dbConnections\3GIS\KNOX_3GIS as GISADMIN.sde"
nash3GIS = r"\\fginc-file\gis\dbConnections\3GIS\NASH_3GIS as GISADMIN.sde"
sea3GIS = r"\\fginc-file\gis\dbConnections\3GIS\SEA_3GIS as GISADMIN.sde"
sea13GIS = r"\\fginc-file\gis\dbConnections\3GIS\SEA1_3GIS as GISADMIN.sde"


############################################################################################
############################################################################################
### CLEVELAND ###

print('*** Begin Cleveland ***')

### Cycle through the Cleveland folder to determine which folder is the newest ###
### according to its 'Date modified' date, and save these attribute to a variable. ###

selectedDate = ""
selectedFolder = ""
selectedName = ""

for root, dirs, files in os.walk(cleveFolder):

    for file in files:

        fullPath = os.path.join(root, file)
        baseName = os.path.basename(fullPath)
        modEpoc = os.path.getmtime(fullPath)
        modTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modEpoc))

        if selectedDate < modTime:

            selectedDate = modTime
            selectedFolder = fullPath
            selectedName = baseName

print('\nThe most recent data in the Cleveland ShareFile is:  ' + str(selectedDate))
print('\nThe selected folder is:  ' + str(selectedFolder))
print('\nCleveland basename is: ' + selectedName)

### Open the associated text file and read in the previous date of the previous import ###
with open(cleveTXT, 'r+') as textFile:

    fileReadIn = textFile.read()
    txtValue = str(fileReadIn)
    print('\nThe last Cleveland GDB imported was:  ' + str(txtValue))

    proceed = False

    if txtValue != selectedName:

        proceed = True
        print('\nData is outdated. Replacing with:  ' + str(selectedName))
        zip_ref = zipfile.ZipFile(selectedFolder)
        zip_ref.extractall(cleveImport)
        zip_ref.close()
        print('\nData successfully unzipped')
        ### Overwrite the TXT with the new file name ###
        textFile.seek(0)
        textFile.write(str(selectedName))
        textFile.truncate()

    elif txtValue == selectedName:
        print('\nCleveland data is current')
        
    else:
        print('\nSomething wrong happened...')


### Truncate all the tables and feature classes in the Cleveland 3GIS DB if necessary ###
if proceed == True:

    print('\nTruncating Cleveland 3GIS DB')

    ### For the truncate, set the workspace environment to the 3GIS database ###
    arcpy.env.workspace = cle3GIS

    ### Truncate Tables ###
    truncateTableList = arcpy.ListTables()
    print("\nTruncating Cleveland Tables:")

    for data in truncateTableList:
        arcpy.TruncateTable_management(data)
        print(data)


    ### Truncate Feature Classes ###
    truncateFeatureList = arcpy.ListFeatureClasses()
    print("\nTruncating Cleveland Feature Classes:")

    for data in truncateFeatureList:
        if data == 'CLE_3GIS.DBO.ASBUILT_POLYGONS':
            print("Not truncating: " + str(data))
            pass

        else:
            arcpy.TruncateTable_management(data)
            print(data)

    ### Go to Cleveland AWS_Imports folder to move the data from ShareFile into the SDE GDB ###
    print('\nMoving Cleveland data into AWS')

    ### For the append, set the workspace environment and list the feature classes/tables in the Input GDB ###
    dirName = os.listdir(cleveImport)

    for file in dirName:

        gdb = cleveImport + '\\' + file
        arcpy.env.workspace = gdb

        ### Append tables into GDB ###
        appendTableList = arcpy.ListTables()
        print('\nAppending Tables:')

        for table in appendTableList:

            try:
                arcpy.Append_management(table, cle3GIS + '\\' + table, 'NO_TEST')
                print(table)

            except:
                print('***UNABLE TO APPEND ' + str(table))
                print(arcpy.GetMessages())

        ### Append feature classes into GDB ###
        appendFeatureList = arcpy.ListFeatureClasses()
        print('\nAppending Feature Classes:')

        for fc in appendFeatureList:
            try:
                arcpy.Append_management(fc, cle3GIS + "\\" + fc, 'NO_TEST')
                print(fc)

            except:
                print('***UNABLE TO APPEND ' + str(fc))
                print(arcpy.GetMessages())

        arcpy.Delete_management(gdb)



elif proceed == False:

    print('\nNot Updating Cleveland DBs')

print('\nEnd Cleveland')
print('*********************************************************************')



############################################################################################
############################################################################################
### KNOXVILLE ###

print('\n*** Begin Knoxville ***')

### Cycle through the Knoxville folder to determine which folder is the newest ###
### according to its 'Date modified' date, and save these attribute to a variable. ###

selectedDate = ""
selectedFolder = ""
selectedName = ""

for root, dirs, files in os.walk(knoxFolder):

    for file in files:

        fullPath = os.path.join(root, file)
        baseName = os.path.basename(fullPath)
        modEpoc = os.path.getmtime(fullPath)
        modTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modEpoc))

        if selectedDate < modTime:

            selectedDate = modTime
            selectedFolder = fullPath
            selectedName = baseName

print('\nThe most recent data in the Knoxville ShareFile is:  ' + str(selectedDate))
print('\nThe selected folder is:  ' + str(selectedFolder))
print('\nKnoxville basename is: ' + selectedName)

### Open the associated text file and read in the previous date of the previous import ###
with open(knoxTXT, 'r+') as textFile:

    fileReadIn = textFile.read()
    txtValue = str(fileReadIn)
    print('\nThe last Knoxville GDB imported was:  ' + str(txtValue))

    proceed = False

    if txtValue != selectedName:

        proceed = True

        print('\nData is outdated. Replacing with:  ' + str(selectedName))
        zip_ref = zipfile.ZipFile(selectedFolder)
        zip_ref.extractall(knoxImport)
        zip_ref.close()
        print('\nData successfully unzipped')
        ### Overwrite the TXT with the new time stamp ###
        textFile.seek(0)
        textFile.write(str(selectedName))
        textFile.truncate()

    elif txtValue == selectedName:
        print('\nKnoxville data is current')

    else:
        print('\nSomething wrong happened...')


### Truncate all the tables and feature classes in the Knoxville 3GIS DB if necessary ###
if proceed == True:

    print('\nTruncating Knoxville 3GIS DB')

    ### For the truncate, set the workspace environment to the 3GIS database ###
    arcpy.env.workspace = knox3GIS

    ### Truncate Tables ###
    truncateTableList = arcpy.ListTables()
    print("\nTruncating Knoxville Tables:")

    for data in truncateTableList:
        arcpy.TruncateTable_management(data)
        print(data)

    ### Truncate Feature Classes ###
    truncateFeatureList = arcpy.ListFeatureClasses()
    print("\nTruncating Knoxville Feature Classes:")

    for data in truncateFeatureList:
        if data == 'KNOX_3GIS.DBO.ASBUILT_POLYGONS':
            print("Not truncating: " + str(data))
            pass

        else:
            arcpy.TruncateTable_management(data)
            print(data)

    ### Go to Knoxville AWS_Imports folder to move the data from ShareFile into the SDE GDB ###
    print('\nMoving Knoxville data into AWS')

    ### For the append, set the workspace environment and list the feature classes/tables in the Input GDB ###
    dirName = os.listdir(knoxImport)

    for file in dirName:

        gdb = knoxImport + '\\' + file
        arcpy.env.workspace = gdb


        ### Append tables into GDB ###
        appendTableList = arcpy.ListTables()
        print('\nAppending Tables:')

        for table in appendTableList:

            try:
                arcpy.Append_management(table, knox3GIS + '\\' + table, 'NO_TEST')
                print(table)

            except:
                print('***UNABLE TO APPEND ' + str(table))
                print(arcpy.GetMessages())


        ### Append feature classes into GDB ###
        appendFeatureList = arcpy.ListFeatureClasses()
        print('\nAppending Feature Classes:')

        for fc in appendFeatureList:
            try:
                arcpy.Append_management(fc, knox3GIS + "\\" + fc, 'NO_TEST')
                print(fc)

            except:
                print('***UNABLE TO APPEND ' + str(fc))
                print(arcpy.GetMessages())

        arcpy.Delete_management(gdb)


elif proceed == False:

    print('\nNot Updating Knoxville DBs')

print('\nEnd Knoxville')
print('*********************************************************************')



############################################################################################
############################################################################################
### NASHEVILLE ###

print('\n*** Begin Nashville ***')

### Cycle through the Nashville folder to determine which folder is the newest ###
### according to its 'Date modified' date, and save these attribute to a variable. ###

selectedDate = ""
selectedFolder = ""
selectedName = ""

for root, dirs, files in os.walk(nashFolder):

    for file in files:

        fullPath = os.path.join(root, file)
        baseName = os.path.basename(fullPath)
        modEpoc = os.path.getmtime(fullPath)
        modTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modEpoc))


        if selectedDate < modTime:

            selectedDate = modTime
            selectedFolder = fullPath
            selectedName = baseName

print('\nThe most recent data in the Nashville ShareFile is:  ' + str(selectedDate))
print('\nThe selected folder is:  ' + str(selectedFolder))
print('\nNashville basename is: ' + selectedName)

### Open the associated text file and read in the previous date of the previous import ###

with open(nashTXT, 'r+') as textFile:

    fileReadIn = textFile.read()
    txtValue = str(fileReadIn)
    print('\nThe last Nasheville GDB imported was:  ' + str(txtValue))

    proceed = False

    if txtValue != selectedName:

        proceed = True

        print('\nData is outdated. Replacing with:  ' + str(selectedName))
        zip_ref = zipfile.ZipFile(selectedFolder)
        zip_ref.extractall(nashImport)
        zip_ref.close()
        print('\nData successfully unzipped')
        ### Overwrite the TXT with the new time stamp ###
        textFile.seek(0)
        textFile.write(str(selectedName))
        textFile.truncate()

    elif txtValue == selectedName:
        print('\nCleveland data is current')

    else:
        print('\nSomething wrong happened...')


### Truncate all the tables and feature classes in the Nashville 3GIS DB if necessary ###

if proceed == True:

    print('\nTruncating Nashville 3GIS DB')


    ### For the truncate, set the workspace environment to the 3GIS database ###
    arcpy.env.workspace = nash3GIS


    ### Truncate Tables ###
    truncateTableList = arcpy.ListTables()
    print("\nTruncating Nashville Tables:")

    for data in truncateTableList:
        arcpy.TruncateTable_management(data)
        print(data)


    ### Truncate Feature Classes ###
    truncateFeatureList = arcpy.ListFeatureClasses()
    print("\nTruncating Nashville Feature Classes:")

    for data in truncateFeatureList:
        if data == 'NASH_3GIS.DBO.ASBUILT_POLYGONS':
            print("Not truncating: " + str(data))
            pass

        else:
            arcpy.TruncateTable_management(data)
            print(data)


    ### Go to Nashville AWS_Imports folder to move the data from ShareFile into the SDE GDB ###
    print('\nMoving Nashville data into AWS')

    ### For the append, set the workspace environment and list the feature classes/tables in the Input GDB ###

    dirName = os.listdir(nashImport)

    for file in dirName:

        gdb = nashImport + '\\' + file
        arcpy.env.workspace = gdb


        ### Append tables into GDB ###
        appendTableList = arcpy.ListTables()
        print('\nAppending Tables:')

        for table in appendTableList:

            try:
                arcpy.Append_management(table, nash3GIS + '\\' + table, 'NO_TEST')
                print(table)

            except:
                print('***UNABLE TO APPEND ' + str(table))
                print(arcpy.GetMessages())


        ### Append feature classes into GDB ###
        appendFeatureList = arcpy.ListFeatureClasses()
        print('\nAppending Feature Classes:')

        for fc in appendFeatureList:
            try:
                arcpy.Append_management(fc, nash3GIS + "\\" + fc, 'NO_TEST')
                print(fc)

            except:
                print('***UNABLE TO APPEND ' + str(fc))
                print(arcpy.GetMessages())

        arcpy.Delete_management(gdb)


elif proceed == False:

    print('\nNot Updating Nashville DBs')

print('\nEnd Nashville')
print('*********************************************************************')


############################################################################################
############################################################################################
### SEATTLE 2###

print('\n*** Begin Seattle 2***')

### Cycle through the Seattle folder to determine which folder is the newest ###
### according to its 'Date modified' date, and save these attribute to a variable. ###

selectedDate = ""
selectedFolder = ""
selectedName = ""

for root, dirs, files in os.walk(seaFolder):

    for file in files:

        fullPath = os.path.join(root, file)
        baseName = os.path.basename(fullPath)
        modEpoc = os.path.getmtime(fullPath)
        modTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modEpoc))

        if selectedDate < modTime:

            selectedDate = modTime
            selectedFolder = fullPath
            selectedName = baseName

print('\nThe most recent data in the Seattle 2 ShareFile is:  ' + str(selectedDate))
print('\nThe selected folder is:  ' + str(selectedFolder))
print('\nSeattle basename is: ' + selectedName)

### Open the associated text file and read in the previous date of the previous import ###

with open(seaTXT, 'r+') as textFile:

    fileReadIn = textFile.read()
    txtValue = str(fileReadIn)
    print('\nThe last Seattle 2 GDB imported was:  ' + str(txtValue))

    proceed = False

    if txtValue != selectedName:

        proceed = True

        print('\nData is outdated. Replacing with:  ' + str(selectedName))
        zip_ref = zipfile.ZipFile(selectedFolder)
        zip_ref.extractall(seaImport)
        zip_ref.close()
        print('\nData successfully unzipped')
        ### Overwrite the TXT with the new time stamp
        textFile.seek(0)
        textFile.write(str(selectedName))
        textFile.truncate()

    elif txtValue == selectedName:
        print('\nSeattle 2 data is current')

    else:
        print('\nSomething wrong happened...')


### Truncate all the tables and feature classes in the Seattle 3GIS DB if necessary ###

if proceed == True:

    print('\nTruncating Seattle 2 3GIS DB')

    ### For the truncate, set the workspace environment to the 3GIS database ###
    arcpy.env.workspace = sea3GIS

    ### Truncate Tables ###
    truncateTableList = arcpy.ListTables()
    print("\nTruncating Seattle 2 Tables:")

    for data in truncateTableList:
        print(data)
        arcpy.TruncateTable_management(data)


    ### Truncate Feature Classes ###
    truncateFeatureList = arcpy.ListFeatureClasses()
    print("\nTruncating Seattle 2 Feature Classes:")

    for data in truncateFeatureList:
        if data == 'SEA_3GIS.DBO.ASBUILT_POLYGONS':
            print("Not truncating: " + str(data))
            pass

        else:
            print(data)
            arcpy.TruncateTable_management(data)


    ### Go to Seattle AWS_Imports folder to move the data from ShareFile into the SDE GDB ###
    print('\nMoving Seattle 2 data into AWS')

    ### For the append, set the workspace environment and list the feature classes/tables in the Input GDB ###

    dirName = os.listdir(seaImport)

    for file in dirName:

        gdb = seaImport + '\\' + file
        arcpy.env.workspace = gdb


        ### Append tables into GDB ###
        appendTableList = arcpy.ListTables()
        print('\nAppending Tables:')

        for table in appendTableList:

            try:
                arcpy.Append_management(table, sea3GIS + '\\' + table, 'NO_TEST')
                print(table)
            except:
                print('***UNABLE TO APPEND ' + str(table))
                print(arcpy.GetMessages())


        ### Append feature classes into GDB ###
        appendFeatureList = arcpy.ListFeatureClasses()
        print('\nAppending Feature Classes:')

        for fc in appendFeatureList:
            try:
                arcpy.Append_management(fc, sea3GIS + "\\" + fc, 'NO_TEST')
                print(fc)
            except:
                print('***UNABLE TO APPEND ' + str(fc))
                print(arcpy.GetMessages())

        arcpy.Delete_management(gdb)


elif proceed == False:

    print('\nNot Updating Seattle 2 DB')

print('\nEnd Seattle 2')
print('*********************************************************************')



############################################################################################
############################################################################################
### SEATTLE 1 ###

print('\n*** Begin Seattle 1 ***')

### Cycle through the Seattle1 folder to determine which folder is the newest ###
### according to its 'Date modified' date, and save these attribute to a variable. ###

selectedDate = ""
selectedFolder = ""
selectedName = ""

for root, dirs, files in os.walk(sea1Folder):

    for file in files:

        fullPath = os.path.join(root, file)
        baseName = os.path.basename(fullPath)
        modEpoc = os.path.getmtime(fullPath)
        modTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modEpoc))

        if selectedDate < modTime:

            selectedDate = modTime
            selectedFolder = fullPath
            selectedName = baseName

print('\nThe most recent data in the Seattle 1 ShareFile is:  ' + str(selectedDate))
print('\nThe selected folder is:  ' + str(selectedFolder))
print('\nSeattle1 basename is: ' + selectedName)

### Open the associated text file and read in the previous date of the previous import ###

with open(sea1TXT, 'r+') as textFile:

    fileReadIn = textFile.read()
    txtValue = str(fileReadIn)
    print('\nThe last Seattle 1 GDB imported was:  ' + str(txtValue))

    proceed = False

    if txtValue != selectedName:

        proceed = True

        print('\nData is outdated. Replacing with:  ' + str(selectedName))
        zip_ref = zipfile.ZipFile(selectedFolder)
        zip_ref.extractall(sea1Import)
        zip_ref.close()
        print('\nData successfully unzipped')
        ### Overwrite the TXT with the new time stamp
        textFile.seek(0)
        textFile.write(str(selectedName))
        textFile.truncate()

    elif txtValue == selectedName:
        print('\nSeattle 1 data is current')

    else:
        print('\nSomething wrong happened...')

### Truncate all the tables and feature classes in the Seattle1 3GIS DB if necessary, and ###

if proceed == True:

    print('\nTruncating Seattle 1 3GIS DB')

    ### For the truncate, set the workspace environment to the 3GIS database ###
    arcpy.env.workspace = sea13GIS

    ### Truncate Tables ###
    truncateTableList = arcpy.ListTables()
    print("\nTruncating Seattle 1 Tables:")

    for data in truncateTableList:
        print(data)
        arcpy.TruncateTable_management(data)


    ### Truncate Feature Classes ###
    truncateFeatureList = arcpy.ListFeatureClasses()
    print("\nTruncating Seattle 1 Feature Classes:")

    for data in truncateFeatureList:
        print(data)
        arcpy.TruncateTable_management(data)

    ### For the append, set the workspace environment and list the feature classes/tables in the Input GDB ###

    dirName = os.listdir(sea1Import)

    for file in dirName:

        gdb = sea1Import + '\\' + file
        arcpy.env.workspace = gdb


        ### Append tables into GDB ###
        appendTableList = arcpy.ListTables()
        print('\nAppending Tables:')

        for table in appendTableList:

            try:
                arcpy.Append_management(table, sea13GIS + '\\' + table, 'NO_TEST')
                print(table)
            except:
                print('***UNABLE TO APPEND ' + str(table))
                print(arcpy.GetMessages())

        ### Append feature classes into GDB ###
        appendFeatureList = arcpy.ListFeatureClasses()
        print('\nAppending Feature Classes:')

        for fc in appendFeatureList:
            try:
                arcpy.Append_management(fc, sea13GIS + "\\" + fc, 'NO_TEST')
                print(fc)
            except:
                print('***UNABLE TO APPEND ' + str(fc))
                print(arcpy.GetMessages())

        arcpy.Delete_management(gdb)

        ### The following is an emulation of Justin's model @ "\\fginc-file\GIS\_Seattle1_Workspaces\PROD1_Workspace\Update Assigned & Spare Fiber.tbx\Model"
        ### and is incorporated with the nightly append of data from 3GIS exports (ShareFile)

        #Variables
        fiberSpliceTable = r'\\fginc-file\gis\dbConnections\3GIS\SEA1_3GIS as GISADMIN.sde\SEA1_3GIS.DBO.FiberSplice' #FiberSplace table
        fiberCable = r'\\fginc-file\gis\dbConnections\3GIS\SEA1_3GIS as GISADMIN.sde\SEA1_3GIS.DBO.fiberCable' #fiberCable feature class
        outTable = 'in_memory\statsTable' #output in memory stats table
        statsFields = [['AFIBERID', 'MIN'],['AFIBERID', 'MAX']] #Statistics Fields
        caseField = 'ASEGMENTIDFKEY' # Case Field

        #Arcpy Functions
        print('Generating Statistics Table...\n')
        arcpy.Statistics_analysis(fiberSpliceTable, outTable, statsFields, caseField) # Compute statistics table

        print('Making fiberCable Feature Layer... \n')
        arcpy.MakeFeatureLayer_management(fiberCable, 'fiberCableFL') # Make fiberCable a feature layer

        print('Joining Tables...\n')
        arcpy.AddJoin_management('fiberCableFL', 'SEGMENTID', outTable, caseField, 'KEEP_COMMON') # Join the fiberSpliceTable to the fiberCable (inner join)

        print('Calculating Fields...\n')
        arcpy.CalculateField_management('fiberCableFL',
                                        'SEA1_3GIS.DBO.fiberCable.Assigned_Fiber',
                                        "str(int(!statsTable.MIN_AFIBERID!)) + ' - ' + str(int(!statsTable.MAX_AFIBERID!))", "PYTHON_9.3")

elif proceed == False:

    print('\nNot Updating Seattle 1 DBs')

print('\nEnd Seattle 1')

############################################################################################
############################################################################################

print('\nProcess Complete')


# Disregard for now
# if __name__ == '__main__':
#     hostname = "myaccount.sharefile.com"
#     username = "ndshare@fg-inc.net"
#     password = "NDuploads18!"
#     client_id = 'myclientid'
#     client_secret = 'myclientsecret'
#
#     token = authenticate(hostname, client_id, client_secret, username, password)
# api = "https://foresitegroupinc.sf-api.com/sf/v3"
