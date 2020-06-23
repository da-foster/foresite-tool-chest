#dFoster#
import arcpy
import sys
import xlsxwriter

reload(sys)
sys.setdefaultencoding('utf8')

gdb = r'C:\Users\dfoster\Downloads\Mastec_LittleRockAR_Bulk_2019-08-28_00-19-24\Mastec_LittleRockAR_Bulk_2019-08-28_00-19-24.gdb'

domains = arcpy.da.ListDomains(gdb)

### Here are some various ways to view/print domain data from a GDB ###

#################################################################################################################################

### Ultimately, this prints data out in a format that JR prefers in his excel sheet ###
     
for domain in domains:
    dValues = domain.codedValues
    name = domain.name
    description = domain.description
     
    print "Domain name:  " + str(name)
    print "Description:  " + str(description)
    print "Coded Values:"
     
    for value, desc in dValues.iteritems():
        print str(value) + " : " + str(desc)
    print "\n"

###############################################################################################################################

import arcpy

domains = arcpy.da.ListDomains("C:/Boston/Boston.gdb")

for domain in domains:
    print('Domain name: {0}'.format(domain.name))
    if domain.domainType == 'CodedValue':
        coded_values = domain.codedValues
        for val, desc in coded_values.items():
            print('{0} : {1}'.format(val, desc))
    elif domain.domainType == 'Range':
        print('Min: {0}'.format(domain.range[0]))
        print('Max: {0}'.format(domain.range[1]))


###############################################################################################################################

for domain in domains:
    values = domain.codedValues
    dValues = eval(values)
    newValues = [str(x) for x in dValues]
    name = domain.name
    description = domain.description
    print "Domain name: " + str(name) + " Description: " + str(description) + " Coded Values: " + str(newValues) + "\n"

###############################################################################################################################

for domain in domains:
    dValues = domain.codedValues
    newValues = [x for x in dValues]
     
    name = domain.name
    description = domain.description
     
    print "Domain name: " + str(name) + " Description: " + str(description) + " Coded Values: " + str(newValues) + "\n"

###############################################################################################################################
