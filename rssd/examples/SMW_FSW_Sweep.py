##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Sweep FSW/SMW Frequncy
### Author:  mclim
### Date:    2018.05.17
##########################################################
### User Entry
##########################################################
import os
BaseDir = os.path.dirname(os.path.realpath(__file__))
OutFile = BaseDir + "\\data\\SMW_FSW_Sweep"

print __file__

SMW_IP = '192.168.1.115'                    #IP Address
FSW_IP = '192.168.1.109'                    #IP Address
FreqStart = int(51e9)
FreqStop = int(75e9)
FreqStep = int(1e9)
fSpan = 100e6
SWM_Out = -20
Mixer = 0

##########################################################
### Code Start
##########################################################
from rssd.SMW_Common import VSG
from rssd.FSW_Common import VSA
from rssd.FileIO     import FileIO
import time

f = FileIO()
DataFile = f.Init(OutFile)
SMW = VSG()
SMW.jav_Open(SMW_IP,f.sFName)
FSW = VSA()
FSW.jav_Open(FSW_IP,f.sFName)

##########################################################
### Instrument Settings
##########################################################
SMW.Set_RFPwr(SWM_Out)                    #Output Power
SMW.Set_RFState('ON')                     #Turn RF Output on

FSW.Set_SweepCont(0)
#FSW.Set_SweepTime(200e-3)
FSW.Set_Span(fSpan)

if Mixer:                                 #Mixer
    FSW.write('SENS:MIX:STAT ON')
    FSW.write('SENS:MIX:HARM:BAND V')

for freq in range(FreqStart,FreqStop,FreqStep):
    SMW.Set_Freq(freq)
    time.sleep(0.5)
    FSW.Set_Freq(freq)
    FSW.Set_InitImm()
    FSW.Set_Mkr_Peak()
    Mkr = FSW.Get_Mkr_XY()
    OutStr = "%d,%s,%s"%(freq,Mkr[0],Mkr[1])
    f.write(OutStr)

SMW.jav_ClrErr()                          #Clear Errors
FSW.jav_ClrErr()                          #Clear Errors
