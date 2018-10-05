##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date   : 2018.05.24
### Steps  : 
###
##########################################################
### User Entry
##########################################################
import os
BaseDir = os.path.dirname(os.path.realpath(__file__))

FSW_IP  = '192.168.1.109'
MeasTim = 500e-6
NumIter = 100
##########################################################
### Code Overhead
##########################################################
from rssd.FSW_Common import VSA
from datetime        import datetime

FSW = VSA()                         #Create FSW Object
FSW.jav_Open(FSW_IP)                #Connect to FSW
FSW.jav_Reset()
FSW.Set_DisplayUpdate("OFF")

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
tick = datetime.now()

### <\thing we are timing>
for i in range(NumIter):
   FSW.query('*IDN?')
   print(FSW.query('*OPT?')) 
### <\thing we are timing>

d = datetime.now() - tick
tTime = d.seconds + d.microseconds/1e6
pTime = tTime/NumIter
OutStr = 'Total Time: %.6f \nTime/Meas : %.6f'%(tTime,pTime)
print(OutStr)
   
##########################################################
### Cleanup Automation
##########################################################
FSW.jav_Close()

