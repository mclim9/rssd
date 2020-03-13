###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : 5G NR Carrier Aggregation Example
### Author : mclim
### Date   : 2020.03.12
###
###############################################################################
### User Entry
###############################################################################
SMW_IP      = '172.24.225.230'
FSW_IP      = '172.24.225.232'
FreqArry    = [28e9, 20e9]
pwrArry     = range(0,8,2)        #Power Array
NR_Dir      = 'UL'
waveparam   = [[100,120,66,'QPSK']]        #ChBW, SubSp, RB
            #   [100,120,66]]       #ChBW, SubSp, RB
            #   [200,60,264],       #ChBW, SubSp, RB
            #   [200,120,132],      #ChBW, SubSp, RB
            #   [400,120,264]]      #ChBW, SubSp, RB
NumCC       = 4
CCSpace     = 99.96e6
CCStart     = (1 - NumCC) * (CCSpace/2)
numMeas     = 1
DFT_S_OFDM  = 'OFF'

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
from datetime                   import datetime     #pylint: disable=E0611,E0401
from rssd.FileIO                import FileIO       #pylint: disable=E0611,E0401
from rssd.VST.NR5G_K144         import VST          #pylint: disable=E0611,E0401
import timeit
import ctypes                                   # An included library with Python install
OFile = FileIO().makeFile(__file__)

###############################################################################
### Code Start
###############################################################################
NR5G = VST().jav_Open(SMW_IP,FSW_IP,OFile)
NR5G.NR_TF      = DFT_S_OFDM
NR5G.NR_Dir     = NR_Dir
NR5G.Freq       = FreqArry[0]

###############################################################################
### Measure Time
###############################################################################
LoopParam   = 'Iter,Model,Freq,Pwr,CC'
WaveParam   = 'ChBW,SubSp,RB,Mod,TF'
SwpParam    = NR5G.FSW.Get_Params_Sweep(1)
AttnParam   = NR5G.FSW.Get_Params_Amp(1)
EVMParam    = NR5G.FSW.Get_5GNR_Params_EVM(1)
TimeParam   = 'AlTime,MeasTime,TotalTIme'
Header      = f'{LoopParam},{WaveParam},{AttnParam},{EVMParam},{TimeParam}'
OFile.write(Header)

NR5G.FSW.Init_5GNR()
NR5G.FSW.Set_5GNR_EVMUnit('DB')
NR5G.FSW.Set_Trig1_Source('IMM')
NR5G.FSW.Set_5GNR_Direction(NR_Dir)
NR5G.FSW.Set_SweepCont(0)
NR5G.FSW.Set_5GNR_FreqRange(2)
NR5G.FSW.Set_5GNR_CA_Num(NumCC)
NR5G.FSW.Set_5GNR_SubFrameCount(1)
NR5G.FSW.Set_SweepTime(10.1e-3)
NR5G.FSW.Set_5GNR_Result_View('ALL')

for i in range(numMeas):                                            #Loop: Measurements
    for param in waveparam:                                         #Loop: Waveform Parameters
        NR5G.NR_ChBW    = param[0]
        NR5G.NR_SubSp   = param[1]
        NR5G.NR_RB      = param[2]
        NR5G.NR_Mod     = param[3]
        for freq  in FreqArry:                                      #Loop: Frequency
            NR5G.Freq   = freq
            NR5G.SMW.Set_Freq(freq)
            NR5G.FSW.write(f':SENS:FREQ:CENT:CC1 {freq + CCStart}')
            for i in range(NumCC):
                NR5G.FSW.cc = i+1
                NR5G.FSW.Set_5GNR_CA_Offset(i+1,i*CCSpace)
                NR5G.FSW.Set_5GNR_PhaseCompensate('OFF')
                NR5G.FSW.Set_5GNR_CellID(i)
                NR5G.FSW.Set_5GNR_BWP_SubSpace(120)
            # NR5G.Set_5GNR_All()                                     #[[[Make Waveform]]]
            print(f'Freq:{freq:.0f} RFBW:{NR5G.NR_ChBW} SubC:{NR5G.NR_SubSp} Mod:{NR5G.NR_Mod}')
            print(Header)
            #ctypes.windll.user32.MessageBoxW(0, "Verify", "Please Verify Waveform", 1)
            for pwr in pwrArry:                                     #Loop: Power
                NR5G.FSW.Init_5GNR()
                tick = timeit.default_timer()
                NR5G.SMW.Set_RFPwr(pwr)
                NR5G.FSW.Set_SweepCont(1)
                # NR5G.FSW.Set_Autolevel()                            # AUTO LEVEL
                tockA = timeit.default_timer()                      #TickAL
                NR5G.FSW.Set_SweepCont(0)
                NR5G.FSW.Set_InitImm()
                tockB    = timeit.default_timer()
                ALTime   = (tockA-tick)
                TotTime  = (tockB-tick)
                TestTime = TotTime - ALTime
                for CC in range(NumCC):                             #Loop: CC
                    NR5G.FSW.cc = CC+1
                    ##############################################################
                    ### LOG DATA
                    ##############################################################
                    LoopParam   = f'{i},{NR5G.FSW.Model},{freq:.0f},{pwr:3d},{NR5G.FSW.cc}'
                    NR5GParam   = f'{NR5G.NR_ChBW},{NR5G.NR_RB},{NR5G.NR_SubSp},{NR5G.NR_Mod},{NR5G.NR_TF}'
                    # AttnParam   = NR5G.FSW.Get_Params_Amp()
                    AttnParam   = '9999,9999,9999'
                    EVM         = NR5G.FSW.Get_5GNR_Params_EVM()
                    TimeParam   = f'{ALTime:2,.6f},{TestTime:2,.6f},{TotTime:2,.6f}'
                    OutStr      = f'{LoopParam},{NR5GParam},{AttnParam},{EVM},{TimeParam}'
                    OFile.write (OutStr)

###############################################################################
### Cleanup Automation
###############################################################################
NR5G.jav_Close()