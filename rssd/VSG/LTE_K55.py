# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Generator LTE Functions
### Author : Martin C Lim
### Date   : 2019.03.05
### Requird: python -m pip install rssd
### Options: K55  LTE Rel  8 Initial Release
###          K84  LTE Rel  9 Pos Ref Signal
###          K85  LTE Rel 10 Carrier aggregation
###          K112 LTE Rel 11
#####################################################################
from rssd.VSG.Common import VSG     #pylint: disable=E0611,E0401

class VSG(VSG):                     #pylint: disable=E0102
    """ Rohde & Schwarz Vector Signal Generator LTE Object """
    def __init__(self):
        super(VSG,self).__init__()    #Python2/3
        self.Model  = "SMW"
        self.ldir   = "UL"
        self.User   = 0
        self.cc     = 1

    #####################################################################
    ### VSG Query
    #####################################################################
    def Get_LTE_CC(self):
        rdStr = self.query(f':SOUR:BB:EUTR:{self.ldir}:CA:CELL0:STAT?')
        return rdStr

    def Get_LTE_ChBW(self):
        rdStr = self.query(f':SOUR:BB:EUTR:{self.ldir}:BW?')
        return rdStr

    def Get_LTE_Direction(self):
        rdStr = self.query(f':SOUR:BB:EUTR:LINK?')
        if rdStr == 'DOWN':
            self.ldir = "DL"
        elif rdStr == 'UP':
            self.ldir = "UL"
        else:
            print('Get_LTE_Direction Error')
        return self.ldir

    def Get_LTE_Duplex(self):
        rdStr = self.query(f':SOUR:BB:EUTR:DUPL?')
        return rdStr

    def Get_LTE_Modulation(self):
        if self.ldir == 'UL':
            rdStr = self.query(f':SOUR:BB:EUTR:{self.ldir}:CELL0:SUBF0:ALL0:CW1:PUSC:MOD?')     # UL Only
        else:
            rdStr = self.query(f':SOUR:BB:EUTR:{self.ldir}:DUMD:MOD?')
        return rdStr

    def Get_LTE_ResBlock(self):
        if self.ldir == 'UL':
            rdStr = self.query(f':SOUR:BB:EUTR:{self.ldir}:CELL0:SUBF0:ALL0:PUSC:SET1:RBC?')    # UL Only
        else:
            rdStr = self.query(f':SOUR:BB:EUTR:DL:SUBF0:ALL0:CW1:RBC?')                         # DL Only
        return rdStr

    def Get_LTE_ResBlockOffset(self):
        if self.ldir == 'UL':
            rdStr = self.query(f':SOUR:BB:EUTR:{self.ldir}:CELL0:SUBF0:ALL0:PUSC:SET1:VRB?')    # UL Only
        else:
            rdStr = self.query(f':SOUR:BB:EUTR:DL:SUBF0:ALL0:CW1:RBOF?')                        # DL Only
        return rdStr

    #####################################################################
    ### VSG Setting
    #####################################################################
    def Set_LTE_BBState(self,iEnable):
        if (iEnable == 1) or (iEnable == 'ON'):
            self.jav_OPC_Wait(':SOUR1:BB:EUTR:STAT 1')
    #         self.query('*OPC?')        # Wait for calculation
        else:
            self.write(':SOUR1:BB:EUTR:STAT 0')


    def Set_LTE_CC(self,iCC):
        self.write(''%())
        if iCC > 0:
            self.write(f':SOUR:BB:EUTR:{self.ldir}:CA:STAT 1')

    def Set_LTE_ChBW(self,iChBW):
        self.write(f':SOUR:BB:EUTR:{self.ldir}:BW BW{iChBW:02d}_00')
        self.write(f':SOUR:BB:EUTR:{self.ldir}:CA:CELL{self.cc - 1}:BW BW{iChBW:02d}_00')

    def Set_LTE_Direction(self, sDir):
        """UL | DL | UP | DOWN """
        if (sDir == 'UL') or (sDir == 'UP'):
            self.write(f':SOUR:BB:EUTR:LINK UP')
            self.ldir = 'UL'
        elif (sDir == 'DL') or (sDir == 'DOWN'):
            self.write(f':SOUR:BB:EUTR:LINK DOWN')
            self.ldir = 'DL'
        else:
            print('Set_LTE_Direction Error.  Must be UL or DL')

    def Set_LTE_Duplex(self,sDuplex):
        #FDD TDD
        self.write(f':SOUR:BB:EUTR:DUPL {sDuplex}')

    def Set_LTE_Modulation(self, sMod):
        if self.ldir == 'UL':
            self.write(f':SOUR:BB:EUTR:{self.ldir}:CELL0:SUBF0:ALL0:CW1:PUSC:MOD {sMod}')
        else:
            self.write(f':SOUR:BB:EUTR:{self.ldir}:DUMD:MOD {sMod}')

    def Set_LTE_ResBlock(self, iRB):
        if self.ldir == 'UL':
            self.write(f':SOUR:BB:EUTR:{self.ldir}:CELL0:SUBF0:ALL0:PUSC:SET1:RBC {iRB}')
        else:
            pass

    def Set_LTE_ResBlockOffset(self,iRBO):
        if self.ldir == 'UL':
            self.write(f':SOUR:BB:EUTR:{self.ldir}:CELL0:SUBF0:ALL0:PUSC:SET1:VRB {iRBO}')
        else:
            pass
