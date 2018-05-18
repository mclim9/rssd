#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Analyzer Common Functions
### Author:  Martin C Lim
### Date:    2018.04.03
### Requird: python -m pip install pyvisa
import FSW_Common

class VSA(FSW_Common.VSA,object):
   def __init__(self):
      try:
         super().__init__()
      except:
         super(VSA, self).__init__()
      
   #####################################################################
   ### FSW V5G
   #####################################################################
   def Init_5GNR(self):
      self.Set_Channel('5GNR')

   def Set_5GNR_Allocation(self,sFilename):
      # \Instr\user\V5GTF\AllocationFiles\UL
      self.write('MMEM:LOAD:DEM "%s"'%sFilename);
      
   def Set_5GNR_Direction(self,sDirection):
      # sDirection = "UL" or "DL"
      self.write(':CONF:V5G:LDIR %s'%sDirection);

   def Set_5GNR_AutoEVM(self):
      self.write(':SENS:ADJ:EVM;*WAI');
      #VISA_OPC_Wait(K2, ':SENS:ADJ:EVM;*WAI')
      
   #####################################################################
   ### FSW LTE Settings
   #####################################################################
   def Set_5GNR_Modulation(self,iMod):
      self.write(':CONF:LTE:UL:SUBF0:ALL:MOD QPSK')

   def Set_5GNR_ResourceBlock(self,iRB):
      self.write(':CONF:LTE:UL:SUBF0:ALL:RBC %d'%iRB)

   def Set_5GNR_ResourceBlockOffset(self,iRBO):
      self.write(':CONF:LTE:UL:SUBF0:ALL:RBOF %d'%iRBO)

   #####################################################################
   ### FSW Common Query
   #####################################################################
   def Get_5GNR_ACLR(self):
      ACLR = self.query(':CALC:MARK:FUNC:POW:RES? MCAC')
      return float(EVM)

   def Get_5GNR_ChPwr(self):
      Power   = float(self.query('FETC:SUMM:POW?'))
      return Power
      
   def Get_5GNR_EVM(self):
      EVM = self.query('FETC:SUMM:EVM?')
      return float(EVM)

   def Get_5GNR_EVMParams(self):
      MAttn   = self.Get_AttnMech()
      RefLvl  = self.Get_RefLevel()
      Power   = self.Get_5GNR_ChPwr()
      EVM     = self.Get_5GNR_EVM()
      return ("%.2f,%.2f,%6.2f,%.2f"%(MAttn,RefLvl,Power,EVM))

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   FSW = VSA()
   FSW.VISA_Open("192.168.1.109")
   FSW.Init_5GNR()
