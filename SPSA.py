import os

import arcpy

import datetime

arcpy.env.overwriteOutput = True

day = datetime.date.today()

today = day.strftime("%Y%m%d")


##### Establish path to Folder / GDB #####

file_path = "C:/GIS/_Seattle_Workspaces/Segment_Permit_Status"

gdb_name = "SPSA_" + str(today)

full_path = file_path + "/" + gdb_name + ".gdb"

##### Creating the geodatabase if it does not exist #####

if arcpy.Exists(full_path):
        print "... " + "This geodatabase already exists" 
        exit()
            
else:
        print "... " + "Geodatabase creation underway"
        arcpy.CreateFileGDB_management(file_path, gdb_name)
        print("\n")


##### Copy Transmedia into new GDB #####

transPath = "C:/GIS/DBconnections/GISADMIN Connections/Seattle as GISADMIN.sde/Seattle.DBO.Core_Delivered/Seattle.DBO.Transmedia_Delivered"

arcpy.ImportXMLWorkspaceDocument_management(full_path, r'C:\GIS\_Seattle_Workspaces\Segment_Permit_Status\Schema.xml')

newTransmedia = full_path + "/" + "Transmedia_Overall"

arcpy.Append_management(transPath, newTransmedia, "NO_TEST")

print "... " + "Copied Transmedia_Overall into GDB"
print("\n")



##### Copy Permit Polygons into new GDB #####

permitPath = "C:/GIS/DBconnections/GISADMIN Connections/Seattle as GISADMIN.sde/Seattle.DBO.Permits"

arcpy.FeatureClassToFeatureClass_conversion(permitPath, full_path, "Permits_Overall")

newPermits = full_path + "/" + "Permits_Overall"

#arcpy.Append_management(permitPath, newPermits, "NO_TEST")

print "... " + 'Copied Permits_Overall into GDB'
print("\n")



##### Delete Unnecessary Fields ##### This works but it is time consuming (PG. 3) ##### DON'T RUN DURING TESTING

##fieldsList = arcpy.ListFields(newTransmedia)
##
##for field in fieldsList:
##    name = ('{0}'.format(field.name))
##    #print name
##    if name == 'OBJECTID' or name == 'Shape' or name == 'WORKORDERID' or name == 'TYPE_NAME' or name =='FQN_ID' or name == 'Shape_Length':
##
##        pass
##
##    else:
##        arcpy.DeleteField_management(newTransmedia, name)
##        print 'Deleted Field: ' + name


##### Add "Status_Code" text field to Permit Polygons (PG. 3) #####

arcpy.AddField_management(newPermits, 'STATUS_CODE', 'TEXT')



##### Export Permits that are == 'Cancelled' into GDB (PG. 3) #####

arcpy.MakeFeatureLayer_management(newPermits, "permitsFC")

arcpy.SelectLayerByAttribute_management("permitsFC", "NEW_SELECTION", "PERMIT_STATUS='Canceled'")

print "... " + (arcpy.GetMessages())
print("\n")

cancelled_permit_path = full_path + "/" + "Permits_Cancelled"

arcpy.CopyFeatures_management("permitsFC", cancelled_permit_path)



##### Delete Cancelled Permits (PG. 3) #####

arcpy.DeleteFeatures_management("permitsFC")
print "... " + (arcpy.GetMessages())
print("\n")



##### Update Cursor to populate the 'STATUS_CODE' field (PG. 4) #####

permitFields = ['PERMIT_STATUS', 'STATUS_CODE']

with arcpy.da.UpdateCursor(newPermits, permitFields) as cursor:

    for row in cursor:
        
        if row[0] == "Not Started":
            row[1] = "1_Not Started"
            
        elif row[0] == "In Production":
            row[1] = "2_In Production"     

        elif row[0] == "On Hold":
            row[1] = "3_On Hold"

        elif row[0] == "Ready For Submission":
            row[1] = "4_Ready For Submission"

        elif row[0] == "Entity Review":
            row[1] = "5_Entity Review"

        elif row[0] == "Respond to Entity Review":
            row[1] = "6_Respond To Entity Review"

        elif row[0] == "Comm Moves In Progress":
            row[1] = "7_Comm Moves In Progress"

        elif row[0] == "Permitted":
            row[1] = "8_Permitted"

        cursor.updateRow(row)



            
##### Spatial Join (PG. 5) #####

