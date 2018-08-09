##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Simple Instrument Socket Example
### Author:  mclim
### Date:    2017.09.01 
##########################################################
### User Entry
##########################################################
OSP_IP   = '192.168.1.114'                    #IP Address
Path = [[1,2,3],[4,5,6]]

##########################################################
### Code Start
##########################################################
from rssd.OSP_Common import OSP
OSP = OSP()
OSP.jav_Open(OSP_IP)
for sw in Path:
   #print(sw)
   OSP.Set_SW(sw[0],sw[1],sw[2])
OSP.jav_ClrErr()                          #Clear Errors

