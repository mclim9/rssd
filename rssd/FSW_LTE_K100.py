#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Analyzer Common Functions
### Author:  Martin C Lim
### Date:    2018.04.03
### Requird: python -m pip install pyvisa
import FSW_Common

class VSA(FSW_Common.VSA):
   def __init__(self):
      try:
         super().__init__()
      except:
         super(VSA, self).__init__()
      
   #####################################################################
   ### FSW LTE Settings
   #####################################################################

   def Set_LTE_BW(self,iBW):
      self.write(':CONF:LTE:UL:BW BW20_00')
      
   def Set_LTE_Dir(self,sDir):
      # UL or DL
      self.write(':CONF:LDIR %s'%sDir)

   def Set_LTE_Modulation(self,iMod):
      self.write(':CONF:LTE:UL:SUBF0:ALL:MOD QPSK')

   def Set_LTE_ResourceBlock(self,iRB):
      self.write(':CONF:LTE:UL:SUBF0:ALL:RBC %d'%iRB)

   def Set_LTE_ResourceBlockOffset(self,iRBO):
      self.write(':CONF:LTE:UL:SUBF0:ALL:RBOF %d'%iRBO)

   #####################################################################
   ### FSW Common Query
   #####################################################################
   def Get_ACLR(self):
      ACLR = self.query(':CALC:MARK:FUNC:POW:RES? MCAC')
      return float(EVM)

   def Get_ChPwr(self):
      Power   = float(self.query('FETC:SUMM:POW?'))
      return Power
      
   def Get_LTE_EVM(self):
      EVM = self.query('FETC:SUMM:EVM?')
      return float(EVM)

   def Get_EVM_n_Params(self):
      MAttn   = self.Get_AttnMech()
      RefLvl  = self.Get_RefLevel()
      Power   = self.Get_ChPwr()
      EVM     = self.Get_EVM()
      return ("%.2f,%.2f,%6.2f,%.2f"%(MAttn,RefLvl,Power,EVM))


#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   FSW = VSA()
   FSW.jav_Open("192.168.1.109")
   FSW.jav_IDN()
   print(FSW.Get_MkrXY())
