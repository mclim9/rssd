###############################################################################
### Record SCPI into file
###############################################################################
from rssd.VSG.NR5G_K144     import VSG                              #pylint: disable=E0611,E0401
from rssd.VSA.NR5G_K144     import VSA                              #pylint: disable=E0611,E0401
from rssd.RCT.NR5G_KM601    import RCT                              #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO                           #pylint: disable=E0611,E0401

CMP  = RCT().jav_Open('192.168.1.160')                              #Create instrument Object
CMP.jav_logscpi()                                                   #Log SCPI to file

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
        self.Rx             = ''
        self.pwr            = -100

###############################################################################
### SCPI Code we want to log
###############################################################################
NR5G = dataClass()
CMP.Init_5GNR()
CMP.Set_5GNR_Path('P1.RRH.RF1')
CMP.Set_Meas_Port('P1.RRH.RF1')
CMP.Set_5GNR_BWP_Frame_Periodicity(2)
CMP.Set_5GNR_BWP_Frame_SlotConfig(0,0,8,0)
CMP.Set_5GNR_ChannelBW(100)
CMP.Set_5GNR_CellID(NR5G.CellID)
CMP.Set_5GNR_BWP_Ch_DMRS_1stDMRSSym(2)
# CMP.Set_5GNR_NumBWP()
CMP.Set_5GNR_BWP_ResBlock(NR5G.RB, NR5G.RBO)
CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:BWP:PUSC:DMTA BWP0, 1, 2, 1')                 #Config; AddPos; MaxLength
CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:BWP:PUSC:DMTB BWP0, 1, 2, 1')                 #Config; AddPos; MaxLength
CMP.Set_5GNR_TransPrecoding(NR5G.TF)
CMP.Set_5GNR_PUSCH(NR5G.Ch_RB, NR5G.Ch_RBO, NR5G.Mod)
CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:ALL{CMP.alloc}:PUSC:ADD 1, 2, 3, 0')          #Len; CDM; Pwr; Ant
CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:ALL{CMP.alloc}:PUSC:SGEN CID, 0, 0')          #SeqType; DMRSID; N_SCID
CMP.Set_5GNR_EVM_MeasOnExcept('ON')
CMP.Set_5GNR_EVM_AvgCount(20)
CMP.Set_5GNR_Trigger_Source('Free Run (Fast Sync)')
