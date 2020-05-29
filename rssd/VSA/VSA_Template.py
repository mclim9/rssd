# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Vector Signal Analyzer Common Functions
### Author:  Martin C Lim
### Date:    2018.03.12
#####################################################################
from rssd.VSA.Common import VSA        #pylint: disable=E0611,E0401

class VSA(VSA):                        #pylint: disable=E0102
    """ Rohde & Schwarz Vector Signal Analyzer Object """
    def __init__(self):
        super(VSA, self).__init__()
        self.WLAN_Std  = 'N'
        self.WLAN_ChBW = 100       #MHz
        self.WLAN_MCS  = 1

    #####################################################################
    ### VSA Query Methods
    #####################################################################
    def Get_ACLR(self):
        """Input Parameters"""
        ACLR = self.queryFloatArry(':CALC:MARK:FUNC:POW:RES? MCAC')
        return ACLR

    #####################################################################
    ### Init Methods
    #####################################################################
    def Init_WLAN(self):
        """Input Parameters"""
        self.Set_Channel('WLAN')
        self.write(':SENS:DEM:FORM:BCON:AUTO 1')            #Auto PPDU Demod

    #####################################################################
    ### VSA Set Methods
    #####################################################################
    def Set_WLAN_AnalysisMode(self):
        """Input Parameters"""
        self.write(':SENS:DEM:FORM:BCON:AUTO 1')

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    FSW = VSA()
    FSW.jav_Open("192.168.1.109")
    FSW.jav_Close()
