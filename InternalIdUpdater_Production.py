### Title: InternalIdUpdater_Production.py
### Description: Python tool to update the IntervalID and FG_ID fields 
###              for the feature classes within the Detailed Design dataset.
###              Execute via the .bat file        
### Company: Foresite Group
### Author: Darren Foster
### MUST RUN IN PYTHON 2.7 ###

import arcpy
import os
from datetime import datetime

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
        print('Begin ' + flName)
        arcpy.MakeFeatureLayer_management(self.inputData, flName)
        arcpy.SelectLayerByAttribute_management(flName, "NEW_SELECTION", "INTERVAL_ID IS NULL")
        result = arcpy.GetCount_management(flName)
        count = int(result.getOutput(0))#This is important!
        print('The selection count is: ' + str(count))
        
        if count == 0:
            print('There is nothing to update for ' + flName)
        
        elif count > 0:
            print('Updating Null records')
            workspace = self.getDbPath()
            edit = arcpy.da.Editor(workspace)
            edit.startEditing(False, True)
            edit.startOperation()
            print('Selection count of ' + self.typeOfData + ' is: ' + str(arcpy.GetCount_management(flName)))
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


#Main Function
if __name__ == '__main__':

    anchorsFC = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.DetailedDesign_SEA1\Seattle.DBO.Anchor_SEA1'
    borepitFC = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.DetailedDesign_SEA1\Seattle.DBO.Bore_pits_SEA1'
    fiberFC = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.DetailedDesign_SEA1\Seattle.DBO.fiberCable_SEA1'
    equipFC = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.DetailedDesign_SEA1\Seattle.DBO.fiberequipment_SEA1'
    midspanFC = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.DetailedDesign_SEA1\Seattle.DBO.Midspan_Clearance_SEA1'
    permitFC = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.DetailedDesign_SEA1\Seattle.DBO.Permit_Polygons_SEA1'
    poleFC = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.DetailedDesign_SEA1\Seattle.DBO.PLD_Poles_SEA1'
    qcpFC = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.DetailedDesign_SEA1\Seattle.DBO.QC_Polygons_SEA1'
    sectorFC = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.DetailedDesign_SEA1\Seattle.DBO.Sector_Carrier_Groups_SEA1'
    slackFC = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.DetailedDesign_SEA1\Seattle.DBO.slackloop_SEA1'
    interceptFC = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.DetailedDesign_SEA1\Seattle.DBO.Span_Intercept_SEA1'
    spanFC = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.DetailedDesign_SEA1\Seattle.DBO.Span_SEA1'
    spliceFC = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.DetailedDesign_SEA1\Seattle.DBO.spliceclosure_SEA1'
    structureFC = r'\\fginc-file\gis\dbConnections\GISADMIN Connections\Seattle as gisadmin.sde\Seattle.DBO.DetailedDesign_SEA1\Seattle.DBO.structure_SEA1'

    LOG = r'\\fginc-file\GIS\Foster\InternalID_Updater\LOGGER.txt'
    full_success = True
    
    #Anchor Instance
    try:
        anchorInst = InternalIdUpdater('anchors', anchorsFC)
        anchorInst.fillList()
        anchorInst.findHighestVal()
        anchorInst.updateFields()
        print('\n')
        
    except Exception as ex:
        full_success = False
        print('Failure on Anchors')
        snapShot = datetime.today()
        with open(LOG, 'a') as logger:
            logger.write('\n' + 'Failure to update Anchors: ' + str(snapShot) + " '" + str(ex) + "'")
        print(ex)
        print('\n')
        
    
    #Bore Pit Instance
    try: 
        borepitInst = InternalIdUpdater('borepits', borepitFC)
        borepitInst.fillList()
        borepitInst.findHighestVal()
        borepitInst.updateFields()
        print('\n')
        
    except Exception as ex:
        full_success = False
        print('Failure on Bore Pits')
        snapShot = datetime.today()
        with open(LOG, 'a') as logger:
            logger.write('\n' + 'Failure to update Bore Pits: ' + str(snapShot) + " '" + str(ex) + "'")
        print(ex)
        print('\n')

    #Fiber cable Instance
    try:
        fiberInst = InternalIdUpdater('fibercables', fiberFC)
        fiberInst.fillList()
        fiberInst.findHighestVal()
        fiberInst.updateFields()
        print('\n')

    except Exception as ex:
        full_success = False
        print('Failure on Fiber Cables')
        snapShot = datetime.today()
        with open(LOG, 'a') as logger:
            logger.write('\n' + 'Failure to update Fiber Cables: ' + str(snapShot) + " '" + str(ex) + "'")
        print(ex)
        print('\n')

    #Fiber Equipment Instance
    try: 
        equipInst = InternalIdUpdater('equipment', equipFC)
        equipInst.fillList()
        equipInst.findHighestVal()
        equipInst.updateFields()
        print('\n')
        
    except Exception as ex:
        full_success = False
        print('Failure on Fiber Equipment')
        snapShot = datetime.today()
        with open(LOG, 'a') as logger:
            logger.write('\n' + 'Failure to update Fiber Equipment: ' + str(snapShot) + " '" + str(ex) + "'")
        print(ex)
        print('\n')

    #Midspance Clearance Instance
    try:
        midspanInst = InternalIdUpdater('midspan', midspanFC)
        midspanInst.fillList()
        midspanInst.findHighestVal()
        midspanInst.updateFields()
        print('\n')

    except Exception as ex:
        full_success = False
        print('Failure on Midspance Clearance')
        snapShot = datetime.today()
        with open(LOG, 'a') as logger:
            logger.write('\n' + 'Failure to update Midspance Clearance: ' + str(snapShot) + " '" + str(ex) + "'")
        print(ex)
        print('\n')

    #Permit Polygons Instance
    try:
        permitInst = InternalIdUpdater('permits', permitFC)
        permitInst.fillList()
        permitInst.findHighestVal()
        permitInst.updateFields()
        print('\n')

    except Exception as ex:
        full_success = False
        print('Failure on Permit Polygons')
        snapShot = datetime.today()
        with open(LOG, 'a') as logger:
            logger.write('\n' + 'Failure to update Permit Polygons: ' + str(snapShot) + " '" + str(ex) + "'")
        print(ex)
        print('\n')

    #Poles Instance
    try:
        poleInst = InternalIdUpdater('poles', poleFC)
        poleInst.fillList()
        poleInst.findHighestVal()
        poleInst.updateFields()
        print('\n')

    except Exception as ex:
        full_success = False
        print('Failure on Poles')
        snapShot = datetime.today()
        with open(LOG, 'a') as logger:
            logger.write('\n' + 'Failure to update Poles: ' + str(snapShot) + " '" + str(ex) + "'")
        print(ex)
        print('\n')

    #QC Polygons Instance
    try:
        qcpInst = InternalIdUpdater('polygons', qcpFC)
        qcpInst.fillList()
        qcpInst.findHighestVal()
        qcpInst.updateFields()
        print('\n')

    except Exception as ex:
        full_success = False
        print('Failure on QC Polygons')
        snapShot = datetime.today()
        with open(LOG, 'a') as logger:
            logger.write('\n' + 'Failure to update QC Polygons: ' + str(snapShot) + " '" + str(ex) + "'")
        print(ex)
        print('\n')

    #Sector Carrier Groups Instance
    try:
        sectorInst = InternalIdUpdater('sectors', sectorFC)
        sectorInst.fillList()
        sectorInst.findHighestVal()
        sectorInst.updateFields()
        print('\n')

    except Exception as ex:
        full_success = False
        print('Failure on Sector Carrier Groups')
        snapShot = datetime.today()
        with open(LOG, 'a') as logger:
            logger.write('\n' + 'Failure to update Sector Carrier Groups: ' + str(snapShot) + " '" + str(ex) + "'")
        print(ex)
        print('\n')

    #Slackloop Instance
    try:
        slackInst = InternalIdUpdater('slackloops', slackFC)
        slackInst.fillList()
        slackInst.findHighestVal()
        slackInst.updateFields()
        print('\n')

    except Exception as ex:
        full_success = False
        print('Failure on Slackloops')
        snapShot = datetime.today()
        with open(LOG, 'a') as logger:
            logger.write('\n' + 'Failure to update Slackloops: ' + str(snapShot) + " '" + str(ex) + "'")
        print(ex)
        print('\n')

    #Span Intercept Instance
    try:
        interceptInst = InternalIdUpdater('intercepts', interceptFC)
        interceptInst.fillList()
        interceptInst.findHighestVal()
        interceptInst.updateFields()
        print('\n')

    except Exception as ex:
        full_success = False
        print('Failure on Span Intercept')
        snapShot = datetime.today()
        with open(LOG, 'a') as logger:
            logger.write('\n' + 'Failure to update Span Intercept: ' + str(snapShot) + " '" + str(ex) + "'")
        print(ex)
        print('\n')

    #Span Instance
    try:
        spanInst = InternalIdUpdater('span', spanFC)
        spanInst.fillList()
        spanInst.findHighestVal()
        spanInst.updateFields()
        print('\n')
        
    except Exception as ex:
        full_success = False
        print('Failure on Span')
        snapShot = datetime.today()
        with open(LOG, 'a') as logger:
            logger.write('\n' + 'Failure to update Span: ' + str(snapShot) + " '" + str(ex) + "'")
        print(ex)
        print('\n')

    #Splice Closure Instance
    try:
        spliceInst = InternalIdUpdater('spliceclosures', spliceFC)
        spliceInst.fillList()
        spliceInst.findHighestVal()
        spliceInst.updateFields()
        print('\n')

    except Exception as ex:
        full_success = False
        print('Failure on Splice Closure')
        snapShot = datetime.today()
        with open(LOG, 'a') as logger:
            logger.write('\n' + 'Failure to update Splice Closures: ' + str(snapShot) + " '" + str(ex) + "'")
        print(ex)
        print('\n')

    #Structure Instance
    try:
        structureInst = InternalIdUpdater('structures', structureFC)
        structureInst.fillList()
        structureInst.findHighestVal()
        structureInst.updateFields()
        print('\n')

    except Exception as ex:
        full_success = False
        print('Failure on Structures')
        snapShot = datetime.today()
        with open(LOG, 'a') as logger:
            logger.write('\n' + 'Failure to update Structures: ' + str(snapShot) + " '" + str(ex) + "'")
        print(ex)

    #Write to LOGGER if full success
    if full_success:
        print('Full success!')
        snapShot = datetime.today()
        with open(LOG, 'a') as logger:
            logger.write('\n' + 'Full Success: ' + str(snapShot))
