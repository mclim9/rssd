# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Radio Communication Tester(RCT) Functions
### Author : Martin C Lim
### Date   : 2018.05.29
###############################################################################
from rssd.RCT.Common import RCT              #pylint: disable=E0611,E0401

class RCT(RCT):
    """ Rohde & Schwarz Radio Comm Tester Object """
    def __init__(self):
        super(RCT, self).__init__()
        self.Model  = "CMW-GPRF"
        self.sdir   = "UL"
        self.BWP    = 0
        self.User   = 0
        self.alloc  = 1
        self.subF   = 0
        self.cc     = 1         # 1 Start

    ###########################################################################
    ### RCT Get Functions
    ###########################################################################
    def Get_AmpSettings(self):
        """Get ExpectPwr; UserMargin; ExtAttn; MixerOffset settings"""
        expp = self.Get_5GNR_ExpPwr()
        user = self.Get_5GNR_UserMargin()
        exta = self.Get_5GNR_ExtAttn()
        mixr = self.Get_5GNR_MixerOff()
        return f'{expp:7.3f},{user:7.3f},{exta:7.3f},{mixr:2d}'

    def Get_5GNR_EVM(self):
        """ Arry4: EVM_RMS_HIGH
            Arry19:TxPwr 
            Arry20:PkPwr 
            Arry16:FrqErr"""
        # self.write('ABOR:NRMM:MEAS:MEV')
        self.query('INIT:NRMM:MEAS:MEV;*OPC?')
        rdStr = self.queryFloatArry('FETC:NRMM:MEAS:MEV:MOD:AVER?')
        try:
            rdStr = [rdStr[2], rdStr[18], rdStr[19], rdStr[15]]
        except:
            rdStr = [-9999,-9999,-9999,-9999]
        return rdStr

    def Get_5GNR_ExpPwr(self):
        """ExpPwr = Range + ExtAttn - UserMargin
           units: dBm """
        rdStr = self.queryFloat(f'CONF:NRMM:MEAS:RFS:ENP?')
        return rdStr

    def Get_5GNR_ExtAttn(self):
        """ExpPwr = Range + ExtAttn - UserMargin
           units: dB """
        rdStr = self.queryFloat(f'CONF:NRMM:MEAS:RFS:EATT?')
        return rdStr

    def Get_5GNR_MixerOff(self):
        """ExpPwr = Range + ExtAttn - UserMargin
           range: -10 to 10"""
        rdStr = self.queryInt(f'CONF:NRMM:MEAS:RFS:MLOF?')
        return rdStr

    def Get_5GNR_UserMargin(self):
        """ExpPwr = Range + ExtAttn - UserMargin
           units: dB """
        rdStr = self.queryFloat(f'CONF:NRMM:MEAS:RFS:UMAR?')
        return rdStr

    #####################################################################
    ### 5GNR Get Methods
    #####################################################################
    def Get_5GNR_BWP_Center(self):
        rdStr = "<notRead>"
        return rdStr

    def Get_5GNR_BWP_Ch_DMRS_1stDMRSSym(self):
        """2 3 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:TAP?')
        return rdStr

    def Get_5GNR_BWP_Ch_DMRS_AddPosition(self):
        """ 0 to 3 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:BWP:PUSC:DMTA?  BWP{self.BWP}').split(',')
        return rdStr[1]

    def Get_5GNR_BWP_Ch_DMRS_Antenna(self):
        """ 1 to 0 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC:ADD?').split(',')
        return rdStr[3]

    def Get_5GNR_BWP_Ch_DMRS_CDMGroup(self):
        """ 1 to 3 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC:ADD?').split(',')
        return rdStr[1]

    def Get_5GNR_BWP_Ch_DMRS_Config(self):
        """ 1 to 2 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:BWP:PUSC:DMTA? BWP{self.BWP}').split(',')
        return rdStr[0]

    def Get_5GNR_BWP_Ch_DMRS_Mapping(self):
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC?').split(',')
        return rdStr[0]

    def Get_5GNR_BWP_Ch_DMRS_MSymbLen(self):
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC:ADD?').split(',')
        return rdStr[0]

    def Get_5GNR_BWP_Ch_DMRS_RelPwr(self):
        """ -10 to 10 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC:ADD?').split(',')
        return rdStr[2]

    def Get_5GNR_BWP_Ch_DMRS_SeqGenMeth(self):
        """CellID DMRS"""
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC:SGEN?').split(',')
        return rdStr[0]

    def Get_5GNR_BWP_Ch_DMRS_SeqGenSeed(self):
        """ 0 to 655535 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC:SGEN?').split(',')
        return rdStr[1]

    def Get_5GNR_BWP_Ch_DMRS_SeqGen_n_SCID(self):
        """ 0 to 1 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC:SGEN?').split(',')
        return rdStr[2]

    def Get_5GNR_BWP_Ch_Modulation(self):
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC?').split(',')
        return rdStr[5]

    def Get_5GNR_BWP_Ch_Mapping(self):
        """PUSCH Mapping"""
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC?').split(',')
        return rdStr[0]

    def Get_5GNR_BWP_Ch_PTRS_K(self):
        """ Freq Density in RB """
        rdStr = "<TBS>"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_L(self):
        """ Time Density in OFDM Sym Freq """
        rdStr = "<TBS>"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_Pow(self):
        rdStr = "<TBS>"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_RE_Offset(self):
        """ PTRS freq (RE) offset """
        rdStr = "<TBS>"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_State(self):
        rdStr = "<TBS>"
        return rdStr

    def Get_5GNR_BWP_Ch_ResBlock(self):
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC?').split(',')
        return rdStr[3]

    def Get_5GNR_BWP_Ch_ResBlockOffset(self):
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC?').split(',')
        return rdStr[4]

    def Get_5GNR_BWP_Ch_SymbNum(self):
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC?').split(',')
        return rdStr[1]

    def Get_5GNR_BWP_Ch_SymbOff(self):
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC?').split(',')
        return rdStr[2]

    def Get_5GNR_BWP_Count(self):
        rdStr = 1
        return rdStr

    def Get_5GNR_BWP_ResBlock(self):
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:BWP? BWP{self.BWP}').split(',')
        return rdStr[2]

    def Get_5GNR_BWP_ResBlockOffset(self):
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:BWP? BWP{self.BWP}').split(',')
        return rdStr[3]
        
    # def Get_5GNR_BWP_SlotNum(self):
    #     ### Number of slots
    #     rdStr = self.query(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:SLOT?')
    #     return rdStr
        
    def Get_5GNR_BWP_SubSpace(self):
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:BWP? BWP{self.BWP}').split(',')
        return rdStr[0]

    def Get_5GNR_CC_Offset(self):
        rdStr = "<notRead>"
        return rdStr

    def Get_5GNR_CellID(self):
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:PLC?')
        return rdStr

    def Get_5GNR_SSB_SubSpace(self):
        if self.sdir == 'DL':
            # rdStr = self.query(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:SSPB0:SCSP?')
            pass
        else:
            rdStr = '<UL n/a>'
        return rdStr

    def Get_5GNR_ChannelBW(self):
        ### 5;10;15;20;25;30;40;50;60;70;80;90;100;200;400
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:CBAN?')
        return rdStr

    def Get_5GNR_Direction(self):
        rdStr = "UP"
        if rdStr == 'DOWN':
            self.sdir = "DL"
            self.alloc = 1         #Alloc 0:CORSET
        elif rdStr == 'UP':
            self.sdir = "UL"            
            self.alloc = 1         #Alloc 0:PUSCH
        else:
            print('Get_5GNR_Direction Error')
        return self.sdir

    def Get_5GNR_FreqRange(self):
        return "HIGH"
        
    # def Get_5GNR_RefA(self):
    #     rdStr = '<notRead>'
    #     return rdStr

    def Get_5GNR_PhaseCompensate(self):
        rdStr = self.query(f'CONF:NRMM:MEAS:MEV:PCOM?').split(',')[0]
        if (rdStr == 'CAF') or (rdStr == 'UDEF'):
            outStr = 'ON'
        else:
            outStr = '<notRead>'
        return outStr

    def Get_5GNR_PhaseCompensate_Freq(self):
        rdStr = self.query(f'CONF:NRMM:MEAS:MEV:PCOM?').split(',')[1]
        return rdStr

    def Get_5GNR_TransPrecoding(self):
        # SC-FDMA or DFT-S-OFDM
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:BWP:PUSC:DFTP? BWP{self.BWP}')
        return rdStr

    ###########################################################################
    ### BSE Init Functions
    ###########################################################################
    def Init_5GNR(self):
        self.write('SYST:GEN:ALL:OFF')
        self.write('SYST:MEAS:ALL:OFF')
        self.write('ABOR:NRMM:MEAS:MEV')
        self.query('INIT:NRMM:MEAS:MEV;*OPC?')

    ###########################################################################
    ### BSE Set Functions
    ###########################################################################

    def Set_5GNR_ExpPwr(self, pwr):
        """ExpPwr = Range + ExtAttn - UserMargin
           units: dBm """
        self.write(f'CONF:NRMM:MEAS:RFS:ENP {pwr} DBM')

    def Set_5GNR_ExtAttn(self, pwr):
        """ExpPwr = Range + ExtAttn - UserMargin
           units: dB """
        self.write(f'CONF:NRMM:MEAS:RFS:EATT {pwr} DB')

    def Set_5GNR_Freq(self,freq):
        """freq in Hz"""
        self.write(f'CONF:NRMM:MEAS:RFS:FREQ {freq}')

    def Set_5GNR_MixerOff(self, pwr):
        """ExpPwr = Range + ExtAttn - UserMargin
           range: -10 to 10
           units: dB """
        self.write(f'CONF:NRMM:MEAS:RFS:MLOF {pwr}')

    def Set_5GNR_PhaseComp(self,state,freq):
        """ State: OFF | CAF | UDEF 
            Freq : Hz"""
        self.write(f'CONF:NRMM:MEAS:MEV:PCOM {state},{freq}')

    def Set_5GNR_Periodicity(self,period):
        """ Period: 05 | 0625 | 1 | 125 | 2 | 25 | 5 | 10 """
        self.write(f'CONF:NRMM:MEAS:ULDL:PER MS{period}')

    def Set_5GNR_UserMargin(self, pwr):
        """ExpPwr = Range + ExtAttn - UserMargin
           units: dB """
        self.write(f'CONF:NRMM:MEAS:RFS:UMAR {pwr} DB')


    def Set_5GNR_BWP_Ch_DMRS_1stDMRSSym(self,TAP):
        """2 3"""
        self.write(f'CONF:NRMM:MEAS:CC{self.cc}:TAP {TAP}')

    # def Set_5GNR_BWP_Ch_Modulation(self,sMod):
    #     self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:MOD {sMod}')
        
    # def Set_5GNR_BWP_Ch_ResBlock(self,iRB):
    #     ### 5GNR-->Scheduling-->PUSCH-->No. RBs
    #     ### RB = (CHBw * 0.95) / (SubSp * 12)
    #     #self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:RBN %d'%iRB)
    #     self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:RBN {iRB}')

    # def Set_5GNR_BWP_Ch_ResBlockOffset(self,iRBO):
    #     ### 5GNR-->Scheduling-->PUSCH-->No. RBs
    #     #self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:RBOF %d'%%(self.alloc,iRBO))
    #     self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:RBOF 0')

    # def Set_5GNR_BWP_Corset_ResBlock(self, iRB):
    #     if self.sdir == 'DL':
    #         self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL0:RBN {iRB}')

    # def Set_5GNR_BWP_Corset_ResBlockOffset(self,iRBO):
    #     if self.sdir == 'DL':
    #     ### 5GNR-->Scheduling-->PUSCH-->No. RBs
    #         self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL0:RBOF {iRBO}')

    # def Set_5GNR_BWP_ResBlock(self,iRB):
    #     ### RB = (CHBw * 0.95) / (SubSp * 12)
    #     self.write(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:{self.sdir}:BWP0:RBN {iRB}')

    # def Set_5GNR_BWP_ResBlockMax(self):
    #     ### RB = (CHBw * 0.95) / (SubSp * 12)
    #     MaxRB =  20
    #     rdStr = self.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:{self.sdir}:BWP0:RBN {MaxRB}')
    #     return rdStr
        
    # def Set_5GNR_BWP_ResBlockOffset(self,iRBO):
    #     self.write(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:{self.sdir}:BWP0:RBOF {iRBO}')

    # def Set_5GNR_BWP_SubSpace(self,iSubSp):
    #     """60| 120"""
    #     self.write(f'CONF:NRMM:MEAS:CCAL:TXBW:SCSP S{iSubSp}K')

    # def Set_5GNR_CC_Num(self,iCC):
    #     """ iCC, 1 start """
    #     self.cc = iCC - 1
    #     self.write(f'SOUR1:BB:NR5G:NODE:NCAR {iCC}')

    # def Set_5GNR_CC_Offset(self,Freq):
    #     """ freq, Hz """
    #     self.write(f':SOUR1:BB:NR5G:NODE:CARM:DFR:ROW{self.cc} {Freq}')

    def Set_5GNR_CellID(self,cell):
        """ 0 to 1007"""
        self.write(f'CONF:NRMM:MEAS:CC{self.cc}:PLC {cell}')

    def Set_5GNR_ChannelBW(self,iBW):
        """ 050 100 200 400"""
        self.write(f'CONF:NRMM:MEAS:CC1:CBAN B{iBW}')

    def Set_5GNR_Direction(self,sDirection):
        """ UP| DOWN """
        if (sDirection == "UL") or (sDirection == "UP"):
            # self.write(f':SOUR1:BB:NR5G:LINK UP')
            self.sdir = "UL"
            self.alloc = 1         #Alloc 0:PUSCH
        elif (sDirection == "DL") or (sDirection == "DOWN"):
            # self.write(f':SOUR1:BB:NR5G:LINK DOWN')
            self.sdir = "DL"
            self.alloc = 1         #Alloc 0:Coreset 1:PDSCH
        else:
            print("Set_5GNR_Direction must be UP or DOWN")

    def Set_5GNR_EVM_AvgCount(self, avg):
        """1 to 1000 slots"""
        self.write(f':CONF:NRMM:MEAS:MEV:SCO:MOD {avg}')


    def Set_5GNR_Path(self,path):
        """string P1.RRH.RF1 P1.RRH.RF2 """
        self.write(f':ROUT:NRMM:MEAS:SPAT "{path}"')

    def Set_5GNR_PhaseCompensate(self,state):
        """ 'ON' | 'OFF' """
        if (state == "ON") or (state == 1):
            self.write(f'CONF:NRMM:MEAS:MEV:PCOM CAF, 28e9')
        else:
            self.write(f'CONF:NRMM:MEAS:MEV:PCOM OFF, 28e9')

    def Set_5GNR_PhaseCompensate_Freq(self,Freq):
        self.write(f'CONF:NRMM:MEAS:MEV:PCOM UDEF, {Freq}')

    # def Set_5GNR_SSB(self):
    #     """Num DL SS/PBCH Patterns"""
    #     if self.sdir == 'DL':
    #         self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:NSSP 1')

    def Set_5GNR_TransPrecoding(self, sState):
        """ SC-FDMA or DFT-S-OFDM  """
        if (sState == 'ON') or (sState == 1):
            self.write(f'CONF:NRMM:MEAS:CC{self.cc}:BWP:PUSC:DFTP BWP{self.BWP}, ON')
        elif (sState == 'OFF') or (sState == 0):
            self.write(f'CONF:NRMM:MEAS:CC{self.cc}:BWP:PUSC:DFTP BWP{self.BWP}, OFF')
        else:
            print('Error Set_5GNR_TransPrecoding')

    def Set_5GNR_Trigger_Source(self, source):
        """ string 'Free Run (Fast Sync)' 'Free Run (No Sync)' 'IF Power' """
        self.write(f':TRIG:NRMM:MEAS:MEV:SOUR "{source}"')
    
    def Set_5GNR_Stop(self):
        self.write(f'STOP:NRMM:MEAS:MEV STOP')

