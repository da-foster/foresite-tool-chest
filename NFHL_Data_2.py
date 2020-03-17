### Title: FEMA NFHL Data Downloader
### Description: This script reaches out to the FEMA MCS website using the 
###              requests package, downloads each state's NFHL data,
###              copies the data as a shapefile into the DB, and deletes the 
###              unnecessary remaining data.
### Company: Foresite Group
### Author: Darren Foster



### Import Packages ###
import os, requests, arcpy, zipfile, shutil

### Main Download Destination ###
folder = r"C:\Users\dfoster\Downloads\GIS_Data"


### Location to Unzip the Files ###
unZipFolder = r"C:\Users\dfoster\Downloads\GIS_Data\Unzip"

os.makedirs(unZipFolder) ### COMMENT OUT IF THE FOLDER ALREADY EXISTS

### GIS Database Destination ###
dbLoc = r'C:\GIS\DBconnections\GISADMIN Connections\LD.sde'



#####################################################################################
#Alabama

AL_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_01_20190522.zip' #1285MB

print "Initiating Alabama..."

AL_resp = requests.get(AL_url, stream = True)
print "Status is " + str(AL_resp.status_code)

AL_dest = folder + "/" + "AL.zip"

if AL_resp.status_code == 200:
    
    with open(AL_dest, 'wb') as data:
        for chunk in AL_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Alabama Download Complete"
    data.close()

    ### Unzip the downloaded file ###
    AL_NFHL = unZipFolder + '/' + "AL_NFHL"

    os.makedirs(AL_NFHL)

    zip_ref = zipfile.ZipFile(AL_dest)

    zip_ref.extractall(AL_NFHL)

    zip_ref.close()

    print "Alabama Unzip Complete"

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(AL_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = AL_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'AL_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Alabama Shapefile Copied"

            
    ### Remove unnecessary remaining data/folder ###
    os.remove(AL_dest)
    shutil.rmtree(AL_NFHL)
    print("Unnecessary Alabama Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Alabama"
    print("\n")



###################################################################################
#Arizona

AZ_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_04_20190614.zip' #177MB

print "Initiating Arizona..."

AZ_resp = requests.get(AZ_url, stream = True)
print "Status is " + str(AZ_resp.status_code)

AZ_dest = folder + "/" + "AZ.zip"

if AZ_resp.status_code == 200:
    
    with open(AZ_dest, 'wb') as data:
        for chunk in AZ_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Arizona Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    AZ_NFHL = unZipFolder + '/' + "AZ_NFHL"

    os.makedirs(AZ_NFHL)

    zip_ref = zipfile.ZipFile(AZ_dest)

    zip_ref.extractall(AZ_NFHL)

    zip_ref.close()

    print "Arizona Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(AZ_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = AZ_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'AZ_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Arizona Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(AZ_dest)
    shutil.rmtree(AZ_NFHL)
    print("Unnecessary Arizona Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Arizona"
    print("\n")



#######################################################################################
#Arkansas

AR_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_05_20190611.zip' #257MB

print "Initiating Arkansas..."

AR_resp = requests.get(AR_url, stream = True)
print "Status is " + str(AR_resp.status_code)

AR_dest = folder + "/" + "AR.zip"

if AR_resp.status_code == 200:
    
    with open(AR_dest, 'wb') as data:
        for chunk in AR_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Arkansas Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    AR_NFHL = unZipFolder + '/' + "AR_NFHL"

    os.makedirs(AR_NFHL)

    zip_ref = zipfile.ZipFile(AR_dest)

    zip_ref.extractall(AR_NFHL)

    zip_ref.close()

    print "Arkansas Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(AR_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = AR_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'AR_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Arkansas Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(AR_dest)
    shutil.rmtree(AR_NFHL)
    print("Unnecessary Arkansas Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Arkansas"
    print("\n")
    

#####################################################################################
#California

CA_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_06_20190612.zip' #434MB

print "Initiating California..."

CA_resp = requests.get(CA_url, stream = True)
print "Status is " + str(CA_resp.status_code)

CA_dest = folder + "/" + "CA.zip"

if CA_resp.status_code == 200:
    
    with open(CA_dest, 'wb') as data:
        for chunk in CA_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "California Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    CA_NFHL = unZipFolder + '/' + "CA_NFHL"

    os.makedirs(CA_NFHL)

    zip_ref = zipfile.ZipFile(CA_dest)

    zip_ref.extractall(CA_NFHL)

    zip_ref.close()

    print "California Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(CA_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = CA_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'CA_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "California Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(CA_dest)
    shutil.rmtree(CA_NFHL)
    print("Unnecessary California Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download California"
    print("\n")



######################################################################################
#Colorado

CO_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_08_20190614.zip' #126MB

print "Initiating Colorado..."

CO_resp = requests.get(CO_url, stream = True)
print "Status is " + str(CO_resp.status_code)

CO_dest = folder + "/" + "CO.zip"

if CO_resp.status_code == 200:
    
    with open(CO_dest, 'wb') as data:
        for chunk in CO_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Colorado Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    CO_NFHL = unZipFolder + '/' + "CO_NFHL"

    os.makedirs(CO_NFHL)

    zip_ref = zipfile.ZipFile(CO_dest)

    zip_ref.extractall(CO_NFHL)

    zip_ref.close()

    print "Colorado Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(CO_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = CO_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'CO_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Colorado Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(CO_dest)
    shutil.rmtree(CO_NFHL)
    print("Unnecessary Colorado Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Colorado"
    print("\n")



#####################################################################################
#Connecticut

CT_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_09_20190224.zip' #86MB

print "Initiating Connecticut..."

CT_resp = requests.get(CT_url, stream = True)
print "Status is " + str(CT_resp.status_code)

CT_dest = folder + "/" + "CT.zip"

if CT_resp.status_code == 200:
    
    with open(CT_dest, 'wb') as data:
        for chunk in CT_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Connecticut Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    CT_NFHL = unZipFolder + '/' + "CT_NFHL"

    os.makedirs(CT_NFHL)

    zip_ref = zipfile.ZipFile(CT_dest)

    zip_ref.extractall(CT_NFHL)

    zip_ref.close()

    print "Connecticut Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(CT_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = CT_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'CT_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Connecticut Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(CT_dest)
    shutil.rmtree(CT_NFHL)
    print("Unnecessary Connecticut Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Connecticut"
    print("\n")


#####################################################################################
#Delaware

DE_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_10_20190130.zip' #85MB

print "Initiating Delaware..."

DE_resp = requests.get(DE_url, stream = True)
print "Status is " + str(DE_resp.status_code)

DE_dest = folder + "/" + "DE.zip"

if DE_resp.status_code == 200:
    
    with open(DE_dest, 'wb') as data:
        for chunk in DE_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Delaware Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    DE_NFHL = unZipFolder + '/' + "DE_NFHL"

    os.makedirs(DE_NFHL)

    zip_ref = zipfile.ZipFile(DE_dest)

    zip_ref.extractall(DE_NFHL)

    zip_ref.close()

    print "Delaware Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(DE_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = DE_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'DE_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Delaware Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(DE_dest)
    shutil.rmtree(DE_NFHL)
    print("Unnecessary Delaware Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Delaware"
    print("\n")


####################################################################################
#Washington D.C.

DC_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_11_20190429.zip' #4MB

print "Initiating Washington D.C. ..."

DC_resp = requests.get(DC_url, stream = True)
print "Status is " + str(DC_resp.status_code)

DC_dest = folder + "/" + "DC.zip"

if DC_resp.status_code == 200:
    
    with open(DC_dest, 'wb') as data:
        for chunk in DC_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Washington D.C. Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    DC_NFHL = unZipFolder + '/' + "DC_NFHL"

    os.makedirs(DC_NFHL)

    zip_ref = zipfile.ZipFile(DC_dest)

    zip_ref.extractall(DC_NFHL)

    zip_ref.close()

    print "Washington D.C. Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(DC_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = DC_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'DC_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Washington D.C. Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(DC_dest)
    shutil.rmtree(DC_NFHL)
    print("Unnecessary Washington D.C. Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Washington D.C."
    print("\n")


#######################################################################################
#Florida

FL_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_12_20190614.zip' #2319MB

print "Initiating Florida..."

FL_resp = requests.get(FL_url, stream = True)
print "Status is " + str(FL_resp.status_code)

FL_dest = folder + "/" + "FL.zip"

if FL_resp.status_code == 200:
    
    with open(FL_dest, 'wb') as data:
        for chunk in FL_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Florida Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    FL_NFHL = unZipFolder + '/' + "FL_NFHL"

    os.makedirs(FL_NFHL)

    zip_ref = zipfile.ZipFile(FL_dest)

    zip_ref.extractall(FL_NFHL)

    zip_ref.close()

    print "Florida Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(FL_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = FL_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'FL_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Florida Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(FL_dest)
    shutil.rmtree(FL_NFHL)
    print("Unnecessary Florida Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Florida"
    print("\n")


#######################################################################################
#Georgia

GA_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_13_20190607.zip' #1219MB

print "Initiating Georgia..."

GA_resp = requests.get(GA_url, stream = True)
print "Status is " + str(GA_resp.status_code)

GA_dest = folder + "/" + "GA.zip"

if GA_resp.status_code == 200:
    
    with open(GA_dest, 'wb') as data:
        for chunk in GA_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Georgia Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    GA_NFHL = unZipFolder + '/' + "GA_NFHL"

    os.makedirs(GA_NFHL)

    zip_ref = zipfile.ZipFile(GA_dest)

    zip_ref.extractall(GA_NFHL)

    zip_ref.close()

    print "Georgia Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(GA_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = GA_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'GA_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Georgia Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(GA_dest)
    shutil.rmtree(GA_NFHL)
    print("Unnecessary Georgia Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Georgia"
    print("\n")



####################################################################################
#Idaho

ID_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_16_20190606.zip' #57MB	

print "Initiating Idaho..."

ID_resp = requests.get(ID_url, stream = True)
print "Status is " + str(ID_resp.status_code)

ID_dest = folder + "/" + "ID.zip"

if ID_resp.status_code == 200:
    
    with open(ID_dest, 'wb') as data:
        for chunk in ID_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Idaho Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    ID_NFHL = unZipFolder + '/' + "ID_NFHL"

    os.makedirs(ID_NFHL)

    zip_ref = zipfile.ZipFile(ID_dest)

    zip_ref.extractall(ID_NFHL)

    zip_ref.close()

    print "Idaho Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(ID_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = ID_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'ID_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Idaho Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(ID_dest)
    shutil.rmtree(ID_NFHL)
    print("Unnecessary Idaho Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Idaho"
    print("\n")


######################################################################################
#Illinois

IL_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_17_20190611.zip' #171MB

print "Initiating Illinois..."

IL_resp = requests.get(IL_url, stream = True)
print "Status is " + str(IL_resp.status_code)

IL_dest = folder + "/" + "IL.zip"

if IL_resp.status_code == 200:
    
    with open(IL_dest, 'wb') as data:
        for chunk in IL_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Illinois Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    IL_NFHL = unZipFolder + '/' + "IL_NFHL"

    os.makedirs(IL_NFHL)

    zip_ref = zipfile.ZipFile(IL_dest)

    zip_ref.extractall(IL_NFHL)

    zip_ref.close()

    print "Illinois Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(IL_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = IL_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'IL_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Illinois Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(IL_dest)
    shutil.rmtree(IL_NFHL)
    print("Unnecessary Illinois Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Illinois"
    print("\n")


######################################################################################
#Indiana

IN_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_18_20190315.zip' #316MB

print "Initiating Indiana..."

IN_resp = requests.get(IN_url, stream = True)
print "Status is " + str(IN_resp.status_code)

IN_dest = folder + "/" + "IN.zip"

if IN_resp.status_code == 200:
    
    with open(IN_dest, 'wb') as data:
        for chunk in IN_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Indiana Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    IN_NFHL = unZipFolder + '/' + "IN_NFHL"

    os.makedirs(IN_NFHL)

    zip_ref = zipfile.ZipFile(IN_dest)

    zip_ref.extractall(IN_NFHL)

    zip_ref.close()

    print "Indiana Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(IN_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = IN_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'IN_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Indiana Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(IN_dest)
    shutil.rmtree(IN_NFHL)
    print("Unnecessary Indiana Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Indiana"
    print("\n")


########################################################################################
#Iowa

IA_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_19_20190221.zip' #1058MB

print "Initiating Iowa..."

IA_resp = requests.get(IA_url, stream = True)
print "Status is " + str(IA_resp.status_code)

IA_dest = folder + "/" + "IA.zip"

if IA_resp.status_code == 200:
    
    with open(IA_dest, 'wb') as data:
        for chunk in IA_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Iowa Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    IA_NFHL = unZipFolder + '/' + "IA_NFHL"

    os.makedirs(IA_NFHL)

    zip_ref = zipfile.ZipFile(IA_dest)

    zip_ref.extractall(IA_NFHL)

    zip_ref.close()

    print "Iowa Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(IA_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = IA_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'IA_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Iowa Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(IA_dest)
    shutil.rmtree(IA_NFHL)
    print("Unnecessary Iowa Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Iowa"
    print("\n")


#####################################################################################
#Kansas

KS_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_20_20190524.zip' #492MB

print "Initiating Kansas..."

KS_resp = requests.get(KS_url, stream = True)
print "Status is " + str(KS_resp.status_code)

KS_dest = folder + "/" + "KS.zip"

if KS_resp.status_code == 200:
    
    with open(KS_dest, 'wb') as data:
        for chunk in KS_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Kansas Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    KS_NFHL = unZipFolder + '/' + "KS_NFHL"

    os.makedirs(KS_NFHL)

    zip_ref = zipfile.ZipFile(KS_dest)

    zip_ref.extractall(KS_NFHL)

    zip_ref.close()

    print "Kansas Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(KS_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = KS_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'KS_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Kansas Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(KS_dest)
    shutil.rmtree(KS_NFHL)
    print("Unnecessary Kansas Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Kansas"
    print("\n")


######################################################################################
#Kentucky

KY_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_21_20190419.zip' #1055MB

print "Initiating Kentucky..."

KY_resp = requests.get(KY_url, stream = True)
print "Status is " + str(KY_resp.status_code)

KY_dest = folder + "/" + "KY.zip"

if KY_resp.status_code == 200:
    
    with open(KY_dest, 'wb') as data:
        for chunk in KY_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Kentucky Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    KY_NFHL = unZipFolder + '/' + "KY_NFHL"

    os.makedirs(KY_NFHL)

    zip_ref = zipfile.ZipFile(KY_dest)

    zip_ref.extractall(KY_NFHL)

    zip_ref.close()

    print "Kentucky Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(KY_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = KY_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'KY_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Kentucky Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(KY_dest)
    shutil.rmtree(KY_NFHL)
    print("Unnecessary Kentucky Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Kentucky"
    print("\n")


######################################################################################
#Louisiana

LA_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_22_20190515.zip' #1070MB

print "Initiating Louisiana..."

LA_resp = requests.get(LA_url, stream = True)
print "Status is " + str(LA_resp.status_code)

LA_dest = folder + "/" + "LA.zip"

if LA_resp.status_code == 200:
    
    with open(LA_dest, 'wb') as data:
        for chunk in LA_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Louisiana Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    LA_NFHL = unZipFolder + '/' + "LA_NFHL"

    os.makedirs(LA_NFHL)

    zip_ref = zipfile.ZipFile(LA_dest)

    zip_ref.extractall(LA_NFHL)

    zip_ref.close()

    print "Louisiana Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(LA_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = LA_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'LA_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Louisiana Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(LA_dest)
    shutil.rmtree(LA_NFHL)
    print("Unnecessary Louisiana Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Louisiana"
    print("\n")
    

####################################################################################
#Maine

ME_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_23_20190129.zip' #140MB

print "Initiating Maine..."

ME_resp = requests.get(ME_url, stream = True)
print "Status is " + str(ME_resp.status_code)

ME_dest = folder + "/" + "ME.zip"

if ME_resp.status_code == 200:
    
    with open(ME_dest, 'wb') as data:
        for chunk in ME_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Maine Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    ME_NFHL = unZipFolder + '/' + "ME_NFHL"

    os.makedirs(ME_NFHL)

    zip_ref = zipfile.ZipFile(ME_dest)

    zip_ref.extractall(ME_NFHL)

    zip_ref.close()

    print "Maine Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(ME_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = ME_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'ME_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Maine Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(ME_dest)
    shutil.rmtree(ME_NFHL)
    print("Unnecessary Maine Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Maine"
    print("\n")



####################################################################################
#Maryland

MD_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_24_20190610.zip' #466MB

print "Initiating Maryland..."

MD_resp = requests.get(MD_url, stream = True)
print "Status is " + str(MD_resp.status_code)

MD_dest = folder + "/" + "MD.zip"

if MD_resp.status_code == 200:
    
    with open(MD_dest, 'wb') as data:
        for chunk in MD_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Maryland Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    MD_NFHL = unZipFolder + '/' + "MD_NFHL"

    os.makedirs(MD_NFHL)

    zip_ref = zipfile.ZipFile(MD_dest)

    zip_ref.extractall(MD_NFHL)

    zip_ref.close()

    print "Maryland Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(MD_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = MD_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'MD_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Maryland Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(MD_dest)
    shutil.rmtree(MD_NFHL)
    print("Unnecessary Maryland Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Maryland"
    print("\n")


#####################################################################################
#Massachusetts

MA_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_25_20190613.zip' #152MB

print "Initiating Massachusetts..."

MA_resp = requests.get(MA_url, stream = True)
print "Status is " + str(MA_resp.status_code)

MA_dest = folder + "/" + "MA.zip"

if MA_resp.status_code == 200:
    
    with open(MA_dest, 'wb') as data:
        for chunk in MA_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Massachusetts Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    MA_NFHL = unZipFolder + '/' + "MA_NFHL"

    os.makedirs(MA_NFHL)

    zip_ref = zipfile.ZipFile(MA_dest)

    zip_ref.extractall(MA_NFHL)

    zip_ref.close()

    print "Massachusetts Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(MA_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = MA_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'MA_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Massachusetts Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(MA_dest)
    shutil.rmtree(MA_NFHL)
    print("Unnecessary Massachusetts Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Massachusetts"
    print("\n")


#####################################################################################
#Michigan

MI_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_26_20190614.zip' #343MB

print "Initiating Michigan..."

MI_resp = requests.get(MI_url, stream = True)
print "Status is " + str(MI_resp.status_code)

MI_dest = folder + "/" + "MI.zip"

if MI_resp.status_code == 200:
    
    with open(MI_dest, 'wb') as data:
        for chunk in MI_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Michigan Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    MI_NFHL = unZipFolder + '/' + "MI_NFHL"

    os.makedirs(MI_NFHL)

    zip_ref = zipfile.ZipFile(MI_dest)

    zip_ref.extractall(MI_NFHL)

    zip_ref.close()

    print "Michigan Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(MI_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = MI_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'MI_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Michigan Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(MI_dest)
    shutil.rmtree(MI_NFHL)
    print("Unnecessary Michigan Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Michigan"
    print("\n")


#####################################################################################
#Minnesota

MN_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_27_20190516.zip' #362MB

print "Initiating Minnesota..."

MN_resp = requests.get(MN_url, stream = True)
print "Status is " + str(MN_resp.status_code)

MN_dest = folder + "/" + "MN.zip"

if MN_resp.status_code == 200:
    
    with open(MN_dest, 'wb') as data:
        for chunk in MN_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Minnesota Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    MN_NFHL = unZipFolder + '/' + "MN_NFHL"

    os.makedirs(MN_NFHL)

    zip_ref = zipfile.ZipFile(MN_dest)

    zip_ref.extractall(MN_NFHL)

    zip_ref.close()

    print "Minnesota Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(MN_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = MN_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'MN_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Minnesota Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(MN_dest)
    shutil.rmtree(MN_NFHL)
    print("Unnecessary Minnesota Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Minnesota"
    print("\n")


######################################################################################
#Mississippi

MS_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_28_20190425.zip' #590MB

print "Initiating Mississippi..."

MS_resp = requests.get(MS_url, stream = True)
print "Status is " + str(MS_resp.status_code)

MS_dest = folder + "/" + "MS.zip"

if MS_resp.status_code == 200:
    
    with open(MS_dest, 'wb') as data:
        for chunk in MS_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Mississippi Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    MS_NFHL = unZipFolder + '/' + "MS_NFHL"

    os.makedirs(MS_NFHL)

    zip_ref = zipfile.ZipFile(MS_dest)

    zip_ref.extractall(MS_NFHL)

    zip_ref.close()

    print "Mississippi Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(MS_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = MS_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'MS_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Mississippi Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(MS_dest)
    shutil.rmtree(MS_NFHL)
    print("Unnecessary Mississippi Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Mississippi"
    print("\n")


######################################################################################
#Missouri

MO_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_29_20190613.zip' #817MB

print "Initiating Missouri..."

MO_resp = requests.get(MO_url, stream = True)
print "Status is " + str(MO_resp.status_code)

MO_dest = folder + "/" + "MO.zip"

if MO_resp.status_code == 200:
    
    with open(MO_dest, 'wb') as data:
        for chunk in MO_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Missouri Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    MO_NFHL = unZipFolder + '/' + "MO_NFHL"

    os.makedirs(MO_NFHL)

    zip_ref = zipfile.ZipFile(MO_dest)

    zip_ref.extractall(MO_NFHL)

    zip_ref.close()

    print "Missouri Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(MO_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = MO_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'MO_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Missouri Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(MO_dest)
    shutil.rmtree(MO_NFHL)
    print("Unnecessary Missouri Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Missouri"
    print("\n")


#####################################################################################
#Montana

MT_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_30_20190613.zip' #82MB

print "Initiating Montana..."

MT_resp = requests.get(MT_url, stream = True)
print "Status is " + str(MT_resp.status_code)

MT_dest = folder + "/" + "MT.zip"

if MT_resp.status_code == 200:
    
    with open(MT_dest, 'wb') as data:
        for chunk in MT_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Montana Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    MT_NFHL = unZipFolder + '/' + "MT_NFHL"

    os.makedirs(MT_NFHL)

    zip_ref = zipfile.ZipFile(MT_dest)

    zip_ref.extractall(MT_NFHL)

    zip_ref.close()

    print "Montana Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(MT_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = MT_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'MT_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Montana Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(MT_dest)
    shutil.rmtree(MT_NFHL)
    print("Unnecessary Montana Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Montana"
    print("\n")


######################################################################################
#Nebraska

NE_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_31_20190502.zip' #367MB

print "Initiating Nebraska..."

NE_resp = requests.get(NE_url, stream = True)
print "Status is " + str(NE_resp.status_code)

NE_dest = folder + "/" + "NE.zip"

if NE_resp.status_code == 200:
    
    with open(NE_dest, 'wb') as data:
        for chunk in NE_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Nebraska Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    NE_NFHL = unZipFolder + '/' + "NE_NFHL"

    os.makedirs(NE_NFHL)

    zip_ref = zipfile.ZipFile(NE_dest)

    zip_ref.extractall(NE_NFHL)

    zip_ref.close()

    print "Nebraska Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(NE_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = NE_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'NE_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Nebraska Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(NE_dest)
    shutil.rmtree(NE_NFHL)
    print("Unnecessary Nebraska Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Nebraska"
    print("\n")


####################################################################################
#Nevada

NV_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_32_20190610.zip' #51MB

print "Initiating Nevada..."

NV_resp = requests.get(NV_url, stream = True)
print "Status is " + str(NV_resp.status_code)

NV_dest = folder + "/" + "NV.zip"

if NV_resp.status_code == 200:
    
    with open(NV_dest, 'wb') as data:
        for chunk in NV_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Nevada Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    NV_NFHL = unZipFolder + '/' + "NV_NFHL"

    os.makedirs(NV_NFHL)

    zip_ref = zipfile.ZipFile(NV_dest)

    zip_ref.extractall(NV_NFHL)

    zip_ref.close()

    print "Nevada Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(NV_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = NV_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'NV_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Nevada Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(NV_dest)
    shutil.rmtree(NV_NFHL)
    print("Unnecessary Nevada Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Nevada"
    print("\n")


#####################################################################################
#New Hampshire

NH_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_33_20190214.zip' #75MB

print "Initiating New Hampshire..."

NH_resp = requests.get(NH_url, stream = True)
print "Status is " + str(NH_resp.status_code)

NH_dest = folder + "/" + "NH.zip"

if NH_resp.status_code == 200:
    
    with open(NH_dest, 'wb') as data:
        for chunk in NH_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "New Hampshire Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    NH_NFHL = unZipFolder + '/' + "NH_NFHL"

    os.makedirs(NH_NFHL)

    zip_ref = zipfile.ZipFile(NH_dest)

    zip_ref.extractall(NH_NFHL)

    zip_ref.close()

    print "New Hampshire Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(NH_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = NH_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'NH_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "New Hampshire Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(NH_dest)
    shutil.rmtree(NH_NFHL)
    print("Unnecessary New Hampshire Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download New Hampshire"
    print("\n")


######################################################################################
#New Jersey

NJ_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_34_20190321.zip' #441MB

print "Initiating New Jersey..."

NJ_resp = requests.get(NJ_url, stream = True)
print "Status is " + str(NJ_resp.status_code)

NJ_dest = folder + "/" + "NJ.zip"

if NJ_resp.status_code == 200:
    
    with open(NJ_dest, 'wb') as data:
        for chunk in NJ_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "New Jersey Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    NJ_NFHL = unZipFolder + '/' + "NJ_NFHL"

    os.makedirs(NJ_NFHL)

    zip_ref = zipfile.ZipFile(NJ_dest)

    zip_ref.extractall(NJ_NFHL)

    zip_ref.close()

    print "New Jersey Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(NJ_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = NJ_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'NJ_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "New Jersey Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(NJ_dest)
    shutil.rmtree(NJ_NFHL)
    print("Unnecessary New Jersey Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download New Jersey"
    print("\n")


######################################################################################
#New Mexico

NM_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_35_20190210.zip' #172MB

print "Initiating New Mexico..."

NM_resp = requests.get(NM_url, stream = True)
print "Status is " + str(NM_resp.status_code)

NM_dest = folder + "/" + "NM.zip"

if NM_resp.status_code == 200:
    
    with open(NM_dest, 'wb') as data:
        for chunk in NM_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "New Mexico Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    NM_NFHL = unZipFolder + '/' + "NM_NFHL"

    os.makedirs(NM_NFHL)

    zip_ref = zipfile.ZipFile(NM_dest)

    zip_ref.extractall(NM_NFHL)

    zip_ref.close()

    print "New Mexico Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(NM_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = NM_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'NM_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "New Mexico Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(NM_dest)
    shutil.rmtree(NM_NFHL)
    print("Unnecessary New Mexico Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download New Mexico"
    print("\n")


######################################################################################
#New York

NY_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_36_20190606.zip' #1106MB	

print "Initiating New York..."

NY_resp = requests.get(NY_url, stream = True)
print "Status is " + str(NY_resp.status_code)

NY_dest = folder + "/" + "NY.zip"

if NY_resp.status_code == 200:
    
    with open(NY_dest, 'wb') as data:
        for chunk in NY_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "New York Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    NY_NFHL = unZipFolder + '/' + "NY_NFHL"

    os.makedirs(NY_NFHL)

    zip_ref = zipfile.ZipFile(NY_dest)

    zip_ref.extractall(NY_NFHL)

    zip_ref.close()

    print "New York Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(NY_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = NY_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'NY_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "New York Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(NY_dest)
    shutil.rmtree(NY_NFHL)
    print("Unnecessary New York Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download New York"
    print("\n")


#######################################################################################
#North Carolina

NC_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_37_20190605.zip' #1303MB

print "Initiating North Carolina..."

NC_resp = requests.get(NC_url, stream = True)
print "Status is " + str(NC_resp.status_code)

NC_dest = folder + "/" + "NC.zip"

if NC_resp.status_code == 200:
    
    with open(NC_dest, 'wb') as data:
        for chunk in NC_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "North Carolina Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    NC_NFHL = unZipFolder + '/' + "NC_NFHL"

    os.makedirs(NC_NFHL)

    zip_ref = zipfile.ZipFile(NC_dest)

    zip_ref.extractall(NC_NFHL)

    zip_ref.close()

    print "North Carolina Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(NC_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = NC_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'NC_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "North Carolina Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(NC_dest)
    shutil.rmtree(NC_NFHL)
    print("Unnecessary North Carolina Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download North Carolina"
    print("\n")


#####################################################################################
#North Dakota

ND_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_38_20190312.zip' #166MB

print "Initiating North Dakota..."

ND_resp = requests.get(ND_url, stream = True)
print "Status is " + str(ND_resp.status_code)

ND_dest = folder + "/" + "ND.zip"

if ND_resp.status_code == 200:
    
    with open(ND_dest, 'wb') as data:
        for chunk in ND_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "North Dakota Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    ND_NFHL = unZipFolder + '/' + "ND_NFHL"

    os.makedirs(ND_NFHL)

    zip_ref = zipfile.ZipFile(ND_dest)

    zip_ref.extractall(ND_NFHL)

    zip_ref.close()

    print "North Dakota Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(ND_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = ND_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'ND_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "North Dakota Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(ND_dest)
    shutil.rmtree(ND_NFHL)
    print("Unnecessary North Dakota Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download North Dakota"
    print("\n")


####################################################################################
#Ohio

OH_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_39_20190505.zip' #595MB

print "Initiating Ohio..."

OH_resp = requests.get(OH_url, stream = True)
print "Status is " + str(OH_resp.status_code)

OH_dest = folder + "/" + "OH.zip"

if OH_resp.status_code == 200:
    
    with open(OH_dest, 'wb') as data:
        for chunk in OH_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Ohio Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    OH_NFHL = unZipFolder + '/' + "OH_NFHL"

    os.makedirs(OH_NFHL)

    zip_ref = zipfile.ZipFile(OH_dest)

    zip_ref.extractall(OH_NFHL)

    zip_ref.close()

    print "Ohio Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(OH_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = OH_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'OH_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Ohio Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(OH_dest)
    shutil.rmtree(OH_NFHL)
    print("Unnecessary Ohio Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Ohio"
    print("\n")
    


#####################################################################################
#Oklahoma

OK_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_40_20190613.zip' #519MB

print "Initiating Oklahoma..."

OK_resp = requests.get(OK_url, stream = True)
print "Status is " + str(OK_resp.status_code)

OK_dest = folder + "/" + "OK.zip"

if OK_resp.status_code == 200:
    
    with open(OK_dest, 'wb') as data:
        for chunk in OK_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Oklahoma Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    OK_NFHL = unZipFolder + '/' + "OK_NFHL"

    os.makedirs(OK_NFHL)

    zip_ref = zipfile.ZipFile(OK_dest)

    zip_ref.extractall(OK_NFHL)

    zip_ref.close()

    print "Oklahoma Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(OK_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = OK_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'OK_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Oklahoma Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(OK_dest)
    shutil.rmtree(OK_NFHL)
    print("Unnecessary Oklahoma Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Oklahoma"
    print("\n")


######################################################################################
#Oregon

OR_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_41_20190508.zip' #158MB

print "Initiating Oregon..."

OR_resp = requests.get(OR_url, stream = True)
print "Status is " + str(OR_resp.status_code)

OR_dest = folder + "/" + "OR.zip"

if OR_resp.status_code == 200:
    
    with open(OR_dest, 'wb') as data:
        for chunk in OR_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Oregon Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    OR_NFHL = unZipFolder + '/' + "OR_NFHL"

    os.makedirs(OR_NFHL)

    zip_ref = zipfile.ZipFile(OR_dest)

    zip_ref.extractall(OR_NFHL)

    zip_ref.close()

    print "Oregon Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(OR_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = OR_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'OR_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Oregon Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(OR_dest)
    shutil.rmtree(OR_NFHL)
    print("Unnecessary Oregon Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Oregon"
    print("\n")


#####################################################################################
#Pennsylvania

PA_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_42_20190614.zip' #1248MB

print "Initiating Pennsylvania..."

PA_resp = requests.get(PA_url, stream = True)
print "Status is " + str(PA_resp.status_code)

PA_dest = folder + "/" + "PA.zip"

if PA_resp.status_code == 200:
    
    with open(PA_dest, 'wb') as data:
        for chunk in PA_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Pennsylvania Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    PA_NFHL = unZipFolder + '/' + "PA_NFHL"

    os.makedirs(PA_NFHL)

    zip_ref = zipfile.ZipFile(PA_dest)

    zip_ref.extractall(PA_NFHL)

    zip_ref.close()

    print "Pennsylvania Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(PA_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = PA_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'PA_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Pennsylvania Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(PA_dest)
    shutil.rmtree(PA_NFHL)
    print("Unnecessary Pennsylvania Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Pennsylvania"
    print("\n")


###################################################################################
#Rhode Island

RI_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_44_20181118.zip' #34MB

print "Initiating Rhode Island..."

RI_resp = requests.get(RI_url, stream = True)
print "Status is " + str(RI_resp.status_code)

RI_dest = folder + "/" + "RI.zip"

if RI_resp.status_code == 200:
    
    with open(RI_dest, 'wb') as data:
        for chunk in RI_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Rhode Island Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    RI_NFHL = unZipFolder + '/' + "RI_NFHL"

    os.makedirs(RI_NFHL)

    zip_ref = zipfile.ZipFile(RI_dest)

    zip_ref.extractall(RI_NFHL)

    zip_ref.close()

    print "Rhode Island Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(RI_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = RI_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'RI_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Rhode Island Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(RI_dest)
    shutil.rmtree(RI_NFHL)
    print("Unnecessary Rhode Island Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Rhode Island"
    print("\n")


######################################################################################
#South Carolina

SC_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_45_20190211.zip' #838MB

print "Initiating South Carolina..."

SC_resp = requests.get(SC_url, stream = True)
print "Status is " + str(SC_resp.status_code)

SC_dest = folder + "/" + "SC.zip"

if SC_resp.status_code == 200:
    
    with open(SC_dest, 'wb') as data:
        for chunk in SC_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "South Carolina Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    SC_NFHL = unZipFolder + '/' + "SC_NFHL"

    os.makedirs(SC_NFHL)

    zip_ref = zipfile.ZipFile(SC_dest)

    zip_ref.extractall(SC_NFHL)

    zip_ref.close()

    print "South Carolina Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(SC_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = SC_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'SC_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "South Carolina Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(SC_dest)
    shutil.rmtree(SC_NFHL)
    print("Unnecessary South Carolina Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download South Carolina"
    print("\n")



###################################################################################
#South Dakota

SD_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_46_20190614.zip' #98MB

print "Initiating South Dakota..."

SD_resp = requests.get(SD_url, stream = True)
print "Status is " + str(SD_resp.status_code)

SD_dest = folder + "/" + "SD.zip"

if SD_resp.status_code == 200:
    
    with open(SD_dest, 'wb') as data:
        for chunk in SD_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "South Dakota Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    SD_NFHL = unZipFolder + '/' + "SD_NFHL"

    os.makedirs(SD_NFHL)

    zip_ref = zipfile.ZipFile(SD_dest)

    zip_ref.extractall(SD_NFHL)

    zip_ref.close()

    print "South Dakota Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(SD_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = SD_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'SD_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "South Dakota Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(SD_dest)
    shutil.rmtree(SD_NFHL)
    print("Unnecessary South Dakota Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download South Dakota"
    print("\n")


#####################################################################################
#Tennessee

TN_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_47_20190213.zip' #540MB

print "Initiating Tennessee..."

TN_resp = requests.get(TN_url, stream = True)
print "Status is " + str(TN_resp.status_code)

TN_dest = folder + "/" + "TN.zip"

if TN_resp.status_code == 200:
    
    with open(TN_dest, 'wb') as data:
        for chunk in TN_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Tennessee Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    TN_NFHL = unZipFolder + '/' + "TN_NFHL"

    os.makedirs(TN_NFHL)

    zip_ref = zipfile.ZipFile(TN_dest)

    zip_ref.extractall(TN_NFHL)

    zip_ref.close()

    print "Tennessee Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(TN_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = TN_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'TN_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Tennessee Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(TN_dest)
    shutil.rmtree(TN_NFHL)
    print("Unnecessary Tennessee Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Tennessee"
    print("\n")


######################################################################################
#Texas

TX_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_48_20190614.zip' #1285MB

print "Initiating Texas..."

TX_resp = requests.get(TX_url, stream = True)
print "Status is " + str(TX_resp.status_code)

TX_dest = folder + "/" + "TX.zip"

if TX_resp.status_code == 200:
    
    with open(TX_dest, 'wb') as data:
        for chunk in TX_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Texas Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    TX_NFHL = unZipFolder + '/' + "TX_NFHL"

    os.makedirs(TX_NFHL)

    zip_ref = zipfile.ZipFile(TX_dest)

    zip_ref.extractall(TX_NFHL)

    zip_ref.close()

    print "Texas Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(TX_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = TX_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'TX_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Texas Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(TX_dest)
    shutil.rmtree(TX_NFHL)
    print("Unnecessary Texas Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Texas"
    print("\n")


####################################################################################
#Utah

UT_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_49_20190609.zip' #71MB

print "Initiating Utah..."

UT_resp = requests.get(UT_url, stream = True)
print "Status is " + str(UT_resp.status_code)

UT_dest = folder + "/" + "UT.zip"

if UT_resp.status_code == 200:
    
    with open(UT_dest, 'wb') as data:
        for chunk in UT_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Utah Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    UT_NFHL = unZipFolder + '/' + "UT_NFHL"

    os.makedirs(UT_NFHL)

    zip_ref = zipfile.ZipFile(UT_dest)

    zip_ref.extractall(UT_NFHL)

    zip_ref.close()

    print "Utah Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(UT_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = UT_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'UT_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Utah Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(UT_dest)
    shutil.rmtree(UT_NFHL)
    print("Unnecessary Utah Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Utah"
    print("\n")


####################################################################################
#Vermont

VT_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_50_20161207.zip' #41MB

print "Initiating Vermont..."

VT_resp = requests.get(VT_url, stream = True)
print "Status is " + str(VT_resp.status_code)

VT_dest = folder + "/" + "VT.zip"

if VT_resp.status_code == 200:
    
    with open(VT_dest, 'wb') as data:
        for chunk in VT_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Vermont Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    VT_NFHL = unZipFolder + '/' + "VT_NFHL"

    os.makedirs(VT_NFHL)

    zip_ref = zipfile.ZipFile(VT_dest)

    zip_ref.extractall(VT_NFHL)

    zip_ref.close()

    print "Vermont Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(VT_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = VT_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'VT_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Vermont Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(VT_dest)
    shutil.rmtree(VT_NFHL)
    print("Unnecessary Vermont Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Vermont"
    print("\n")


####################################################################################
#Virginia

VA_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_51_20190425.zip' #668MB

print "Initiating Virginia..."

VA_resp = requests.get(VA_url, stream = True)
print "Status is " + str(VA_resp.status_code)

VA_dest = folder + "/" + "VA.zip"

if VA_resp.status_code == 200:
    
    with open(VA_dest, 'wb') as data:
        for chunk in VA_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Virginia Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    VA_NFHL = unZipFolder + '/' + "VA_NFHL"

    os.makedirs(VA_NFHL)

    zip_ref = zipfile.ZipFile(VA_dest)

    zip_ref.extractall(VA_NFHL)

    zip_ref.close()

    print "Virginia Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(VA_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = VA_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'VA_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Virginia Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(VA_dest)
    shutil.rmtree(VA_NFHL)
    print("Unnecessary Virginia Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Virginia"
    print("\n")


###################################################################################
#Washington

WA_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_53_20190606.zip' #172MB

print "Initiating Washington..."

WA_resp = requests.get(WA_url, stream = True)
print "Status is " + str(WA_resp.status_code)

WA_dest = folder + "/" + "WA.zip"

if WA_resp.status_code == 200:
    
    with open(WA_dest, 'wb') as data:
        for chunk in WA_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Washington Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    WA_NFHL = unZipFolder + '/' + "WA_NFHL"

    os.makedirs(WA_NFHL)

    zip_ref = zipfile.ZipFile(WA_dest)

    zip_ref.extractall(WA_NFHL)

    zip_ref.close()

    print "Washington Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(WA_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = WA_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'WA_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Washington Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(WA_dest)
    shutil.rmtree(WA_NFHL)
    print("Unnecessary Washington Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Washington"
    print("\n")


###################################################################################
#West Virginia

WV_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_54_20190405.zip' #239MB

print "Initiating West Virginia..."

WV_resp = requests.get(WV_url, stream = True)
print "Status is " + str(WV_resp.status_code)

WV_dest = folder + "/" + "WV.zip"

if WV_resp.status_code == 200:
    
    with open(WV_dest, 'wb') as data:
        for chunk in WV_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "West Virginia Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    WV_NFHL = unZipFolder + '/' + "WV_NFHL"

    os.makedirs(WV_NFHL)

    zip_ref = zipfile.ZipFile(WV_dest)

    zip_ref.extractall(WV_NFHL)

    zip_ref.close()

    print "West Virginia Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(WV_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = WV_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'WV_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "West Virginia Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(WV_dest)
    shutil.rmtree(WV_NFHL)
    print("Unnecessary West Virginia Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download West Virginia"
    print("\n")


#####################################################################################
#Wisconsin

WI_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_55_20190513.zip' #745MB

print "Initiating Wisconsin..."

WI_resp = requests.get(WI_url, stream = True)
print "Status is " + str(WI_resp.status_code)

WI_dest = folder + "/" + "WI.zip"

if WI_resp.status_code == 200:
    
    with open(WI_dest, 'wb') as data:
        for chunk in WI_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Wisconsin Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    WI_NFHL = unZipFolder + '/' + "WI_NFHL"

    os.makedirs(WI_NFHL)

    zip_ref = zipfile.ZipFile(WI_dest)

    zip_ref.extractall(WI_NFHL)

    zip_ref.close()

    print "Wisconsin Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(WI_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = WI_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'WI_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Wisconsin Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(WI_dest)
    shutil.rmtree(WI_NFHL)
    print("Unnecessary Wisconsin Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Wisconsin"
    print("\n")


####################################################################################
#Wyoming

WY_url = 'https://hazards.fema.gov/nfhlv2/output/State/NFHL_56_20190313.zip' #63MB

print "Initiating Wyoming..."

WY_resp = requests.get(WY_url, stream = True)
print "Status is " + str(WY_resp.status_code)

WY_dest = folder + "/" + "WY.zip"

if WY_resp.status_code == 200:
    
    with open(WY_dest, 'wb') as data:
        for chunk in WY_resp.iter_content(chunk_size=10485760): ### Roughly 10MB
            data.write(chunk)
    print "Wyoming Download Complete"
    data.close()
    

    ### Unzip the downloaded file ###
    WY_NFHL = unZipFolder + '/' + "WY_NFHL"

    os.makedirs(WY_NFHL)

    zip_ref = zipfile.ZipFile(WY_dest)

    zip_ref.extractall(WY_NFHL)

    zip_ref.close()

    print "Wyoming Unzip Complete"
    

    ### Sift through layers and export 'S_Fld_Haz_Ar' as shapefile ###
    file_list = os.listdir(WY_NFHL)

    for item in file_list:
        if item.endswith(".gdb"):
            gdb = item

    arcpy.env.workspace = WY_NFHL + '/' + gdb

    featureClasses = arcpy.ListFeatureClasses()

    for fc in featureClasses:
        if fc == "S_Fld_Haz_Ar":
            newName = arcpy.Rename_management(fc, 'WY_Fld_Haz_Ar')
            arcpy.FeatureClassToShapefile_conversion(newName, dbLoc)
            print "Wyoming Shapefile Copied"

            
    ### Remove unnecessary remaining data/folders ###
    os.remove(WY_dest)
    shutil.rmtree(WY_NFHL)
    print("Unnecessary Wyoming Files Deleted")
    print("\n")
    
else:
    
    print "Failed to download Wyoming"
    print("\n")
    
### Complete ###
print "Data Download Complete. \nPlease review the list of States above.\nStates with '400 Status' have been updated with new data, and their URLs must be resourced."


##### Unpack each of the zip files into desired location #####

##dir_name = "..." #Filepath to the zip files
##
##unpack = "..." #Filepath where files should be unpacked (include new folder name)
##
##os.makedirs(unpack)
##
##
##file_list = os.listdir(dir_name)
##
##for item in file_list:
##    
##    if item.endswith(".zip"):
##        
##        print item
##        
##        file_name = dir_name + "/" + item
##        
##        zip_ref = zipfile.ZipFile(file_name)
##        
##        zip_ref.extractall(unpack)
##
##        zip_ref.close()
