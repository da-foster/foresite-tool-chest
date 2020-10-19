### Title: InternalIdUpdater_v2.py
### Description: Python tool to update the IntervalID and FG_ID fields 
###              for the feature classes within the Detailed Design dataset.
###              Execute via the .bat file        
### Company: Foresite Group
### Author: Darren Foster
### MUST RUN IN PYTHON 2.7 ###

import arcpy
import os

class InternalIdUpdater:
    #Constructor
    def __init__(self, typeOfData, inputData):
        self.typeOfData = typeOfData
        self.inputData = inputData
        self.num = 0
        self.arr = []
        self.fields = ['INTERVAL_ID', 'FG_ID']
        self.prefixes = {'anchor': 'ANC-',
                         'bore': 'PIT-',
                         'fiber': 'FIB-',
                         'equip': 'EQ-',
                         'midspan': 'MID-',
                         'permit': 'PMT-',
                         'pole': 'POLE-',
                         'qcp': 'QCP-',
                         'sector': 'SEC-',
                         'slack': 'LOOP-',
                         'intercept': 'INT-',
                         'span': 'SPAN-',
                         'splice': 'SPL-',
                         'structure': 'STR-'}

    #Method to append all the numbers from the IntervalID field into the list
    def fillList(self):
        with arcpy.da.SearchCursor(self.inputData, self.fields) as cur:
            for row in cur:
                if row[0] is not None:
                    self.arr.append(row[0])

    #Method to find the highest number in the list
    def findHighestVal(self):
        if len(self.arr) == 0:
            print('Empty list')
        else:
            max_num = max(self.arr)
            print('Max num is: ' + str(max_num))
            self.num = max_num

    #Method to get the path to the SDE
    def getDbPath(self):
        sdePath = os.path.dirname(self.inputData)
        if [any(ext) for ext in ('.gdb', '.sde') if ext in os.path.splitext(sdePath)]:
            return sdePath
        else:
            return os.path.dirname(sdePath)

    #Method to return the next interval
    def autoIncrement(self):
        #global num
        interval = 1
        if self.num == 0:
            self.num = 1
        else:
            self.num += interval
        return self.num

    #Method to determine the prefix
    def selectPrefix(self):
        pfx = None
        if self.typeOfData == 'anchors':
            pfx = self.prefixes['anchor']
        elif self.typeOfData == 'borepits':
            pfx = self.prefixes['bore']
        elif self.typeOfData == 'fibercables':
            pfx = self.prefixes['fiber']
        elif self.typeOfData == 'equipment':
            pfx = self.prefixes['equip']
        elif self.typeOfData == 'midspan':
            pfx = self.prefixes['midspan']
        elif self.typeOfData == 'permits':
            pfx = self.prefixes['permit']
        elif self.typeOfData == 'poles':
            pfx = self.prefixes['pole']
        elif self.typeOfData == 'polygons':
            pfx = self.prefixes['qcp']
        elif self.typeOfData == 'sectors':
            pfx = self.prefixes['sector']
        elif self.typeOfData == 'slackloops':
            pfx = self.prefixes['slack']
        elif self.typeOfData == 'intercepts':
            pfx = self.prefixes['intercept']
        elif self.typeOfData == 'span':
            pfx = self.prefixes['span']
        elif self.typeOfData == 'spliceclosures':
            pfx = self.prefixes['splice']
        elif self.typeOfData == 'structures':
            pfx = self.prefixes['structure']

        return pfx

    ### Method to update the IntervalID & FG_ID fields ###
    def updateFields(self):
        flName = self.typeOfData + '_featurelayer'
        arcpy.MakeFeatureLayer_management(self.inputData, flName)
        arcpy.SelectLayerByAttribute_management(flName, "NEW_SELECTION", "INTERVAL_ID IS NULL")

        if len(arcpy.GetCount_management(flName)) == 0:
            print('Selection count is: 0. Nothing to update')
            print('Complete')

        else:
            workspace = self.getDbPath()
            edit = arcpy.da.Editor(workspace)
            edit.startEditing(False, False)
            edit.startOperation()
            print('Selection count is: ' + str(arcpy.GetCount_management(flName)))
            with arcpy.da.UpdateCursor(flName, self.fields) as cur:
                for row in cur:
                    # Update the IntervalID field
                    val = self.autoIncrement()
                    print('Val = ' + str(val))
                    row[0] = val
                    # Update the FG_ID field
                    code = self.selectPrefix()
                    fgID = code + str(val)
                    print('FG_ID = ' + fgID)
                    row[1] = fgID
                    cur.updateRow(row)
            edit.stopOperation()
            edit.stopEditing(True)
            print('Complete')

#Main Fuction
if __name__ == '__main__':

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

    #Anchor Instance
    anchorInst = InternalIdUpdater('anchors', anchorsFC)
    anchorInst.fillList()
    anchorInst.findHighestVal()
    anchorInst.updateFields()
    
    #Bore Pit Instance
    borepitInst = InternalIdUpdater('borepits', borepitFC)
    borepitInst.fillList()
    borepitInst.findHighestVal()
    borepitInst.updateFields()
    
    #Fiber cable Instance
    fiberInst = InternalIdUpdater('fibercables', fiberFC)
    fiberInst.fillList()
    fiberInst.findHighestVal()
    fiberInst.updateFields()
    
    #Fiber Equipment Instance
    equipInst = InternalIdUpdater('equipment', equipFC)
    equipInst.fillList()
    equipInst.findHighestVal()
    equipInst.updateFields()

    #Midspance Clearance Instance
    midspanInst = InternalIdUpdater('midspan', midspanFC)
    midspanInst.fillList()
    midspanInst.findHighestVal()
    midspanInst.updateFields()
    
    #Permit Polygons Instance
    permitInst = InternalIdUpdater('permits', permitFC)
    permitInst.fillList()
    permitInst.findHighestVal()
    permitInst.updateFields()

    #Poles Instance
    poleInst = InternalIdUpdater('poles', poleFC)
    poleInst.fillList()
    poleInst.findHighestVal()
    poleInst.updateFields()

    #QC Polygons Instance
    qcpInst = InternalIdUpdater('polygons', qcpFC)
    qcpInst.fillList()
    qcpInst.findHighestVal()
    qcpInst.updateFields()
    
    #Sector Carrier Groups Instance
    sectorInst = InternalIdUpdater('sectors', sectorFC)
    sectorInst.fillList()
    sectorInst.findHighestVal()
    sectorInst.updateFields()

    #Slackloop Instance
    slackInst = InternalIdUpdater('slackloops', slackFC)
    slackInst.fillList()
    slackInst.findHighestVal()
    slackInst.updateFields()

    #Span Intercept Instance
    interceptInst = InternalIdUpdater('intercepts', interceptFC)
    interceptInst.fillList()
    interceptInst.findHighestVal()
    interceptInst.updateFields()
    
    #Span Instance
    spanInst = InternalIdUpdater('span', spanFC)
    spanInst.fillList()
    spanInst.findHighestVal()
    spanInst.updateFields()

    #Splice Closure Instance
    spliceInst = InternalIdUpdater('spliceclosures', spliceFC)
    spliceInst.fillList()
    spliceInst.findHighestVal()
    spliceInst.updateFields()

    #Structure Instance
    structureInst = InternalIdUpdater('structures', structureFC)
    structureInst.fillList()
    structureInst.findHighestVal()
    structureInst.updateFields()
