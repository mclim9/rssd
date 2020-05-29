# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Generator Fading Methods
### Author : Martin C Lim
### Date   : 2020.03.09
### Requird: python -m pip install rssd
#####################################################################
from rssd.VSG.Common import VSG             #pylint: disable=E0611,E0401

class VSG(VSG):                             #pylint: disable=E0102
    """ Rohde & Schwarz Vector Signal Generator 5GNR Object """
    def __init__(self):
        super(VSG,self).__init__()          #Python2/3
        self.Model = "SMW"
        self.entity = 1

    #####################################################################
    ### Fading Get Methods
    #####################################################################
    def Get_Fade_Standard(self):
        rdStr = self.queryInt(f'ENT{self.entity}:SOUR1:FSIM:STAN?')
        return rdStr

    def Get_Fade_State(self):
        rdStr = self.queryInt(f'ENT{self.entity}:SOUR1:FSIM:STAT?')
        return rdStr

    #####################################################################
    ### Fading Set Methods
    #####################################################################
    def Set_Fade_State(self,State):
        """ON OFF 1 0 """
        self.K2.timeout = 20000
        if (State == 1) or (State == 'ON'):
            self.write(':SCON:MODE ADV')
            self.write(':SCON:APPL;*OPC?')
            self.delay(1)
            self.jav_OPC_Wait(f'ENT{self.entity}:SOUR1:FSIM:STAT 1')
        elif (State == 0) or (State == 'OFF'):
            # self.write(':SCON:MODE STAN')
            # self.write(':SCON:APPL')
            self.jav_OPC_Wait(f'ENT{self.entity}:SOUR1:FSIM:STAT 0')
        else:
            print('State not supported, please set ON or OFF')
        self.K2.timeout = 5000



#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    # this won't be run when imported
    SMW = VSG()
    SMW.jav_Open("192.168.1.115")
    SMW.entity = 2
    SMW.Set_Fade_State(1)
    SMW.jav_Close()
