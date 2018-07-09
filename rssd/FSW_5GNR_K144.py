#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Analyzer 5GNR Functions
### Author:  Martin C Lim
### Date:    2018.04.03
### Requird: python -m pip install pyvisa
import FSW_Common

class VSA(FSW_Common.VSA):
   def __init__(self):
      super(VSA, self).__init__()      #Python 2/3
      self.ldir = "UL"
      
   #####################################################################
   ### FSW V5G
   #####################################################################
   def Init_5GNR(self):
      self.Set_Channel('NR5G')
      
   def Init_5GNR_Meas(self,sMeas):
      ### EMV; ESPectrum; ACLR; MCAClr; CACLr; MCESpectrum
      self.write('CONF:NR5G:MEAS %s'%sMeas)

   def Set_5GNR_Allocation(self,sFilename):
      # \Instr\user\V5GTF\AllocationFiles\UL
      self.write('MMEM:LOAD:DEM "%s"'%sFilename);
      
   def Set_5GNR_FreqRange(self,iRange):
      ### 0:LessThan3GHz 1:3to6GHz 2:GreaterThan 6GHz
      ### LOW; MIDD; HIGH
      self.write(':CONF:NR5G:UL:CC:DFR %s'%iRange);      
      
   def Get_5GNR_BWP(self):
      rdStr = self.query(':CONF:NR5G:DL:CC:FRAM:BWPC?')
      return int(rdStr)
      
   #####################################################################
   ### FSW 5GNR Settings
   #####################################################################
   def Set_5GNR_Direction(self,sDirection):
      # sDirection = "UL" or "DL"
      if (sDirection == "UL") or (sDirection == "UP"):
         self.write(':CONF:NR5G:LDIR UL')
         self.ldir = sDirection
      elif (sDirection == "DL") or (sDirection == "DOWN"):
         self.write(':CONF:NR5G:LDIR DL')
         self.ldir = sDirection
      else:
         print("Set_5GNR_Direction must be UL or DL")

   def Set_5GNR_ChannelBW(self,iBW):
      ### 5;10;15;20;25;30;40;50;60;70;80;90;100;200;400
      self.write(':CONF:NR5G:UL:CC:BW BW%d'%iBW)
      
   def Set_5GNR_SubSpace(self,iSubSp):
      self.write(':CONF:NR5G:UL:CC:BW BW%d'%iSubSp)
      
   def Set_5GNR_ResourceBlock(self,iRB):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      self.write(':CONF:NR5G:UL:SUBF0:ALL:RBC %d'%iRB)

   def Set_5GNR_ResourceBlockOffset(self,iRBO):
      self.write(':CONF:NR5G:UL:SUBF0:ALL:RBOF %d'%iRBO)

   def Set_5GNR_Modulation(self,iMod):
      self.write(':CONF:NR5G:UL:SUBF0:ALL:MOD QPSK')

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
   FSW.jav_Open("192.168.1.109")
   FSW.Init_5GNR()
   FSW.Set_5GNR_Direction('UL')
   #FSW.Set_5GNR_Allocation('C:/R_S/Instr/Debug/Files/FullQPSK30kHz.allocation')
   FSW.Set_5GNR_Allocation('C:/R_S/Instr/Debug/Files/ULFullQPSK30kHz-noPTRS.allocation')
   #print(FSW.Get_5GNR_EVM())
   FSW.jav_ClrErr()
