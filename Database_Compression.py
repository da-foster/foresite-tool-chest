### Title: Database_Compression.py
### Description: This Python tool loops through each of the SDE connections stored in a folder 
###              location, and attempts to compress each database. A corresponding log is
###              updated based on whether the database is successfully compressed or not.
### Company: Foresite Group
### Author: Darren Foster

### RUNS IN PYTHON 2.7 ###
import arcpy
import os
from datetime import datetime

# Location of folder storing the SDE connections
dbFolder = r"\\fginc-file\gis\dbConnections\GISADMIN Connections"
# Location storing the logs for successfully compressed databases
compressLogPass = r"\\fginc-file\GIS\Foster\DatabaseCompression\DBCompressLogPASS.txt"
# Location storing the logs for unsuccessfully compressed databases
compressLogFail = r"\\fginc-file\GIS\Foster\DatabaseCompression\DBCompressLogFAIL.txt"


# The last night this tool was ran
lastRan = datetime.today()
lastRunTxt = r"\\fginc-file\GIS\Foster\DatabaseCompression\LastRan.txt"
with open(lastRunTxt, 'r+') as textFile:
    textFile.write(str(lastRan))

class DatabaseCompression:
    # Constructor
    def __init__(self, dbfolder, compresslogpass, compresslogfail):
        self.dbfolder = dbfolder
        self.compresslogpass = compresslogpass
        self.compresslogfail = compresslogfail

    # compress() loops through the database connections folder, tries to compress each SDE
    # connection, and generates an entry in the associated log
    def compress(self):
        for root, dirs, files in os.walk(self.dbfolder):
            for fileName in files:
                fullPath = os.path.join(root, fileName)
                try:
                    snapshot = datetime.today()
                    print("Compressing " + fileName)
                    arcpy.Compress_management(fullPath)
                    txtPass = open(self.compresslogpass, 'a')
                    txtPass.write("\n" + fileName + " succeeded at: " + str(snapshot))
                    txtPass.close()
                    
                except:
                    snapshot = datetime.today()
                    print("FAILED: " + fileName)
                    txtFail = open(self.compresslogfail, 'a')
                    txtFail.write("\n" + fileName + " failed at: " + str(snapshot))
                    txtFail.close()


if __name__ == "__main__":
    # Instantiate DatabaseCompression 
    instance = DatabaseCompression(dbFolder, compressLogPass, compressLogFail)
    instance.compress()
