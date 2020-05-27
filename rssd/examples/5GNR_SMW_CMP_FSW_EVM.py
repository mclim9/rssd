###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Date   : mclim.2020.05.12
###############################################################################
SMW_IP      = '192.168.1.114'
FSW_IP      = '192.168.1.109'
CMP_IP      = '192.168.1.160'
UserDir     = '2020.05.12-CMPEval'
FSW_Rx      = True
freqArry    = [24.250e9, 26e9, 28e9, 39e9]
pwrArry     = range(-40,10,1)                                       #Power Array
comment     = '-autoEVM-SMW-IQ'

###############################################################################
### Overhead
###############################################################################
from rssd.VSG.NR5G_K144     import VSG                              #pylint: disable=E0611,E0401
from rssd.VSA.NR5G_K144     import VSA                              #pylint: disable=E0611,E0401
from rssd.RCT.NR5G_KM601    import RCT                              #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO                           #pylint: disable=E0611,E0401
from rssd.RSI.time          import timer                            #pylint: disable=E0611,E0401

OFile = FileIO().makeFile(__file__)
TMR = timer()
SMW = VSG().jav_Open(SMW_IP,OFile)                                  #Create SMW Object
if FSW_Rx:
    FSW = VSA().jav_Open(FSW_IP,OFile)                              #Create FSW Object
else:
    RCT().jav_Close()
    CMP = RCT().jav_Open(CMP_IP,OFile)                              #Create CMP Object

class dataClass():
    def __init__(self):
        self.Direction      = 'UL'
        self.CellID         = 1
        # self.FreqRng      = 'HIGH'
        self.ChBW           = 100
        self.TF             = 'ON'
        self.SubSp          = 120
        self.RB             = 60
        self.RBO            = 0
        self.Ch_RB          = 60
        self.Ch_RBO         = 0
        self.Mod            = 'QPSK'

def ReadSMW_Settings(NR5G):
    # NR5G.freq         = SMW.Get_Freq()
    NR5G.Direction      = SMW.Get_5GNR_Direction()
    NR5G.CellID         = SMW.Get_5GNR_BWP_CellID()
    SMW.subF            = 1
    # NR5G.FreqRng      = SMW.Get_5GNR_FreqRange()
    NR5G.ChBW           = SMW.Get_5GNR_ChannelBW()
    NR5G.TF             = SMW.Get_5GNR_TransPrecoding()
    NR5G.SubSp          = SMW.Get_5GNR_BWP_SubSpace()
    NR5G.RB             = SMW.Get_5GNR_BWP_ResBlock()
    NR5G.RBO            = SMW.Get_5GNR_BWP_ResBlockOffset()
    NR5G.Ch_RB          = SMW.Get_5GNR_BWP_Ch_ResBlock()
    NR5G.Ch_RBO         = SMW.Get_5GNR_BWP_Ch_ResBlockOffset()
    # NR5G.Ch_DMRS_Config  = SMW.Get_5GNR_BWP_Ch_DMRS_Config()
    # NR5G.Ch_DMRS_1st     = SMW.Get_5GNR_BWP_Ch_DMRS_1stDMRSSym()
    # NR5G.Ch_DMRS_AddPost = SMW.Get_5GNR_BWP_Ch_DMRS_AddPosition()
    # NR5G.Ch_DMRS_Mapping = SMW.Get_5GNR_BWP_Ch_DMRS_Mapping()
    # NR5G.Ch_DMRS_MSymbL  = SMW.Get_5GNR_BWP_Ch_DMRS_MSymbLen()
    # NR5G.Ch_DMRS_RelPwr  = SMW.Get_5GNR_BWP_Ch_DMRS_RelPwr()
    # NR5G.Ch_DMRS_SGMeth  = SMW.Get_5GNR_BWP_Ch_DMRS_SeqGenMeth()
    # NR5G.Ch_DMRS_SGSeed  = SMW.Get_5GNR_BWP_Ch_DMRS_SeqGenSeed()
    NR5G.Mod            = SMW.Get_5GNR_BWP_Ch_Modulation()
    return NR5G

def NR5G_Rx_Init():
    """Start 5GNR Measurement Channel"""
    if FSW_Rx:
        FSW.Init_5GNR()
        FSW.Set_5GNR_FrameCount('OFF')
    else:
        CMP.Init_5GNR()

