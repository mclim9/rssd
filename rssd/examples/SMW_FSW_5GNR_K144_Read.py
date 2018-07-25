##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: FSW/SMW 5G NR Demo
### Author:  mclim
### Date:    2018.07.05
### Descrip: FSW 3.20-18.7.1.0 Beta
###          SMW 4.30 SP2
##########################################################
### User Entry
##########################################################
import os
BaseDir = os.path.dirname(os.path.realpath(__file__))
OutFile = BaseDir + "\\data\\SMW_FSW_5GNR"
 
print(__file__)

SMW_IP   = '192.168.1.114'                    #IP Address
FSW_IP   = '192.168.1.109'                    #IP Address
Freq     = 10e9
odata =  [[] for i in range(3)]

##########################################################
### Code Start
##########################################################
from rssd.SMW_5GNR_K144 import VSG
from rssd.FSW_5GNR_K144 import VSA
from rssd.FileIO        import FileIO
import time

f = FileIO()
odataFile = f.Init(OutFile)
SMW = VSG()
SMW.jav_Open(SMW_IP,f.sFName)
FSW = VSA()
FSW.jav_Open(FSW_IP,f.sFName)

##########################################################
### Instrument Settings
##########################################################
odata[0].append("               ")
odata[0].append("RefA,MHz       ")
odata[0].append("Ch BW          ")
odata[0].append("SubSpacing     ")
odata[0].append("Num BWP        ")
odata[0].append("BWP_RB         ")
odata[0].append("BWP_RBoff      ")
odata[0].append("BWP_Slot_Mod   ")
odata[0].append("BWP_Slot_RB    ")
odata[0].append("BWP_Slot_RBOff ")
odata[0].append("BWP_Slot_SymNum")
odata[0].append("BWP_Slot_SymOff")
odata[0].append("BWP_Slot_Cntr  ")

if 1:
   SMW.Set_5GNR_Parameters("DL")
   odata[1].append("SMW   ")
   odata[1].append(int(SMW.Get_5GNR_RefA())/1e6)
   odata[1].append(SMW.Get_5GNR_ChannelBW())
   odata[1].append(SMW.Get_5GNR_BWP_SubSpace())
   odata[1].append(SMW.Get_5GNR_BWP_Count())
   odata[1].append(SMW.Get_5GNR_BWP_ResBlock())
   odata[1].append(SMW.Get_5GNR_BWP_ResBlockOffset())
   odata[1].append(SMW.Get_5GNR_BWP_Slot_Modulation())
   odata[1].append(SMW.Get_5GNR_BWP_Slot_ResBlock())
   odata[1].append(SMW.Get_5GNR_BWP_Slot_ResBlockOffset())
   odata[1].append(SMW.Get_5GNR_BWP_Slot_SymbNum())
   odata[1].append(SMW.Get_5GNR_BWP_Slot_SymbOff())
   odata[1].append(int(SMW.Get_5GNR_BWP_Center())/1e6)

FSW.Init_5GNR()
FSW.Set_5GNR_Parameters("DL")
odata[2].append("FSW")
odata[2].append(int(FSW.Get_5GNR_RefA())/1e6)
odata[2].append(FSW.Get_5GNR_ChannelBW())
odata[2].append(FSW.Get_5GNR_BWP_SubSpace())
odata[2].append(FSW.Get_5GNR_BWP_Count())
odata[2].append(FSW.Get_5GNR_BWP_ResBlock())
odata[2].append(FSW.Get_5GNR_BWP_ResBlockOffset())
odata[2].append(FSW.Get_5GNR_BWP_Slot_Modulation())
odata[2].append(FSW.Get_5GNR_BWP_Slot_ResBlock())
odata[2].append(FSW.Get_5GNR_BWP_Slot_ResBlockOffset())
odata[2].append(FSW.Get_5GNR_BWP_Slot_SymbNum())
odata[2].append(FSW.Get_5GNR_BWP_Slot_SymbOff())
odata[2].append(int(FSW.Get_5GNR_BWP_Center())/1e6)

for i in range(13):
   print("%s\t%s\t%s"%(odata[0][i],odata[1][i],odata[2][i]))

SMW.jav_ClrErr()                          #Clear Errors
FSW.jav_ClrErr()                          #Clear Errors
