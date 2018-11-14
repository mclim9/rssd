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

class NR(object):
   def __init__(self):
      self.Freq     = 19e9
      self.SWM_Out  = 0
      self.NR_Dir   = 'DL'
      self.NR_Deploy= 'HIGH'    #LOW:MIDD:HIGH
      self.NR_ChBW  = 100       #MHz
      self.NR_SubSp = 120       #kHz
      self.NR_RB    = 66        #RB
      self.NR_RBO   = 0         #RB Offset
      self.NR_Mod   = 'QAM64'   #QPSK; QAM16; QAM64; QAM256; PITB

##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.SMW_5GNR_K144 import VSG
from rssd.FSW_5GNR_K144 import VSA
#from rssd.FileIO        import FileIO
#OFile = FileIO().makeFile(__file__)

##########################################################
### Instrument Settings
##########################################################
def NR5G_SetSettings(FSW,SMW,NR):
   try:
      ### SMW Settings
      SMW.Set_Freq(NR.Freq)
      SMW.Set_5GNR_BBState('OFF')
      SMW.Set_5GNR_Direction(NR.NR_Dir)
      SMW.Set_5GNR_FreqRange(NR.NR_Deploy)
      SMW.Set_5GNR_ChannelBW(NR.NR_ChBW)
      SMW.Set_5GNR_BWP_SubSpace(NR.NR_SubSp)
      SMW.Set_5GNR_BWP_ResBlock(NR.NR_RB)
      #SMW.Set_5GNR_BWP_ResBlockOffset(NR_RBO)
      SMW.Set_5GNR_BWP_Ch_ResBlock(NR.NR_RB)
      SMW.Set_5GNR_BWP_Ch_Modulation(NR.NR_Mod)
      SMW.Set_5GNR_SSB()
      SMW.Set_5GNR_BBState('ON')
      SMW.Set_RFState('ON')                     #Turn RF Output on
      SMW.Set_RFPwr(NR.SWM_Out)                    #Output Power
   except:
      print("NR5G_SetSettings: SMW Error")
      pass

   try:
      ### FSW Setting
      FSW.Set_Freq(NR.Freq)
      FSW.Init_5GNR()
      FSW.Set_5GNR_Direction(NR.NR_Dir)
      FSW.Set_5GNR_FreqRange(NR.NR_Deploy)
      FSW.Set_5GNR_ChannelBW(NR.NR_ChBW)
      FSW.Set_5GNR_BWP_SubSpace(NR.NR_SubSp)
      FSW.Set_5GNR_BWP_ResBlock(NR.NR_RB)
      FSW.Set_5GNR_BWP_Ch_ResBlock(NR.NR_RB)
      FSW.Set_5GNR_BWP_Ch_Modulation(NR.NR_Mod)
      FSW.Set_SweepCont(1)
      FSW.Set_InitImm()
   except:
      print("NR5G_SetSettings: FSW Error")
      pass

   #EVM = FSW.Get_5GNR_EVM()


if __name__ == "__main__":
   SMW = VSG().jav_Open(SMW_IP)              #Create SMW Object
   FSW = VSA().jav_Open(FSW_IP)              #Create FSW Object
   odata = NR5G_SetSettings(FSW,SMW,NR())
   SMW.jav_ClrErr()                          #Clear Errors
   FSW.jav_ClrErr()                          #Clear Errors
   SMW.jav_Close()
   FSW.jav_Close()
