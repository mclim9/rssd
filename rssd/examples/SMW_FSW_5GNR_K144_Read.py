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

print __file__

SMW_IP   = '192.168.1.114'                    #IP Address
FSW_IP   = '192.168.1.109'                    #IP Address
Freq     = 10e9

##########################################################
### Code Start
##########################################################
from rssd.SMW_5GNR_K144 import VSG
from rssd.FSW_5GNR_K144 import VSA
from rssd.FileIO        import FileIO
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
SMW.Get_Freq(Freq)
print(SMW.Get_5GNR_UL_ChannelBW())
print(SMW.Get_5GNR_UL_SubSpace())
print(SMW.Get_5GNR_UL_BWP_Count())
print(SMW.Get_5GNR_UL_BWP_ResourceBlock())
print(SMW.Get_5GNR_UL_BWP_ResourceBlockOffset())   
print(SMW.Get_5GNR_UL_BWP_SlotNum())

print(SMW.Get_5GNR_UL_BWP_Slot_Modulation())
print(SMW.Get_5GNR_UL_BWP_Slot_ResourceBlock())
print(SMW.Get_5GNR_UL_BWP_Slot_ResourceBlockOffset())
print(SMW.Get_5GNR_UL_BWP_Slot_SymbNum())
print(SMW.Get_5GNR_UL_BWP_Slot_SymbOff())

FSW.Get_Freq(Freq)
FSW.Init_5GNR()
print(FSW.Get_5GNR_UL_ChannelBW())
print(FSW.Get_5GNR_UL_SubSpace())
print(FSW.Get_5GNR_UL_BWP_Count())
print(FSW.Get_5GNR_UL_BWP_ResourceBlock())
print(FSW.Get_5GNR_UL_BWP_ResourceBlockOffset())
print(FSW.Get_5GNR_UL_BWP_SlotCount())

print(FSW.Get_5GNR_UL_BWP_SlotNum())
print(FSW.Get_5GNR_UL_BWP_Slot_Modulation())
print(FSW.Get_5GNR_UL_BWP_Slot_ResourceBlock())
print(FSW.Get_5GNR_UL_BWP_Slot_ResourceBlockOffset())
print(FSW.Get_5GNR_UL_BWP_Slot_SymbNum())
print(FSW.Get_5GNR_UL_BWP_Slot_SymbOff())

OutStr = "%d,%s"%(freq,EVM)
f.write(OutStr)

SMW.jav_ClrErr()                          #Clear Errors
FSW.jav_ClrErr()                          #Clear Errors
