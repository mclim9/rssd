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
    def Get_CDM_Center(self):
        rdStr = self.queryInt(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:%s:BWP0:DFR?'%(self.sdir))
        return rdStr

    #####################################################################
    ### SMW Set Functions
    #####################################################################
    def Set_CDM_Modulation(self,sMod):
        self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:MOD %s'%(self.alloc,sMod))

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    # this won't be run when imported 
    SMW = VSG()
    SMW.jav_Open("192.168.1.114")
    SMW.jav_Close()
