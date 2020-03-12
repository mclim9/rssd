# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Analyzer 5GNR Functions
### Author : Martin C Lim
### Date   : 2018.04.03
from rssd.VSA.Common import VSA          #pylint: disable=E0611,E0401

class VSA(VSA):                                #pylint: disable=E0102
    """ Rohde & Schwarz Vector Signal Analyzer 5GNR Object """
    def __init__(self):
        super(VSA, self).__init__()        #Python 2/3
        self.sdir   = "UL"
        self.cc     = 1

    #####################################################################
    ### FSW 5GNR Get
    #####################################################################
    def Get_5GNR_ACLR(self):
        rdStr = self.query(':CALC:MARK:FUNC:POW:RES? MCAC')
        return rdStr

    def Get_5GNR_BWP_Center(self):
        SS = self.Get_5GNR_BWP_SubSpace()
        SS = int(''.join(c for c in SS if c.isdigit()))
        RB = int(self.Get_5GNR_BWP_ResBlock())
        RBO = int(self.Get_5GNR_BWP_ResBlockOffset())
        self.write(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:RBC MAX')
        RBMax = int(self.Get_5GNR_BWP_ResBlock())
        self.Set_5GNR_BWP_ResBlock(RB)
        self.Set_5GNR_BWP_ResBlockOffset(RBO)
        ressy = (SS * 1e3 *12*(RB - RBMax + 2 * RBO))/2 
        return ressy
                 
    #####################################################################
    ### FSW 5GNR DMRS Config
    #####################################################################
    def Get_5GNR_BWP_Ch_DMRS_1stDMRSSym(self):
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:DMRS:TAP?')
        return rdStr
        
    def Get_5GNR_BWP_Ch_DMRS_AddPosition(self):
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:DMRS:MSYM:APOS?')
        return rdStr
        
    def Get_5GNR_BWP_Ch_DMRS_Config(self):
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:DMRS:CTYP?')
        return rdStr
        
    def Get_5GNR_BWP_Ch_DMRS_MSymbLen(self):
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:DMRS:MSYM:LENG?')
        return rdStr
        
    def Get_5GNR_BWP_Ch_DMRS_Mapping(self):
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:DMRS:MTYP?')
        return rdStr
        
    def Get_5GNR_BWP_Ch_DMRS_RelPwr(self):
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:DMRS:POW?')
        return rdStr

    def Get_5GNR_BWP_Ch_DMRS_SeqGenMeth(self):
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:DMRS:SGEN?')
        return rdStr

    def Get_5GNR_BWP_Ch_DMRS_SeqGenSeed(self):
        #Only for SeqGenMeth NICP.  Not Valid for NIDC
        if self.Get_5GNR_BWP_Ch_DMRS_SeqGenMeth() == 'NIDP':
            rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:DMRS:NID?')
        else:
            rdStr = '<!CELL>'
        return rdStr

    def Get_5GNR_BWP_Ch_Modulation(self):
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:MOD?')
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_K(self):
        """ Freq Density in RB """
        if self.Get_5GNR_BWP_Ch_PTRS_State() == '1':
            rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:PTRS:K?')
        else:
            rdStr = "PTRS Off"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_L(self):
        """ Time Density in OFDM Sym Freq """
        if self.Get_5GNR_BWP_Ch_PTRS_State() == '1':
            rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:PTRS:L?')
        else:
            rdStr = "PTRS Off"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_Pow(self):
        if self.Get_5GNR_BWP_Ch_PTRS_State() == '1':
            rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:PTRS:POW?')
        else:
            rdStr = "PTRS Off"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_RE_Offset(self):
        """ PTRS freq (RE) offset """
        if self.Get_5GNR_BWP_Ch_PTRS_State() == '1':
            rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:PTRS:REOF?')
        else:
            rdStr = "PTRS Off"
        return rdStr

    def Get_5GNR_BWP_Ch_PTRS_State(self):
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:PTRS:STAT?')
        return rdStr

    def Get_5GNR_BWP_Ch_ResBlock(self):
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:RBC?')
        return rdStr
        
    def Get_5GNR_BWP_Ch_ResBlockOffset(self):
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:RBOF?')
        return rdStr
        
    def Get_5GNR_BWP_Ch_SymbNum(self):
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:SCO?')
        return rdStr
        
    def Get_5GNR_BWP_Ch_SymbOff(self):
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:SOFF?')
        return rdStr
        
    def Get_5GNR_BWP_Count(self):
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWPC?')
        return rdStr
 
    def Get_5GNR_BWP_ResBlock(self):
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:RBC?')
        return rdStr
        
    def Get_5GNR_BWP_ResBlockOffset(self):
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:RBOF?')
        return rdStr
        
    def Get_5GNR_BWP_SlotNum(self):
        ### Number of slots
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SCO?')
        return rdStr
        
    def Get_5GNR_BWP_SubSpace(self):
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SSP?')
        return rdStr

    def Get_5GNR_ChPwr(self):
        Power = self.queryFloat(f'FETC:CC1:FRAM:SUMM:POW:AVER?')
        return Power
        
    def Get_5GNR_ChannelBW(self):
        ### 5;10;15;20;25;30;40;50;60;70;80;90;100;200;400
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:BW?')
        return rdStr

    def Get_5GNR_CrestFactor(self):
        rdStr = self.queryFloat(f':FETC:SUMM:CRES:AVER?')
        return rdStr

    def Get_5GNR_Direction(self):
        rdStr = self.query(f':CONF:NR5G:LDIR?')
        if rdStr == 'DL':
            self.sdir = "DL"
            self.alloc = 1         #Alloc 0:CORSET
        elif rdStr == 'UL':
            self.sdir = "UL"            
            self.alloc = 0         #Alloc 0:PUSCH
        else:
            print('Get_5GNR_Direction Error')
        return rdStr

    def Get_5GNR_EVM(self):
        EVM = self.queryFloat(f':FETC:CC1:FRAM:SUMM:EVM:ALL:AVER?')
        return EVM

    def Get_5GNR_EVMParams(self):
        Crest = self.Get_5GNR_CrestFactor()
        Power = self.Get_5GNR_ChPwr()
        EVM    = self.Get_5GNR_EVM()
        return (f"{Crest:6.3f},{Power:6.3f},{EVM:.2f}")

    def Get_5GNR_FreqRange(self):
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC{self.CC}:DFR?')
        return rdStr

    def Get_5GNR_Meas_ACLR(self):
        rdStr = self.query(f':CALC:MARK:FUNC:POW:RES? MCAC')
        return rdStr

    def Get_5GNR_RefA(self):
        rdStr = self.queryInt(f':CONF:NR5G:{self.sdir}:CC{self.CC}:RPA:RTCF?')
        return rdStr

    def Get_5GNR_PhaseCompensate(self):
        rdStr = self.query(f':CONF:NR5G:{self.sdir}:CC1:RFUC:STAT?')
        return rdStr

    def Get_5GNR_SEM(self):
        rdStr = self.query(f':CALC1:LIM:FAIL?')
        return rdStr

    def Get_5GNR_SSB_SubSpace(self):
        if self.sdir == 'DL':
            SyncDetStat = self.query(':CONF:NR5G:DL:SSBL1:DET?')
            if SyncDetStat == 'MAN':
                rdStr = self.query(':CONF:NR5G:DL:CC1:SSBL1:SSP?')
            else:
                rdStr = '<Scanng>'
        else:
            rdStr = '<UL n/a>'
        return rdStr
    
    def Get_5GNR_TM_Cat(self):
        rdStr = self.query('MMEM:LOAD:TMOD:CC1:CAT?').split(',')
        return rdStr

    def Get_5GNR_TransPrecoding(self):
        if self.sdir == 'UL':
            rdStr = self.query(':CONF:NR5G:UL:CC1:TPR?')
        else:
            rdStr = '<DL N/A>'
        return rdStr

    #####################################################################
    ### FSW 5GNR Init
    #####################################################################
    def Init_5GNR(self):
        self.Set_Channel('NR5G')
        
    def Init_5GNR_Meas(self,sMeas):
        """ EVM; ESPectrum; ACLR; TAER"""
        self.write('CONF:NR5G:MEAS %s'%sMeas)

    def Init_5GNR_SEM(self):
        self.Set_Channel('NR5G')
        self.write(':CONF:NR5G:MEAs ESP')
        
    #####################################################################
    ### FSW 5GNR Settings
    #####################################################################
    def Set_5GNR_AutoEVM(self):
        self.jav_OPC_Wait(':SENS:ADJ:EVM;*OPC?')
        #self.query(':SENS:ADJ:EVM;*OPC?')
        #self.delay(60)  #timed at 45sec

    def Set_5GNR_AutoRefLvl(self):
        pass

    def Set_5GNR_AllocFile(self,sFilename):
        # \Instr\user\V5GTF\AllocationFiles\UL
        self.write('MMEM:LOAD:DEM "%s"'%sFilename)

    def Set_5GNR_AllocFileSave(self,sFilename):
        self.write(f'MMEM:STOR:DEM:CC1 "C:\\R_S\\Instr\\user\\{sFilename}.allocation"')

    def Set_5GNR_BWP_Ch_Modulation(self,sMod):
        # QPSK; QAM16; QAM64; QAM256; PITB
        self.write(':CONF:NR5G:%s:FRAM1:BWP0:SLOT0:ALL0:MOD %s'%(self.sdir, sMod))

    def Set_5GNR_BWP_Ch_ResBlock(self,iRB):
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        self.write(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:RBC %d'%(self.sdir,iRB))

    def Set_5GNR_BWP_Ch_ResBlockOffset(self,iRBO):
        self.write(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SLOT0:ALL0:RBOF %d'%(self.sdir,iRBO))

    def Set_5GNR_BWP_Corset_ResBlock(self, iRB):
        if self.sdir == 'DL':
            self.write(f':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:COR0:RBC {iRB}')

    def Set_5GNR_BWP_Corset_ResBlockOffset(self,iRBO):
        if self.sdir == 'DL':
            self.write(f':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:COR0:RBOF {iRBO}')
    
    def Set_5GNR_BWP_ResBlock(self,iRB):
        ### RB = (CHBw * 0.95) / (SubSp * 12)
        self.write(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:RBC {iRB}')

    def Set_5GNR_BWP_ResBlockOffset(self,iRBO):
        self.write(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:RBOF {iRBO}')

    def Set_5GNR_BWP_SubSpace(self,iSubSp):
        self.write(f':CONF:NR5G:{self.sdir}:CC{self.CC}:FRAM1:BWP0:SSP SS{iSubSp}')

    def Set_5GNR_CA_Num(self,iNumCC):
        self.write(f'CONF:NR5G:NOCC {iNumCC}')

    def Set_5GNR_CA_Offset(self,iCC, fFreq):
        if iCC > 1:
            self.write(f':SENS:FREQ:CENT:CC{iCC}:OFFS {fFreq}')

    def Set_5GNR_ChannelBW(self,iBW):
        ### 5;10;15;20;25;30;40;50;60;70;80;90;100;200;400
        self.write(f':CONF:NR5G:{self.sdir}:CC{self.CC}:BW BW{iBW}')
        
    def Set_5GNR_Direction(self,sDirection):
        """UL | DL"""
        if (sDirection == "UL") or (sDirection == "UP"):
            self.write(':CONF:NR5G:LDIR UL')
            if self.Get_5GNR_TransPrecoding() == '0':
                self.write(':CONF:NR5G:UL:CC1:IDC ON')
            self.write(':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:FORM 1')     #All UL
            self.sdir = "UL"
        elif (sDirection == "DL") or (sDirection == "DOWN"):
            self.write(':CONF:NR5G:LDIR DL')
            self.write(':CONF:NR5G:DL:CC1:FRAM1:BWP0:SLOT0:FORM 0')     #All DL
            self.write(':CONF:NR5G:DL:CC1:IDC ON')
            self.sdir = "DL"
        else:
            print("Set_5GNR_UL_Direction must be UL or DL")
    
    def Set_5GNR_EVMUnit(self,sUnit):
        #DB or PCT
        self.write('UNIT:EVM %s'%sUnit)

    def Set_5GNR_FreqRange(self,iRange):
        ### 0:<3GHz 1:3-6GHz 2:>6GHz
        ### LOW; MIDD; HIGH
        if (iRange==0) or (iRange == 'LOW'):
            self.write(f':CONF:NR5G:{self.sdir}:CC{self.CC}:DFR LOW')
        elif (iRange==1) or (iRange == 'MIDD'):
            self.write(f':CONF:NR5G:{self.sdir}:CC{self.CC}:DFR MIDD')
        elif (iRange==2) or (iRange == 'HIGH'):
            self.write(f':CONF:NR5G:{self.sdir}:CC{self.CC}:DFR HIGH')
        else:
            print('Set_5GNR_FreqRange invalid parameter')

    def Set_5GNR_Parameters(self,sDir):
        self.Set_5GNR_Direction(sDir)

    def Set_5GNR_PhaseCompensate(self,state):
        """ 'ON' | 'OFF' """
        if (state == "ON") or (state == 1):
            self.write(f':CONF:NR5G:{self.sdir}:CC{self.CC}:RFUC:STAT ON')
        else:
            self.write(f':CONF:NR5G:{self.sdir}:CC{self.CC}:RFUC:STAT OFF')

    def Set_5GNR_savesetting(self, sName):
        self.query(f":MMEM:STOR:DEM:CC{self.CC} 'C:\\R_S\\Instr\\user\\NR5G\\AllocationFiles\\{sName}.allocation';*OPC?")
        
    def Set_5GNR_SEM_Freq(self,fFreq,dSubBlock=1):
        self.write(':SENS:ESP%d:SCEN %f'%(dSubBlock,fFreq))

    def Set_5GNR_SEM_SubBlockNum(self,dSubBlock):
        self.write(':SENS:ESP:SCO %d'%(dSubBlock))

    def Set_5GNR_SubFrameCount(self,dSubFrame):
        self.write(':SENS:NR5G:FRAM:COUN:STAT OFF')
        self.write(':SENS:NR5G:FRAM:SCO %d'%dSubFrame)

    def Set_5GNR_TM(self, file):
        self.query(f'MMEM:LOAD:TMOD:CC{self.CC} "{file}";*OPC?')

    def Set_5GNR_TransPrecoding(self,sState):
        if self.sdir == 'UL':
            self.write(f':CONF:NR5G:UL:CC{self.CC}:TPR {sState}')
        else:
            print('<DL TransPrecoding N/A>')

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    FSW = VSA().jav_Open("192.168.1.109")
    print(FSW.Get_5GNR_EVMParams())
    FSW.Set_5GNR_savesetting('asdf'+'1')
    FSW.jav_ClrErr()
    FSW.jav_Close()
