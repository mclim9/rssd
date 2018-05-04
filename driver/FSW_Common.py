#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Analyzer Common Functions
### Author:  Martin C Lim
### Date:    2018.02.01
### Strctr : pyvisa-->yavisa-->FSW_Common.py
#####################################################################
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
      #print("Chan:%s in %s"%(Chan,ChList))
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
   ### FSW Input/Output
   #####################################################################
   def Set_Input(self,sType):
      self.write('INP:SEL %s'%sType);              #RF|AIQ|DIQ|FILE
   
   def Set_In_YIG(self,sState):
      self.write('INP:FILT:YIG:STATe %s'%sState);  #ON|OFF|0|1
      
   def Set_In_HPFilter(self,sState):               #Filter for 1-3GHz meas
      self.write('INP:FILT:HPASs:STATe %s'%sState) #ON|OFF|0|1
      
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

   def Set_Autolevel_Proto(self,sState):
   ### Used by WLAN for legacy reasons.  Please use ADJ:LEV;
      self.write('CONF:POW:AUTO %s;*WAI'%sState);  #ON|OFF|1|0

   def Get_RefLevel(self):
      RefLvl = self.query('DISP:TRAC:Y:RLEV?');
      return float(RefLvl)

   def Set_RefLevel(self,fReflevel):
      self.write('DISP:TRAC:Y:RLEV %f'%fReflevel);
      
   def Set_Preamp(self,sState):
      self.write('INP:GAIN:STAT %s;*WAI'%sState);

   def Get_Ovld_Stat(self):
      Read = int(self.query('STAT:QUES:POW:COND?').strip());
      RF_Ovld = Read & 1
      RF_Udld = Read & 2
      IF_Ovld = Read & 4
      return RF_Ovld | IF_Ovld
      
   #####################################################################
   ### FSW Frequency
   #####################################################################
   def Set_Freq(self,fFreq):
      self.write(':SENS:FREQ:CENT %.0f HZ'%fFreq);         #RF Freq

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
   ### FSW Equalization K544
   #####################################################################
   def Set_EQ_State(self,sState):
      FSW.write('SENS:CORR:FRES:Input1:USER:PRES');
      self.write('SENS:CORR:FRES:Input1:USER:STATe %s'%sState);

   def Set_EQ_File(self,sFile):
      #self.write('SENS:CORR:FRES:Input1:USER:SLIS1:SEL "c:\\R_S\\Instr\\Debug\\K544\\IFH.s2p"');
      self.write('SENS:CORR:FRES:Input1:USER:SLIS1:SEL "%s"'%sFile);
      
   #####################################################################
   ### FSW Time/Sweep
   #####################################################################
   def Set_SamplingRate(self,fFreq):
      self.write('TRAC:IQ:SRAT %f'%fFreq);

   def Set_SweepPoints(self,iNum):
      self.write(':SENS:SWE:POIN %f'%iNum);     #Number of trace points

   def Get_SweepPoints(self,iNum):
      points = self.write(':SENS:SWE:POIN?');   #Number of trace points
      return float(points.strip())
      
   def Get_SweepTime(self):
      RdTime = self.write('SENS:SWE:TIME?');             #Sweep/Capture Time
      return float(RdTime.strip())
      
   def Set_SweepTime(self,fSwpTime):
      self.write('SENS:SWE:TIME %f'%fSwpTime);  #Sweep/Capture Time

   def Set_SweepCont(self,iON):
      if iON > 0:
         self.write('INIT:CONT ON');            #Continuous Sweep
      else:
         self.write('INIT:CONT OFF');           #Single Sweep

   def Set_InitImm(self):
      self.query('INIT:IMM;*OPC?');
         
   def Get_Trace_Data(self,trace=1):
      self.write('FORM ASCII ')
      DataY = self.query('TRAC%d:DATA? TRACE1'%trace)
      DataX = self.query('TRAC%d:DATA:X? TRACE1'%trace)
      return [DataX.split(','),DataY.split(',')]
   
   def Set_Trace_Avg(self,sType,trace=1):
      self.write('DISP:TRAC%d:MODE AVER'%trace)
      self.write('SENS:DET1:FUNC AVER')
      self.write('SENS:AVER:TYPE %s'%sType)  #LIN|VID
      
   def Set_Trace_AvgCount(self,iAvg,trace=1):
      self.write('SENS:SWE:COUN %d'%(iAvg))
      
   def Set_Trace_AvgOff(self,trace=1):
      self.write('DISP:TRAC%d:MODE WRIT'%(trace))
   
   def Set_Trace_Detector(self,sDetect,trace=1):
      self.write('SENS:DET %s'%sDetect)      #RMS|
      
   #####################################################################
   ### FSW IQ Analyzer
   #####################################################################
   def Init_IQ(self):
      self.Set_Channel("IQ")
      
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
   
   def Get_IQ_RecLength(self):
      RLEN = self.query('TRAC:IQ:RLEN?')	         #Sweep Points
      print(RLEN)
      return int(RLEN)
      
   def Get_IQ_Data_Ascii(self,MLEN=1e3):
      CSVd = ""
      self.write('TRAC:DATA ASCII');      
      self.write('TRAC:IQ:DATA:FORM IQP');
      RLEN = self.Get_IQ_RecLength()               #Sweep Points
      numLoops  = int(round(RLEN/MLEN))+1
      for i in xrange(numLoops):                   #Read data in chunks
         
         SCPI = "TRAC:IQ:DATA:MEM? %d,%d"%((i * MLEN),MLEN)  #TRAC:IQ:DATA:MEM? <MemStrt>,<MLEN>
         CSVd = CSVd + self.query(SCPI)            #IQ Dump
      print("Memory Done Reading %d"%len(CSVd.split(',')))
      return CSVd

   def Get_IQ_Data(self,sFilename="file.iqw"):
    ####################################################################
    """ Get the IQ data and store to IQW file to process in VSE """
    ####################################################################
    self.write("FORM REAL,32")
    self.write("TRAC:IQ:DATA:FORM IQP")
    self.write("TRAC:IQ:DATA?")
    data = self.read_raw()

    samples = self.Get_IQ_RecLength()
    
    # Read num of digits to get for No of floats
    if int(samples) < 125000000:
        digits = data[1]
    else:
        digits = "10"
    
    """
    # Don't need this but including for completeness
    # Reads total number of bytes that holds IQ data
    
    i = 2
    totalbytes = ""
    while i <= int(digits)+1:
        totalbytes = totalbytes + data [i]
        i += 1
    """
        
    iqfile = open (sFilename, "wb")
    iqfile.write(data[2 + int(digits):])
    iqfile.close()
      
   #####################################################################
   ### FSW Common Query
   #####################################################################
   def Get_ACLR(self):
      ACLR = self.query(':CALC:MARK:FUNC:POW:RES? MCAC').split(',')
      return float(EVM)

   def Get_ChPwr(self):
      Power = self.query('FETC:SUMM:POW?')
      try:
         out = float(Power)
      except:
         out = -9999
      return out 
      
   def Get_EVM(self):
      #EVM = self.query('FETC:SUMM:EVM:ALL:AVER?')
      EVM = self.query('FETC:SUMM:EVM?')
      return float(EVM)

   def Get_EVM_Params(self):
      MAttn   = self.Get_AttnMech()
      RefLvl  = self.Get_RefLevel()
      Power   = self.Get_ChPwr()
      EVM     = self.Get_EVM()
      return ("%.2f,%.2f,%6.2f,%.2f"%(MAttn,RefLvl,Power,EVM))

   #####################################################################
   ### FSW marker
   #####################################################################
   def Get_Mkr_XY(self,iNum=1):
      ValX = self.query(':CALC:MARK%d:X?'%iNum).strip();
      ValY = self.query(':CALC:MARK%d:Y?'%iNum).strip();
      return [ValX, ValY]

   def Get_Mkr_Band(self,iNum=1):
      ValX = self.query(':CALC:MARK%d:X?'%iNum).strip();
      ValY = self.query(':CALC:MARK%d:FUNC:BPOW:'%iNum).strip();
      return [ValX, ValY]

   def Set_Mkr_Band(self,fFreq,iNum=1):
      self.write('CALC:MARK%d:FUNC:BPOW:STAT ON'%(iNum));
      self.write(':CALC1:MARK%d:FUNC:BPOW:SPAN %f'%(iNum, fFreq));

   def Get_Mkr_Freq(self,iNum=1):
      MkrFreq = self.query(':CALC1:MARK%d:X?'%(iNum)).strip();
      return float(MkrFreq)
      
   def Get_Mkr_TimeDomain(self,iNum=1):
      MkrFreq = self.query(':CALC1:MARK%d:X?'%(iNum)).strip();
      MkrPwr = self.query(':CALC:MARK%d:FUNC:SUMM:RMS:RES?'%(iNum)).strip();
      return [float(MkrFreq), MkrPwr]
      
   def Set_Mkr_Freq(self,fFreq,iNum=1):
      self.write(':CALC1:MARK%d:X %fHz'%(iNum,fFreq));

   def Set_Mkr_Next(self,iNum=1):
      self.write(':CALC:MARK%d:MAX:NEXT'%iNum);

   def Set_Mkr_Peak(self,iNum=1):
      self.write(':CALC:MARK%d:MAX:PEAK'%iNum);

   def Set_Mkr_Time(self,fSec,iNum=1):
      self.write(':CALC1:MARK%d:X %fS'%(iNum,fSec));

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   FSW = VSA()
   FSW.VISA_Open("192.168.1.109")
   FSW.Get_IQ_Data()