def NR5G_Rx_Config(sSetting):
    if FSW_Rx:
        sSetting = sSetting.split('.nr5g')[0]
        FSW.Set_5GNR_AllocFile(f'C:\\R_S\\instr\\user\\Demo\\2020.05-CMPEval\\{sSetting}.allocation')
        FSW.Set_5GNR_FrameCount('OFF')
        FSW.Set_Trig1_Source('EXT')
        FSW.Set_SweepTime(3e-3)
        FSW.Set_5GNR_SubFrameCount(16)
        NR5G.Rx = FSW.Model + comment
    else:
        CMP.Init_5GNR()
        CMP.Set_5GNR_Path('P1.RRH.RF1')
        CMP.Set_Meas_Port('P1.RRH.RF1')
        CMP.write(f'CONF:NRMM:MEAS:ULDL:PER MS2')
        CMP.write(f'CONF:NRMM:MEAS:ULDL:PATT S120k, 0,0,8,0')                               #DL Slot; DL Sym; UL SLot; UL Sym
        CMP.write(f'CONF:NRMM:MEAS:ULDL:PATT S60k,  0,0,1,0')                               #DL Slot; DL Sym; UL SLot; UL Sym
        CMP.Set_5GNR_ChannelBW(100)
        CMP.Set_5GNR_CellID(NR5G.CellID)
        CMP.Set_5GNR_BWP_Ch_DMRS_1stDMRSSym(2)
        # CMP.Set_5GNR_NumBWP()
        CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:BWP BWP0, S120K, NORM, {NR5G.RB}, {NR5G.RBO}')#SCS; NORM; RB; RBO
        CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:BWP:PUSC:DMTA BWP0, 1, 2, 1')                 #Config; AddPos; MaxLength
        CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:BWP:PUSC:DMTB BWP0, 1, 2, 1')                 #Config; AddPos; MaxLength
        CMP.Set_5GNR_TransPrecoding(NR5G.TF)
        CMP.Set_5GNR_PUSCH(NR5G.Ch_RB, NR5G.Ch_RBO, NR5G.Mod)
        # CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:ALL{CMP.alloc}:PUSC A, 14, 0, {NR5G.Ch_RB}, {NR5G.Ch_RBO}, {mod}')   #Map; Sym; SymStrt; RB; RBO; Mod
        CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:ALL{CMP.alloc}:PUSC:ADD 1, 2, 3, 0')          #Len; CDM; Pwr; Ant
        CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:ALL{CMP.alloc}:PUSC:SGEN CID, 0, 0')          #SeqType; DMRSID; N_SCID
        CMP.write(f'CONF:NRMM:MEAS:MEV:MOEX')
        CMP.Set_5GNR_EVM_AvgCount(10)
        CMP.Set_5GNR_Trigger_Source('Free Run (Fast Sync)')
        NR5G.Rx = CMP.Model + comment

def NR5G_Rx_SetFreq(freq):
    if FSW_Rx:
        FSW.Set_Freq(freq)
        FSW.Set_5GNR_PhaseCompensate_Freq(freq)
    else:
        CMP.Set_5GNR_Freq(freq)
        CMP.Set_Meas_Freq(freq)
        CMP.Set_5GNR_PhaseCompensate_Freq(freq)

def NR5G_Rx_SetLevel(NR5G):
    if FSW_Rx:
        # FSW.Set_SweepCont(1)
        # FSW.Set_Autolevel()
        FSW.Set_5GNR_AutoEVM()
    else:
        CF  = SMW.Get_CrestFactor()
        CMP.Init_Meas_Power()
        CMP.Set_Meas_UserMargin(CF)
        CMP.Set_Meas_Expected_Nom_Power(NR5G.pwr)
        CMP.Set_Meas_TriggerSource('IF Power')
        # CMP.Set_Meas_TriggerThreshold(NR5G.pwr)
        CMP.Set_Meas_TriggerThreshold(-40)
        CMP.Set_Meas_Pwr_MLength(100e-6)
        CMP.Set_Meas_RFBW(100e6)
        Pwr = CMP.Get_Meas_Power()
        CMP.Set_5GNR_ExpPwr(Pwr)
        CMP.Set_5GNR_UserMargin(CF)

def NR5G_Rx_Get_EVM():
    if FSW_Rx:
        FSW.Set_SweepCont(0)
        FSW.Set_InitImm()
        EVM = FSW.Get_5GNR_Params_EVM()
    else:
        EVM = CMP.Get_5GNR_Params_EVM()
    return EVM

###############################################################################
### Code Start
###############################################################################
LoopParam   = 'State,Model,SMW_Fre,SMW_Pwr'
WaveParam   = 'ChBW,SubSp,RB,Mod,TF'
AttnParam   = FSW.Get_Params_Amp(1) if FSW_Rx else CMP.Get_5GNR_Params_Amp(1)
EVMParam    = FSW.Get_5GNR_Params_EVM(1) if FSW_Rx else CMP.Get_5GNR_Params_EVM(1)
TimeParam   = 'AlTime,MeasTime,TotalTIme'
Header      = f'{LoopParam},{AttnParam},{EVMParam},{TimeParam}'
OFile.write(Header)

### Instr Init
NR5G        = dataClass()
SMW.Set_OS_Dir(UserDir)
saveArry = SMW.Get_OS_FileList('savrcltxt')
saveArry = SMW.Get_OS_FileList('nr5g')
NR5G_Rx_Init()

for saveState in saveArry:
    SMW.Set_5GNR_Setting_Load(f'{UserDir}/{saveState}')
    ReadSMW_Settings(NR5G)
    NR5G_Rx_Config(saveState)
    for freq in freqArry:
        SMW.Set_Freq(freq)
        SMW.Set_5GNR_PhaseCompensate_Freq(freq)
        NR5G_Rx_SetFreq(freq)
        for pwr in pwrArry:
            SMW.Set_RFPwr(pwr)
            SMW.jav_OPC_Wait(':CAL1:IQM:LOC?')
            NR5G.pwr = pwr
            TMR.start()
            NR5G_Rx_SetLevel(NR5G)
            TMR.tick()
            EVM      = NR5G_Rx_Get_EVM()
            TMR.tick()

            ### Log Data
            LoopParam   = f'{saveState},{NR5G.Rx},{freq},{pwr:3d}'
            # NR5GParam   = f'{NR5G.ChBW},{NR5G.RB},{NR5G.SubSp},{NR5G.Mod},{NR5G.TF}'
            AttnParam   = FSW.Get_Params_Amp() if FSW_Rx else CMP.Get_5GNR_Params_Amp(0)
            TimeParam   = TMR.deltaTimeTxt()
            OutStr      = f'{LoopParam},{AttnParam},{EVM},{TimeParam}'
            OFile.write(OutStr)


