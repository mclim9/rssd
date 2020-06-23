# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Analyzer Common Functions
### Author:  Martin C Lim
### Date:    2018.04.03
### Requird: python -m pip install pyvisa
#####################################################################
from datetime           import datetime     #pylint: disable=E0611,E0401
from rssd.VSA.Common    import VSA          #pylint: disable=E0611,E0401

class VSA(VSA):                        #pylint: disable=E0102
    """ Rohde & Schwarz Vector Signal Analyzer LTE Object """
    def __init__(self):
        super(VSA, self).__init__()
        self.ldir = "DL"
        self.cc   = 1

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
        return "%.2f,%.2f,%6.2f,%.2f"%(MAttn,RefLvl,Power,EVM)

    def Get_LTE_CC(self):
        rdStr = self.query(':CONF:LTE:NOCC?')
        return rdStr

    def Get_LTE_ChBW(self):
        rdStr = self.query(f':CONF:LTE:{self.ldir}:BW?')
        return rdStr

    def Get_LTE_ChPwr(self):
        rdStr = self.queryFloat('FETC:CC1:SUMM:POW:AVER?')
        return rdStr

    def Get_LTE_CrestFactor(self):
        rdStr = self.queryFloat('FETC:CC1:SUMM:CRES:AVER?')
        return rdStr

    def Get_LTE_Direction(self):
        rdStr = self.query(':CONF:LDIR?')
        if rdStr == 'DL':
            self.ldir = "DL"
        elif rdStr == 'UL':
            self.ldir = "UL"
        else:
            if self.debug: print('Get_LTE_Direction Error')
        # print(f'LTE DIRECTION = {self.ldir}')
        return rdStr

    def Get_LTE_Duplex(self):
        rdStr = self.query(':CONF:LTE:DUPL?')
        return rdStr

    def Get_LTE_EVM(self):
        rdStr = self.queryFloat('FETC:SUMM:EVM?')
        return rdStr

    def Get_LTE_EVMParams(self):
        Crest = self.Get_LTE_CrestFactor()
        Power = self.Get_LTE_ChPwr()
        EVM   = self.Get_LTE_EVM()
        return f"{Crest:6.3f},{Power:6.3f},{EVM:.2f}"

    def Get_LTE_Modulation(self):
        if self.ldir == 'UL':
            rdStr = self.query(f':CONF:LTE:{self.ldir}:SUBF0:ALL:MOD?')
        elif self.ldir == 'DL':
            rdStr = self.query(f':CONF:LTE:{self.ldir}:SUBF0:ALL0:MOD?')
        else:
            print('LDIR error in Get_LTE_Mod')
        return rdStr

    def Get_LTE_ResBlock(self):
        if self.ldir == 'UL':
            rdStr = self.query(f':CONF:LTE:{self.ldir}:SUBF0:ALL:RBC?')
        elif self.ldir == 'DL':
            rdStr = self.query(f':CONF:LTE:{self.ldir}:SUBF0:ALL0:RBC?')
        else:
            print('LDIR error in Get_LTE_RB')
        return rdStr

    def Get_LTE_ResBlockOffset(self):
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
    def Set_LTE_AutoRef(self):
        #Assumes we are in LTE personality
        tick = datetime.now()
        self.Init_CCDF()
        self.Set_AttnAuto()
        self.Set_InitImm()
        Crest = self.queryFloat(f':CALC:STAT:CCDF:X1? P0_1;*WAI')
        ChPwr = self.queryFloat(f':CALC:STAT:RES? MEAN')
        refLvl = Crest + ChPwr
        self.Set_RefLevel(refLvl)
        self.Set_PreampToggle(ChPwr,-23)        #FSVA:-23  FSW:-27
        d = datetime.now() - tick
        print(f'Set_LTE_AutoRef: {d.seconds:3d}.{d.microseconds:06d}')

    def Set_LTE_CC(self,iCC):
        self.write(':CONF:LTE:NOCC %d'%iCC)
        self.cc = iCC

    def Set_LTE_ChBW(self,iBW):
        self.write(f':CONF:LTE:{self.ldir}:CC:BW BW{iBW:d}_00')

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
        # print(self.ldir)

    def Set_LTE_Duplex(self,sDup):
        # TDD or FDD
        self.write(f':CONF:LTE:DUPL {sDup}')

    def Set_LTE_EVMUnit(self,sUnit):
        #DB or PCT
        self.write(':UNIT:EVM %s'%sUnit)

    def Set_LTE_SubFrameCount(self,dSubFrame):
        self.write(':SENS:LTE:FRAM:COUN:STAT ON')
        self.write(':SENS:LTE:FRAM:COUN:AUTO OFF')
        self.write(':SENS:LTE:FRAM:COUN %d'%dSubFrame)

    def Set_LTE_Modulation(self,iMod):
        self.write(f':CONF:LTE:{self.ldir}:SUBF0:ALL:MOD {iMod}')

    def Set_LTE_ResBlock(self,iRB):
        self.write(f':CONF:LTE:{self.ldir}:SUBF0:ALL:RBC {iRB}')

    def Set_LTE_ResBlockOffset(self,iRBO):
        self.write(f':CONF:LTE:{self.ldir}:SUBF0:ALL:RBOF %d'%iRBO)

    def Set_LTE_SweepTime(self,fSwpTime):
        if fSwpTime < 0.00201:
            fSwpTime = 0.0021
        self.write('SENS:SWE:TIME %f'%fSwpTime)  #Sweep/Capture Time

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
