# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Digital Storage Oscilloscope Spectrum Analysis Methods
### Author : Martin C Lim
### Date   : 2020.03.24
###
###############################################################################
from rssd.DSO.Common import DSO

class DSO(DSO):
    """ Rohde & Schwarz Digital Storage Oscilloscope Object """
    def __init__(self):
        super(DSO, self).__init__()

    #####################################################################
    ### DSO Get Functions
    #####################################################################
    def Get_SA_AcqTime(self):
        """ Seconds """
        rdStr = self.query(':TIM:RANG?')
        return rdStr

    #####################################################################
    ### DSO Init Functions
    #####################################################################
    def Init_SpecAn(self):
        #Configure instrument measurment
        pass

    #####################################################################
    ### DSO Set Functions
    #####################################################################
    def Set_SA_AcqTime(self, sec):
        """ Seconds """
        self.write(f':TIM:RANG {sec}')

###############################################################################
### Debug Main.  Won't run when imported
###############################################################################
if __name__ == "__main__":
    DSO_Inst = DSO().jav_Open("192.168.1.100")
    DSO_Inst.jav_IDN()
    DSO_Inst.jav_ClrErr()
