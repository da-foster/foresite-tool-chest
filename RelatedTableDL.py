### This tool is designed to operate within Jupyter Notebooks.
### It downloads a singular OR a batch of related data table from AGOL, and 
### converts it to an Excel sheet.
### Company: Foresite Group
### Author: Darren Foster


from arcgis.gis import GIS
from IPython.display import display
from pathlib import Path
import pandas as pd

#Log in authentication for AGOL
gis = GIS(url="https://www.arcgis.com/sharing/rest/oauth2/authorize?client_id=arcgisonline&display=default&response_type=token&state=%7B%22useLandingPage%22%3Atrue%7D&expiration=20160&locale=en-us&redirect_uri=https%3A%2F%2Fwww.arcgis.com%2Fhome%2Faccountswitcher-callback.html&force_login=true&showSignupOption=true", \
          username="fg_WS1", \
          password="GISws101!")

#Basic search for content within the account that starts with "Mono"
results = gis.content.search("Mono")

#Prints a list of the results
print results

#Capturing a specific item in the list [0], [1], etc.
fl = results[1]

#Shows a list of the tables associated with this FL
tables = flc.tables
print tables

#An alternative way of capturing a specific entity within AGOl is to specify its "ID"
featureLayer = gis.content.get("6d4af05336e44a3c9a33c59260b42b0a")

#Generates a list of tables again
tablesList = featureLayer.tables

#Specify the desired table
tbl_1 = tablesList[0]

#Create a query against the table
q = tbl_1.query()

#Create a Pandas data frame against the query
data_frame = q.df

#Print the data frame
print data_frame

#Set a download path
data_path = Path(r'C:\Users\dfoster\Downloads\TEST')

#Create an Excel Writer to convert the data frame into an Excel sheet
writer = pd.ExcelWriter(r'C:\Users\dfoster\Downloads\TEST\SectionRepeatStart.xlsx')

#Convert the data frame into an Excel sheet
data_frame.to_excel(writer)

#Save the file
writer.save()


###########################################################################################
### This code will loop through the list of related tables for a given Feature Layer, rather
### than specifying an individual table.

from arcgis.gis import GIS
from IPython.display import display
from pathlib import Path
import pandas as pd

#Log in authentication for AGOL
gis = GIS(url="https://www.arcgis.com/sharing/rest/oauth2/authorize?client_id=arcgisonline&display=default&response_type=token&state=%7B%22useLandingPage%22%3Atrue%7D&expiration=20160&locale=en-us&redirect_uri=https%3A%2F%2Fwww.arcgis.com%2Fhome%2Faccountswitcher-callback.html&force_login=true&showSignupOption=true", \
          username="fg_WS1", \
          password="GISws101!")

#Capture a specific entity within AGOl by specifying its "ID"
featureLayer = gis.content.get("6d4af05336e44a3c9a33c59260b42b0a")

#Generates a list of tables
tables = featureLayer.tables

#Set a download path
data_path = Path(r'C:\Users\dfoster\Downloads\TEST')

#Loop through each of the related tables in the Feature Layer, write the table to an excel sheet, & save the file
for item in tables:
    q = item.query()
    data_frame = q.df
    print (data_frame)
    writer = pd.ExcelWriter(r"C:/Users/dfoster/Downloads/TEST" + "/" + item.properties.name + ".xlsx")
    data_frame.to_excel(writer)
    writer.save()
