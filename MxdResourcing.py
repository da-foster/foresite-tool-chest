### Title: MXDResourcingTool.py
### Description: This Python tool loops through each of the layers within the dataframe,
###              and resources them to the SQL user set within the input parameters.
###              Each user takes 3 input paramters: (1) is the named user. (2) is their
###              specific database connection that corresponds to the data within the
###              dataframe (e.g. if the mxd contains data from the Utopia database,
###              resource the layers to that user's SQL connection into the Utopia database).
###              (3) the output folder location where the new mxd will be saved.
### Company: Foresite Group
### Author: Darren Foster

### RUNS IN PYTHON 2.7 ###

import arcpy
import os

mxd = arcpy.mapping.MapDocument("CURRENT")

### First User ###
userInput1 = arcpy.GetParameterAsText(0)
dbcInput1 = arcpy.GetParameterAsText(1)
outPath1 = arcpy.GetParameterAsText(2)

### Second User ###
userInput2 = arcpy.GetParameterAsText(3)
dbcInput2 = arcpy.GetParameterAsText(4)
outPath2 = arcpy.GetParameterAsText(5)

### Third User
userInput3 = arcpy.GetParameterAsText(6)
dbcInput3 = arcpy.GetParameterAsText(7)
outPath3 = arcpy.GetParameterAsText(8)

### Fourth User ###
userInput4 = arcpy.GetParameterAsText(9)
dbcInput4 = arcpy.GetParameterAsText(10)
outPath4 = arcpy.GetParameterAsText(11)

### Fifth User ###
userInput5 = arcpy.GetParameterAsText(12)
dbcInput5 = arcpy.GetParameterAsText(13)
outPath5 = arcpy.GetParameterAsText(14)


class MxdResource:

    def __init__(self, mxd, user, userDBC, outPath):

        self.mxd = mxd
        self.user = user
        self.userDBC = userDBC
        self.outPath = outPath

    def swap_connection(self):

        for lyr in arcpy.mapping.ListLayers(self.mxd):

            try:
                if lyr.isFeatureLayer == False:
                    pass
                elif lyr.isFeatureLayer == True:
                    lyr.replaceDataSource(self.userDBC)
                    arcpy.AddMessage("\n" + str(lyr) + " resourced to: " + str(self.userDBC))

            except:
                print(arcpy.GetMessages())
                arcpy.AddMessage("\nUnable to resource: " + str(lyr))

    def copy_mxd(self):

        savePath = str(self.outPath)  #a self reference to the out path parameter
        outMXD = self.mxd #a self reference to the mxd parameter

        mapPath = outMXD.filePath #the file path to the mxd itself
        baseName = os.path.basename(mapPath) #grabbing the base name of the file (eliminating the remainder of the file path)
        baseSplit = str(os.path.splitext(baseName)[0]) #Remove the file extension from the string (.mxd)
        userInitials = str(self.user[:2]).upper() # appending the (2 upper) initials of the user to the end of the mxd name (ex. "_DF.mxd")

        newMXD = os.path.join(savePath, baseSplit + "_" + userInitials) #construct the new path of the output
        arcpy.AddMessage("\nOut path = " + str(newMXD)) #print a message to the console confirming the out path.

        outMXD.saveACopy(newMXD)


### MxdResource instance # 1 ### 
instance1 = MxdResource(mxd, userInput1, dbcInput1, outPath1)
instance1.swap_connection()
instance1.copy_mxd()

### MxdResource instance # 2 ###
instance2 = MxdResource(mxd, userInput2, dbcInput2, outPath2)
instance2.swap_connection()
instance2.copy_mxd()

### MxdResource instance # 3 ###
instance3 = MxdResource(mxd, userInput3, dbcInput3, outPath3)
instance3.swap_connection()
instance3.copy_mxd()

### MxdResource instance # 4 ###
instance4 = MxdResource(mxd, userInput4, dbcInput4, outPath4)
instance4.swap_connection()
instance4.copy_mxd()

### MxdResource instance # 5 ###
instance5 = MxdResource(mxd, userInput5, dbcInput5, outPath5)
instance5.swap_connection()
instance5.copy_mxd()
