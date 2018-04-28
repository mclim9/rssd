#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Analyzer Common Functions
### Author:  Martin C Lim
### Date:    2018.02.01
### Requird: python -m pip install pyvisa
###          yaVISA
import yaVISA

class VSA(yaVISA.RSVisa):
   def __init__(self):
      pass
      
   #####################################################################
   ### FSW Display
   #####################################################################
   def Set_Channel(self,Chan,sName=""):
      ##################################################################
      ### SANALYZER, IQ, PNOISE, NOISE, Spur, ADEM, V5GT, LTE, OFDMVSA
      ##################################################################
      if sName == "":
         sName = Chan
      ChList = self.query('INST:LIST?').split(',')
      print("Chan:%s in %s"%(Chan,ChList))
      if ("'" + sName + "'") in ChList:
         pass
      else:
         self.write(":INST:CRE %s,'%s'"%(Chan,sName))
      self.write(":INST:SEL '%s'"%sName)
      
   def Get_Channels(self):
      ChList = self.query('INST:LIST?').split(',')
      return(ChList)
   def Set_DisplayUpdate(self,state):
      self.write('SYST:DISP:UPD %s'%state);     #Display Update State
       
   #####################################################################
   ### FSW Attenuation
   #####################################################################
   def Get_AttnMech(self):
      MAttn   = self.query('INP:ATT?').strip()
      return float(MAttn)

   def Set_AttnMech(self,fMAttn):
      self.write('INP:EATT:STAT OFF');
      self.write('INP:ATT %.0f'%fMAttn);
      
   def Set_Autolevel(self):
      self.query('ADJ:LEV;*OPC?');

   def Get_RefLevel(self):
      RefLvl = self.query('DISP:TRAC:Y:RLEV?');
      return float(RefLvl)

   def Set_RefLevel(self,fReflevel):
      self.write('DISP:TRAC:Y:RLEV %f'%fReflevel);
      
   def Set_Preamp(self,sState):
      self.write('INP:GAIN:STAT %s;*WAI'%sState);

   #####################################################################
   ### FSW Frequency
   #####################################################################
   def Set_Freq(self,fFreq):
      self.write('FREQ:CENT %f'%fFreq);         #RF Freq

   def Set_FreqStart(self,fFreq):
      self.write(':SENS:FREQ:STAR %f'%fFreq);   #RF Freq

   def Set_FreqStep(self,fFreq):
      self.write(':SENS:FREQ:STEP %f'%fFreq);   #RF Freq

   def Set_FreqStop(self,fFreq):
      self.write(':SENS:FREQ:STOP %f'%fFreq);   #RF Freq

   def Set_ResBW(self,fFreq):
      if fFreq == 0:
         self.write(':SENS:BAND:RES:AUTO ON');
      else:
         self.write(':SENS:BAND:RES %f'%fFreq);
      
   def Set_Span(self,fFreq):
      self.write('SENS:FREQ:SPAN %f'%fFreq);
      
   def Set_VidBW(self,fFreq):
      if fFreq == 0:
         self.write(':SENS:BAND:VID:AUTO ON');
      else:
         self.write(':SENS:BAND:VID %f'%fFreq);

   #####################################################################
   ### FSW Time/Sweep
   #####################################################################
   def Set_SamplingRate(self,fFreq):
      self.write('TRAC:IQ:SRAT %f'%fFreq);

   def Set_SweepPoints(self,iNum):
      self.write(':SENS:SWE:POIN %f'%iNum);     #Number of trace points

   def Set_SweepTime(self,fSwpTime):
      self.write('SENS:SWE:TIME %f'%fSwpTime);  #Sweep/Capture Time

   def Set_SweepCont(self,iON):
      if iON > 0:
         self.write('INIT:CONT ON');            #Continuous Sweep
      else:
         self.write('INIT:CONT OFF');           #Single Sweep

   def Set_InitImm(self):
      self.query('INIT:IMM;*OPC?');
         
   #####################################################################
   ### FSW IQ Analyzer
   #####################################################################
   def Set_IQ_BW(self,fFreq):
      # IQ_BW = SamplingRate * 0.8
      self.write('TRAC:IQ:BWID %f'%fFreq);      #Analysis BW
      
   def Set_IQ_SamplingRate(self,fFreq):
      # SamplingRate = IQ_BW / 0.8
      self.write('TRAC:IQ:SRAT %f'%fFreq);      #Sampling Rate

   def Set_IQ_Samples(self,iNum):
      # Samples = MeasTime * SamplingRate
      self.write('TRAC:IQ:RLEN %d'%iNum);       #Samples
      
   def Set_IQ_WideBandMax(self,fFreq):
      self.write('TRAC:IQ:WBAN:STAT ON');       #Wideband reduction activated
      self.write('TRAC:IQ:WBAN:MBW %f; *WAI'%fFreq);
      
   #####################################################################
   ### FSW Common Query
   #####################################################################
   def Get_ACLR(self):
      ACLR = self.query(':CALC:MARK:FUNC:POW:RES? MCAC').split(',')
      return float(EVM)

   def Get_ChPwr(self):
      Power   = float(self.query('FETC:SUMM:POW?'))
      return Power
      
   def Get_EVM(self):
      EVM = self.query('FETC:SUMM:EVM?')
      return float(EVM)

   def Get_EVM_n_Params(self):
      MAttn   = self.Get_AttnMech()
      RefLvl  = self.Get_RefLevel()
      Power   = self.Get_ChPwr()
      EVM     = self.Get_EVM()
      return ("%.2f,%.2f,%6.2f,%.2f"%(MAttn,RefLvl,Power,EVM))

   #####################################################################
   ### FSW marker
   #####################################################################
   def Get_Mkr(self,iNum=1):
      ValX = self.query(':CALC:MARK%d:X?'%iNum).strip();
      ValY = self.query(':CALC:MARK%d:Y?'%iNum).strip();
      return [ValX, ValY]

   def Get_MkrBand(self,iNum=1):
      ValX = self.query(':CALC:MARK%d:X?'%iNum).strip();
      ValY = self.query(':CALC:MARK%d:FUNC:BPOW:'%iNum).strip();
      return [ValX, ValY]

   def Set_MkrBand(self,fFreq,iNum=1):
      self.write('CALC:MARK%d:FUNC:BPOW:STAT ON'%(iNum));
      self.write(':CALC1:MARK%d:FUNC:BPOW:SPAN %f'%(iNum, fFreq));

   def Get_MkrFreq(self,iNum=1):
      MkrFreq = self.query(':CALC1:MARK%d:X?'%(iNum)).strip();
      return float(MkrFreq)
      
   def Set_MkrFreq(self,fFreq,iNum=1):
      self.write(':CALC1:MARK%d:X %fHz'%(iNum,fFreq));

   def Set_MkrNext(self,iNum=1):
      self.write(':CALC:MARK%d:MAX:NEXT'%iNum);

   def Set_MkrPeak(self,iNum=1):
      self.write(':CALC:MARK%d:MAX:PEAK'%iNum);

   def Set_MkrTime(self,fSec,iNum=1):
      self.write(':CALC1:MARK%d:X %fS'%(iNum,fSec));

   #####################################################################
   ### FSW V5G
   #####################################################################
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
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   FSW = VSA()
   FSW.VISA_Open("192.168.1.109")
   FSW.VISA_IDN()
   print FSW.Get_MkrXY()
