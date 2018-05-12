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
      pass

   #####################################################################
   ### FSW V5G
   #####################################################################
   def Init_5GNR(self):
      self.Set_Channel('5GNR')

   def Set_V5G_Allocation(self,sFilename):
      # \Instr\user\V5GTF\AllocationFiles\UL
      self.write('MMEM:LOAD:DEM "%s"'%sFilename);
      
   def Set_V5G_Direction(self,sDirection):
      # sDirection = "UL" or "DL"
      self.write(':CONF:V5G:LDIR %s'%sDirection);

   def Set_V5G_AutoEVM(self):
      self.write(':SENS:ADJ:EVM;*WAI');
      #VISA_OPC_Wait(K2, ':SENS:ADJ:EVM;*WAI')
      
   #####################################################################
   ### FSW LTE Settings
   #####################################################################
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
   FSW.VISA_Open("192.168.1.109")
   FSW.Init_5GNR()
