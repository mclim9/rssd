#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Generator LTE Functions
### Author : Martin C Lim
### Date   : 2019.03.05
### Requird: python -m pip install rssd
#####################################################################
from rssd.SMW_Common import VSG     #pylint: disable=E0611,E0401

class VSG(VSG):                     #pylint: disable=E0102
    def __init__(self):
        super(VSG,self).__init__()    #Python2/3
        self.Model = "SMW"
        self.ldir = "UL"
        self.User = 0

    #####################################################################
    ### VSG Query
    #####################################################################
    def Get_LTE_CC(self):
        SCPI = self.query(f':SOUR:BB:EUTR:{self.ldir}:CA:CELL0:STAT?')
        return SCPI

    def Get_LTE_ChBW(self,cc=1):
        SCPI = self.query(f':SOUR:BB:EUTR:{self.ldir}:BW?')
        return SCPI

    def Get_LTE_Direction(self,cc=1):
        SCPI = self.query(f':SOUR:BB:EUTR:LINK?')
        return SCPI

    def Get_LTE_Modulation(self,cc=1):
        SCPI = self.query(f':SOUR:BB:EUTR:{self.ldir}:CELL0:SUBF0:ALL0:CW1:PUSC:MOD?')
        return SCPI     

    def Get_LTE_ResBlock(self,cc=1):
        SCPI = self.query(':SOUR:BB:EUTR:{self.ldir}:CELL0:SUBF0:ALL0:PUSC:SET1:RBC?')
        return SCPI

    def Get_LTE_ResBlockOffset(self,cc=1):
        SCPI = self.query(':SOUR:BB:EUTR:{self.ldir}:CELL0:SUBF0:ALL0:PUSC:SET1:VRB')
        return SCPI


    #####################################################################
    ### VSG Setting
    #####################################################################
    def Set_LTE_CC(self,iCC):
        self.write(''%())
        if iCC > 0:
            self.write(f':SOUR:BB:EUTR:{self.ldir}:CA:STAT 1')

    def Set_LTE_ChBW(self,iChBW, cc=1):
        self.write(f':SOUR:BB:EUTR:{self.ldir}:BW BW{iChBW:02d}_00')
        self.write(f':SOUR:BB:EUTR:{self.ldir}:CA:CELL{cc - 1}:BW BW{iChBW:02d}_00')

    def Set_LTE_Direction(self,sDir, cc=1):
        if self.ldir == 'UL':
            self.write(f':SOUR:BB:EUTR:LINK UP')
        else:
            self.write(f':SOUR:BB:EUTR:LINK DOWN')

    def Set_LTE_Modulation(self, sMod, cc=1):
        if self.ldir == 'UL':
            self.write(f':SOUR:BB:EUTR:{self.ldir}:CELL0:SUBF0:ALL0:CW1:PUSC:MOD {sMod}')
        else:
            self.write(f':SOUR:BB:EUTR:{self.ldir}:DUMD:MOD {sMod}')

    def Set_LTE_ResBlock(self, iRB, cc=1):
        if self.ldir == 'UL':
            self.write(f':SOUR:BB:EUTR:{self.ldir}:CELL0:SUBF0:ALL0:PUSC:SET1:RBC {iRB}')

    def Set_LTE_ResBlockOffset(self,iRBO, cc=1):
        if self.ldir == 'UL':
            self.write(f':SOUR:BB:EUTR:{self.ldir}:CELL0:SUBF0:ALL0:PUSC:SET1:VRB {iRBO}')

