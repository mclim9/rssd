"""5G NR FSW/SMW Carrier Aggregation Setup Example"""
###############################################################################
### User Entry
###############################################################################
SMW_IP      = '192.168.58.114'
FSW_IP      = '192.168.58.109'
FreqArry    = range(9500000000, 12900000000, 50000000)
pwrArry     = [-5]                              #Power Array
NR_Dir      = 'UL'
waveparam   = [[100,120,66,'QPSK']]                #ChBW, SubSp, RB, Mod
NumCC       = 14
CCSpace     = 99.96e6
CCStart     = (1 - NumCC) * (CCSpace/2)
numMeas     = 1
DFT_S_OFDM  = 'ON'

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
import timeit
from rssd.FileIO                import FileIO       #pylint: disable=E0611,E0401
from rssd.VST.NR5G_K144         import VST          #pylint: disable=E0611,E0401
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
LoopParam   = 'Iter,Model,SMW_Fre,CCFreq_GHz,SMW_Pwr,CC,NumCC'
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
NR5G.FSW.Set_5GNR_CC_Num(NumCC)
NR5G.FSW.Set_5GNR_SubFrameCount(10)
NR5G.FSW.Set_SweepTime(10.1e-3)
NR5G.FSW.Set_5GNR_Result_View('ALL')

for i in range(numMeas):                                            #LOOP: Measurements
    for param in waveparam:                                         #LOOP: Waveform Parameters
        NR5G.NR_ChBW    = param[0]
        NR5G.NR_SubSp   = param[1]
        NR5G.NR_RB      = param[2]
        NR5G.NR_Mod     = param[3]
        for freq  in FreqArry:                                      #LOOP: Frequency
            NR5G.Freq   = freq
            NR5G.SMW.Set_Freq(freq)
            NR5G.FSW.Set_Freq(freq + CCStart)
            print(f'Freq:{freq:.0f} RFBW:{NR5G.NR_ChBW} SubC:{NR5G.NR_SubSp} Mod:{NR5G.NR_Mod}')
            print(Header)
            for CC in range(NumCC):
                NR5G.FSW.cc = CC+1
                NR5G.FSW.Set_5GNR_CC_Offset(CC+1,CC*CCSpace)
            for pwr in pwrArry:                                     #LOOP: Power
                tick = timeit.default_timer()                       #Tick Begin meas
                NR5G.SMW.Set_RFPwr(pwr)
                NR5G.FSW.Set_5GNR_CC_Capture('AUTO')
                NR5G.FSW.Set_SweepCont(1)
                NR5G.FSW.Set_Autolevel()
                NR5G.FSW.Set_5GNR_CC_Capture('SING')
                tockA = timeit.default_timer()                      #Tick Auto Lev
                NR5G.FSW.Set_SweepCont(0)
                NR5G.FSW.Set_InitImm()
                tockB    = timeit.default_timer()                   #Tick Meas
                ALTime   = (tockA-tick)
                TotTime  = (tockB-tick)
                TestTime = TotTime - ALTime

                ##############################################################
                ### LOG DATA
                ##############################################################
                for CC in range(NumCC):                             #LOOP: CC
                    NR5G.FSW.cc = CC+1
                    CurrFreq    = NR5G.FSW.Get_5GNR_CC_Freq()
                    LoopParam   = f'{i},{NR5G.FSW.Model},{freq},{CurrFreq/1e9:9.6f},{pwr:3d},{NR5G.FSW.cc},{NumCC}'
                    NR5GParam   = f'{NR5G.NR_ChBW},{NR5G.NR_RB},{NR5G.NR_SubSp},{NR5G.NR_Mod},{NR5G.NR_TF}'
                    AttnParam   = NR5G.FSW.Get_Params_Amp()
                    EVM         = NR5G.FSW.Get_5GNR_Params_EVM()
                    TimeParam   = f'{ALTime:2,.3f},{TestTime:2,.3f},{TotTime:2,.3f}'
                    OutStr      = f'{LoopParam},{NR5GParam},{AttnParam},{EVM},{TimeParam}'
                    OFile.write(OutStr)

###############################################################################
### Cleanup Automation
###############################################################################
NR5G.jav_Close()
