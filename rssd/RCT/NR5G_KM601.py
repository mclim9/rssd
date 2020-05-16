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
            rdStr = [rdStr[3], rdStr[18], rdStr[19], rdStr[15]]
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
    def Get_5GNR_BWP_Center(self):#MMM
        rdStr = "<notRead>"
        return rdStr

    def Get_5GNR_BWP_Ch_DMRS_1stDMRSSym(self):#MMM
        """2 3 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:TAP?')
        return rdStr

    def Get_5GNR_BWP_Ch_DMRS_AddPosition(self):#MMM
        """ 0 to 3 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:BWP:PUSC:DMTA?  BWP{self.BWP}').split(',')
        return rdStr[1]

    def Get_5GNR_BWP_Ch_DMRS_Antenna(self):#MMM
        """ 1 to 0 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC:ADD?').split(',')
        return rdStr[3]

    def Get_5GNR_BWP_Ch_DMRS_CDMGroup(self):#MMM
        """ 1 to 3 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC:ADD?').split(',')
        return rdStr[1]

    def Get_5GNR_BWP_Ch_DMRS_Config(self):#MMM
        """ 1 to 2 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:BWP:PUSC:DMTA? BWP{self.BWP}').split(',')
        return rdStr[0]

    def Get_5GNR_BWP_Ch_DMRS_Mapping(self):
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC?').split(',')
        return rdStr[0]

    def Get_5GNR_BWP_Ch_DMRS_MSymbLen(self):#MMM
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC:ADD?').split(',')
        return rdStr[0]

    def Get_5GNR_BWP_Ch_DMRS_RelPwr(self):#MMM
        """ -10 to 10 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC:ADD?').split(',')
        return rdStr[2]

    def Get_5GNR_BWP_Ch_DMRS_SeqGenMeth(self):#MMM
        """CellID DMRS"""
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC:SGEN?').split(',')
        return rdStr[0]

    def Get_5GNR_BWP_Ch_DMRS_SeqGenSeed(self):#MMM
        """ 0 to 655535 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC:SGEN?').split(',')
        return rdStr[1]

    def Get_5GNR_BWP_Ch_DMRS_SeqGen_n_SCID(self):#MMM
        """ 0 to 1 """
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC:SGEN?').split(',')
        return rdStr[2]

    def Get_5GNR_BWP_Ch_Modulation(self):#MMM
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC?').split(',')
        return rdStr[5]

    def Get_5GNR_BWP_Ch_Mapping(self):#MMM
        """PUSCH Mapping"""
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC?').split(',')
        return rdStr[0]

    def Get_5GNR_BWP_Ch_PTRS_K(self):#MMM
        """ Freq Density in RB """
        rdStr = "<TBS>"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_L(self):#MMM
        """ Time Density in OFDM Sym Freq """
        rdStr = "<TBS>"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_Pow(self):#MMM
        rdStr = "<TBS>"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_RE_Offset(self):#MMM
        """ PTRS freq (RE) offset """
        rdStr = "<TBS>"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_State(self):#MMM
        rdStr = "<TBS>"
        return rdStr

    def Get_5GNR_BWP_Ch_ResBlock(self):#MMM
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC?').split(',')
        return rdStr[3]

    def Get_5GNR_BWP_Ch_ResBlockOffset(self):#MMM
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC?').split(',')
        return rdStr[4]

    def Get_5GNR_BWP_Ch_SymbNum(self):#MMM
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC?').split(',')
        return rdStr[1]

    def Get_5GNR_BWP_Ch_SymbOff(self):
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:ALL{self.alloc}:PUSC?').split(',')
        return rdStr[2]

    def Get_5GNR_BWP_Count(self):#MMM
        rdStr = 1
        return rdStr

    def Get_5GNR_BWP_ResBlock(self):#MMM
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:BWP? BWP{self.BWP}').split(',')
        return rdStr[2]

    def Get_5GNR_BWP_ResBlockOffset(self):#MMM
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:BWP? BWP{self.BWP}').split(',')
        return rdStr[3]
        
    def Get_5GNR_BWP_SlotNum(self):
        ### Number of slots
        rdStr = self.query(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:SLOT?')
        return rdStr
        
    def Get_5GNR_BWP_SubSpace(self):#MMM
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:BWP? BWP{self.BWP}').split(',')
        return rdStr[0]

    def Get_5GNR_CC_Offset(self):#MMM
        rdStr = "<notRead>"
        return rdStr

    def Get_5GNR_CellID(self):#MMM
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:PLC?')
        return rdStr

    def Get_5GNR_SSB_SubSpace(self):#MMM
        if self.sdir == 'DL':
            # rdStr = self.query(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:SSPB0:SCSP?')
            pass
        else:
            rdStr = '<UL n/a>'
        return rdStr

    def Get_5GNR_ChannelBW(self):#MMM
        ### 5;10;15;20;25;30;40;50;60;70;80;90;100;200;400
        rdStr = self.query(f'CONF:NRMM:MEAS:CC{self.cc}:CBAN?')
        return rdStr

    def Get_5GNR_Direction(self):#MMM
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

    def Get_5GNR_FreqRange(self):#MMM
        return "HIGH"
        
    def Get_5GNR_RefA(self):
        rdStr = '<notRead>'
        return rdStr

    def Get_5GNR_PhaseCompensate(self):#MMM
        rdStr = self.query(f'CONF:NRMM:MEAS:MEV:PCOM?').split(',')[0]
        if (rdStr == 'CAF') or (rdStr == 'UDEF'):
            outStr = 'ON'
        else:
            outStr = '<notRead>'
        return outStr

    def Get_5GNR_PhaseCompensate_Freq(self):#MMM
        rdStr = self.query(f'CONF:NRMM:MEAS:MEV:PCOM?').split(',')[1]
        return rdStr

    def Get_5GNR_TransPrecoding(self):#MMM
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

    def Set_5GNR_BWP_Ch_Modulation(self,sMod):
        self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:MOD {sMod}')
        
    def Set_5GNR_BWP_Ch_ResBlock(self,iRB):
        ### 5GNR-->Scheduling-->PUSCH-->No. RBs
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        #self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:RBN %d'%iRB)
        self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:RBN {iRB}')

    def Set_5GNR_BWP_Ch_ResBlockOffset(self,iRBO):
        ### 5GNR-->Scheduling-->PUSCH-->No. RBs
        #self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:RBOF %d'%%(self.alloc,iRBO))
        self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:RBOF 0')

    def Set_5GNR_BWP_Corset_ResBlock(self, iRB):
        if self.sdir == 'DL':
            self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL0:RBN {iRB}')

    def Set_5GNR_BWP_Corset_ResBlockOffset(self,iRBO):
        if self.sdir == 'DL':
        ### 5GNR-->Scheduling-->PUSCH-->No. RBs
            self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL0:RBOF {iRBO}')

    def Set_5GNR_BWP_ResBlock(self,iRB):
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        self.write(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:{self.sdir}:BWP0:RBN {iRB}')

    def Set_5GNR_BWP_ResBlockMax(self):
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        MaxRB =  20
        rdStr = self.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:{self.sdir}:BWP0:RBN {MaxRB}')
        return rdStr
        
    def Set_5GNR_BWP_ResBlockOffset(self,iRBO):
        self.write(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:{self.sdir}:BWP0:RBOF {iRBO}')

    def Set_5GNR_BWP_SubSpace(self,iSubSp):
        """60| 120"""
        self.write(f'CONF:NRMM:MEAS:CCAL:TXBW:SCSP S{iSubSp}K')

    # def Set_5GNR_CC_Num(self,iCC):
    #     """ iCC, 1 start """
    #     self.cc = iCC - 1
    #     self.write(f'SOUR1:BB:NR5G:NODE:NCAR {iCC}')

    # def Set_5GNR_CC_Offset(self,Freq):
    #     """ freq, Hz """
    #     self.write(f':SOUR1:BB:NR5G:NODE:CARM:DFR:ROW{self.cc} {Freq}')

    def Set_5GNR_ChannelBW(self,iBW):#MMM
        """ 050 100 200 400"""
        self.write(f'CONF:NRMM:MEAS:CC1:CBAN B{iBW}')

    def Set_5GNR_Direction(self,sDirection):#MMM
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

    def Set_5GNR_FRC_State(self,state):
        """ 'ON' | 'OFF' """
        if (state == "ON") or (state == 1):
            self.write(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:UL:BWP0:FRC:STAT ON')
        else:
            self.write(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:UL:BWP0:FRC:STAT OFF')

    def Set_5GNR_FreqRange(self,iRange):
        """ 0:<3GHz 1:3-6GHz 2:>6GHz """ 
        """ LOW; MIDD; HIGH """ 
        if (iRange==0) or (iRange == 'LOW'):
            # self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CARD LT3')     #4.70.026.51
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CARD FR1LT3')    #C45.4.70.026.51.131
        elif (iRange==1) or (iRange == 'MIDD'):
            # self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CARD BT36')    #4.70.026.51
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CARD FR1GT3')    #C45.4.70.026.51.131
        elif (iRange==2) or (iRange == 'HIGH'):
            # self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CARD GT6')     #4.70.026.51
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CARD FR2')       #C45.4.70.026.51.131

    def Set_5GNR_PhaseCompensate(self,state):#MMM
        """ 'ON' | 'OFF' """
        if (state == "ON") or (state == 1):
            self.write(f'CONF:NRMM:MEAS:MEV:PCOM CAF, 28e9')
        else:
            self.write(f'CONF:NRMM:MEAS:MEV:PCOM OFF, 28e9')

    def Set_5GNR_PhaseCompensate_Freq(self,Freq):#MMM
        self.write(f'CONF:NRMM:MEAS:MEV:PCOM UDEF, {Freq}')

    def Set_5GNR_SSB(self):
        """Num DL SS/PBCH Patterns"""
        if self.sdir == 'DL':
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:NSSP 1')

    def Set_5GNR_TransPrecoding(self, sState):#MMM
        """ SC-FDMA or DFT-S-OFDM  """
        if (sState == 'ON') or (sState == 1):
            self.write(f'CONF:NRMM:MEAS:CC{self.cc}:BWP:PUSC:DFTP BWP{self.BWP}, ON')
        elif (sState == 'OFF') or (sState == 0):
            self.write(f'CONF:NRMM:MEAS:CC{self.cc}:BWP:PUSC:DFTP BWP{self.BWP}, OFF')
        else:
            print('Error Set_5GNR_TransPrecoding')


###############################################################################
### Run if Main
###############################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    CMP = RCT()
    CMP.jav_Open("192.168.1.160")
    CMP.jav_Close()