outSpatJoin = full_path + "/" + "Trans_PermPoly_SpJoin"

arcpy.SpatialJoin_analysis(newTransmedia, newPermits, outSpatJoin, "JOIN_ONE_TO_MANY", "KEEP_ALL")



##### Select <Null> Values in new Trans_PermPoly_SpJoin Layer & Field calculate these fields (PG. 5/6) #####

arcpy.MakeFeatureLayer_management(outSpatJoin, "spatJoinLyr")

arcpy.SelectLayerByAttribute_management("spatJoinLyr", "NEW_SELECTION", "PERMIT_STATUS IS NULL")
result = arcpy.GetCount_management("spatJoinLyr")
print "... " + str(result) + " <Null> records selected"
print("\n")

spatJoinFields = ['PERMIT_STATUS', 'STATUS_CODE']

count = 0

with arcpy.da.UpdateCursor("spatJoinLyr", spatJoinFields) as cursor:
        
    for row in cursor:
            
       row[0] = "Not Started"
       row[1] = "1_Not Started"
       cursor.updateRow(row)
       count += 1

print "... " + str(count) + " records were updated"
print("\n")



##### Filter out contradicting records & Export new Layer to GDB (PG. 6) #####

arcpy.SelectLayerByAttribute_management("spatJoinLyr", "NEW_SELECTION", "TYPE_NAME = 'AERIAL' AND PERMIT_TYPE = 'UG Easement' OR \
                                                                         TYPE_NAME = 'AERIAL' AND PERMIT_TYPE = 'UG Railroad' OR \
                                                                         TYPE_NAME = 'AERIAL' AND PERMIT_TYPE = 'UG ROW Construction' OR \
                                                                         TYPE_NAME = 'AERIAL' AND PERMIT_TYPE = 'UG ROW Use' OR \
                                                                         TYPE_NAME = 'AERIAL' AND PERMIT_TYPE = 'UG Easement' OR \
                                                                         TYPE_NAME = 'BURIED' AND PERMIT_TYPE = 'AE ROW Use' OR \
                                                                         TYPE_NAME = 'BURIED' AND PERMIT_TYPE = 'Pole Attachment' OR \
                                                                         TYPE_NAME = 'BURIED' AND PERMIT_TYPE = 'AE Railroad' OR \
                                                                         TYPE_NAME = 'BURIED' AND PERMIT_TYPE = 'AE Easement'")

result2 = arcpy.GetCount_management("spatJoinLyr")
print "... " + str(result2) + " records selected"
print("\n")

arcpy.SelectLayerByAttribute_management("spatJoinLyr", "SWITCH_SELECTION")
result3 = arcpy.GetCount_management("spatJoinLyr")
print "... " + str(result3) + " records were reverse selected"
print("\n")

newSpJoin_Trans_Permit = full_path + "/" + "Trans_PermitPoly_SpJoin_NEW"

arcpy.CopyFeatures_management("spatJoinLyr", newSpJoin_Trans_Permit)
print "... " +(arcpy.GetMessages())
print("\n")



##### Dissolve "Trans_Permit_Poly_SpJoin_NEW" Layer (PG. 7) #####

dissolvePath = full_path + "/" + "Trans_PermitPoly_SpJoin_NEW_DISS"

arcpy.Dissolve_management(newSpJoin_Trans_Permit, dissolvePath, "FQN_ID", [["STATUS_CODE","MIN"]])
print "... " + (arcpy.GetMessages())
print("\n")



##### Add a new field to the Dissolved FC & Field Calculate (PG. 8) #####

arcpy.AddField_management(dissolvePath, 'STATUS', 'TEXT')

dissFields = ['MIN_STATUS_CODE', 'STATUS']

with arcpy.da.UpdateCursor(dissolvePath, dissFields) as cursor:

        for row in cursor:

                if row[0] == "1_Not Started":
                        row[1] = row[0][2:]
            
                elif row[0] == "2_In Production":
                        row[1] = row[0][2:]    

                elif row[0] == "3_On Hold":
                        row[1] = row[0][2:]

                elif row[0] == "4_Ready For Submission":
                        row[1] = row[0][2:]

                elif row[0] == "5_Entity Review":
                        row[1] = row[0][2:]

                elif row[0] == "6_Respond To Entity Review":
                        row[1] = row[0][2:]

                elif row[0] == "7_Comm Moves In Progress":
                        row[1] = row[0][2:]

                elif row[0] == "8_Permitted":
                        row[1] = row[0][2:]

                cursor.updateRow(row)
                #print "... " +(arcpy.GetMessages())

                

