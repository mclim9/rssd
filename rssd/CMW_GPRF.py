#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: CMW100 General Purpose RF Functions
### Author:  Martin C Lim
### Date:    2018.05.29
### Strctr : pyvisa-->yavisa-->CMW_GPRF.py
#####################################################################
import yaVISA

class BSE(yaVISA.jaVisa):
   def __init__(self):
      super(BSE, self).__init__()
      self.Model = "CMW-GPRF"

   #####################################################################
   ### CMW System
   #####################################################################
   def Set_Channel(self,Chan,sName=""):
      ##################################################################
      ### SANALYZER, IQ, PNOISE, NOISE, Spur, ADEM, V5GT, LTE, OFDMVSA
      ##################################################################
      if sName == "":
         sName = Chan
      ChList = self.query('INST:LIST?').split(',')
      #print("Chan:%s in %s"%(Chan,ChList))
      if ("'" + sName + "'") in ChList:
         pass
      else:
         self.query(":INST:CRE %s,'%s';*OPC?"%(Chan,sName))
      self.query(":INST:SEL '%s';*OPC?"%sName)
      
   def Get_Channels(self):
      ChList = self.query('INST:LIST?').split(',')
      return(ChList)
      
   def Set_DisplayUpdate(self,state):
      self.write('SYST:DISP:UPD %s'%state);     #Display Update State
            
   #####################################################################
   ### CMW Port Configuration
   #####################################################################
   def Set_Sys_PortAttn(self):
      CONF:CMWS:FDC:DEAC:TX R11
      CONF:BASE:FDC:CTAB:CRE 'downlink', 500.0e6, 0.5, 1000e6, 1.0, 1800.e6, 1.5, 2300.e6, 1.8, 5000.e6, 2.5,  6000.e6, 2.8  
      CONF:CMWS:FDC:ACT:TX R11, 'downlink'
      CONF:CMWS:FDC:DEAC:RX R12
      CONF:BASE:FDC:CTAB:CRE 'uplink', 500.0e6, 19.5, 1000e6, 19.0, 1800.e6, 18.5, 2300.e6, 18.2, 5000.e6, 17.5,  6000.e6, 17.2
      CONF:CMWS:FDC:ACT:RX R12, 'uplink'

            
   #####################################################################
   ### CMW Vector Spectrum Analyzer
   #####################################################################
   def Get_VSA_ACLR(self):
      ACLR = self.query('FETC:NRS:MEAS:MEV:ACLR:AVER?').split(',')
      return ACLR

   def Get_ChPwr(self):
      out = self.queryFloat('FETC:SUMM:POW?')
      return out 
   
   def Set_VSA_Freq(self,fFreq):
      self.write('CONF:GPRF:MEAS:SPEC:FREQ:CENT %f'%fFreq)

   def Set_VSA_FreqSpan(self,fFreq):
      self.write('CONF:GPRF:MEAS:SPEC:FREQ:SPAN %f'%fFreq)

   def Set_VSA_RefLevl(self,fRefLvl):
      ### ENP = Expected Nominal Power
      self.write('CONF:GPRF:MEAS:RFS:ENP %f'%fRefLvl)

   def Set_VSA_InitImm(self):
      self.query('INIT:GPRF:MEAS:SPEC;*OPC?')
   
   def Set_VSA_ResBW(self,fFreq):
      if fFreq > 0:
         self.write('CONF:GPRF:MEAS:SPEC:FSW:RBW %f'%fFreq)
      else:
         self.write('CONF:GPRF:MEAS:SPEC:FSW:RBW:AUTO ON')
         
   def Set_VSA_VidBW(self,fFreq):
      if fFreq > 0:
         self.write('CONF:GPRF:MEAS:SPEC:FSW:VBW %f'%fFreq)
      else:
         self.write('CONF:GPRF:MEAS:SPEC:FSW:VBW:AUTO ON')
   
   def Set_VSA_SweepTime(self,fTime):
      if fTime > 0:
         self.write('CONF:GPRF:MEAS:SPEC:FSW:SWT %f'%fTime)
      else:
         self.write('CONF:GPRF:MEAS:SPEC:FSW:SWT:AUTO ON')
         

         
   #####################################################################
   ### CMW Generator
   #####################################################################
   def Get_Gen_ArbWv(self):
      SCPI = self.query('SOUR:GPRF:GEN:ARB:FILE?')
      return SCPI

   def Set_Gen_ArbWv(self,sName):
      #self.write(':SOUR:GPRF:GEN:ARB:FILE 'C:\ProgramData\Rohde-Schwarz\CMW\Data\waveform\NRsub6G_ARB_Waveforms\NR_CP_SCS30kHz_BW20MHz_16-QAM_cellID3.wv')
      self.write(":SOUR:GPRF:GEN:ARB:FILE '%s'"%sName)

   def Set_Gen_ArbStateOn(self):
      self.query('SOUR:GPRF:GEN:BBM ARB;*OPC?')

   def Set_Gen_Freq(self,freq):
      self.write('SOUR:GPRF:GEN:RFS:FREQ %f'%freq);    #RF Freq

   def Set_Gen_ListMode(self,sState):
      if sState.upper() == "ON":
         self.query('SOUR:GPRF:GEN:LIST ON;*OPC?')
      else:
         self.query('SOUR:GPRF:GEN:LIST OFF;*OPC?')

   def Set_Gen_RFPwr(self,fPwr):
      self.write('SOUR:GPRF:GEN:RFS:LEV %f'%(fPwr));

   def Set_Gen_RFState(self,sState):
      ### ON | OFF
      if sState.upper() == "ON":
         self.query('SOUR:GPRF:GEN:STAT ON;*OPC?')
      else:
         self.query('SOUR:GPRF:GEN:STAT OFF;*OPC?')
         
#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   CMW = BSE()
   CMW.jav_Open("127.0.0.1")
   CMW.jav_ClrErr()
