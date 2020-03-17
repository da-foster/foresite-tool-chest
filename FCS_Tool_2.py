### Title: Fiber Cable Schedule (FCS) Tool
### Description: A table join and comparison of the Fiber Cable Schedule 
###              table and the exported CSV from the Seattle Segment Tracker.
###              Any new records in the CSV table will be appended into the
###              Fiber Cable Schedule table.
### Company: Foresite Group
### Author: Darren Foster

import arcpy
import csv

from datetime import datetime

arcpy.env.overwriteOutput = True



##### Set Date Info #####

date = datetime.today()

today = str(date.month) + str(date.day) + str(date.year)



##### Establish Folder Path / Create new GDB #####

folder_path = "C:/GIS/_Seattle_Workspaces/SEAPROD1_Workspace/FiberCableSchedule"

gdbName = "scratchFCS_" + str(today)

arcpy.CreateFileGDB_management(folder_path, gdbName)

gdbPath = folder_path + "/" + gdbName + ".gdb"

print "... GDB Created"



##### Re-create CSV without blank rows #####

csvTable = folder_path + "/" + "FG_Segment_SS_" + today + ".csv" 

with open(csvTable) as in_file:
    with open(csvTable.split(".csv")[0] + "_2" + ".csv", 'w') as out_file:
        writer = csv.writer(out_file)
        for row in csv.reader(in_file):
            if any(row):
                writer.writerow(row)


##### Copy Fibercable_Schedule into new GDB & Convert CSV to Table in new GDB #####

OGcsvTable = folder_path + "/" + "FG_Segment_SS_" + today +"_2"+ ".csv" 

arcpy.TableToTable_conversion(OGcsvTable, gdbPath, "newTable") ### Converts this CSV to SDE Table

OG_FCS_data = "C:/GIS/DBconnections/GISADMIN Connections/Seattle as GISADMIN.sde/Seattle.DBO.Fibercable_Schedule"

arcpy.TableToTable_conversion(OG_FCS_data, gdbPath, "FCS_Backup") ### This is merely an untouched copy of the FCS data table & only serves as a benchmark comparison. 

arcpy.TableToTable_conversion(OG_FCS_data, gdbPath, "Fibercable_Schedule_Export")



##### SDE Table Paths/Fields/Cursor #####

sdeTable = gdbPath + "/" + "Fibercable_Schedule_Export"

sdeFields = ['FQN_ID']

sdeList = []

with arcpy.da.SearchCursor(sdeTable, sdeFields) as sdeCursor:

    for row in sdeCursor:
        
        sdeList.append(row[0])

num = len(sdeList)

print str(num) + " records in the SDE table"
    
del sdeCursor
print("\n")



##### CSV Table Paths/Fields/Cursor #####

csvTable = gdbPath + "/" + "newTable"

csvFields = ['Segment_Name__FQNID_']

csvList = []
    
with arcpy.da.SearchCursor(csvTable, csvFields) as csvCursor:

    for row in csvCursor:

        csvList.append(row[0])

num2 = len(csvList)

print str(num2) + " records in the Exported CSV table"
    
del csvCursor
print("\n")



##### Difference between two lists #####

missingList = []

for item in csvList:
    
    if item not in sdeList:
        
        missingList.append(item)

num3 = len(missingList)

print str(num3) + " records need to be appended"

##for item in missingList:
##    print item
    
print("\n")



##### Table Join #####

arcpy.MakeTableView_management(sdeTable, "sdeTableView")

arcpy.AddJoin_management("sdeTableView", "FQN_ID", csvTable, "Segment_Name__FQNID_")

print (arcpy.GetMessages())
print("\n")

arcpy.SelectLayerByAttribute_management("sdeTableView", "NEW_SELECTION", "FQN_ID IS NOT NULL")

result = arcpy.GetCount_management("sdeTableView")
print "... " + str(result) + " records selected"
print("\n")



##### Field Calculates #####

arcpy.CalculateField_management("sdeTableView", "Fibercable_Schedule_Export.CONSTR_START_PLANNED", "!newTable.Construction_Start_Planned!", "PYTHON_9.3")
print "... " + (arcpy.GetMessages())
print("\n")
arcpy.CalculateField_management("sdeTableView", "Fibercable_Schedule_Export.CONSTR_START_ACTUAL", "!newTable.Construction_Start_Actual!", "PYTHON_9.3")
print "... " + (arcpy.GetMessages())
print("\n")
arcpy.CalculateField_management("sdeTableView", "Fibercable_Schedule_Export.CABLE_PLACED_PLANNED", "!newTable.Cable_Placed_Planned!", "PYTHON_9.3")
print "... " + (arcpy.GetMessages())
print("\n")
arcpy.CalculateField_management("sdeTableView", "Fibercable_Schedule_Export.CABLE_PLACED_ACTUAL", "!newTable.Cable_Placed_Actual!", "PYTHON_9.3")
print "... " + (arcpy.GetMessages())
print("\n")
arcpy.CalculateField_management("sdeTableView", "Fibercable_Schedule_Export.SPLICE_TEST_PLANNED", "!newTable.Splice___Test_Planned!", "PYTHON_9.3")
print "... " + (arcpy.GetMessages())
print("\n")
arcpy.CalculateField_management("sdeTableView", "Fibercable_Schedule_Export.SPLICE_TEST_ACTUAL", "!newTable.Splice___Test_Actual!", "PYTHON_9.3")
print "... " + (arcpy.GetMessages())
print("\n")
arcpy.CalculateField_management("sdeTableView", "Fibercable_Schedule_Export.CONDUIT_PARTIALLYPLACED_ACTUAL", "!newTable.CONDUIT_PARTIALLYPLACED_ACTUAL!", "PYTHON_9.3")
print "... " + (arcpy.GetMessages())
print("\n")
arcpy.CalculateField_management("sdeTableView", "Fibercable_Schedule_Export.CONDUIT_PLACED_ESTIMATED", "!newTable.CONDUIT_PLACED_ESTIMATED!", "PYTHON_9.3")
print "... " + (arcpy.GetMessages())
print("\n")
arcpy.CalculateField_management("sdeTableView", "Fibercable_Schedule_Export.CONDUIT_PLACED_ACTUAL", "!newTable.CONDUIT_PLACED_ACTUAL!", "PYTHON_9.3")
print "... " + (arcpy.GetMessages())
print("\n")
arcpy.CalculateField_management("sdeTableView", "Fibercable_Schedule_Export.OPERATION_TYPE", "'U'", "PYTHON_9.3")
print "... " + (arcpy.GetMessages())
print("\n")



