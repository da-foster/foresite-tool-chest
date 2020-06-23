### Title: WebMapBackup
### Description: THIS TOOL MUST BE RUN IN PYTHON 3
###              The intent of this tool is to back up a copy
###              of a web map into a designated, pre-created folder
###              
### Company: Foresite Group
### Author: Darren Foster

print ("Running... \n The imports will take a few moments...")
print("\n")

from arcgis.gis import GIS
from IPython.display import display
from arcgis.mapping import WebMap
import datetime

day = datetime.date.today()
today = day.strftime("%m_%d_%y")

#Provide log-in credentials for authentication#
gis = GIS(url = "https://www.arcgis.com/sharing/rest/oauth2/authorize?client_id=arcgisonline&display=default&response_type=token&state=%7B%22returnUrl%22%3A%22https%3A%2F%2Fwww.arcgis.com%2Fhome%2Findex.html%22%2C%22useLandingPage%22%3Atrue%7D&expiration=20160&locale=en-us&redirect_uri=https%3A%2F%2Fwww.arcgis.com%2Fhome%2Faccountswitcher-callback.html&force_login=true&hideCancel=true&showSignupOption=true&signuptype=esri", \
          username = "******", \
          password = "******")

#Specify the desired existing web map using the query and item type#
webmap_search = gis.content.search(query = "Knoxville_QC_Map_Live", item_type = "Web Map")

#There should only be one result, but you still must specify its index, which is [0]#
webmap_result = webmap_search[0]

#Set the Title of the web map#
name = webmap_result.title

print ("The title of the map is " + name)
print("\n")

#Place the search result into the WebMap class#
webmap = WebMap(webmap_result)

#Collect and display a list of the layers within the web map#
layersList = webmap.layers

print ("Layers: \n")

for item in layersList:
    print (item.title)
    
print("\n")

#Establish the required Item Properties#
itemProperties = {'title':'Knoxville_QC_Map_Live_BACKUP_' + today, 
                   'snippet':'Backup Knoxville_QC_Map_Live map created using Python API', 
                   'tags':['automation', 'Backup']}

#Save the web map as a copy into the desired folder#
webmap.save(item_properties = itemProperties, folder = "Backup Web Maps")

print ("Backup Complete")

