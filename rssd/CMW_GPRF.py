# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose : CMW100 General Purpose RF Functions
### Author  : Martin C Lim
### Date    : 2018.05.29
#####################################################################
from rssd.yaVISA import jaVisa

class BSE(jaVisa):
     """ Rohde & Schwarz Base Station Emulator Object """
    def __init__(self):
        super(BSE, self).__init__()
        self.Model = "CMW-GPRF"

    #####################################################################
    ### CMW System
    #####################################################################
    def Set_DisplayUpdate(self,state):
        self.write('SYST:DISP:UPD %s'%state);      #Display Update State
                
    #####################################################################
    ### CMW Port Configuration
    #####################################################################
    def Set_Sys_TxPortLoss(self,dPort=1,fLoss=0):                        #Val
        #CONF:BASE:FDC:CTAB:CRE 'downlink', 500.0e6,0.5, 1000e6,1.0, 1800.e6,1.5, 2300.e6,1.8, 5000.e6,2.5,  6000.e6,2.8
        self.write("CONF:CMWS:FDC:DEAC:TX R1%d"%dPort)
        self.write("CONF:BASE:FDC:CTAB:CRE 'Out%d',70.0e6,%f,6000.e6,%f"%(dPort,fLoss,fLoss))
        self.write("CONF:CMWS:FDC:ACT:TX R1%d,'Out%d'"%(dPort,dPort))
        
    def Set_Sys_RxPortLoss(self,dPort=1,fLoss=0):                                             #Val
        self.write("CONF:CMWS:FDC:DEAC:RX R1%d"%dPort)
        self.write("CONF:BASE:FDC:CTAB:CRE 'In%d',70.0e6,%f,6000.e6,%f"%(dPort,fLoss,fLoss))
        self.write("CONF:CMWS:FDC:ACT:RX R1%d,'In%d'"%(dPort,dPort))
        
    #####################################################################
    ### CMW Vector Spectrum Analyzer
    #####################################################################
    def Init_MeasVSA(self,port=1):                                                 #Val
        self.write('ROUT:GPRF:MEAS:SCEN:SAL R1%d, RX1'%port)
        
    def Init_MeasPower(self,port=1):                                              #Val
        self.write('ROUT:GPRF:MEAS:SCEN:SAL R1%d, RX1'%port)
        self.write('INIT:GPRF:MEAS:POW')
        self.write('CONF:GPRF:MEAS:POW:MODE POW')      #POW|STAT
        
    def Init_MeasFFT(self,port=1):                                              #Val
        self.write('ROUT:GPRF:MEAS:SCEN:SAL R1%d, RX1'%port)
        self.write('INIT:GPRF:MEAS:FFTS')

    def Get_VSA_ACLR(self):
        ACLR = self.query('FETC:NRS:MEAS:MEV:ACLR:AVER?').split(',')
        return ACLR

    def Get_ChPwr(self):                                                         #Val
        out = self.queryFloat('FETC:GPRF:MEAS:POW:CURR?')
        return out 
    
    def Set_VSA_Freq(self,fFreq):                                             #Val
#        self.write('CONF:GPRF:MEAS:SPEC:FREQ:CENT %d'%fFreq)
        self.write('CONF:GPRF:MEAS:RFS:FREQ %d'%fFreq)

    def Set_VSA_FreqSpan(self,fFreq):
        self.write('CONF:GPRF:MEAS:SPEC:FREQ:SPAN %f'%fFreq)

    def Set_VSA_RefLevl(self,fRefLvl):                                      #Val
        ### ENP = Expected Nominal Power
        self.write('CONF:GPRF:MEAS:RFS:ENP %f'%fRefLvl)

    def Set_VSA_InitImm(self):
        #self.query('INIT:GPRF:MEAS:SPEC;*OPC?')
        self.query('INIT:GPRF:MEAS:;*OPC?')
    
    def Set_VSA_ResBW(self,fFreq):
        if fFreq > 0:
            self.write('CONF:GPRF:MEAS:SPEC:FSW:RBW %f'%fFreq)
        else:
            self.write('CONF:GPRF:MEAS:SPEC:FSW:RBW:AUTO ON')
            
    def Set_VSA_VidBW(self,fFreq):
        if fFreq > 0:
            self.write('CONF:GPRF:MEAS:SPEC:FSW:VBW %f'%fFreq)
        else:
            self.write('CONF:GPRF:MEAS:SPEC:FSW:VBW:AUTO ON')
    
    def Set_VSA_SweepTime(self,fTime):
        if fTime > 0:
            self.write('CONF:GPRF:MEAS:SPEC:FSW:SWT %f'%fTime)
        else:
            self.write('CONF:GPRF:MEAS:SPEC:FSW:SWT:AUTO ON')
            
    #####################################################################
    ### CMW Generator
    #####################################################################
    def Init_VSG(self,port=1):                                                 #Val
        self.write('ROUTe:GPRF:GEN:SCENario:SALone R118, TX11')
        self.write('CONFigure:GPRF:GEN:CMWS:USAGe:TX:ALL R118, OFF, OFF,OFF, OFF, OFF, OFF, OFF, OFF')

    def Set_Gen_PortON(self,port=1):
        self.write('CONFigure:GPRF:GEN:CMWS:USAGe:TX R1%d, ON'%port)

    def Set_Gen_PortOFF(self,port=1):
        self.write('CONFigure:GPRF:GEN:CMWS:USAGe:TX R1%d, OFF'%port)
        
    def Get_Gen_ArbWv(self):
        SCPI = self.query('SOUR:GPRF:GEN:ARB:FILE?')
        return SCPI

    def Set_Gen_ArbWv(self,sName):
        #self.write(':SOUR:GPRF:GEN:ARB:FILE 'C:\ProgramData\Rohde-Schwarz\CMW\Data\waveform\NRsub6G_ARB_Waveforms\NR_CP_SCS30kHz_BW20MHz_16-QAM_cellID3.wv')
        self.write(":SOUR:GPRF:GEN:ARB:FILE '%s'"%sName)

    def Set_Gen_ArbStateOn(self):
        self.query('SOUR:GPRF:GEN:BBM ARB;*OPC?')

    def Set_Gen_Freq(self,freq):                                              #Val
        self.write('SOUR:GPRF:GEN:RFS:FREQ %f'%freq);     #RF Freq

    def Set_Gen_ListMode(self,sState):
        if sState.upper() == "ON":
            self.query('SOUR:GPRF:GEN:LIST ON;*OPC?')
        else:
            self.query('SOUR:GPRF:GEN:LIST OFF;*OPC?')

    def Set_Gen_RFPwr(self,fPwr):                                             #Val
        self.write('SOUR:GPRF:GEN:RFS:LEV %f'%(fPwr));

    def Set_Gen_RFState(self,sState):                                        #Val
        ### ON | OFF
        if sState.upper() == "ON":
            self.query('SOUR:GPRF:GEN:STAT ON;*OPC?')
        else:
            self.query('SOUR:GPRF:GEN:STAT OFF;*OPC?')
            
#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    CMW = BSE()
    CMW.jav_Open("127.0.0.1")