##### Generate a new VZ_STATUS field and delete STATUS_CODE field #####

arcpy.AddField_management(dissolvePath, 'VZ_STATUS', 'TEXT')
print "... " + (arcpy.GetMessages()) + "ADDED NEW FIELD: 'VZ_STATUS'"
print("\n")

newFields = ['STATUS', 'VZ_STATUS']

with arcpy.da.UpdateCursor(dissolvePath, newFields) as cursor:

        for row in cursor:

                if row[0] == "In Production" or row[0] == "Not Started" or row[0] == "On Hold" or row[0] == "Ready For Submission":
                        row[1] = "In Design"
                        
                elif row[0] == "Permitted":
                        row[1] = "Permits Received"
                        
                elif row[0] == "Entity Review" or row[0] == "Respond To Entity Review":
                        row[1] = "Permits Submitted"
                        
                elif row[0] == "Comm Moves In Progress":
                        row[1] = "Comm Moves In Progress"
                        
                cursor.updateRow(row)

arcpy.DeleteField_management(dissolvePath, 'MIN_STATUS_CODE')      


##### Clementini Selection of Trans_PermitPoly_SpJoin & Export to GDB (PG. 9) #####

arcpy.MakeFeatureLayer_management(outSpatJoin, "spatJoinLyr")

arcpy.SelectLayerByLocation_management("spatJoinLyr", "CONTAINS_CLEMENTINI", dissolvePath, "", "NEW_SELECTION")
result4 = arcpy.GetCount_management("spatJoinLyr")
print "... " + str(result4) + " records selected"
print("\n")

arcpy.SelectLayerByAttribute_management("spatJoinLyr", "SWITCH_SELECTION")
result5 = arcpy.GetCount_management("spatJoinLyr")
print "... " + str(result5) + " records were reverse selected"
print("\n")

NA_FC = full_path + "/" + "NA"

arcpy.CopyFeatures_management("spatJoinLyr", NA_FC)
print"... " + (arcpy.GetMessages())
print("\n")



##### Query out Aerial Segments and Export to GDB (PG. 10) #####

arcpy.MakeFeatureLayer_management(NA_FC, "NA_FL")

arcpy.SelectLayerByAttribute_management("NA_FL", "NEW_SELECTION", "TYPE_NAME = 'AERIAL'")
result6 = arcpy.GetCount_management("NA_FL")
print "... " + str(result6) + " records were selected"
print("\n")

NA_AER = full_path + "/" "NA_AER_FC"
arcpy.CopyFeatures_management("NA_FL", NA_AER)
print"... " + (arcpy.GetMessages())
print("\n")



##### Dissolve new NA_AER Layer #####

NA_AER_DISS = full_path + "/" + "NA_AER_DISS"

arcpy.Dissolve_management(NA_AER, NA_AER_DISS, "FQN_ID")
print"... " + (arcpy.GetMessages())
print("\n")



##### Add new Field to NA_AER_DISS #####

arcpy.AddField_management(NA_AER_DISS, "STATUS", "TEXT")
print"... " + (arcpy.GetMessages())
print("\n")

arcpy.AddField_management(NA_AER_DISS, "VZ_STATUS", "TEXT")
print"... " + (arcpy.GetMessages())
print("\n")



##### Field calculate new fields with Cursor #####

NA_AER_DISS_fields = ["STATUS", "VZ_STATUS"]

with arcpy.da.UpdateCursor(NA_AER_DISS, NA_AER_DISS_fields) as cursor:

        for row in cursor:

                row[0] = "Not Started"
                row[1] = "In Design"
                cursor.updateRow(row)
                #print"... " + (arcpy.GetMessages())

##### Query out Buried Segments and Export to GDB (PG. 10) #####

arcpy.MakeFeatureLayer_management(NA_FC, "NA_FL")

arcpy.SelectLayerByAttribute_management("NA_FL", "NEW_SELECTION", "TYPE_NAME = 'BURIED'")
result7 = arcpy.GetCount_management("NA_FL")
print "... " + str(result7) + " records were selected"
print("\n")


NA_BUR = full_path + "/" + "NA_BUR"
arcpy.CopyFeatures_management("NA_FL", NA_BUR)
print"... " + (arcpy.GetMessages())
print("\n")

