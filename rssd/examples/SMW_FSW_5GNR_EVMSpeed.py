##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date : 2018.05.24
### Steps  : 
###
##########################################################
### User Entry
##########################################################
import os
BaseDir 	= os.path.dirname(os.path.realpath(__file__))
OutFile 	= BaseDir + "\\data\\" + __file__

SMW_IP  	= '192.168.1.114'
FSW_IP  	= '192.168.1.109'
ChBW 		= 100
SubSp		= 60
Mod		= 'QAM256'		#QPSK; QAM16; QAM64; QAM256; PITB

##########################################################
### Code Overhead
##########################################################
from    rssd.SMW_5GNR_K144	import VSG
from    rssd.FSW_5GNR_K144	import VSA
from    datetime				import datetime
import  rssd.FileIO

f = rssd.FileIO.FileIO()
OFile = f.Init(OutFile)
SMW = VSG()                         #Create SMW Object
FSW = VSA()                         #Create FSW Object
SMW.jav_Open(SMW_IP,f.sFName)       #Connect to SMW
FSW.jav_Open(FSW_IP,f.sFName)       #Connect to FSW
if 0:
   SMW.jav_logSCPI()
   FSW.jav_logSCPI()
   
#FSW.jav_Reset()
FSW.Init_5GNR()								#FSW 5G NR Channel
FSW.Set_Freq(19e9)
FSW.Set_5GNR_Direction('UL')				#UL or DL
FSW.Set_5GNR_FreqRange('HIGH')			#LOW:<3GHz MIDD:3-6GHz HIGH:>6GHz
FSW.Set_5GNR_ChannelBW(ChBW)				#MHz
FSW.Set_5GNR_BWP_SubSpace(SubSp)			#kHz
#  FSW.Set_5GNR_ResBlock(NR_RB)
#  FSW.Set_5GNR_ResBlockOffset(NR_RBO)
FSW.Set_5GNR_BWP_Slot_Modulation(Mod) 	#QPSK; QAM16; QAM64; QAM256; PITB

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
FSW.Set_SweepCont(0)
OFile.write('EVM,ChBW,SubSp,Mod,Iter,CmdTime')

for i in range(10):
   tick = datetime.now()
   FSW.Set_InitImm()
   EVM = FSW.Get_5GNR_EVM()
   tock = datetime.now()
   d = tock - tick
   OutStr = '%f,%d,%d,%s,%2d,%3d.%d'%(EVM,ChBW,SubSp,Mod,i,d.seconds,d.microseconds)
   OFile.write (OutStr)
   
##########################################################
### Cleanup Automation
##########################################################
SMW.jav_Close()
FSW.jav_Close()
