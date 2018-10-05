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
BaseDir  = os.path.dirname(os.path.realpath(__file__))
OutFile  = BaseDir + "\\" + __file__

SMW_IP   = '192.168.1.114'
FSW_IP   = '192.168.1.109'
Freq     = 28e9
ChBW     = 100
subCarr  = [60, 120]
modArry  = ['QPSK', 'QAM64'] #QPSK; QAM16; QAM64; QAM256; PITB
numMeas  = 10

##########################################################
### Code Overhead
##########################################################
from    rssd.SMW_5GNR_K144 import VSG
from    rssd.FSW_5GNR_K144 import VSA
from    datetime           import datetime
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

SMW.Set_Freq(Freq)
SMW.Set_5GNR_Direction('UL')        #UL or DL
FSW.Set_5GNR_FreqRange('HIGH')      #LOW:<3GHz MIDD:3-6GHz HIGH:>6GHz
SMW.Set_RFPwr(-2)                    #Output Power
SMW.Set_RFState('ON')               #Turn RF Output on

#FSW.jav_Reset()
FSW.Init_5GNR()                     #FSW 5G NR Channel
FSW.Set_Freq(Freq)
FSW.Set_5GNR_Direction('UL')        #UL or DL
FSW.Set_5GNR_FreqRange('HIGH')      #LOW:<3GHz MIDD:3-6GHz HIGH:>6GHz
FSW.Set_5GNR_ChannelBW(ChBW)        #MHz
FSW.Set_Trig1_Source('EXT')
#FSW.Set_5GNR_ResBlock(NR_RB)
#FSW.Set_5GNR_ResBlockOffset(NR_RBO)

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('EVM,ChBW,SubSp,Mod,SubFram,Iter,CmdTime')
FSW.Set_SweepCont(0)

for mod in modArry:
   for subC in subCarr:
      SMW.Set_5GNR_BBState(0)
      SMW.Set_5GNR_BWP_SubSpace(subC)        #kHz
      FSW.Set_5GNR_BWP_SubSpace(subC)        #kHz
      SMW.Set_5GNR_BWP_Slot_Modulation(mod)  #QPSK; QAM16; QAM64; QAM256; PITB
      FSW.Set_5GNR_BWP_Slot_Modulation(mod)  #QPSK; QAM16; QAM64; QAM256; PITB
      SMW.Set_5GNR_BBState(1)
      print('SubC:%d %s'%(subC,mod))
      FSW.Set_InitImm()
      if 1:
         name = input("Verify EVM on FSW? ")
         FSW.Set_DisplayUpdate(0)
         FSW.Set_SweepCont(0)
      for subFram in [1,2,3,5,10]:
         FSW.Set_SweepTime((subFram)*1.1e-3)
         FSW.Set_5GNR_SubFrameCount(subFram)
         FSW.Set_InitImm()
         for i in range(numMeas):
            tick = datetime.now()
            FSW.Set_InitImm()
            EVM = FSW.Get_5GNR_EVM()
            d = datetime.now() - tick
            OutStr = '%f,%d,%d,%s,%d,%2d,%3d.%06d'%(EVM,ChBW,subC,mod,subFram,i,d.seconds,d.microseconds)
            OFile.write (OutStr)
   
##########################################################
### Cleanup Automation
##########################################################
SMW.jav_Close()
FSW.jav_Close()
