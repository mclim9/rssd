##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Multiple CC K96 Example
### Author:  mclim
### Date:    2018.05.01
##########################################################
### User Entry
##########################################################
host = '127.0.0.1'               #Get local machine name
port = 5025                      #Reserve a port for your service.

import driver.VSE_K96

##########################################################
### Code Start
##########################################################
VSE = driver.VSE_K96.VSE()
if 0:
   VSE.VISA_Open("192.168.1.109")
else:
   VSE.VISA_Open("127.0.0.1")
   
VSE.Set_DisplayUpdate("ON")
#VSE.Set_Group("")
VSE.Set_Channel("OFDMVSA")
VSE.Set_Channel("OFDMVSA","K962")
VSE.Set_SweepCont(0)
VSE.Set_InitImm()
VSE.VISA_ClrErr()
 

