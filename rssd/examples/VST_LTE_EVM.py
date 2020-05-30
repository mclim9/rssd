##########################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date    : 2018.05.24
##########################################################
### User Entry
##########################################################
SMW_IP      = '192.168.1.114'
FSW_IP      = '192.168.1.109'
FreqArry    = [6e9]
pwrArry     = range(-50,8,1)
LTE_Dir     = 'UL'
waveparam   =[[20,100],
              [20,66]]
subFArry    = [1]
modArry     = ['QPSK', 'QAM64'] #QPSK; QAM16; QAM64; QAM256
numMeas     = 1
AutoLvl     = 0                #0:AutoRef 1:AutoLevel
SCFDMA      = 'OFF'

##########################################################
### Code Overhead: Import and create objects
##########################################################
from datetime               import datetime     #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO       #pylint: disable=E0611,E0401
from rssd.VST.LTE           import VST          #pylint: disable=E0611,E0401
# import time
# import ctypes  # An included library with Python install
OFile = FileIO().makeFile(__file__)

##########################################################
### Code Start
##########################################################
LTE = VST().jav_Open(SMW_IP,FSW_IP,OFile)
LTE.LTE_TF     = SCFDMA
LTE.LTE_Dir    = LTE_Dir
LTE.Freq       = FreqArry[0]

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
Header = 'Iter,Model,Freq,K144Crest,K144Pwr,EVM,ChBW,SCFDMA,RB,Mod,SMWPwr,SubFram,Attn,Preamp,RefLvl,AutoLvl,AlTime,CrestF,P10_00,P01_00,P00_10,P00_01,CmdTime,TotTime'
OFile.write(Header)

LTE.FSW.Init_LTE()
LTE.FSW.Set_LTE_EVMUnit('DB')
LTE.FSW.Set_Trig1_Source('EXT')
LTE.FSW.Set_SweepCont(0)
LTE.FSW.Init_CCDF()
LTE.FSW.Set_YIG(0)
LTE.FSW.Set_CCDF_BW(120e6)
LTE.FSW.Set_CCDF_Samples(2e6)
LTE.FSW.Set_Trig1_Source('IMM')
LTE.FSW.Set_AttnAuto()
LTE.FSW.Set_SweepCont(0)

for i in range(numMeas):                                        #Loop: Measurements
    for mod in modArry:                                         #Loop: Modulation
        for param in waveparam:                                 #Loop: Subcarrier
            LTE.LTE_ChBW    = param[0]
            LTE.LTE_Mod     = mod
            LTE.LTE_RB      = param[1]
            for freq  in FreqArry:                              #Loop: Frequency
                LTE.Freq     = FreqArry[0]
                LTE.Set_LTE_All()                             #[[[Make Waveform]]]
                LTE.FSW.Init_CCDF()
                LTE.FSW.Set_InitImm()
                ccdf = LTE.FSW.Get_CCDF()
                print(f'Freq:{freq} RFBW:{LTE.LTE_ChBW} SubC:{LTE.LTE_RB} Mod:{LTE.LTE_Mod}')
                print(Header)
                #ctypes.windll.user32.MessageBoxW(0, "Verify", "Please Verify Waveform", 1)
                for pwr in pwrArry:                             #Loop: Power
                    LTE.SMW.Set_RFPwr(pwr)
                    tickA = datetime.now()
                    if AutoLvl == 1:
                        LTE.FSW.Init_LTE()
                        LTE.FSW.Set_Autolevel()
                    else:
                        LTE.FSW.Set_LTE_AutoRef()
                    ALTime = datetime.now() - tickA
                    for subFram in subFArry:                    #Loop: Subframe
                        LTE.FSW.Set_LTE_SweepTime((subFram)*1.1e-3)
                        LTE.FSW.Set_LTE_SubFrameCount(subFram)
                        tick = datetime.now()
                        LTE.FSW.Init_LTE()
                        LTE.FSW.Set_SweepCont(0)
                        LTE.FSW.Set_InitImm()
                        EVM = LTE.FSW.Get_LTE_EVMParams()
                        Attn = LTE.FSW.Get_AmpSettings()
                        d = datetime.now() - tick       #Measurement only
                        t = datetime.now() - tickA      #Autolevel + Measurement
                        OutStr = f'{i},{LTE.FSW.Model},{freq},{EVM},{LTE.LTE_ChBW},{LTE.LTE_TF},{LTE.LTE_RB},{LTE.LTE_Mod},{pwr:3d},{subFram},{Attn},{AutoLvl},{ALTime.seconds:3d}.{ALTime.microseconds:06d},cf:{ccdf},{d.seconds:3d}.{d.microseconds:06d},{t.seconds:3d}.{t.microseconds:06d}'
                        OFile.write (OutStr)

##########################################################
### Cleanup Automation
##########################################################
LTE.jav_Close()
