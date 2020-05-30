########################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: CMP200A Example
### Author:  mclim
### Date:    2019.09.09
########################################################################
### User Entry
########################################################################
CMP_IP      = '192.168.1.160'                   #IP Address
FSW_IP      = '192.168.1.109'                   #IP Address
FreqArry    = [6e9,10e9,14e9,20e9]
FreqArry    = [24.5e9,26e9,28e9,31e9]
FreqArry    = [37.5e9,38.5e9,40e9,43.4e9]
pwrArry     = range(-50,8,2)                    #Power Array
# modArry     = ['QAM64']                       #QPSK; QAM16; QAM64; QAM256;
waveparam   = [[100,60,132,'QPSK']]             #ChBW, SubSp, RB, Modulation
numMeas     = 1
########################################################################
### Code Overhead: Import and create objects
########################################################################
# import math
from datetime               import datetime     #pylint: disable=E0611,E0401
from rssd.RCT.GPRF          import RCT          #pylint: disable=E0611,E0401
from rssd.VSA.NR5G_K144     import VSA          #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO       #pylint: disable=E0611,E0401

OFile = FileIO().makeFile(__file__)
OFile.write("")
class vari:
    def __init__(self):
        self.NR_ChBW    = 0
        self.NR_SubSp   = 0
        self.NR_RB      = 0
        self.NR_Mod     = ''
        self.NR_TF      = "off"
NR5G = vari()

########################################################################
### Code Start
########################################################################
CMP = RCT()
FSW = VSA()
CMP.jav_Open(CMP_IP,OFile)
FSW.jav_Open(FSW_IP,OFile)

CMP.query('*IDN?')
FSW.write(':UNIT:EVM DB')
FSW.Set_SweepCont(0)
##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
Header = 'Iter,Model,Freq,EVM,ChBW,UL-TP,SubSp,Mod,SMWPwr,Attn,Preamp,RefLvl,StepTime'
OFile.write(Header)

for i in range(numMeas):                                            #Loop: Repeatability
    for param in waveparam:                                         #Loop: Waveform Parameters
        NR5G.NR_ChBW    = param[0]
        NR5G.NR_SubSp   = param[1]
        NR5G.NR_RB      = param[2]
        NR5G.NR_Mod     = param[3]
        CMP.Init_Gen()
        for freq  in FreqArry:                                      #Loop: Frequency
            print(f'Freq:{freq:.0f} RFBW:{NR5G.NR_ChBW} SubC:{NR5G.NR_SubSp} Mod:{NR5G.NR_Mod}')
            FSW.Set_Freq(freq)
            CMP.Set_Gen_Freq(freq)
            print(Header)
            for pwr in pwrArry:                                     #Loop: Power
                FSW.Set_Autolevel()
                CMP.Set_Gen_RFPwr(pwr)
                tick = datetime.now()                               #Tick
                FSW.Set_InitImm()
                evm     = FSW.Get_5GNR_EVM()
                attn    = FSW.Get_AmpSettings()
                s = datetime.now() - tick                          #Total test time
                OutStr = f'{i},{CMP.Model},{freq:.0f},{evm},{NR5G.NR_ChBW},{NR5G.NR_TF},{NR5G.NR_SubSp},{NR5G.NR_Mod},{pwr:3d},{attn},{s.seconds:3d}.{s.microseconds:06d}'
                OFile.write (OutStr)
            #end PwrLoop
        #end FreqLoop
    #end ParamLoop
#end repeatabilityLoop
CMP.jav_ClrErr()                                                    #Clear Errors