###############################################################################
### Run if Main
###############################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    CMP = RCT()
    CMP.jav_Open("192.168.1.160")
    CMP.Set_5GNR_Path('P1.RRH.RF1')
    CMP.Set_5GNR_Freq(28e9)
    CMP.Get_GPRF_Pwr()
    CMP.Set_5GNR_ExpPwr(-9)
    CMP.Set_5GNR_UserMargin(13)
    CMP.Set_5GNR_PhaseCompensate_Freq(28e9)
    CMP.write(f'CONF:NRMM:MEAS:ULDL:PER MS2')
    CMP.write(f'CONF:NRMM:MEAS:ULDL:PATT S120k, 0,0,8,0')                               #DL Slot; DL Sym; UL SLot; UL Sym
    CMP.write(f'CONF:NRMM:MEAS:ULDL:PATT S60k,  0,0,1,0')                               #DL Slot; DL Sym; UL SLot; UL Sym
    CMP.Set_5GNR_ChannelBW(100)
    CMP.Set_5GNR_CellID(1)
    CMP.Set_5GNR_BWP_Ch_DMRS_1stDMRSSym(2)
    # CMP.Set_5GNR_NumBWP()
    CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:BWP BWP0, S120K, NORM, 66, 0')                #SCS; NORM; RB; RBO
    CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:BWP:PUSC:DMTA BWP0, 1, 2, 1')                 #Config; AddPos; MaxLength
    CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:BWP:PUSC:DMTB BWP0, 1, 2, 1')                 #Config; AddPos; MaxLength
    CMP.Set_5GNR_TransPrecoding('OFF')
    CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:ALL{CMP.alloc}:PUSC A, 14, 0, 22, 22, Q64')   #Map; Sym; SymStrt; RB; RBO; Mod
    CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:ALL{CMP.alloc}:PUSC:ADD 1, 2, 3, 0')          #Len; CDM; Pwr; Ant
    CMP.write(f'CONF:NRMM:MEAS:CC{CMP.cc}:ALL{CMP.alloc}:PUSC:SGEN CID, 0, 0')          #SeqType; DMRSID; N_SCID
    CMP.Set_5GNR_EVM_AvgCount(50)
    CMP.Set_5GNR_Trigger_Source('Free Run (Fast Sync)')
    print(CMP.Get_5GNR_EVM())
    CMP.Set_5GNR_Stop
    CMP.jav_Close()
