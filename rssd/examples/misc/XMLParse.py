##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Simple Instrument Socket Example
### Author:  mclim
### Date:     2017.09.01
##########################################################
### User Entry
##########################################################
xmlFile = 'syst_dfpr-FSW.txt'              #Instrument IP address

##########################################################
### Code Begin
##########################################################
import xml.etree.ElementTree as ET  

##########################################################
### Main Code
##########################################################
tree = ET.parse('syst_dfpr-FSW.txt')
root = tree.getroot()
#xmlIn = xmlIn[xmlIn.find('>')+1:]#Remove header
#root  = ET.fromstring(xmlIn)
# DData = root.find('DeviceData').items()
# devID = DData[0][1]
# dType = DData[1][1]
devID = root[0].attrib['deviceId']
dType = root[0].attrib['type']
os     = root[2][1].attrib['name']
osVer = root[2][1].attrib['version']
print(os, osVer)
print(dType, devID)

print("HW Options:")
for hwopt in root.iter('Hardware'):
    try:
        print("    ",hwopt.attrib['name'],hwopt.attrib['partNumber'],hwopt.attrib['sn'])
    except:
        pass
        
print("SW Options:")
for swopt in root.iter('Software'):
    try:
        print("    ",swopt.attrib['name'], end='')
        print(swopt.attrib['version'], end='')
    except:
        pass
    print("")
    
print("License Options:")
for swopt in root.iter('ActiveLicense'):
    try:
        print("    ",end='')
        print(swopt.attrib['optionIndex'], end='')
        print(swopt.attrib['used'], end='')
    except:
        pass
    print("")
