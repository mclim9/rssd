#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Generator 5G NR Functions
### Author : Martin C Lim
### Date   : 2018.02.01
### Requird: python -m pip install rssd
#####################################################################
from rssd.SMW_Common import VSG

class VSG(VSG):
   def __init__(self):
      super(VSG,self).__init__()    #Python2/3
      self.Model = "SMW"
      self.ldir = "UL"
      self.BWP = 0
      self.User = 0
      
   #####################################################################
   ### SMW 5GNR Common
   #####################################################################
   def Set_5GNR_Direction(self,sDirection):
      ### UP| DOWN
      if (sDirection == "UL") or (sDirection == "UP"):
         self.write(':SOUR1:BB:NR5G:LINK UP')
         self.sdir = "UL"
      elif (sDirection == "DL") or (sDirection == "DOWN"):
         self.write(':SOUR1:BB:NR5G:LINK DOWN')
         self.sdir = "DL"
      else:
         print("Set_5GNR_Direction must be UP or DOWN")

   def Set_5GNR_BBState(self,iEnable):
      if (iEnable == 1) or (iEnable == 'ON'):
         self.jav_OPC_Wait(':SOUR1:BB:NR5G:STAT 1')
#         self.query('*OPC?')        # Wait for calculation
      else:
         self.write(':SOUR1:BB:NR5G:STAT 0')

   def Set_5GNR_ChannelBW(self,iBW):
      ### BW in MHz
      ### 5GNR-->NODE-->Carriers-->Channel BW
      self.write(':SOUR1:BB:NR5G:NODE:CELL0:CBW BW%d'%iBW)

   def Set_5GNR_ResourceBlock(self,iRB):
      ### 5GNR-->Scheduling-->PUSCH-->No. RBs
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      #self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:RBN %d'%iRB)
      self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:RBN 273')

   def Set_5GNR_ResourceBlockOffset(self,iRBO):
      ### 5GNR-->Scheduling-->PUSCH-->No. RBs
      #self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:RBOF %d'%iRBO)
      self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:RBOF 0')

   def Set_5GNR_Modulation(self,iMod):
      ### 5GNR-->Scheduling-->PUSCH-->Config-->MOdulation
      self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:MOD QPSK')

   def Set_5GNR_Parameters(self,sDir):
      self.Set_5GNR_Direction(sDir)

   def Set_5GNR_FreqRange(self,iRange):
      ### 0:<3GHz 1:3-6GHz 2:>6GHz
      ### LOW; MIDD; HIGH
      if iRange == 'LOW':
         self.write(':SOUR1:BB:NR5G:NODE:CELL0:CARD LT6')
      elif iRange == 'MIDD':
         self.write(':SOUR1:BB:NR5G:NODE:CELL0:CARD BT36')
      elif iRange == 'HIGH':
         self.write(':SOUR1:BB:NR5G:NODE:CELL0:CARD GT6')
         
   #####################################################################
   ### FSW 5GNR Settings
   #####################################################################
   def Get_5GNR_RefA(self):
      rdStr = self.query(':SOUR1:BB:NR5G:NODE:CELL0:TXBW:POIN?')
      return rdStr

   def Get_5GNR_TransPrecoding(self):
      rdStr = self.query(':SOUR1:BB:NR5G:NODE:CELL0:DUMR:TPST?')
      return rdStr

   def Get_5GNR_BWP_Center(self):
      rdStr = self.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:%s:BWP0:DFR?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Count(self):
      rdStr = self.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:%s:NBWP?'%(self.sdir))
      return rdStr      

   def Get_5GNR_BWP_ResBlock(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:%s:BWP0:RBN?'%(self.sdir))
      return rdStr

   def Set_5GNR_BWP_ResBlockMax(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      MaxRB =  20
      rdStr = self.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:%s:BWP0:RBN %d'%(self.sdir,MaxRB))
      return rdStr
      
   def Get_5GNR_BWP_ResBlockOffset(self):
      rdStr = self.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:%s:BWP0:RBOF?'%(self.sdir))
      return rdStr      
      
   def Get_5GNR_BWP_SlotNum(self):
      ### Number of slots
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:SLOT?'%(self.sdir))
      return rdStr
      
   def Get_5GNR_BWP_Slot_Modulation(self):
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:MOD?')
      return rdStr
      
   def Set_5GNR_BWP_Slot_Modulation(self,sMod):
      self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:MOD %s'%(sMod))
      
   def Get_5GNR_BWP_Slot_ResBlock(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:RBN?')
      return rdStr
      
   def Get_5GNR_BWP_Slot_ResBlockOffset(self):
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:RBOF?')
      return rdStr
      
   def Get_5GNR_BWP_Slot_SymbNum(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:SYMN?')
      return rdStr
      
   def Get_5GNR_BWP_Slot_SymbOff(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:SYM?')
      return rdStr
      
   def Get_5GNR_BWP_SubSpace(self):
      rdStr = self.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:%s:BWP0:SCSP?'%(self.sdir))
      return rdStr

   def Get_5GNR_BWP_TotalSubSpace(self):
      rdStr = []
      rdStr.append(self.query(':SOUR1:BB:NR5G:NODE:CELL0:TXBW:S15K:NRB?'))
      rdStr.append(self.query(':SOUR1:BB:NR5G:NODE:CELL0:TXBW:S30K:NRB?'))
      rdStr.append(self.query(':SOUR1:BB:NR5G:NODE:CELL0:TXBW:S60K:NRB?'))
      rdStr.append(self.query(':SOUR1:BB:NR5G:NODE:CELL0:TXBW:S120K:NRB?'))
      return rdStr
      
   def Set_5GNR_BWP_SubSpace(self,iSubSp):
      self.write(':SOUR1:BB:NR5G:NODE:CELL0:TXBW:S%dK:USE 1'%(iSubSp))
      self.write(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:%s:BWP0:SCSP N%d'%(self.sdir,iSubSp))

   def Get_5GNR_ChannelBW(self):
      ### 5;10;15;20;25;30;40;50;60;70;80;90;100;200;400
      rdStr = self.query(':SOUR1:BB:NR5G:NODE:CELL0:CBW?')
      return rdStr
      
   #####################################################################
   ### FSW 5G NR DMRS Config
   #####################################################################
   def Get_5GNR_DMRS_Config(self):
      rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:PUSC:DMRS:CONF?')
      return rdStr
      
   def Get_5GNR_DMRS_Mapping(self):
      rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:PUSC:DMRS:MAPT?')
      return rdStr
      
   def Get_5GNR_DMRS_1stDMRSSym(self):
      rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:PUSC:DMRS:APOS?')
      return rdStr
      
   def Get_5GNR_DMRS_AddPosition(self):
      rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:PUSC:DMRS:IND?')
      return rdStr
      
   def Get_5GNR_DMRS_MSymbLen(self):
      rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:PUSC:DMRS:LENG?')
      return rdStr
      
   def Get_5GNR_DMRS_SeqGenMeth(self):
      #rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:PUSC:DMRS:APOS?')
      rdStr = "<TBD>"
      return rdStr
      
   def Get_5GNR_DMRS_SeqGenSeed(self):
      #rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:PUSC:DMRS:APOS?')
      rdStr = "<TBD>"
      return rdStr

   def Get_5GNR_DMRS_RelPwr(self):
      #rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:PUSC:DMRS:APOS?')
      rdStr = "<TBD>"
      return rdStr
   
#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   # this won't be run when imported 
   SMW = VSG()
   SMW.jav_Open("192.168.1.114")
   SMW.Set_5GNR_FreqRange('LOW')
   SMW.jav_Close()
