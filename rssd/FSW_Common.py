#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Analyzer Common Functions
### Author:  Martin C Lim
### Date:    2018.02.01
### Strctr : pyvisa-->yavisa-->FSW_Common.py
#####################################################################
from rssd.yaVISA import jaVisa

class VSA(jaVisa):
   def __init__(self):
      super(VSA, self).__init__()
      self.Model = "FSW"
      
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
         self.query(":INST:CRE %s,'%s';*OPC?"%(Chan,sName))
      self.query(":INST:SEL '%s';*OPC?"%sName)
      
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
      out = self.queryFloat('INP:ATT?')
      return out 

   def Set_AttnMech(self,fMAttn):
      self.write('INP:EATT:STAT OFF');
      self.write('INP:ATT %.0f'%fMAttn);
      
   def Set_Autolevel(self):
      self.query('ADJ:LEV;*OPC?');

   def Set_Autolevel_Proto(self,sState):
   ### Used by WLAN; K96.  Please use ADJ:LEV;
      self.write('CONF:POW:AUTO %s;*WAI'%sState);     #ON|OFF|1|0

   def Get_RefLevel(self):
      RefLvl = self.queryFloat('DISP:TRAC:Y:RLEV?');
      return RefLvl

   def Set_RefLevel(self,fReflevel):
      self.write('DISP:TRAC:Y:RLEV %f'%fReflevel);
      
   def Set_Preamp(self,sState):
      self.write('INP:GAIN:STAT %s;*WAI'%sState);     #ON|OFF|1|0

   def Get_Ovld_Stat(self):
      self.Set_InitImm()
      Read = self.queryInt('STAT:QUES:POW:COND?')
      RF_Ovld = Read & 1
      RF_Udld = Read & 2
      IF_Ovld = Read & 4
      return Read
      
   def Set_Autolevel_IFOvld(self):
      ####################################################################
      """ Algorithm designed by Darren Tipton, RSUK"""
      """ Optimise level for Mixer Input => Optimal EVM """
      """ Optimises for signals using IF gain as well as 1dB steps """    
      ####################################################################
      optmix = 10                     # Optimal mixer level
      self.Set_SweepCont(0)
      self.Set_Autolevel()
      level = self.Get_Mkr_TimeDomain()
      
      """ Switch Pre-Amp """                                                             
      if level >= -20:
         self.query("INP:GAIN:STAT OFF; *OPC?")
         gain = 0
         maxmix = 0
      else:
         self.query("INP:GAIN:STAT ON; *OPC?")     
         gain = 20
         maxmix = -30
      
      rfatt = level + gain - optmix    #Calc RfAttn for optimal mixer level
      if rfatt < 0: rfatt = 0          #If calculated RF atten < 0, set 0
      self.Set_AttnMech(rfatt)         #Set Attenuation
       
      reflev = maxmix + rfatt
      self.Set_RefLevel(reflev)        #Set RefLevel

      ifovl = self.Get_Ovld_Stat()     #Check Overload
      print ("Inital: Ovl:%d Attn:%d RfLvl:%d"%(ifovl,rfatt,reflev))

      """ Optimising for attenuation """
      while ifovl != 0:
         print ("ATloop: Ovl:%d Attn:%d RfLvl:%d"%(ifovl,rfatt,reflev))
         rfatt = rfatt + 1
         self.Set_AttnMech(rfatt)

         reflev = maxmix + rfatt
         self.Set_RefLevel(reflev)

         """ Check if there is IF Overload """
         ifovl = self.Get_Ovld_Stat()

      """ Optimising for reference level """
      while reflev > (-20 - gain) and ifovl == 0:
         print ("RefLop: Ovl:%d Attn:%d RfLvl:%d"%(ifovl,rfatt,reflev))
         reflev = reflev - 1
         self.Set_RefLevel(reflev)

         """ Check if there is IF Overload """        
         ifovl = self.Get_Ovld_Stat()
       
      """ Final check for IF Overload """
      if ifovl != 0:
         reflev = reflev + 1
         self.Set_RefLevel(reflev)
      print ("Final : Ovl:%d Attn:%d RfLvl:%d"%(ifovl,rfatt,reflev))

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
      points = self.queryInt(':SENS:SWE:POIN?');   #Number of trace points
      return points
      
   def Get_SweepTime(self):
      SwpTime = self.queryInt('SENS:SWE:TIME?');             #Sweep/Capture Time
      return SwpTime
      
   def Set_SweepTime(self,fSwpTime):
      self.write('SENS:SWE:TIME %f'%fSwpTime);  #Sweep/Capture Time

   def Set_SweepCont(self,iON):
      if iON == 1:
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
   
   def Set_Trace_Detector(self,sDetect,iWind):
      #APE; NEG; POS; QPE; SAMP; RMS; CAV; CRMS
      self.write('SENS:WIND%d:DET %s'%(iWind,sDetect))      #RMS|

   #####################################################################
   ### FSW Trigger
   #####################################################################
   def Set_Trig1_Source(self,sDetect):
      #IMM; EXT; EXT2; EXT3; RFP; IFP; TIME; VID; PSEN 
      self.write('TRIG:SEQ:SOUR %s'%sDetect)      #RMS|
   
   def Set_Trig2_Dir(self,sDir):
      if (sDir == 'OUT'):
         self.write('OUTP:TRIG2:DIR OUTP')
      else:
         self.write('OUTP:TRIG2:DIR INP')
      
   def Set_Trig2_OutType(self,sDir):
      #DEV : Device
      #TARM: Trigger Armed
      #UDEF: User Defined
      self.write('OUTP:TRIG2:OTYP %s')

   #####################################################################
   ### FSW IQ Analyzer
   #####################################################################
   def Init_IQ(self):
      self.Set_Channel("IQ")
      
   def Set_IQ_BW(self,fFreq):
      # IQ_BW = SamplingRate * 0.8
      self.write('TRAC:IQ:BWID %f'%fFreq);      #Analysis BW
      
   def Get_IQ_RecLength(self):
      RLEN = self.queryInt('TRAC:IQ:RLEN?')	      #Record(Samples) Length
      return RLEN

   def Set_IQ_RecLength(self,iLen):
      self.query('TRAC:IQ:RLEN %d'%iLen)        #Record(Samples) Length
      
   def Set_IQ_SamplingRate(self,fFreq):
      # SamplingRate = IQ_BW / 0.8
      self.write('TRAC:IQ:SRAT %f'%fFreq);      #Sampling Rate

   def Set_IQ_Samples(self,iNum):
      # Samples = MeasTime * SamplingRate
      self.write('TRAC:IQ:RLEN %d'%iNum);       #Samples
      
   def Set_IQ_SpectrumWindow(self):
      self.write(":LAY:ADD:WIND? '1',RIGH,FREQ")
      self.write(":DISP:WIND2:SUBW:SEL")
      
   def Set_IQ_Time(self,fSwpTime):
      self.Set_SweepTime(fSwpTime)

   def Set_IQ_WideBandMax(self,fFreq):
      self.write('TRAC:IQ:WBAN:STAT ON');       #Wideband reduction activated
      self.write('TRAC:IQ:WBAN:MBW %f; *WAI'%fFreq);

   def Get_IQ_Data_Ascii(self,MLEN=1e3):
      CSVd = ""
      self.write('TRAC:DATA ASCII');      
      self.write('TRAC:IQ:DATA:FORM IQP');
      RLEN = self.Get_IQ_RecLength()            #Sweep Points
      numLoops  = int(round(RLEN/MLEN))+1
      for i in xrange(numLoops):                #Read data in chunks
         
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
      data = self.jav_read_raw()

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
   ### FSW ACLR
   #####################################################################
   def Init_ACLR(self):
      self.Set_Channel("Spectrum")
      self.write('CALC:MARK:FUNC:POW:SEL ACP')
   
   def Set_ACLR_CHBW(self,dCHBW):
      self.write('POW:ACH:BAND %d'%dCHBW)
      
   def Set_ACLR_AdjBW(self,dCHBW):
      self.write('POW:ACH:BAND:ACH %d;ALT1 %d;ALT2 %d'%(dCHBW,dCHBW,dCHBW))

   def Set_ACLR_AdjSpace(self,dCHBW):
      self.write('POW:ACH:SPAC:ACH %d;ALT1 %d;ALT2 %d'%(dCHBW,dCHBW,dCHBW))


   #####################################################################
   ### FSW Common Query
   #####################################################################
   def Get_ACLR(self):
      ACLR = self.query(':CALC:MARK:FUNC:POW:RES? MCAC')
      return ACLR

   def Get_ChPwr(self):
      out = self.queryFloat('FETC:SUMM:POW?')
      return out 
      
   def Get_EVM(self):
      #EVM = self.query('FETC:SUMM:EVM:ALL:AVER?')
      out = self.queryFloat('FETC:SUMM:EVM?;*WAI').strip()
      return out

   def Get_EVM_Params(self):
      MAttn   = self.Get_AttnMech()
      RefLvl  = self.Get_RefLevel()
      Power   = self.Get_ChPwr()
      EVM     = self.Get_EVM()
      return ("%.2f,%.2f,%6.2f,%.2f"%(MAttn,RefLvl,Power,EVM))

   #####################################################################
   ### FSW marker
   #####################################################################
   def Get_Mkr_XY(self,iNum=1,iWind=1):
      ValX = self.query(':CALC%d:MARK%d:X?'%(iWind,iNum)).strip()
      ValY = self.query(':CALC%d:MARK%d:Y?'%(iWind,iNum)).strip()
      return [ValX, ValY]

   def Get_Mkr_Band(self,iNum=1,iWind=1):
      ValX = self.query(':CALC%d:MARK%d:X?'%(iWind,iNum)).strip();
      ValY = self.query(':CALC%d:MARK%d:FUNC:BPOW:RES?'%(iWind,iNum)).strip();
      return [ValX, ValY]

   def Set_Mkr_Band(self,fFreq,iNum=1,iWind=1):
      self.write(':CALC%d:MARK%d:FUNC:BPOW:STAT ON'%(iWind,iNum));
      self.write(':CALC%d:MARK%d:FUNC:BPOW:SPAN %f'%(iWind,iNum, fFreq));

   def Get_Mkr_Freq(self,iNum=1,iWind=1):
      MkrFreq = self.queryFloat(':CALC%d:MARK%d:X?'%(iWind,iNum))
      return float(MkrFreq)
      
   def Get_Mkr_TimeDomain(self,iNum=1,iWind=1):
     # self.write(':CALC:MARK%d:FUNC:SUMM:STAT ON'%iNum)
      MkrFreq = self.query(':CALC%d:MARK%d:X?'%(iWind,iNum)).strip();
      MkrPwr  = self.query(':CALC%d:MARK%d:FUNC:SUMM:RMS:RES?'%(iWind,iNum)).strip();
      return float(MkrPwr)
            
   def Set_Mkr_Freq(self,fFreq,iNum=1,iWind=1):
      self.write(':CALC%d:MARK%d:X %fHz'%(iWind,iNum,fFreq));

   def Set_Mkr_Next(self,iNum=1,iWind=1):
      self.write(':CALC%d:MARK%d:MAX:NEXT'%(iWind,iNum));

   def Set_Mkr_Peak(self,iNum=1,iWind=1):
      self.write(':CALC%d:MARK%d:MAX:PEAK'%(iWind,iNum));

   def Set_Mkr_Time(self,fSec,iNum=1):
      self.write(':CALC1:MARK%d:X %fS'%(iNum,fSec));

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   FSW = VSA()
   FSW.jav_Open("192.168.1.109")
   #FSW.Set_Autolevel_IFOvld()
#   FSW.jav_ClrErr()
   FSW.Set_Trig2_Dir('OUT')
   del FSW
