#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Analyzer Common Functions
### Author:  Martin C Lim
### Date:    2018.04.03
### Requird: python -m pip install pyvisa
#####################################################################
from rssd.FSW_Common import VSA        #pylint: disable=E0611,E0401

class VSA(VSA):                        #pylint: disable=E0102
    def __init__(self):
        super(VSA, self).__init__()
        self.ldir = "DL"
      
    #####################################################################
    ### VSA Query
    #####################################################################
    def Get_ACLR(self):
        ACLR = self.queryFloatArry(':CALC:MARK:FUNC:POW:RES? MCAC')
        return ACLR

    def Get_EVM_n_Params(self):
        MAttn   = self.Get_AttnMech()
        RefLvl  = self.Get_RefLevel()
        Power   = self.Get_ChPwr()
        EVM     = self.Get_EVM()
        return ("%.2f,%.2f,%6.2f,%.2f"%(MAttn,RefLvl,Power,EVM))

    def Get_LTE_CC(self):
        rdStr = self.query(':CONF:LTE:NOCC?')
        return rdStr

    def Get_LTE_ChBW(self,cc=1):
        rdStr = self.query(f':CONF:LTE:{self.ldir}:BW?')
        return rdStr

    def Get_LTE_Direction(self,cc=1):
        rdStr = self.query(':CONF:LDIR?')
        if rdStr == 'DL':
            self.ldir = "DL"
        elif rdStr == 'UL':
            self.ldir = "UL"
        else:
            print('Get_5GNR_Direction Error')
        print(f'LTE DIRECTION = {self.ldir}')
        return rdStr

    def Get_LTE_Duplex(self):
        rdStr = self.query(':CONF:LTE:DUPL?')
        return rdStr

    def Get_LTE_EVM(self):
        rdStr = self.queryFloat('FETC:SUMM:EVM?')
        return rdStr

    def Get_LTE_Modulation(self,cc=1):
        if self.ldir == 'UL':
            rdStr = self.query(f':CONF:LTE:{self.ldir}:SUBF0:ALL:MOD?')
        elif self.ldir == 'DL':
            rdStr = self.query(f':CONF:LTE:{self.ldir}:SUBF0:ALL0:MOD?')
        else:
            print('LDIR error in Get_LTE_Mod')
        return rdStr

    def Get_LTE_ResBlock(self,cc=1):
        if self.ldir == 'UL':
            rdStr = self.query(f':CONF:LTE:{self.ldir}:SUBF0:ALL:RBC?')
        elif self.ldir == 'DL':
            rdStr = self.query(f':CONF:LTE:{self.ldir}:SUBF0:ALL0:RBC?')
        else:
            print('LDIR error in Get_LTE_RB')
        return rdStr

    def Get_LTE_ResBlockOffset(self,cc=1):
        if self.ldir == 'UL':
            rdStr = self.query(f':CONF:LTE:{self.ldir}:SUBF0:ALL:RBOF?')
        elif self.ldir == 'DL':
            rdStr = self.query(f':CONF:LTE:{self.ldir}:SUBF0:ALL0:RBOF?')
        else:
            print('LDIR error in Get_LTE_RB')
        return rdStr

    #####################################################################
    ### Init LTE
    #####################################################################
    def Init_LTE(self):
        self.Set_Channel('LTE')

    def Init_LTE_Meas(self,sMeas):
        ### EMV; ESPectrum; ACLR; MCAClr; CACLr; MCESpectrum
        self.write('CONF:LTE:MEAS %s'%sMeas)

    def Init_LTE_SEM(self):
        self.Set_Channel('LTE')
        self.write(':CONF:LTE:MEAS ESP')

    #####################################################################
    ### VSA Settings
    #####################################################################
    def Set_LTE_CC(self,iCC):
        self.write(':CONF:LTE:NOCC %d'%iCC)

    def Set_LTE_ChBW(self,iBW):
        self.write(f':CONF:LTE:{self.ldir}:BW BW{iBW:02d}_00')

    def Set_LTE_Direction(self,sDir):
        # UL or DL
        if (sDir == "UL") or (sDir == "UP"):
            self.write(f':CONF:LDIR UL')
            self.ldir = 'UL'
        elif (sDir == "DL") or (sDir == "DOWN"):
            self.write(f':CONF:LDIR DL')
            self.ldir = 'DL'
        else:
            print("Set_5GNR_UL_Direction must be UL or DL")
        print(self.ldir)

    def Set_LTE_Duplex(self,sDup):
        # TDD or FDD
        self.write(f':CONF:LTE:DUPL {sDup}')

    def Set_LTE_Modulation(self,iMod):
        self.write(f':CONF:LTE:{self.ldir}:SUBF0:ALL:MOD {iMod}')

    def Set_LTE_ResBlock(self,iRB):
        self.write(f':CONF:LTE:{self.ldir}:SUBF0:ALL:RBC {iRB}')

    def Set_LTE_ResBlockOffset(self,iRBO):
        self.write(f':CONF:LTE:{self.ldir}:SUBF0:ALL:RBOF %d'%iRBO)

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   FSW = VSA()
   FSW.ldir = 'UL'
   FSW.jav_Open("192.168.1.109")
   FSW.Get_LTE_Direction()
   FSW.jav_IDN()
