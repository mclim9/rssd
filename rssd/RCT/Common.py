# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Radio Communication Tester(RCT) Functions
### Author : Martin C Lim
### Date   : 2018.05.29
###############################################################################
from rssd.yaVISA import jaVisa              #pylint: disable=E0611,E0401

class RCT(jaVisa):
    """ Rohde & Schwarz Base Station Emulator Object """
    def __init__(self):
        super(RCT, self).__init__()
        self.Model = "CMW-GPRF"

    ###########################################################################
    ### BSE Get Functions
    ###########################################################################
    def Get_Gen_ArbWv(self):                                                    #val
        rdStr = self.query('SOUR:GPRF:GEN:ARB:FILE?')
        return rdStr

    def Get_Gen_Port(self):                                                     #val
        rdStr = self.query('ROUT:GPRF:GEN:SPAT?')
        return rdStr

    def Get_Meas_Power(self):                                                   #Val
        rdStr   = -9999
        num     = 0
        while (rdStr == -9999) and (num < 10):
            num += 1
            try:
                self.write('INIT:GPRF:MEAS:POW')                                #RUN state
                self.query('*OPC?')
                rdStr = self.queryFloatArry('FETC:GPRF:MEAS:POW:AVER?')[1]      # Doesnt Clr Memory
                # rdStr = self.query('READ:GPRF:MEAS:POW:AVER?')                # Clears Memory
                # rdStr = self.query('CALC:GPRF:MEAS:POW:AVER?')                # Chk Limits
            except:
                print(f'CMP.Get_Meas_Power{num}')
        return rdStr

    def Get_Meas_Port(self):                                                    #Val
        rdStr = self.query('ROUT:GPRF:MEAS:SPAT?')
        return rdStr

    def Get_Options(self):
        rdStr = self.query('SYST:BASE:OPT:LIST?').split(',')
        return rdStr

    ###########################################################################
    ### BSE Init Functions
    ###########################################################################
    def Init_Syst(self):
        self.write('SYST:GEN:ALL:OFF')
        self.write('SYST:MEAS:ALL:OFF')

    ###########################################################################
    ### RCT Init Functions
    ###########################################################################
    def Init_Gen(self,port=1):                                                  #Val
        # self.write('ROUT:GPRF:GEN:SCENario:SALone R118, TX11')
        self.Set_Gen_Port(port)
        self.write('CONF:GPRF:GEN:CMWS:USAGe:TX:ALL R118, OFF, OFF,OFF, OFF, OFF, OFF, OFF, OFF')

    def Init_Meas_FFT(self,port=1):                                             #Val
        # self.write('ROUT:GPRF:MEAS:SCEN:SAL R1{port}, RX1'%port)
        self.Set_Meas_Port(port)
        self.write('INIT:GPRF:MEAS:FFTS')

    def Init_Meas_Power(self,port=1):                                           #Val
        # self.write('ROUT:GPRF:MEAS:SCEN:SAL R1{port}, RX1'%port)
        self.Set_Meas_Port(port)
        self.write('FORMAT:BASE:DATA ASCII')
        self.write('INIT:GPRF:MEAS:POW')
        self.write('CONF:GPRF:MEAS:POW:MODE POW')      #POW|STAT

    ###########################################################################
    ### RCT INIT Functions
    ###########################################################################
    def Set_Gen_ArbExec(self):
        self.query('TRIG:GPRF:GEN:ARB:MAN:EXEC')

    def Set_Gen_ArbWv(self,sName):
        self.write(f":SOUR:GPRF:GEN:ARB:FILE '@Waveform/{sName}'")

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

    def Set_Gen_Port(self, port):                                               #Val
        """ CMP: 'P<x>.IFOut' | 'P<x>.RRH.RF<y>'"""
        self.write(f'ROUT:GPRF:GEN:SPAT "{port}"')

    def Set_Gen_Port_State(self,port=1,state='ON'):                             #val
        """ 'ON' 'OFF' """
        if state == 'ON':
            self.write(f'CONFigure:GPRF:GEN:CMWS:USAGe:TX R1{port}, ON')
        else:
            self.write(f'CONFigure:GPRF:GEN:CMWS:USAGe:TX R1{port}, OFF')

    def Set_Gen_RFPwr(self,fPwr):                                               #Val
        self.write(f'SOUR:GPRF:GEN:RFS:LEV {fPwr}')

    def Set_Gen_RFState(self,sState):                                           #Val
        """ ON | OFF """
        if sState.upper() == "ON":
            self.query('SOUR:GPRF:GEN:STAT ON;*OPC?')
        else:
            self.query('SOUR:GPRF:GEN:STAT OFF;*OPC?')

    def Set_Meas_Autolevel(self):
        self.Init_Meas_Power()
        self.Set_Meas_UserMargin(0)
        self.Set_Meas_Expected_Nom_Power(40)
        pwr = self.Get_Meas_Power()
        print(pwr)
        self.Set_Meas_Expected_Nom_Power(pwr + 2)

    def Set_Meas_RFBW(self,fFreq):
        """Expected RF BW"""
        self.write(f'CONF:GPRF:MEAS:POW:FILT:TYPE BAND')
        self.write(f'CONF:GPRF:MEAS:POW:FILT:BAND:BWID  {fFreq}')

    def Set_Meas_Expected_Nom_Power(self,fPwr):
        """Expected Nominal Power (RMS)"""
        self.write(f'CONFigure:GPRF:MEAS:RFSettings:ENPower {fPwr}')

    def Set_Meas_Freq(self,fFreq):                                              #Val
        # self.write('CONF:GPRF:MEAS:SPEC:FREQ:CENT %d'%fFreq)
        self.write(f'CONF:GPRF:MEAS:RFS:FREQ {fFreq}')

    # def Set_Meas_InitImm(self):
    #     #self.query('INIT:GPRF:MEAS:SPEC;*OPC?')
    #     self.query('INIT:GPRF:MEAS:;*OPC?')

    def Set_Meas_Port(self, port):
        """ CMP: 'P<x>.IFIn' | 'P<x>.RRH.RF<y>'"""
        self.write(f'ROUT:GPRF:MEAS:SPAT "{port}"')

    def Set_Meas_Pwr_MLength(self,length):
        self.write(f'CONF:GPRF:MEAS:POW:SLEN {length}')
        self.write(f'CONF:GPRF:MEAS:POW:MLEN {length}')

    def Set_Meas_RefLevl(self,fRefLvl):                                         #Val
        ### ENP = Expected Nominal Power
        self.write(f'CONF:GPRF:MEAS:RFS:ENP {fRefLvl}')

    def Set_Meas_Span(self,fFreq):
        """ 10; 20; 40; 80; 160; 250; 500; 1000 MHz allowed """
        self.write(f'CONF:GPRF:MEAS:FFTS:FSP {fFreq}')

    def Set_Meas_SweepTime(self,fTime):
        if fTime > 0:
            self.write(f'CONF:GPRF:MEAS:SPEC:FSW:SWT {fTime}')
        else:
            self.write(f'CONF:GPRF:MEAS:SPEC:FSW:SWT:AUTO ON')

    def Set_Meas_TriggerSource(self,source):
        """string: IF Power Free Run """
        self.write(f'TRIG:GPRF:MEAS:POW:SOUR "{source}"')

    def Set_Meas_TriggerThreshold(self,num):
        """ -50 to 0 """
        self.write(f'TRIG:GPRF:MEAS:POW:THR {num}')

    def Set_Meas_UserMargin(self,fPwr):
        """User Margin (Crest Factor)"""
        self.write(f'CONFigure:GPRF:MEAS:RFSettings:UMARgin {fPwr}')

    def Set_Sys_DisplayUpdate(self,state):
        self.write('SYST:DISP:UPD %s'%state)                                #Display Update State

    def Set_Sys_RxPortLoss(self,port=1,fLoss=0):                            #Val
        self.write(f"CONF:CMWS:FDC:DEAC:RX R1{port}")
        self.write(f"CONF:BASE:FDC:CTAB:CRE 'In{port}',70.0e6,{fLoss},6000.e6,{fLoss}")
        self.write(f"CONF:CMWS:FDC:ACT:RX R1{port},'In{port}'")

    def Set_Sys_TxPortLoss(self,port=1,fLoss=0):                            #Val
        #CONF:BASE:FDC:CTAB:CRE 'downlink', 500.0e6,0.5, 1000e6,1.0, 1800.e6,1.5, 2300.e6,1.8, 5000.e6,2.5,  6000.e6,2.8
        self.write(f"CONF:CMWS:FDC:DEAC:TX R1{port}")
        self.write(f"CONF:BASE:FDC:CTAB:CRE 'Out{port}',70.0e6,{fLoss},6000.e6,{fLoss}")
        self.write(f"CONF:CMWS:FDC:ACT:TX R1{port},'Out{port}'")

###############################################################################
### Run if Main
###############################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    CMW = RCT()
    CMW.jav_Open("192.168.1.160")
    print(CMW.Get_Meas_Power())
    CMW.jav_Close()
