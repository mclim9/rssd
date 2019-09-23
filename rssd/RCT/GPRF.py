# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose : Radio Communication Tester(RCT) General Purpose RF (GPRF) Functions
### Author  : Martin C Lim
### Date    : 2018.05.29
###############################################################################
from rssd.yaVISA import jaVisa

class BSE(jaVisa):
    """ Rohde & Schwarz Base Station Emulator Object """
    def __init__(self):
        super(BSE, self).__init__()
        self.Model = "CMW-GPRF"

    ###########################################################################
    ### CMW Get Functions
    ###########################################################################
    def Get_Meas_ACLR(self):
        ACLR = self.query('FETC:NRS:MEAS:MEV:ACLR:AVER?').split(',')
        return ACLR

    def Get_Meas_ChPwr(self):                                               #Val
        out = self.queryFloat('FETC:GPRF:MEAS:POW:CURR?')
        return out 

    def Get_VSG_ArbWv(self):
        SCPI = self.query('SOUR:GPRF:GEN:ARB:FILE?')
        return SCPI

    ###########################################################################
    ### CMW Init Functions
    ###########################################################################
    def Init_Gen(self,port=1):                                              #Val
        self.write('ROUTe:GPRF:GEN:SCENario:SALone R118, TX11')
        self.write('CONF:GPRF:GEN:CMWS:USAGe:TX:ALL R118, OFF, OFF,OFF, OFF, OFF, OFF, OFF, OFF')

    def Init_MeasFFT(self,port=1):                                          #Val
        self.write('ROUT:GPRF:MEAS:SCEN:SAL R1{port}, RX1'%port)
        self.write('INIT:GPRF:MEAS:FFTS')

    def Init_MeasPower(self,port=1):                                        #Val
        self.write('ROUT:GPRF:MEAS:SCEN:SAL R1{port}, RX1'%port)
        self.write('INIT:GPRF:MEAS:POW')
        self.write('CONF:GPRF:MEAS:POW:MODE POW')      #POW|STAT

    def Init_MeasVSA(self,port=1):                                          #Val
        self.write(f'ROUT:GPRF:MEAS:SCEN:SAL R1{port}, RX1')
        
    ###########################################################################
    ### CMW Init Functions
    ###########################################################################
    def Set_Gen_ArbMode(self):
        self.query('SOUR:GPRF:GEN:BBM ARB;*OPC?')

    def Set_Gen_ArbWv(self,sName):
        #self.write(':SOUR:GPRF:GEN:ARB:FILE 'C:\ProgramData\Rohde-Schwarz\CMW\Data\waveform\NRsub6G_ARB_Waveforms\NR_CP_SCS30kHz_BW20MHz_16-QAM_cellID3.wv')
        self.write(f":SOUR:GPRF:GEN:ARB:FILE '{sName}'")

    def Set_Gen_Freq(self,freq):                                            #Val
        self.write(f'SOUR:GPRF:GEN:RFS:FREQ {freq}')

    def Set_Gen_ListMode(self,sState):
        if sState.upper() == "ON":
            self.query('SOUR:GPRF:GEN:LIST ON;*OPC?')
        else:
            self.query('SOUR:GPRF:GEN:LIST OFF;*OPC?')

    def Set_Gen_PortOFF(self,port=1):
        self.write(f'CONFigure:GPRF:GEN:CMWS:USAGe:TX R1{port}, OFF')
        
    def Set_Gen_PortON(self,port=1):
        self.write(f'CONFigure:GPRF:GEN:CMWS:USAGe:TX R1{port}, ON')

    def Set_Gen_RFPwr(self,fPwr):                                           #Val
        self.write('SOUR:GPRF:GEN:RFS:LEV %f'%(fPwr))

    def Set_Gen_RFState(self,sState):                                       #Val
        """ ON | OFF """
        if sState.upper() == "ON":
            self.query('SOUR:GPRF:GEN:STAT ON;*OPC?')
        else:
            self.query('SOUR:GPRF:GEN:STAT OFF;*OPC?')

    def Set_Meas_Freq(self,fFreq):                                          #Val
        # self.write('CONF:GPRF:MEAS:SPEC:FREQ:CENT %d'%fFreq)
        self.write('CONF:GPRF:MEAS:RFS:FREQ %d'%fFreq)

    def Set_Meas_InitImm(self):
        #self.query('INIT:GPRF:MEAS:SPEC;*OPC?')
        self.query('INIT:GPRF:MEAS:;*OPC?')
    
    def Set_Meas_RefLevl(self,fRefLvl):                                     #Val
        ### ENP = Expected Nominal Power
        self.write('CONF:GPRF:MEAS:RFS:ENP %f'%fRefLvl)

    def Set_Meas_ResBW(self,fFreq):
        if fFreq > 0:
            self.write('CONF:GPRF:MEAS:SPEC:FSW:RBW %f'%fFreq)
        else:
            self.write('CONF:GPRF:MEAS:SPEC:FSW:RBW:AUTO ON')
            
    def Set_Meas_Span(self,fFreq):
        self.write('CONF:GPRF:MEAS:SPEC:FREQ:SPAN %f'%fFreq)

    def Set_Meas_SweepTime(self,fTime):
        if fTime > 0:
            self.write('CONF:GPRF:MEAS:SPEC:FSW:SWT %f'%fTime)
        else:
            self.write('CONF:GPRF:MEAS:SPEC:FSW:SWT:AUTO ON')
            
    def Set_Meas_VidBW(self,fFreq):
        if fFreq > 0:
            self.write('CONF:GPRF:MEAS:SPEC:FSW:VBW %f'%fFreq)
        else:
            self.write('CONF:GPRF:MEAS:SPEC:FSW:VBW:AUTO ON')

    ###########################################################################
    ### CMW Generator
    ###########################################################################
    def Set_Sys_DisplayUpdate(self,state):
        self.write('SYST:DISP:UPD %s'%state)      #Display Update State

    def Set_Sys_RxPortLoss(self,port=1,fLoss=0):                           #Val
        self.write(f"CONF:CMWS:FDC:DEAC:RX R1{port}")
        self.write(f"CONF:BASE:FDC:CTAB:CRE 'In{port}',70.0e6,{fLoss},6000.e6,{fLoss}")
        self.write(f"CONF:CMWS:FDC:ACT:RX R1{port},'In{port}'")

    def Set_Sys_TxPortLoss(self,port=1,fLoss=0):                           #Val
        #CONF:BASE:FDC:CTAB:CRE 'downlink', 500.0e6,0.5, 1000e6,1.0, 1800.e6,1.5, 2300.e6,1.8, 5000.e6,2.5,  6000.e6,2.8
        self.write(f"CONF:CMWS:FDC:DEAC:TX R1{port}")
        self.write(f"CONF:BASE:FDC:CTAB:CRE 'Out{port}',70.0e6,{fLoss},6000.e6,{fLoss}")
        self.write(f"CONF:CMWS:FDC:ACT:TX R1{port},'Out{port}'")

###############################################################################
### Run if Main
###############################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    CMW = BSE()
    CMW.jav_Open("192.168.1.160")
    print(CMW.Get_Meas_ACLR())
    CMW.jav_Close()
