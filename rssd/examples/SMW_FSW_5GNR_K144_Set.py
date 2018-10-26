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
SMW_IP   = '192.168.1.114'                #IP Address
FSW_IP   = '192.168.1.109'                #IP Address
Freq     = 19e9
SWM_Out  = 0

NR_Dir   = 'UL'
NR_BW    = 100       #MHz
NR_SubSp = 120       #kHz
NR_RB    = 100       #RB
NR_RBO   = 0         #RB Offset
NR_Mod   = 'QAM64'   #QPSK; QAM16; QAM64; QAM256; PITB

##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.SMW_5GNR_K144 import VSG
from rssd.FSW_5GNR_K144 import VSA
from rssd.FileIO        import FileIO
import time

OFile = FileIO().makeFile(__file__)
SMW = VSG().jav_Open(SMW_IP,OFile)  #Create SMW Object
FSW = VSA().jav_Open(FSW_IP,OFile)  #Create FSW Object

##########################################################
### Instrument Settings
##########################################################
try:
   SMW.Set_Freq(Freq)
   Set_5GNR_BBState(0)
   SMW.Set_5GNR_Direction(NR_Dir)
   SMW.Set_5GNR_ChannelBW(NR_BW)
   SMW.Set_5GNR_SubSpace(NR_SubSp)
   SMW.Set_5GNR_ResBlock(NR_RB)
   SMW.Set_5GNR_ResBlockOffset(NR_RBO)
   SMW.Set_5GNR_Modulation(NR_Mod)
   SMW.Set_5GNR_BBState(1)
   SMW.Set_RFPwr(SWM_Out)                   #Output Power
   SMW.Set_RFState('ON')                     #Turn RF Output on
except:
   pass

if 1:
   FSW.Init_5GNR()
   FSW.Set_Freq(Freq)
   FSW.Set_5GNR_Direction(NR_Dir)
   FSW.Set_5GNR_ChannelBW(NR_BW)
   FSW.Set_5GNR_BWP_SubSpace(NR_SubSp)
#  FSW.Set_5GNR_ResBlock(NR_RB)
#  FSW.Set_5GNR_ResBlockOffset(NR_RBO)
   FSW.Set_5GNR_BWP_Ch_Modulation(NR_Mod) 

EVM = FSW.Get_5GNR_EVM()
OFile.write("%d,%s"%(Freq,EVM))

SMW.jav_ClrErr()                         #Clear Errors
FSW.jav_ClrErr()                         #Clear Errors
