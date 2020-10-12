### Title: GDB_Clear.py
### Description: This Python Script Tool is meant to be used against Enterprise SDE connections,
###              where simply deleting the database is not an option. Provide an input database
###              SDE connection to reset the database entirely. All feature classes, tables, datasets
###              and domains will be deleted.
### Company: Foresite Group
### Author: Darren Foster
### MUST RUN IN PYTHON 2.7 ###

import arcpy

def obliterate(group, dataIn, inputGDB=None):
    """
    Function to remove all feature classes, domain values, feature datasets,  
    & SDE tables from an Enterprise GDB.
    
    Parameter 1 = The kind of input data. 
    Parameter 2 = A list of input data. 
    Parameter 3 (Optional) = An input GDB
    """
    
    if group == 'feature classes':
        
        arcpy.AddMessage('Deleting Feature Classes')
        arcpy.AddMessage('\n')
        if not dataIn:
            arcpy.AddMessage('Empty input for feature classes')
        else:
            for el in dataIn:
                arcpy.AddMessage(el)
                arcpy.Delete_management(el)
            
    elif group == 'tables':
        
        arcpy.AddMessage('Deleting Tables')
        arcpy.AddMessage('\n')
        if not dataIn:
            arcpy.AddMessage('Empty input for tables')
        else:
            for el in dataIn:
                arcpy.AddMessage(el)
                arcpy.Delete_management(el)

    elif group == 'domains':
        
        arcpy.AddMessage('Deleting Domains')
        arcpy.AddMessage('\n')
        if not dataIn:
            arcpy.AddMessage('Empty input for domains')
        else:
            for el in dataIn:
                name = el.name
                arcpy.AddMessage(name)
                arcpy.DeleteDomain_management(inputGDB, name)

    elif group == 'datasets':
        
        arcpy.AddMessage('Deleting Datasets')
        arcpy.AddMessage('\n')
        if not dataIn:
            arcpy.AddMessage('Empty input for datasets')
        else:
            for el in dataIn:
                arcpy.AddMessage('Feature dataset: ' + el)
                # print('Feature classes:')
                # for fc in arcpy.ListFeatureClasses(feature_dataset=el):
                #     arcpy.AddMessage(fc)
                #     arcpy.Delete_management(fc)
                arcpy.Delete_management(el)

    else:
        
        arcpy.AddMessage('Bad input into function...')

### User GDB Input / Environment Setup ###
gdb = arcpy.GetParameterAsText(0)
arcpy.env.workspace = gdb
arcpy.AddMessage('Input GDB:  ' + gdb)
arcpy.AddMessage('\n')

### Retrieve a list of the standalone feature classes ###
fcs = 'feature classes'
layers = arcpy.ListFeatureClasses()
obliterate(fcs, layers)
arcpy.AddMessage('\n')

### Retrieve a list of the standalone SDE tables ###
tbls = 'tables'
tables = arcpy.ListTables()
obliterate(tbls, tables)
arcpy.AddMessage('\n')

### Retrieve a list of the datasets ###
ds = 'datasets'
datasets = arcpy.ListDatasets(feature_type='feature')
obliterate(ds, datasets)
arcpy.AddMessage('\n')

### Retrieve a list of the domains ###
dms = 'domains'
domains = arcpy.da.ListDomains(gdb)
obliterate(dms, domains, gdb)
arcpy.AddMessage('\n')
