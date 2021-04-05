##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Simple Instrument Socket Example
### Author:  mclim
### Date:    2017.09.01
##########################################################
### User Entry
##########################################################
VSE_IP = '127.0.0.1'               #Get local machine name

##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.VSE.ADemod import VSE
VSE = VSE()
VSE.jav_Open(VSE_IP)
#VSE.logSCPI()

##########################################################
### Code Start
##########################################################
VSE.Set_DisplayUpdate("ON")
VSE.Set_Channel("ADEM")
VSE.Set_Adem_dbw(500e6)
VSE.Set_Adem_LPassStat("ON")
VSE.Set_Adem_LPassRelative("5PCT")
VSE.Set_InitImm()
VSE.jav_ClrErr()
