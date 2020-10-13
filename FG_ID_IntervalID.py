### Title: FG_ID_IntervalID.py
### Description: Ongoing dev of a tool to populate the IntervalID & FG_ID fields.
###              Currently have this working for anchors... Make class-based to handle all 14 feature class
###              
###              
### Company: Foresite Group
### Author: Darren Foster
### MUST RUN IN PYTHON 2.7 ###

import arcpy

### Global variables ###
arr = []
num = 0
anchorsFC = r'\\fginc-file\GIS\dbConnections\TEST_ENVS\TEST_2 as GISADMIN.sde\TEST_2.DBO.SEA1_Detailed_Design_Tryouts\TEST_2.DBO.Anchor_SEA1'
borepitFC = r'\\fginc-file\GIS\dbConnections\TEST_ENVS\TEST_2 as GISADMIN.sde\TEST_2.DBO.SEA1_Detailed_Design_Tryouts\TEST_2.DBO.Bore_pits_SEA1'
fiberFC = r'\\fginc-file\GIS\dbConnections\TEST_ENVS\TEST_2 as GISADMIN.sde\TEST_2.DBO.SEA1_Detailed_Design_Tryouts\TEST_2.DBO.fiberCable_SEA1'
equipFC = r'\\fginc-file\GIS\dbConnections\TEST_ENVS\TEST_2 as GISADMIN.sde\TEST_2.DBO.SEA1_Detailed_Design_Tryouts\TEST_2.DBO.fiberequipment_SEA1'
midspanFC = r'\\fginc-file\GIS\dbConnections\TEST_ENVS\TEST_2 as GISADMIN.sde\TEST_2.DBO.SEA1_Detailed_Design_Tryouts\TEST_2.DBO.Midspan_Clearance_SEA1'
permitFC = r'\\fginc-file\GIS\dbConnections\TEST_ENVS\TEST_2 as GISADMIN.sde\TEST_2.DBO.SEA1_Detailed_Design_Tryouts\TEST_2.DBO.Permit_Polygons_SEA1'
poleFC = r'\\fginc-file\GIS\dbConnections\TEST_ENVS\TEST_2 as GISADMIN.sde\TEST_2.DBO.PLD_Poles_SEA1'
qcpFC = r'\\fginc-file\GIS\dbConnections\TEST_ENVS\TEST_2 as GISADMIN.sde\TEST_2.DBO.SEA1_Detailed_Design_Tryouts\TEST_2.DBO.QC_Polygons_SEA1'
sectorFC = r'\\fginc-file\GIS\dbConnections\TEST_ENVS\TEST_2 as GISADMIN.sde\TEST_2.DBO.SEA1_Detailed_Design_Tryouts\TEST_2.DBO.Sector_Carrier_Groups_SEA1'
slackFC = r'\\fginc-file\GIS\dbConnections\TEST_ENVS\TEST_2 as GISADMIN.sde\TEST_2.DBO.SEA1_Detailed_Design_Tryouts\TEST_2.DBO.slackloop_SEA1'
interceptFC = r'\\fginc-file\GIS\dbConnections\TEST_ENVS\TEST_2 as GISADMIN.sde\TEST_2.DBO.SEA1_Detailed_Design_Tryouts\TEST_2.DBO.Span_Intercept_SEA1'
spanFC = r'\\fginc-file\GIS\dbConnections\TEST_ENVS\TEST_2 as GISADMIN.sde\TEST_2.DBO.SEA1_Detailed_Design_Tryouts\TEST_2.DBO.Span_SEA1'
spliceFC = r'\\fginc-file\GIS\dbConnections\TEST_ENVS\TEST_2 as GISADMIN.sde\TEST_2.DBO.SEA1_Detailed_Design_Tryouts\TEST_2.DBO.spliceclosure_SEA1'
structureFC = r'\\fginc-file\GIS\dbConnections\TEST_ENVS\TEST_2 as GISADMIN.sde\TEST_2.DBO.SEA1_Detailed_Design_Tryouts\TEST_2.DBO.structure_SEA1'

### Fields to use in each feature class ###
fields = ['INTERVAL_ID', 'FG_ID']

### Dictionary of prefixes ###
prefixes = {'anchor' : 'ANC-',
            'bore' : 'PIT-',
            'fiber' : 'FIB-',
            'equip' : 'EQ-',
            'midspan' : 'MID-',
            'permit' : 'PMT-',
            'pole' : 'POLE-',
            'qcp' : 'QCP-',
            'sector' : 'SEC-',
            'slack' : 'LOOP-',
            'intercept' : 'INT-',
            'span' : 'SPAN-',
            'splice' : 'SPL-',
            'structure' : 'STR-'}

### Method to return the next interval ###
def autoIncrement():
    global num
    interval = 1
    if (num == 0):
        num = 1
    else:
        num += interval
    return num

### Append all the numbers from the IntervalID field into the list ###
with arcpy.da.SearchCursor(anchorsFC, fields) as cur:
    for row in cur:
        if row[0] is not None:
            arr.append(row[0])

### Find the highest number in the list ###
if len(arr) == 0:
    print('Empty array')
else:
    max_num = max(arr)
    print('Max num is: ' + str(max_num))
    num = max_num

### Method to update the IntervalID & FG_ID fields ###
arcpy.MakeFeatureLayer_management(anchorsFC, 'anchors')

arcpy.SelectLayerByAttribute_management('anchors', "NEW_SELECTION", "INTERVAL_ID IS NULL")

print('Selection count is: ' + str(arcpy.GetCount_management("anchors")))

with arcpy.da.UpdateCursor('anchors', fields) as cur:
    for row in cur:
        #Update the IntervalID field
        val = autoIncrement()
        print('Val = ' + str(val))
        row[0] = val
        #Update the FG_ID field
        pfx = prefixes['anchor']
        fgID = pfx + str(val)
        print('FG_ID = ' + fgID)
        row[1] = fgID
        cur.updateRow(row)
