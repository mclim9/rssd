###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Capture EVM based on SMW *.nr5G & FSW *.allocation files
#pylint: disable=E0611,E0401
###############################################################################
SMW_IP      = '192.168.1.114'
FSW_IP      = '192.168.1.109'
UserDir     = '2020.07.30-Autolevel'
freqArry    = [28e9]
pwrArry     = range(-50,10,2)                               #Power Array
comment     = '-Autolevel'

###############################################################################
### Overhead
###############################################################################
from rssd.VSG.NR5G_K144     import VSG
from rssd.VSA.NR5G_K144     import VSA
from rssd.FileIO            import FileIO
from rssd.RSI.time          import timer

OFile = FileIO().makeFile(__file__)
TMR = timer()
SMW = VSG().jav_Open(SMW_IP,OFile)                          #Create SMW Object
SMW.debug = 0
FSW = VSA().jav_Open(FSW_IP,OFile)                          #Create FSW Object
FSW.debug = 0

class dataClass():
    def __init__(self):
#         self.Direction      = 'UL'
#         self.CellID         = 1
#         # self.FreqRng      = 'HIGH'
#         self.ChBW           = 100
#         self.TF             = 'ON'
#         self.SubSp          = 120
#         self.RB             = 60
#         self.RBO            = 0
#         self.Ch_RB          = 60
#         self.Ch_RBO         = 0
#         self.Mod            = 'QPSK'
        self.Rx             = ''
#         self.pwr            = -100

def NR5G_Rx_Init():
    """Start 5GNR Measurement Channel"""
    FSW.Init_5GNR()
    FSW.Set_5GNR_FrameCount('OFF')

def NR5G_Rx_Config(sSetting):
    sSetting = sSetting.split('.nr5g')[0]
    FSW.Set_5GNR_AllocFile(f'C:\\R_S\\instr\\user\\Demo\\{UserDir}\\{sSetting}.allocation')
    FSW.Set_5GNR_FrameCount('OFF')
    FSW.Set_Trig1_Source('EXT')
    FSW.Set_SweepTime(3e-3)
    FSW.Set_5GNR_SubFrameCount(16)
    NR5G.Rx = FSW.Model + comment

def NR5G_Rx_SetFreq(freq):
    FSW.Set_Freq(freq)
    FSW.Set_5GNR_PhaseCompensate_Freq(freq)

def NR5G_Rx_SetLevel():
    FSW.Set_SweepCont(1)
    FSW.Set_Autolevel()
    # FSW.Set_5GNR_AutoEVM()

def NR5G_Rx_Get_EVM():
    FSW.Set_SweepCont(0)
    FSW.Set_InitImm()
    EVM = FSW.Get_5GNR_Params_EVM()
    return EVM

###############################################################################
### Code Start
###############################################################################
LoopParam   = 'State,Model,SMW_Fre,SMW_Pwr'
# WaveParam   = 'ChBW,SubSp,RB,Mod,TF'
AttnParam   = FSW.Get_Params_Amp(1)
EVMParam    = FSW.Get_5GNR_Params_EVM(1)
TimeParam   = 'AlTime,MeasTime,TotalTime,HoursLeft'
Header      = f'{LoopParam},{AttnParam},{EVMParam},{TimeParam}'
OFile.write(Header)

### Instr Init
NR5G        = dataClass()
SMW.Set_OS_Dir(UserDir)
SMW.Set_5GNR_BBState(1)
SMW.Set_RFPwr(-50)
SMW.Set_RFState(1)
saveArry = SMW.Get_OS_FileList('savrcltxt')
saveArry = SMW.Get_OS_FileList('nr5g')
NR5G_Rx_Init()

TMR.numTest = len(saveArry) * len(freqArry) * len(pwrArry)
TMR.suite_start()
for saveState in saveArry:
    SMW.Set_5GNR_Setting_Load(f'{UserDir}/{saveState}')
    NR5G_Rx_Config(saveState)
    for freq in freqArry:
        SMW.Set_Freq(freq)
        SMW.Set_5GNR_PhaseCompensate_Freq(freq)
        NR5G_Rx_SetFreq(freq)
        for pwr in pwrArry:
            TMR.start()
            SMW.Set_RFPwr(pwr)
            # SMW.Set_OptimizeAll()
            # NR5G.pwr = pwr
            NR5G_Rx_SetLevel()
            TMR.tick()
            EVM = NR5G_Rx_Get_EVM()
            TMR.tick()

            ### Log Data
            LoopParam   = f'{saveState},{NR5G.Rx},{freq},{pwr:3d}'
            AttnParam   = FSW.Get_Params_Amp()
            TimeParam   = TMR.Get_Params_Time()
            OutStr      = f'{LoopParam},{AttnParam},{EVM},{TimeParam}'
            OFile.write(OutStr)
SMW.Set_RFPwr(-100)
