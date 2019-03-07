#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Analyzer Common Functions
### Author:  Martin C Lim
### Date:    2018.04.03
### Requird: python -m pip install pyvisa
from rssd.FSW_Common import VSA

class VSA(VSA):
    def __init__(self):
        super(VSA, self).__init__()
      
    #####################################################################
    ### VSA Query
    #####################################################################
    def Get_ACLR(self):
      ACLR = self.queryFloatArry(':CALC:MARK:FUNC:POW:RES? MCAC')
      return ACLR

    def Get_LTE_CC(self):
        SCPI = self.query(':CONF:LTE:NOCC?')
        return SCPI

    def Get_LTE_ChBW(self,cc=1):
        SCPI = self.query(':CONF:LTE:UL:BW?')
        return SCPI

    def Get_LTE_Direction(self,cc=1):
       SCPI = self.query(':CONF:LDIR?')
       return SCPI 

    def Get_LTE_EVM(self):
        EVM = self.queryFloat('FETC:SUMM:EVM?')
        return EVM

    def Get_LTE_Modulation(self,cc=1):
        SCPI = self.query(':CONF:LTE:UL:SUBF0:ALL:MOD?')
        return SCPI

    def Get_LTE_ResBlock(self,cc=1):
        SCPI = self.query(':CONF:LTE:UL:SUBF0:ALL:RBC?')
        return SCPI

    def Get_LTE_ResBlockOffset(self,cc=1):
        SCPI = self.query(':CONF:LTE:UL:SUBF0:ALL:RBOF?')
        return SCPI
      
    def Get_EVM_n_Params(self):
        MAttn   = self.Get_AttnMech()
        RefLvl  = self.Get_RefLevel()
        Power   = self.Get_ChPwr()
        EVM     = self.Get_EVM()
        return ("%.2f,%.2f,%6.2f,%.2f"%(MAttn,RefLvl,Power,EVM))

    #####################################################################
    ### VSA Settings
    #####################################################################
    def Set_LTE_CC(self,iCC):
        self.write(':CONF:LTE:NOCC %d'%iCC)

    def Set_LTE_ChBW(self,iBW):
        self.write(':CONF:LTE:UL:BW BW20_00')

    def Set_LTE_Direction(self,sDir):
       # UL or DL
       self.write(':CONF:LDIR %s'%sDir)

    def Set_LTE_Modulation(self,iMod):
        self.write(':CONF:LTE:UL:SUBF0:ALL:MOD QPSK')

    def Set_LTE_ResourceBlock(self,iRB):
        self.write(':CONF:LTE:UL:SUBF0:ALL:RBC %d'%iRB)

    def Set_LTE_ResourceBlockOffset(self,iRBO):
        self.write(':CONF:LTE:UL:SUBF0:ALL:RBOF %d'%iRBO)

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   FSW = VSA()
   FSW.jav_Open("192.168.1.109")
   FSW.jav_IDN()
