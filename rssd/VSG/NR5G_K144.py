# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Generator 5G NR Functions
### Author : Martin C Lim
### Date   : 2018.02.01
### Requird: python -m pip install rssd
#####################################################################
from rssd.VSG.Common import VSG             #pylint: disable=E0611,E0401

class VSG(VSG):                             #pylint: disable=E0102
    """ Rohde & Schwarz Vector Signal Generator 5GNR Object """
    def __init__(self):
        super(VSG,self).__init__()          #Python2/3
        self.Model  = "SMW"
        self.sdir   = "UL"
        self.BWP    = 0
        self.User   = 0
        self.alloc  = 0
        self.subF   = 0
        self.cc     = 0         # 0 Start

    #####################################################################
    ### 5GNR Get Methods
    #####################################################################
    def Get_5GNR_BWP_CellID(self):
        rdStr = self.queryInt(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CELL?')
        return rdStr

    def Get_5GNR_BWP_Center(self):
        rdStr = self.queryInt(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:{self.sdir}:BWP0:DFR?')
        return rdStr

    def Get_5GNR_BWP_Ch_DMRS_1stDMRSSym(self):
        #rdStr = self.query(f':SOUR:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:PUSC:DMRS:APOS?')
        rdStr = "<TBD>"
        return rdStr

    def Get_5GNR_BWP_Ch_DMRS_AddPosition(self):
        #rdStr = self.query(f':SOUR:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:PUSC:DMRS:IND?')
        if self.sdir == 'UL':
            # User/BWP-->ULBWP COnfig
            rdStr = self.query(f':SOUR:BB:NR5G:UBWP:USER0:CELL{self.cc}:UL:BWP0:PUSCH:DMTA:APIN?')
        else:
            rdStr = self.query(f':SOUR:BB:NR5G:UBWP:USER0:CELL{self.cc}:DL:BWP0:PDSCH:DMTA:APIN?')
        return rdStr

    def Get_5GNR_BWP_Ch_DMRS_Config(self):
        rdStr = "<TBD>"
        if self.sdir == 'UL':
            # User/BWP-->ULBWP COnfig
            rdStr = self.query(f':SOUR:BB:NR5G:UBWP:USER0:CELL{self.cc}:UL:BWP0:PUSCH:DMTA:CTYP?')
        else:
            rdStr = self.query(f':SOUR:BB:NR5G:UBWP:USER0:CELL{self.cc}:DL:BWP0:PDSCH:DMTA:CTYP?')
        return rdStr[1]

    def Get_5GNR_BWP_Ch_DMRS_Mapping(self):
        rdStr = self.query(f':SOUR:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:MAPT?')
        # rdStr = "<TBD>"
        return rdStr

    def Get_5GNR_BWP_Ch_DMRS_MSymbLen(self):
        if self.sdir == 'DL':
            rdStr = self.query(f':SOUR:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:PDSCH:DMRS:LENG?')  #MMM
        else:
            rdStr = self.query(f':SOUR:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:PUSC:DMRS:LENG?')
        return rdStr

    def Get_5GNR_BWP_Ch_DMRS_RelPwr(self):
        if self.sdir == 'DL':
            rdStr = self.query(f':SOUR:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:PDSCH:DMRS:POW?')
        else:
            rdStr = self.query(f':SOUR:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:PUSCH:DMRS:POW?')
        #rdStr = "<TBD>"
        return rdStr

    def Get_5GNR_BWP_Ch_DMRS_SeqGenMeth(self):
        if self.sdir == 'DL':
            rdStr = self.query(f':SOUR:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:PDSC:DMRS:SEQG?') #MMM
        else:
            rdStr = self.query(f':SOUR:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:PUSC:DMRS:SEQG?')
        # rdStr = "<TBD>"
        return rdStr

    def Get_5GNR_BWP_Ch_DMRS_SeqGenSeed(self):
        #Only for SeqGenMeth NICP.  Not Valid for NIDC
        if self.Get_5GNR_BWP_Ch_DMRS_SeqGenMeth() == 'DMRS':
            rdStr = self.query(f':SOUR:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:PUSC:DMRS:NSID?')
        else:
            rdStr = '<!CELL>'
        return rdStr

    def Get_5GNR_BWP_Ch_Modulation(self):
        rdStr = self.query(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:MOD?')
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_K(self):
        """ Freq Density in RB """
        if self.Get_5GNR_BWP_Ch_PTRS_State() == '1':
            rdStr = self.query(f':SOUR:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:PUSC:PTRS:FRQD?')
        else:
            rdStr = "PTRS Off"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_L(self):
        """ Time Density in OFDM Sym Freq """
        if self.Get_5GNR_BWP_Ch_PTRS_State() == '1':
            rdStr = self.query(f':SOUR:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:PUSC:PTRS:TMD?')
        else:
            rdStr = "PTRS Off"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_Pow(self):
        if self.Get_5GNR_BWP_Ch_PTRS_State() == '1':
            rdStr = self.query(f':SOUR:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:PUSC:PTRS:POW?')
        else:
            rdStr = "PTRS Off"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_RE_Offset(self):
        """ PTRS freq (RE) offset """
        if self.Get_5GNR_BWP_Ch_PTRS_State() == '1':
            rdStr = self.query(f':SOUR:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:PUSC:PTRS:REOF?')
        else:
            rdStr = "PTRS Off"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_State(self):
        rdStr = self.query(f':SOUR:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:PUSC:PTRS:STAT?')
        return rdStr

    def Get_5GNR_BWP_Ch_ResBlock(self):
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        rdStr = self.query(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:RBN?')
        return rdStr

    def Get_5GNR_BWP_Ch_ResBlockOffset(self):
        rdStr = self.query(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:RBOF?')
        return rdStr

    def Get_5GNR_BWP_Ch_SymbNum(self):
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        rdStr = self.query(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:SYMN?')
        return rdStr

    def Get_5GNR_BWP_Ch_SymbOff(self):
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        rdStr = self.query(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:SYM?')
        return rdStr

    def Get_5GNR_BWP_Count(self):
        rdStr = self.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:{self.sdir}:NBWP?')
        return rdStr

    def Get_5GNR_BWP_ResBlock(self):
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        rdStr = self.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:{self.sdir}:BWP0:RBN?')
        return rdStr

    def Get_5GNR_BWP_ResBlockOffset(self):
        rdStr = self.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:{self.sdir}:BWP0:RBOF?')
        return rdStr

    def Get_5GNR_BWP_SlotNum(self):
        ### Number of slots
        rdStr = self.query(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:SLOT?')
        return rdStr

    def Get_5GNR_BWP_SubSpace(self):
        rdStr = self.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:{self.sdir}:BWP0:SCSP?')
        return rdStr

    def Get_5GNR_CC_Freq(self):
        offset = self.Get_5GNR_CC_Offset()
        freq    = self.Get_Freq()
        return offset + freq

    def Get_5GNR_CC_Offset(self):
        rdStr = self.queryFloat(f'SOUR1:BB:NR5G:NODE:CARM:DFREQ:ROW{self.cc}?')
        return rdStr

    def Get_5GNR_SSB_SubSpace(self):
        if self.sdir == 'DL':
            rdStr = self.query(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:SSPB0:SCSP?')
        else:
            rdStr = '<UL n/a>'
        return rdStr

    def Get_5GNR_BWP_SubSpaceTotal(self):
        rdStr = []
        rdStr.append(self.query(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S15K:NRB?'))
        rdStr.append(self.query(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S30K:NRB?'))
        rdStr.append(self.query(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S60K:NRB?'))
        rdStr.append(self.query(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S120K:NRB?'))
        return rdStr

    def Get_5GNR_ChannelBW(self):
        ### 5;10;15;20;25;30;40;50;60;70;80;90;100;200;400
        rdStr = self.query(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CBW?')
        return rdStr

    def Get_5GNR_Direction(self):
        rdStr = self.query(f':SOUR1:BB:NR5G:LINK?')
        if rdStr == 'DOWN':
            self.sdir = "DL"
            self.alloc = 1         #Alloc 0:CORSET
        elif rdStr == 'UP':
            self.sdir = "UL"
            self.alloc = 0         #Alloc 0:PUSCH
        else:
            print('Get_5GNR_Direction Error')
        return self.sdir

    def Get_5GNR_FreqRange(self):
        rdStr = self.query(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CARD?')
        if (rdStr == 'LT3') or (rdStr == 'LT3') or (rdStr == 'FR1LT3'):
            outStr = 'LOW'
        elif (rdStr == 'BT36') or (rdStr == 'BT37125')or (rdStr == 'FR1GT3'):
            outStr = 'MIDD'
        elif (rdStr == 'GT6') or (rdStr == 'GT7125')or (rdStr == 'FR2'):
            outStr = 'HIGH'
        else:
            outStr = 'Error Get_5GNR_FreqRange {rdStr}'
        return outStr

    def Get_5GNR_RefA(self):
        rdStr = self.queryInt(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:POIN?')
        return rdStr

    def Get_5GNR_RBMax(self):
        odata = []
        rdStr = self.queryInt(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S15K:NRB?')
        odata.append([15,rdStr])
        rdStr = self.queryInt(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S30K:NRB?')
        odata.append([30,rdStr])
        rdStr = self.queryInt(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S60K:NRB?')
        odata.append([60,rdStr])
        rdStr = self.queryInt(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S120K:NRB?')
        odata.append([120,rdStr])
        return odata

    def Get_5GNR_PhaseCompensate(self):
        rdStr = self.query(f':SOUR:BB:NR5G:NODE:RFPH:STAT?')
        return rdStr

    def Get_5GNR_TM_Cat(self):
        rdStr = self.query(f'SOUR1:BB:NR5G:SETT:TMOD:DL:CAT?').split(',')
        return rdStr

    def Get_5GNR_TransPrecoding(self):
        # SC-FDMA or DFT-S-OFDM
        # 5GNR--> User/BWP --> UL BWP Config --> PUSCH --> TP
        # rdStr = self.query(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL0:TPST?')
        rdStr = self.query(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:UL:BWP0:PUSC:TPST?') #4.50
        return rdStr

    #####################################################################
    ### 5GNR Settings
    #####################################################################
    def Set_5GNR_BBState(self,iEnable):
        """ON OFF"""
        if (iEnable == 1) or (iEnable == 'ON'):
            self.jav_Wait(':SOUR1:BB:NR5G:STAT 1')
#            self.query(f'*OPC?')          # Wait for calculation
        else:
            self.write(f':SOUR1:BB:NR5G:STAT 0')

    def Set_5GNR_BWP_Ch_Modulation(self,sMod):
        self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:MOD {sMod}')

    def Set_5GNR_BWP_Ch_ResBlock(self,iRB):
        """5GNR-->Scheduling-->PUSCH-->No. RBs"""
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:RBN {iRB}')

    def Set_5GNR_BWP_Ch_ResBlockOffset(self,iRBO):
        """5GNR-->Scheduling-->PUSCH-->RB Offset"""
        self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL{self.alloc}:RBOF {iRBO}')

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
        """15 30 60 120"""
        if iSubSp == 15:
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S15K:USE 1')
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S30K:USE 0')
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S60K:USE 0')
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S120K:USE 0')
        elif iSubSp == 30:
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S30K:USE 1')
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S15K:USE 0')
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S60K:USE 0')
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S120K:USE 0')
        elif iSubSp == 60:
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S60K:USE 1')
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S15K:USE 0')
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S30K:USE 0')
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S120K:USE 0')
        elif iSubSp == 120:
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S120K:USE 1')
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S15K:USE 0')
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S30K:USE 0')
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:S60K:USE 0')
        else:
            print('Subcarrier spacing not supported')
        self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:TXBW:RES')
        self.write(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:{self.sdir}:BWP0:SCSP N{iSubSp}')

    def Set_5GNR_CC_Num(self,iCC):
        """ iCC, 1 start """
        self.cc = iCC - 1
        self.write(f'SOUR1:BB:NR5G:NODE:NCAR {iCC}')

    def Set_5GNR_CC_Offset(self,Freq):
        """ freq, Hz """
        self.write(f':SOUR1:BB:NR5G:NODE:CARM:DFR:ROW{self.cc} {Freq}')


    def Set_5GNR_ChannelBW(self,iBW):
        """ BW in MHz
         5GNR-->NODE-->Carriers-->Channel BW"""
        self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CBW BW{iBW}')

    def Set_5GNR_Direction(self,sDirection):
        """ UP| DOWN """
        if (sDirection == "UL") or (sDirection == "UP"):
            self.write(f':SOUR1:BB:NR5G:LINK UP')
            self.sdir = "UL"
            self.alloc = 0         #Alloc 0:PUSCH
        elif (sDirection == "DL") or (sDirection == "DOWN"):
            self.write(f':SOUR1:BB:NR5G:LINK DOWN')
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
        # """ LOW; MIDD; HIGH """
        if (iRange==0) or (iRange == 'LOW'):
            # self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CARD LT3')     #4.70.026.51
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CARD FR1LT3')    #C45.4.70.026.51.131
        elif (iRange==1) or (iRange == 'MIDD'):
            # self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CARD BT36')    #4.70.026.51
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CARD FR1GT3')    #C45.4.70.026.51.131
        elif (iRange==2) or (iRange == 'HIGH'):
            # self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CARD GT6')     #4.70.026.51
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:CARD FR2')       #C45.4.70.026.51.131

    def Set_5GNR_GenerateWv(self,sName):
        """ Generate Waveform File"""
        self.write(f':SOUR1:BB:NR5G:WAV:CRE "{sName}"')
        self.delay(2)
        self.jav_OPC_Wait('*IDN?')

    def Set_5GNR_Parameters(self,sDir):
        self.Set_5GNR_Direction(sDir)

    def Set_5GNR_PhaseCompensate(self,state):
        """ 'ON' | 'OFF' """
        if (state == "ON") or (state == 1):
            self.write(f':SOUR:BB:NR5G:NODE:RFPH:STAT ON')
        else:
            self.write(f':SOUR:BB:NR5G:NODE:RFPH:STAT OFF')

    def Set_5GNR_PhaseCompensate_Freq(self,Freq):
        self.write(f':SOUR:BB:NR5G:NODE:CELL{self.cc}:PCFR {Freq}')

    def Set_5GNR_SSB(self):
        """Num DL SS/PBCH Patterns"""
        if self.sdir == 'DL':
            self.write(f':SOUR1:BB:NR5G:NODE:CELL{self.cc}:NSSP 1')

    def Set_5GNR_TM(self, file):
        """NR-FR1-TM1_1__FDD_100MHz_30kHz """
        self.query(f'SOUR1:BB:NR5G:SETT:TMOD:DL "{file}";*OPC?')

    def Set_5GNR_TransPrecoding(self, sState):
        """ SC-FDMA or DFT-S-OFDM
        5GNR--> User/BWP --> UL BWP Config --> PUSCH --> TP  """
        if sState == 'ON':
            # self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL0:TPST ON') #4.30SP2?
            self.write(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:UL:BWP0:PUSC:TPST ON') #4.50
        else:
            # self.write(f':SOUR1:BB:NR5G:SCH:CELL{self.cc}:SUBF{self.subF}:USER0:BWP0:ALL0:TPST OFF') #4.30SP2?
            self.write(f':SOUR1:BB:NR5G:UBWP:USER0:CELL{self.cc}:UL:BWP0:PUSC:TPST OFF') #4.50

    def Set_5GNR_Setting_Load(self, sName):
        self.query(f':SOUR:BB:NR5G:SETT:LOAD "/var/user/{sName}";*OPC?')

    def Set_5GNR_savesetting(self, sName):
        self.query(f':SOUR:BB:NR5G:SETT:STOR "/var/user/{sName}";*OPC?')
        # self.query(f':SOUR:BB:NR5G:WAV:CRE "/var/user/{sName}";*OPC?')
        # self.delay(10)

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    # this won't be run when imported
    SMW = VSG()
    SMW.jav_Open("192.168.1.114")
    SMW.cc = 1
    print(SMW.Get_5GNR_CC_Freq())
    SMW.jav_Close()
