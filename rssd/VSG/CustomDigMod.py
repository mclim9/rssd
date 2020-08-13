# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Generator Custom Digital Modulation
### Author : Martin C Lim
### Date   : 2019.12.06
#####################################################################
from rssd.VSG.Common import VSG             #pylint: disable=E0611,E0401

class VSG(VSG):                             #pylint: disable=E0102
    """ Rohde & Schwarz Vector Signal Generator 5GNR Object """
    def __init__(self):
        super(VSG,self).__init__()          #Python2/3
        self.Model = "SMW"

    #####################################################################
    ### SMW Get Methods
    #####################################################################
    def Get_CDM_State(self):
        rdStr = self.queryInt(':SOUR1:BB:DM:STAT?')
        return rdStr

    #####################################################################
    ### SMW Set Functions
    #####################################################################
    def Set_CDM_State(self,State):
        """ON OFF 1 0 """
        if (State == 1) or (State == 'ON'):
            self.write(':SOUR1:BB:DM:STAT ON')
        elif (State == 0) or (State == 'OFF'):
            self.write(':SOUR1:BB:DM:STAT OFF')
        else:                                                   # pragma: no cover
            print('State not supported, please set ON or OFF')

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    # this won't be run when imported
    SMW = VSG()
    SMW.jav_Open("192.168.1.114")
    SMW.jav_Close()
