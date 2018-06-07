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
OutFile = BaseDir + "\\data\\" + __file__

SMW_IP = '192.168.1.115'                    #IP Address
FSW_IP = '192.168.1.109'                    #IP Address
SWM_Out = -30
Mixer = 0
##########################################################
### Code Start
##########################################################
from rssd.SMW_Common import VSG
from rssd.FSW_Common import VSA
from rssd.FileIO     import FileIO

f = FileIO()
DataFile = f.Init(OutFile)
SMW = VSG()
SMW.jav_Open(SMW_IP,f.sFName)
FSW = VSA()
FSW.jav_Open(FSW_IP,f.sFName)

SMW.Set_RFPwr(SWM_Out)                    #Output Power
SMW.Set_RFState('ON')                     #Turn RF Output on

FSW.Set_SweepCont(0)

if Mixer:                                 #Mixer
    FSW.write('SENS:MIX:STAT ON')
    FSW.write('SENS:MIX:HARM:BAND V')

for freq in range(1,20,1):
    SMW.Set_Freq(freq*1e9)
    #FSW.Set_Freq(freq*1e9)
    FSW.Set_InitImm()
    FSW.Set_Mkr_Peak()
    Mkr = FSW.Get_Mkr_XY()
    OutStr = "%f,%s,%s"%(freq,Mkr[0],Mkr[1])
    f.write(OutStr)

SMW.jav_ClrErr()                          #Clear Errors
FSW.jav_ClrErr()                          #Clear Errors
