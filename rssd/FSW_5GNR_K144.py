#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Analyzer 5GNR Functions
### Author:  Martin C Lim
### Date:    2018.04.03
### Requird: python -m pip install pyvisa
from rssd.FSW_Common import VSA

class VSA(VSA):
   def __init__(self):
      super(VSA, self).__init__()      #Python 2/3
      self.sdir = "UL"
      
   #####################################################################
   ### FSW 5GNR Get
   #####################################################################
   def Get_5GNR_ACLR(self): 
      ACLR = self.query(':CALC:MARK:FUNC:POW:RES? MCAC')
      return float(EVM)

   def Get_5GNR_BWP_Center(self):
      SS = self.Get_5GNR_BWP_SubSpace()
      SS = int(''.join(c for c in SS if c.isdigit()))
      RB = int(self.Get_5GNR_BWP_ResBlock())
      RBO = int(self.Get_5GNR_BWP_ResBlockOffset())
      self.write(':CONF:NR5G:%s:CC1:FRAM1:BWP0:RBC MAX'%(self.sdir))
      RBMax = int(self.Get_5GNR_BWP_ResBlock())
      self.Set_5GNR_BWP_ResBlock(RB)
      self.Set_5GNR_BWP_ResBlockOffset(RBO)
      ressy = (SS * 1e3 *12*(RB - RBMax + 2 * RBO))/2 
      return ressy
             
   #####################################################################
   ### FSW 5GNR DMRS Config
   #####################################################################
   def Get_5GNR_BWP_Ch_DMRS_1stDMRSSym(self):
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:TAP?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Ch_DMRS_AddPosition(self):
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:MSYM:APOS?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Ch_DMRS_Config(self):
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:CTYP?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Ch_DMRS_MSymbLen(self):
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:MSYM:LENG?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Ch_DMRS_Mapping(self):
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:MTYP?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Ch_DMRS_RelPwr(self):
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:POW?'%(self.sdir))
      return rdStr

   def Get_5GNR_BWP_Ch_DMRS_SeqGenMeth(self):
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:SGEN?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Ch_DMRS_SeqGenSeed(self):
      #rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SLOT0:ALL0:DMRS:NID?'%(self.sdir))
      #rdStr = "debug"
      rdStr = "<TBD>"
      return rdStr
  
   def Get_5GNR_BWP_Ch_Modulation(self):
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SLOT0:ALL0:MOD?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Ch_ResBlock(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SLOT0:ALL0:RBC?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Ch_ResBlockOffset(self):
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SLOT0:ALL0:RBOF?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Ch_SymbNum(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SLOT0:ALL0:SCO?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Ch_SymbOff(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SLOT0:ALL0:SOFF?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Count(self):
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWPC?'%(self.sdir))
      return rdStr
 
   def Get_5GNR_BWP_ResBlock(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:RBC?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_ResBlockOffset(self):
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:RBOF?'%(self.sdir))
      return rdStr      
      
   def Get_5GNR_BWP_SlotNum(self):
      ### Number of slots
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SCO?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_SubSpace(self):
      rdStr = self.query(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SSP?'%(self.sdir))
      return rdStr

   def Get_5GNR_ChPwr(self):
      Power = float(self.query('FETC:SUMM:POW?'))
      return Power
      
   def Get_5GNR_ChannelBW(self):
      ### 5;10;15;20;25;30;40;50;60;70;80;90;100;200;400
      rdStr = self.query(':CONF:NR5G:%s:CC1:BW?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_EVM(self):
      EVM = self.queryFloat('FETC:SUMM:EVM?')
      return EVM

   def Get_5GNR_EVMParams(self):
      MAttn = self.Get_AttnMech()
      RefLvl  = self.Get_RefLevel()
      Power = self.Get_5GNR_ChPwr()
      EVM     = self.Get_5GNR_EVM()
      return ("%.2f,%.2f,%6.2f,%.2f"%(MAttn,RefLvl,Power,EVM))

   def Get_5GNR_RefA(self):
      rdStr = self.query(':CONF:NR5G:%s:CC1:RPA:RTCF?'%(self.sdir))
      return rdStr

   def Get_5GNR_TransPrecoding(self):
      rdStr = self.query(':CONF:NR5G:UL:CC1:TPR?')
      return rdStr

   #####################################################################
   ### FSW 5GNR Init
   #####################################################################
   def Init_5GNR(self):
      self.Set_Channel('NR5G')
      
   def Init_5GNR_Meas(self,sMeas):
      ### EMV; ESPectrum; ACLR; MCAClr; CACLr; MCESpectrum
      self.write('CONF:NR5G:MEAS %s'%sMeas)

   #####################################################################
   ### FSW 5GNR Settings
   #####################################################################
   def Set_5GNR_AllocFile(self,sFilename):
      # \Instr\user\V5GTF\AllocationFiles\UL
      self.write('MMEM:LOAD:DEM "%s"'%sFilename);
      
   def Set_5GNR_BWP_Ch_Modulation(self,sMod):
      # QPSK; QAM16; QAM64; QAM256; PITB
      self.write(':CONF:NR5G:%s:FRAM1:BWP0:SLOT0:ALL0:MOD %s'%(self.sdir, sMod))

   def Set_5GNR_BWP_Ch_ResBlock(self,iRB):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      self.write(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SLOT0:ALL0:RBC %d'%(self.sdir,iRB))

   def Set_5GNR_BWP_Ch_ResBlockOffset(self,iRBO):
      self.write(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SLOT0:ALL0:RBOF %d'%(self.sdir,iRBO))

   def Set_5GNR_BWP_ResBlock(self,iRB):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      self.write(':CONF:NR5G:%s:CC1:FRAM1:BWP0:RBC %d'%(self.sdir,iRB))

   def Set_5GNR_BWP_ResBlockOffset(self,iRBO):
      self.write(':CONF:NR5G:%s:CC1:FRAM1:BWP0:RBOF %d'%(self.sdir,iRBO))

   def Set_5GNR_BWP_SubSpace(self,iSubSp):
      self.write(':CONF:NR5G:%s:CC1:FRAM1:BWP0:SSP SS%d'%(self.sdir,iSubSp))

   def Set_5GNR_ChannelBW(self,iBW):
      ### 5;10;15;20;25;30;40;50;60;70;80;90;100;200;400
      self.write(':CONF:NR5G:%s:CC1:BW BW%d'%(self.sdir,iBW))
      
   def Set_5GNR_Direction(self,sDirection):
      # sDirection = "UL" or "DL"
      if (sDirection == "UL") or (sDirection == "UP"):
         self.write(':CONF:NR5G:LDIR UL')
         self.write(':CONF:NR5G:UL:CC1:IDC ON')

         self.sdir = "UL"
      elif (sDirection == "DL") or (sDirection == "DOWN"):
         self.write(':CONF:NR5G:LDIR DL')
         self.write(':CONF:NR5G:DL:CC1:IDC ON')
         self.sdir = "DL"
      else:
         print("Set_5GNR_UL_Direction must be UL or DL")
   
   def Set_5GNR_FreqRange(self,iRange):
      ### 0:<3GHz 1:3-6GHz 2:>6GHz
      ### LOW; MIDD; HIGH
      self.write(':CONF:NR5G:%s:CC1:DFR %s'%(self.sdir,iRange))      

   def Set_5GNR_Parameters(self,sDir):
      self.Set_5GNR_Direction(sDir)
   
   def Set_5GNR_SubFrameCount(self,dSubFrame):
      self.write(':SENS:NR5G:FRAM:COUN:STAT OFF')
      self.write(':SENS:NR5G:FRAM:SCO %d'%dSubFrame)

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   FSW = VSA()
   FSW.jav_Open("192.168.1.109")
   FSW.Init_5GNR()
   EVM = FSW.Get_5GNR_EVM()
   print(EVM)
   FSW.jav_ClrErr()
   FSW.jav_Close()
