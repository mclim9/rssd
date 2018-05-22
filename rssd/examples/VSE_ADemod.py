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

##########################################################
### Code Start
##########################################################
import rssd.VSE_ADemod

VSE = rssd.VSE_ADemod.VSE()
VSE.jav_Open(host) 
#VSE.logSCPI()
VSE.Set_DisplayUpdate("ON")
VSE.Set_Channel("ADEM")
VSE.Set_Adem_dbw(500e6)   
VSE.Set_Adem_LPassStat("ON")
VSE.Set_Adem_LPassRelative("5PCT")
VSE.Set_InitImm()
VSE.jav_ClrErr()