##### Remove Join #####

arcpy.RemoveJoin_management("sdeTableView")



##### Find FQN_IDs that do NOT exist & append them to the new table #####
                                    
arcpy.MakeTableView_management(csvTable, "csvTableView")
 
for item in csvList:

    if item not in sdeList:

        try:
        
            arcpy.SelectLayerByAttribute_management("csvTableView", "ADD_TO_SELECTION", "Segment_Name__FQNID_ = '" + item + "'")

        except:
            
            print "ERROR! You are missing an FQNID - please populate and re-run the tool."
            
            exit()
        
num_of_rows = int(arcpy.GetCount_management("csvTableView").getOutput(0))

print str(num_of_rows) + " - NEW RECORDS TO BE APPENDED"
print("\n")

arcpy.Append_management(inputs="csvTableView", target=sdeTable, schema_type="NO_TEST", field_mapping='FQN_ID "FQN_ID" true true false 50 Text 0 0 ,First,#,"csvTableView",Segment_Name__FQNID_,-1,-1;CONSTR_START_PLANNED "CONST_START_PLANNED" true true false 8 Date 0 0 ,First,#,"csvTableView",Construction_Start_Planned,-1,-1;CONSTR_START_ACTUAL "CONSTR_START_ADATE" true true false 8 Date 0 0 ,First,#,"csvTableView",Construction_Start_Actual,-1,-1;CABLE_PLACED_PLANNED "CABLE_PLACED_PDATE" true true false 8 Date 0 0 ,First,#,"csvTableView",Cable_Placed_Planned,-1,-1;CABLE_PLACED_ACTUAL "CABLE_PLACED_ADATE" true true false 8 Date 0 0 ,First,#,"csvTableView",Cable_Placed_Actual,-1,-1;SPLICE_TEST_PLANNED "SPLICE_TEST_PDATE" true true false 8 Date 0 0 ,First,#,"csvTableView",Splice___Test_Planned,-1,-1;SPLICE_TEST_ACTUAL "SPLICE_TEST_ADATE" true true false 8 Date 0 0 ,First,#,"csvTableView",Splice___Test_Actual,-1,-1;OPERATION_TYPE "OPERATION_TYPE" true true false 50 Text 0 0 ,First,#;VENDOR_REFERENCE_ID "VENDOR_REFERENCE_ID" true true false 50 Text 0 0 ,First,#;CONDUIT_PARTIALLYPLACED_ACTUAL "CONDUIT_PARTIALLYPLACED_ACTUAL" true true false 8 Date 0 0 ,First,#,"csvTableView",CONDUIT_PARTIALLYPLACED_ACTUAL,-1,-1;CONDUIT_PLACED_ESTIMATED "CONDUIT_PLACED_ESTIMATED" true true false 8 Date 0 0 ,First,#,"csvTableView",CONDUIT_PLACED_ESTIMATED,-1,-1;CONDUIT_PLACED_ACTUAL "CONDUIT_PLACED_ACTUAL" true true false 8 Date 0 0 ,First,#,"csvTableView",CONDUIT_PLACED_ACTUAL,-1,-1', subtype="")

print "... " + (arcpy.GetMessages())
print("\n")



##### Insert an "I" into the newly added rows #####

arcpy.SelectLayerByAttribute_management("sdeTableView", "NEW_SELECTION", "OPERATION_TYPE IS NULL")

num_of_rows2 = int(arcpy.GetCount_management("sdeTableView").getOutput(0))

arcpy.CalculateField_management("sdeTableView", "OPERATION_TYPE", "'I'", "PYTHON_9.3")
print "... " + (arcpy.GetMessages())
print("\n")

print "..." + str(num_of_rows2) + " new rows updated"
print("\n")


##### Create Deliverable GDB with GDB2S Schema #####

gdbName2 = "SEA_FiberCableSchedule_" + str(today)

arcpy.CreateFileGDB_management(folder_path, gdbName2)

gdbPath2 = folder_path + "/" + gdbName2 + ".gdb"

print "... Deliverable GDB Created with GDB2S Schema"
print("\n")

xmlPath = r"C:/GIS/LLD_Schema/GDB2S_SCHEMA_LLD_RELEASED_03JAN_V1.xml" ### The path to the schema XML

delivPath = gdbPath2 + '/' + "Fibercable_Schedule"

arcpy.ImportXMLWorkspaceDocument_management(gdbPath2, xmlPath) ### Import the XML Schema from GDB2

arcpy.Append_management(sdeTable, delivPath, 'NO_TEST')

print "... Data Appended - Process Complete"
