##########################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date   : 2018.05.24
##########################################################
### User Entry
##########################################################
FSW_IP   = '192.168.1.109'
Freq     = 28e9
ChBW     = 100
numMeas  = 10

##########################################################
### Code Overhead: Import and create objects
##########################################################
# from datetime              import datetime
from rssd.VSA.NR5G_K144    import VSA
from rssd.FileIO           import FileIO

OFile = FileIO().makeFile(__file__)
FSW = VSA().jav_Open(FSW_IP,OFile)  #Create FSW Object

##########################################################
### Code Start
##########################################################

#FSW.jav_Reset()
FSW.Init_5GNR_SEM()                 #FSW 5G NR Channel
FSW.Set_Freq(Freq)
FSW.Set_5GNR_Direction('DL')        #UL or DL
FSW.Set_5GNR_SEM_SubBlockNum(3)
FSW.Set_5GNR_FreqRange('HIGH')      #LOW:<3GHz MIDD:3-6GHz HIGH:>6GHz
FSW.Set_5GNR_ChannelBW(ChBW)        #MHz

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('asdf')
FSW.Set_SweepCont(0)

##########################################################
### Cleanup Automation
##########################################################
FSW.jav_Close()
