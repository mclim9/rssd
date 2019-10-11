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
    def Get_Meas_IQ_Srate(self):
        """Sampling Rate, Hz"""
        rdStr = self.query('FETC:GPRF:MEAS:IQR:SRAT?')
        return rdStr

    def Get_Meas_IQ_Data(self):
        rdStr = self.query('READ:GPRF:MEAS:IQR?')
        return rdStr

    ###########################################################################
    ### RCT Init Functions
    ###########################################################################
    def Init_Meas_IQCapture(self,port=1):
        self.write('ABOR:GPRF:MEAS:IQR')
        self.write('INIT:GPRF:MEAS:IQR')

    ###########################################################################
    ### RCT INIT Functions
    ###########################################################################
    def Set_Meas_IQ_Filename(self,filename):
        """FIle to save IQW data to"""
        self.write(f'CONF:GPRF:MEAS:IQR:IQF {filename}')

    def Set_Meas_IQ_Format(self):
        """"Binary: 4bytes per value little-endian, LSB first"""
        self.write('FORM:BASE:DATA ')

    def Set_Meas_IQ_Length(self,length):
        """Number of IQ samples to capture"""
        self.write(f'CONF:GPRF:MEASIQR:CAPT {length}')

    def Set_Meas_IQ_Srate(self,freq):
        """Sampling Rate, Hz"""
        self.write(f'FETC:GPRF:MEAS:IQR:SRAT {freq}')

###############################################################################
### Run if Main
###############################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    CMW = RCT()
    CMW.jav_Open("192.168.1.160")
    CMW.Init_Meas_IQCapture()
    print(CMW.Get_Meas_IQ_Srate())
    CMW.jav_Close()