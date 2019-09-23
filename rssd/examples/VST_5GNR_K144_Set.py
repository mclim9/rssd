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
SMW_IP   = '192.168.1.114'
FSW_IP   = '192.168.1.109'

##########################################################
### Code Start
##########################################################
from rssd.VST.NR5G_K144 import VST        #pylint: disable=E0611,E0401

def NR5G_SetSettings(FSW,SMW):
   pass


if __name__ == "__main__":
   NR5G = VST().jav_Open(SMW_IP,FSW_IP)
   NR5G.Freq     = 19e9
   NR5G.SWM_Out  = 0
   NR5G.NR_Dir   = 'DL'
   NR5G.NR_Deploy= 'HIGH'    #LOW:MIDD:HIGH
   NR5G.NR_ChBW  = 200       #MHz
   NR5G.NR_SubSp = 120       #kHz
   NR5G.NR_RB    = 66        #RB
   NR5G.NR_RBO   = 0         #RB Offset
   NR5G.NR_Mod   = 'QAM64'   #QPSK; QAM16; QAM64; QAM256; PITB
   NR5G.Set_5GNR_All()
   NR5G.jav_Clear()
   NR5G.jav_Close()