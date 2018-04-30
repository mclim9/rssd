##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Simple Instrument Socket Example
### Author:  mclim
### Date:    2017.09.01
##########################################################
### User Entry
##########################################################
host = '127.0.0.1'               #Get local machine name
port = 5025                      #Reserve a port for your service.

import driver.VSE_ADemod

##########################################################
### Code Start
##########################################################
VSE = driver.VSE_ADemod.VSE()
if 0:
   VSE.VISA_Open("192.168.1.109")
else:
   VSE.VISA_Open("127.0.0.1")
VSE.Set_DisplayUpdate("ON")
VSE.Set_Channel("ADEM")
VSE.Set_Adem_dbw(500e6)   
VSE.Set_Adem_LPassStat("ON")
VSE.Set_Adem_LPassRelative("5PCT")
VSE.Set_InitImm()
VSE.VISA_ClrErr()
 

