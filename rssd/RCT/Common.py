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
    ### BSE Set Functions
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
    CMW = RCT()
    CMW.jav_Open("192.168.1.160")
    CMW.Init_Syst()
    print(CMW.Get_Options())
    CMW.jav_Close()
