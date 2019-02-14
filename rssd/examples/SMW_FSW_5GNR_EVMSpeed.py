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
SMW_IP   = '192.168.1.114'
FSW_IP   = '192.168.1.109'
subCarr  = [120]
modArry  = ['QPSK', 'QAM64'] #QPSK; QAM16; QAM64; QAM256; PITB
pwrArry  = [-20,-10,-5,0,5]
numMeas  = 1

##########################################################
### Code Overhead: Import and create objects
##########################################################
from datetime           import datetime
from rssd.FileIO        import FileIO
from rssd.VST_5GNR_K144 import VST

OFile = FileIO().makeFile(__file__)

##########################################################
### Code Start
##########################################################
NR5G = VST().jav_Open(SMW_IP,FSW_IP,OFile)
NR5G.NR_Dir  = 'UL'
NR5G.NR_ChBW = 400
NR5G.NR_RB   = 264      #100:060:132  200:060:264  <Not Appli>
                        #100:120:066  200:120:132  400:120:264
NR5G.Freq    = 40e9

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('EVM,ChBW,SubSp,Mod,Pwr,SubFram,Iter,CmdTime')

for mod in modArry:
   for subC in subCarr:
      NR5G.NR_SubSp = subC
      NR5G.NR_Mod   = mod
      NR5G.Set_5GNR_All()              #Create Waveform
      NR5G.FSW.Set_SweepCont(0)
      NR5G.FSW.Set_5GNR_EVMUnit('DB')
      NR5G.FSW.Set_Trig1_Source('EXT')
      print(f'RFBW:{NR5G.NR_ChBW} SubC:{subC} Mod:{mod}')
      for pwr in pwrArry:
         NR5G.SMW.Set_RFPwr(pwr)
         NR5G.FSW.Set_Autolevel()
         for subFram in [10]:
            NR5G.FSW.Set_SweepTime((subFram)*1.1e-3)
            NR5G.FSW.Set_5GNR_SubFrameCount(subFram)
            for i in range(numMeas):
               tick = datetime.now()
               NR5G.FSW.Set_InitImm()
               EVM = NR5G.FSW.Get_5GNR_EVM()
               d = datetime.now() - tick
#               OutStr = '%f,%d,%d,%s,%d,%2d,%3d.%06d'%(EVM,ChBW,subC,mod,subFram,i,d.seconds,d.microseconds)
               OutStr = f'{EVM},{NR5G.NR_ChBW},{subC},{mod},{pwr},{subFram},{i},{d.seconds},{d.microseconds}'
               OFile.write (OutStr)
   
##########################################################
### Cleanup Automation
##########################################################
NR5G.jav_Close()
