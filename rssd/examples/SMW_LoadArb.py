##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Load arb file on SMW
### Author:  mclim
### Date:    2018.05.17
##########################################################
### User Entry
##########################################################
host = '192.168.1.114'               #Get local machine name

##########################################################
### Code Start
##########################################################
from rssd.VSG.Common import VSG

SMW = VSG().jav_Open(host) 
#SMW.jav_logSCPI()                  #Log SCPI commands
SMW.Set_Freq(10e9)                  #Set 10GHz
SMW.Set_RFPwr(-30)                  #Output -30dBm
SMW.Set_RFState('ON')               #Turn RF Output on
SMW.Set_ArbWv('composer.wv')        #Load file
SMW.Set_ArbState('ON')              #Turn on Arb & IQ Mod
SMW.jav_ClrErr                      #Clear Errors
