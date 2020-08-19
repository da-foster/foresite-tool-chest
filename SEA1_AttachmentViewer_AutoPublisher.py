### Title: SEA1_AttachmentViewer_AutoPublisher.py
### Description: This Python script publishes a refreshed hosted feature layer to ArcGIS Online, which is then
###              consumed in Attachment Viewer. This script is intended to be triggered on a nightly basis in
###              order for new data to be visible from the previous day.
### Company: Foresite Group
### Author: Darren Foster
### MUST RUN IN PYTHON 3.6 ###

import arcpy
import os
from arcgis.gis import GIS
from datetime import datetime
arcpy.env.overwriteOutput = True

### Sign in to portal (In this case, sign into ArcGIS Online) ###
arcpy.SignInToPortal('https://www.arcgis.com', 'fgarconline', 'ForesiteROKS19!')

### Set constants ###
OUT_DIR = r'\\fginc-file\GIS\Foster\AutoPublishing\SEA1_AttachmentViewer'
SERVICE = 'SEA1_AttViewer_HFS'
SD_DRAFT = SERVICE + '.sddraft'
SD_FILENAME = SERVICE + '.sd'
LOG = r'\\fginc-file\GIS\Foster\AutoPublishing\SEA1_AttachmentViewer\Logger.txt'

### Construct a GIS object ###
gis = GIS('https://www.arcgis.com', 'fgarconline', 'ForesiteROKS19!')

### Paths to the Service Definition and the Draft ###
sdDraftOutput = os.path.join(OUT_DIR, SD_DRAFT)
sdPath = os.path.join(OUT_DIR, SD_FILENAME)

### Process to field calculate the Pole's and Structure's COUNT_ATTACHMENT fields with an Arcade Expression ###
#Poles Feature Class path
poles = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.DetailedDesign_SEA1\Seattle.DBO.PLD_Poles_SEA1'
#Structures Feature Class path
structures = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.CRO_SEA1\Seattle.DBO.CRO_Structure_SEA1'
#Field Name (for both)
field = 'COUNT_ATTACHMENTS'

try:
    #Select all features in the Poles Feature Class
    print('Field calculating Poles')
    arcpy.SelectLayerByAttribute_management(poles, 'NEW_SELECTION')
    #Field calculate all the Poles
    arcpy.CalculateField_management(poles, field, 'Count(Attachments($feature))', 'ARCADE')
    #Clear the selection
    arcpy.SelectLayerByAttribute_management(poles, 'CLEAR_SELECTION')
    print('Field Calculating Poles - Complete')

except Exception as ex:
    snapShot = datetime.today()
    with open(LOG, 'a') as logger:
        logger.write('\n' + 'Failure to calculate poles at: ' + str(snapShot) + "'" + str(ex) + "'")
    print(ex)

try:
    #Select all features in the Structures Feature Class
    print('Field calculating Structures')
    arcpy.SelectLayerByAttribute_management(structures, 'NEW_SELECTION')
    #Field calculate all the Structures
    arcpy.CalculateField_management(structures, field, 'Count(Attachments($feature))', 'ARCADE')
    #Clear the selection
    arcpy.SelectLayerByAttribute_management(structures, 'CLEAR_SELECTION')
    print('Field Calculating Structures - Complete')

except Exception as ex:
    snapShot = datetime.today()
    with open(LOG, 'a') as logger:
        logger.write('\n' + 'Failure to calculate Structures at: ' + str(snapShot) + "'" + str(ex) + "'")
    print(ex)

# ### OPTIONAL: If the SD Draft / SD should exist already, and you want to delete them, do so here ###
# def deletePreviousSD(sdDraftPath, sdPath):
#     if os.path.exists(sdDraftOutput):
#         print("Removing previous SD draft")
#         os.remove(sdDraftOutput)
#     if os.path.exists(sdPath):
#         print("Removing previous SD")
#         os.remove(sdPath)
#
# deletePreviousSD(sdDraftOutput, sdPath)
# ### OPTIONAL: Get an array of items to delete in AGOL based on a query###
# def deleteAgolItems():
#     items = gis.content.search(query="ex. Test_AV_SEA1", item_type="ex. Service Definition") #Must updated per service
#     for item in items:
#         print("Deleting " + str(item.name))
#         item.delete()
#
# deleteAgolItems()

### Reference map to publish ###
aprx = r'\\fginc-file\GIS\Foster\AutoPublishing\SEA1_AttachmentViewer\SEA1_AttViewer_HFS.aprx'
prj = arcpy.mp.ArcGISProject(aprx)
m = prj.listMaps()[0] #Specifies the first (and only) map in the .aprx
names = [x.name for x in m.listLayers()] #Run this to verify the right layers in map
print(names)

### Create FeatureSharingDraft and set service properties ###
sharing_draft = m.getWebLayerSharingDraft('HOSTING_SERVER', 'FEATURE', SERVICE)
### Set the overwrite property to true ###
sharing_draft.overwriteExistingService = True
### Pass in the folder location ###
sharing_draft.portalFolder = 'VZ-Seattle1 Client and Sub'
### Create Service Definition Draft file ###
sharing_draft.exportToSDDraft(sdDraftOutput)

### Stage the Service ###
sdFilenameOutput = os.path.join(OUT_DIR, SD_FILENAME)

try:
    print('Staging the Service')
    arcpy.StageService_server(sdDraftOutput, sdFilenameOutput)
    print('Staging Complete')
    
except Exception as ex:
    print('Staging failed')
    print(ex)
    snapShot = datetime.today()
    with open(LOG, 'a') as logger:
        logger.write('\n' + 'Failure to stage the service at: ' + str(snapShot))

### Share to ArcGIS Online (or Portal) ###
try:
    print('Uploading Service Definition...')
    arcpy.UploadServiceDefinition_server(sdFilenameOutput, 'My Hosted Services')
    print('Successfully Uploaded service.')
    snapShot = datetime.today()
    with open(LOG, 'a') as logger:
        logger.write('\n' + 'Success at: ' + str(snapShot))

except Exception as ex:
    print('Unable to upload Service Definition')
    print(ex)
    snapShot = datetime.today()
    with open(LOG, 'a') as logger:
        logger.write('\n' + 'Failure to upload Service Definition at: ' + str(snapShot))
