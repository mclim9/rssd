# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Radio Communication Tester(RCT) General Purpose RF(GPRF) Functions
### Author : Martin C Lim
### Date   : 2018.05.29
###############################################################################
from rssd.RCT.Common import RCT              #pylint: disable=E0611,E0401

class RCT(RCT):
    """ Rohde & Schwarz Radio Comm Tester Object """
    def __init__(self):
        super(RCT, self).__init__()
        self.Model = "CMW-GPRF"

    ###########################################################################
    ### RCT Get Functions
    ###########################################################################
    def Get_Gen_ArbWv(self):                                                #val
        rdStr = self.query('SOUR:GPRF:GEN:ARB:FILE?')
        return rdStr

    def Get_Gen_Port(self):                                                 #val
        rdStr = self.query('ROUT:GPRF:GEN:SPAT?')
        return rdStr

    def Get_Meas_ChPwr_RMS(self):                                           #Val
        # out = self.queryFloat('FETC:GPRF:MEAS:POW:CURR?')
        # out = self.queryFloat('FETC:GPRF:MEAS:FFTS:POW:AVER?')
        out = self.query('FETC:GPRF:MEAS:POW:CURR?')
        return out 

    def Get_Meas_Port(self):                                                #Val
        rdStr = self.query('ROUT:GPRF:MEAS:SPAT?')
        return rdStr

    ###########################################################################
    ### RCT Init Functions
    ###########################################################################
    def Init_Gen(self,port=1):                                              #Val
        self.write('ROUT:GPRF:GEN:SCENario:SALone R118, TX11')
        self.write('CONF:GPRF:GEN:CMWS:USAGe:TX:ALL R118, OFF, OFF,OFF, OFF, OFF, OFF, OFF, OFF')

    def Init_Meas_FFT(self,port=1):                                          #Val
        self.write('ROUT:GPRF:MEAS:SCEN:SAL R1{port}, RX1'%port)
        self.write('INIT:GPRF:MEAS:FFTS')

    def Init_Meas_Power(self,port=1):                                        #Val
        self.write('ROUT:GPRF:MEAS:SCEN:SAL R1{port}, RX1'%port)
        self.write('INIT:GPRF:MEAS:POW')
        self.write('CONF:GPRF:MEAS:POW:MODE POW')      #POW|STAT

    ###########################################################################
    ### RCT INIT Functions
    ###########################################################################
    def Set_Gen_ArbExec(self):
        self.query('TRIG:GPRF:GEN:ARB:MAN:EXEC')

    def Set_Gen_ArbWv(self,sName):
        #self.write(':SOUR:GPRF:GEN:ARB:FILE 'C:\ProgramData\Rohde-Schwarz\CMW\Data\waveform\NRsub6G_ARB_Waveforms\NR_CP_SCS30kHz_BW20MHz_16-QAM_cellID3.wv')
        self.write(f":SOUR:GPRF:GEN:ARB:FILE '@Waveform\{sName}'")

    def Set_Gen_Freq(self,freq):
        self.write(f'SOUR:GPRF:GEN:RFS:FREQ {freq}')

    def Set_Gen_ListMode(self,sState):
        if sState.upper() == "ON":
            self.query('SOUR:GPRF:GEN:LIST ON;*OPC?')
        else:
            self.query('SOUR:GPRF:GEN:LIST OFF;*OPC?')

    def Set_Gen_Mode(self, mode):
        """ 'CW', 'ARB' or 'DTONE' """
        self.write(f'SOUR:GPRF:GEN:BBM {mode}')

    def Set_Gen_Port(self, port):                                           #Val
        """ CMP: 'P<x>.IFOut' | 'P<x>.RRH.RF<y>'"""
        rdStr = self.write(f'ROUT:GPRF:GEN:SPAT "{port}"')
        return rdStr

    def Set_Gen_Port_State(self,port=1,state='ON'):                         #val
        """ 'ON' 'OFF' """
        if state == 'ON':
            self.write(f'CONFigure:GPRF:GEN:CMWS:USAGe:TX R1{port}, ON')
        else:
            self.write(f'CONFigure:GPRF:GEN:CMWS:USAGe:TX R1{port}, OFF')

    def Set_Gen_RFPwr(self,fPwr):                                           #Val
        self.write(f'SOUR:GPRF:GEN:RFS:LEV {fPwr}')

    def Set_Gen_RFState(self,sState):                                       #Val
        """ ON | OFF """
        if sState.upper() == "ON":
            self.query('SOUR:GPRF:GEN:STAT ON;*OPC?')
        else:
            self.query('SOUR:GPRF:GEN:STAT OFF;*OPC?')

    def Set_Meas_Freq(self,fFreq):                                          #Val
        # self.write('CONF:GPRF:MEAS:SPEC:FREQ:CENT %d'%fFreq)
        self.write(f'CONF:GPRF:MEAS:RFS:FREQ {fFreq}')

    def Set_Meas_InitImm(self):
        #self.query('INIT:GPRF:MEAS:SPEC;*OPC?')
        self.query('INIT:GPRF:MEAS:;*OPC?')

    def Set_Meas_Port(self, port):
        """ CMP: 'P<x>.IFIn' | 'P<x>.RRH.RF<y>'"""
        rdStr = self.write(f'ROUT:GPRF:MEAS:SPAT "{port}"')
        return rdStr

    def Set_Meas_RefLevl(self,fRefLvl):                                     #Val
        ### ENP = Expected Nominal Power
        self.write('CONF:GPRF:MEAS:RFS:ENP %f'%fRefLvl)

    # def Set_Meas_ResBW(self,fFreq):
    #     if fFreq > 0:
    #         self.write('CONF:GPRF:MEAS:SPEC:FSW:RBW %f'%fFreq)
    #     else:
    #         self.write('CONF:GPRF:MEAS:SPEC:FSW:RBW:AUTO ON')
            
    def Set_Meas_Span(self,fFreq):
        """ 10; 20; 40; 80; 160; 250; 500; 1000 MHz allowed """
        self.write('CONF:GPRF:MEAS:FFTS:FSP %f'%fFreq)

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

###############################################################################
### Run if Main
###############################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    CMW = RCT()
    CMW.jav_Open("192.168.1.160")
    CMW.Set_Gen_Freq(6000)
    print(CMW.Get_Meas_ChPwr_RMS())
    CMW.jav_Close()