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
      self.sdir = "UL"
      
   #####################################################################
   ### FSW V5G
   #####################################################################
   def Init_5GNR(self):
      self.Set_Channel('NR5G')
      
   def Init_5GNR_Meas(self,sMeas):
      ### EMV; ESPectrum; ACLR; MCAClr; CACLr; MCESpectrum
      self.write('CONF:NR5G:MEAS %s'%sMeas)

   def Set_5GNR_AllocFile(self,sFilename):
      # \Instr\user\V5GTF\AllocationFiles\UL
      self.write('MMEM:LOAD:DEM "%s"'%sFilename);
      
   def Set_5GNR_Direction(self,sDirection):
      # sDirection = "UL" or "DL"
      if (sDirection == "UL") or (sDirection == "UP"):
         self.write(':CONF:NR5G:LDIR UL')
         self.sdir = "UL"
      elif (sDirection == "DL") or (sDirection == "DOWN"):
         self.write(':CONF:NR5G:LDIR DL')
         self.sdir = "DL"
      else:
         print("Set_5GNR_UL_Direction must be UL or DL")
   
   def Set_5GNR_Parameters(self,sDir):
      self.Set_5GNR_Direction(sDir)
      
   #####################################################################
   ### FSW 5GNR Settings
   #####################################################################
   def Get_5GNR_RefA(self):
      rdStr = self.query(':CONF:NR5G:%s:CC:RPA:RTCF?'%(self.sdir))
      return rdStr

   def Get_5GNR_BWP_Center(self):
      SS = self.Get_5GNR_SubSpace()
      SS = int(''.join(c for c in SS if c.isdigit()))
      RB = int(self.Get_5GNR_BWP_ResBlock())
      RBO = int(self.Get_5GNR_BWP_ResBlockOffset())
      self.write(':CONF:NR5G:%s:CC:FRAM:BWP0:RBC MAX'%(self.sdir))
      RBMax = int(self.Get_5GNR_BWP_ResBlock())
      self.Set_5GNR_BWP_ResBlock(RB)
      self.Set_5GNR_BWP_ResBlockOffset(RBO)
      ressy = (SS * 1e3 *12*(RB - RBMax + 2 * RBO))/2 
      return ressy
             
   def Get_5GNR_BWP_Count(self):
      rdStr = self.query(':CONF:NR5G:%s:CC:FRAM:BWPC?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_ResBlock(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':CONF:NR5G:%s:CC:FRAM:BWP0:RBC?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_ResBlockOffset(self):
      rdStr = self.query(':CONF:NR5G:%s:CC:FRAM:BWP0:RBOF?'%(self.sdir))
      return rdStr      
      
   def Get_5GNR_BWP_SlotNum(self):
      ### Number of slots
      rdStr = self.query(':CONF:NR5G:%s:CC:FRAM:BWP0:SCO?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Slot_Modulation(self):
      rdStr = self.query(':CONF:NR5G:%s:CC:FRAM:BWP0:SLOT0:ALL0:MOD?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Slot_ResBlock(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':CONF:NR5G:%s:CC:FRAM:BWP0:SLOT0:ALL0:RBC?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Slot_ResBlockOffset(self):
      rdStr = self.query(':CONF:NR5G:%s:CC:FRAM:BWP0:SLOT0:ALL0:RBOF?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Slot_SymbNum(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':CONF:NR5G:%s:CC:FRAM:BWP0:SLOT0:ALL0:SCO?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Slot_SymbOff(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':CONF:NR5G:%s:CC:FRAM:BWP0:SLOT0:ALL0:SOFF?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_SubSpace(self):
      rdStr = self.query(':CONF:NR5G:%s:CC:FRAM:BWP0:SSP?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_ChannelBW(self):
      ### 5;10;15;20;25;30;40;50;60;70;80;90;100;200;400
      rdStr = self.query(':CONF:NR5G:%s:CC:BW?'%(self.sdir))
      return rdStr
      
   def Set_5GNR_ChannelBW(self,iBW):
      ### 5;10;15;20;25;30;40;50;60;70;80;90;100;200;400
      self.write(':CONF:NR5G:%s:CC:BW BW%d'%(self.sdir,iBW))
      
   def Set_5GNR_BWP_ResBlock(self,iRB):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      self.write(':CONF:NR5G:%s:CC:FRAM:BWP0:RBC %d'%(self.sdir,iRB))

   def Set_5GNR_BWP_ResBlockOffset(self,iRBO):
      self.write(':CONF:NR5G:%s:CC:FRAM:BWP0:RBOF %d'%(self.sdir,iRBO))

   def Set_5GNR_BWP_Slot_Modulation(self,iMod):
      self.write(':CONF:NR5G:%s:SUBF0:ALL:MOD QPSK'%(self.sdir))

   def Set_5GNR_BWP_Slot_SubSpace(self,iSubSp):
      self.write(':CONF:NR5G:%s:CC:BW BW%d'%(self.sdir,iSubSp))
      
   def Set_5GNR_FreqRange(self,iRange):
      ### 0:LessThan3GHz 1:3to6GHz 2:GreaterThan 6GHz
      ### LOW; MIDD; HIGH
      self.write(':CONF:NR5G:%s:CC:DFR %s'%(self.sdir,iRange))      
            
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
   FSW.Set_5GNR_Parameters("DL")
   print(FSW.Get_5GNR_ChannelBW())
   print(FSW.Get_5GNR_SubSpace())
   print(FSW.Get_5GNR_BWP_Count())
   print(FSW.Get_5GNR_BWP_ResBlock())
   print(FSW.Get_5GNR_BWP_ResBlockOffset())   
   print(FSW.Get_5GNR_RefA())

   print(FSW.Get_5GNR_BWP_Center())
   
   
