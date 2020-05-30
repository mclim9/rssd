# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Digital Storage Oscilloscope Common Functions
### Author : Martin C Lim
### Date   : 2019.05.28
###  _____  _____   ____ _______ ____ _________     _______  ______
### |  __ \|  __ \ / __ \__   __/ __ \__   __\ \   / /  __ \|  ____|
### | |__) | |__) | |  | | | | | |  | | | |   \ \_/ /| |__) | |__
### |  ___/|  _  /| |  | | | | | |  | | | |    \   / |  ___/|  __|
### | |    | | \ \| |__| | | | | |__| | | |     | |  | |    | |____
### |_|    |_|  \_\\____/  |_|  \____/  |_|     |_|  |_|    |______|
###                         _            _           _
###                        | |          | |         | |
###             _   _ _ __ | |_ ___  ___| |_ ___  __| |
###            | | | | '_ \| __/ _ \/ __| __/ _ \/ _` |
###            | |_| | | | | ||  __/\__ \ ||  __/ (_| |
###             \__,_|_| |_|\__\___||___/\__\___|\__,_|
###
###############################################################################
from rssd.yaVISA import jaVisa

class DSO(jaVisa):
    """ Rohde & Schwarz Digital Storage Oscilloscope Object """
    def __init__(self):
        super(DSO, self).__init__()
        self.Model = "DSO"

    #####################################################################
    ### DSO Get Functions
    #####################################################################
    def Get_AcqTime(self):
        """ Seconds """
        rdStr = self.query(f':TIM:RANG?')
        return rdStr

    def Get_ChState(self, Ch=1):
        rdStr = self.query(f':CHAN{Ch}:STAT?')
        return rdStr

    def Get_SamplingRate(self):
        """ MHz? """
        rdStr = self.query(f':ACQ:SRR?')
        return rdStr

    def Get_TimeRes(self):
        """ Seconds """
        rdStr = self.query(f':ACQ:RES?')
        return rdStr

    def Get_TimeScale(self):
        """ Seconds """
        rdStr = self.query(f':TIM:SCAL?')
        return rdStr

    def Get_Trace(self,Ch,Wave):
        """ ASCII Trace """
        self.write(f'FORM ASCII')
        YVals = self.query(f':CHAN{Ch}:WAV{Wave}:DATA?')
        Headr = self.queryFloatArry(f':CHAN{Ch}:WAV{Wave}:DATA:HEAD?')
        # Start = Headr[0]
        # Stops = Headr[1]
        # Sampl = Headr[2]
        return YVals, Headr

    #####################################################################
    ### DSO Init Functions
    #####################################################################
    def Init_Measurement(self):
        #Configure instrument measurment
        pass

    #####################################################################
    ### DSO Set Functions
    #####################################################################
    def Set_AcqTime(self,sec):
        """ Seconds """
        self.write(f':TIM:RANG {sec}')

    def Set_ChCoupling(self,state, Ch=1):
        """ AC DC DCL """
        self.write(f':CHAN{Ch}:COUP {state}')        #Display Update State

    def Set_ChStatus(self,state, Ch=1):
        """ ON OFF """
        self.write(f':CHAN{Ch}:STAT {state}')        #Display Update State

    def Set_DisplayUpdate(self,state):
        """ ON OFF """
        self.write(f'SYST:DISP:UPD {state}')        #Display Update State

    def Set_SweepCont(self, state):
        """ ON OFF """
        if ('ON' in state.upper()) or (state == 1):
            self.write(f'RUN')                      #Continuous
        else:
            self.write(f'SING')                     #Single

    def Set_TimeRef(self,sec):
        """ Seconds """
        self.write(f':TIM:REF {sec}')

    def Set_TimeScale(self,sec):
        """ Seconds """
        self.write(f':TIM:SCAL {sec}')

    def Set_TimeRes(self,sec):
        """ Seconds """
        self.write(f':ACQ:RES {sec}')

    def Set_VoltOffset(self,volt, Ch=1):
        """ Volts """
        self.write(f':CHAN{Ch}:OFFS {volt}')

    def Set_VoltRange(self,volt, Ch=1):
        """ Volts """
        self.write(f':CHAN{Ch}:RANG {volt}')

    def Set_VoltScale(self,volt, Ch=1):
        """ Volts """
        self.write(f':CHAN{Ch}:SCAL {volt}')

###############################################################################
### Debug Main.  Won't run when imported
###############################################################################
if __name__ == "__main__":
    DSO_Inst = DSO().jav_Open("192.168.1.100")
    DSO_Inst.jav_IDN()
    DSO_Inst.jav_ClrErr()
