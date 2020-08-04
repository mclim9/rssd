"""Parse R&S SYST:DFPR String"""
# pylint: disable=bad-whitespace,invalid-name
##########################################################
from xml.etree      import ElementTree as ET
from rssd.yaVISA    import jaVisa
from rssd.FileIO    import FileIO

### User Entry
##########################################################
IPaddr = '10.0.0.25'

##########################################################
### Code Begin
##########################################################

OFile   = FileIO().makeFile(__file__)
K2      = jaVisa().jav_openvisa(f'TCPIP0::{IPaddr}::INSTR', OFile)  #Create VISA object
rdStr   = K2.query('SYST:DFPR?')
XMLstr  = '<' + rdStr.split('<',1)[1]
# print(XMLstr)

if rdStr == '<notRead>':
    print('Instrument not supported')
else:
    root_element = ET.fromstring(XMLstr)

    for child in root_element:
        print(child)
        for key,value in child.attrib.items():
            print(f'    {key}:{value}')
