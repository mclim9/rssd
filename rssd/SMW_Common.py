#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Generator Common Functions
### Author : Martin C Lim
### Date   : 2018.02.01
### Requird: python -m pip install pyvisa
#####################################################################
from yaVISA import jaVisa

class VSG(jaVisa):
   def __init__(self):
      super(VSG,self).__init__()    #Python2/3
      self.Model = "SMW"
      
   #####################################################################
   ### SMW Arb
   #####################################################################
   def Set_ArbNextSeg(self,num):
      self.query('BB:ARB:WSEG:NEXT %d;*OPC?'%d)

   def Set_ArbState(self,sState):
      self.query('BB:ARB:STATE %s;*OPC?'%sState)

   def Set_ArbWv(self,InWv):
       self.query('BB:ARB:WAV:SEL "%s"; *OPC?'%InWv)
      
   def Set_ArbSeg(self,Seg):
       self.write('SOUR:BB:ARB:WSEG:NEXT %d'%Seg)
       self.write('SOUR:BB:ARB:WSEG:NEXT:EXEC')

   def Get_ArbClockFreq(self):
      SCPI = self.queryFloat('SOUR:BB:ARB:CLOC?')
      return SCPI

   def Set_ArbClockFreq(self,fFreq,RF=1):
      self.write('SOUR%d:BB:ARB:CLOC %f'%(RF,fFreq))

   def Get_ArbTime(self):
      Fs = Get_ArbClockFreq()
      Points = self.query('BB:ARB:WAV:POIN?').strip()
      WvTime = int(Points)/int(Fs)
      return WvTime
      
   #####################################################################
   ### SMW Generic
   #####################################################################
   def Init_Wideband(self):
      self.write('SOUR:POW:ATT:DIG 3')         #Set Digital Attenuation
      self.write('POW:ALC:STATE AUTO')         #Turn ALC ON|OFF|OFFT|AUTO|
      self.write('SOUR:POW:ALC:DAMP AUTO')     #Turn Driver AMP ON|OFF|AUTO
      self.write('SOUR:BB:IQG DB8')            #Baseband IQ gain
      
      ## Not so critical
      self.write('SOUR:AWGN:STAT 0')           #Turn AWGN off (default)
      self.write('BBIN:STAT OFF')              #Turn BB Input off(default)

   def Set_Freq(self,freq):
      self.write(':SOUR1:FREQ:CW %f'%freq);    #RF Freq

   def Set_IQMod(self,sState):
      ### ON, OFF 
      self.query('SOUR:POW:ALC:DAMP %s;*OPC?'%sState)
      
   #####################################################################
   ### Generator Power
   #####################################################################
   def Get_CrestFactor(self):
      PEP = self.Get_PowerPEP()
      RMS = self.Get_PowerRMS()
      return (PEP - RMS)

   def Get_PowerPEP(self,RF=1):
      SCPI = self.queryFloat('SOUR%d:POW:PEP?'%RF)
      return SCPI

   def Get_PowerRMS(self,RF=1):
      SCPI = self.queryFloat('SOUR%d:POW?'%RF)
      return SCPI

   def Set_RFPwr(self,fPow):   #fPow
      self.write('SOUR:POW %f'%fPow);          #RF Pwr
      
   def Set_RFState(self,sState):
      self.query('OUTP %s;*OPC?'%sState)

   def Set_DriveAmp(self,sState):
      ### ON, OFF, AUTO, FIX, 
      self.query('SOUR:POW:ALC:DAMP %s;*OPC?'%sState)
      
   #####################################################################
   ### NRP connected to SMW
   #####################################################################
   def Get_NRPPower(self,NRP=2):
      self.write(':INIT%d:POW:CONT 1'%(NRP))
      self.write('SENS%d:UNIT DBM'%(NRP))
      self.write('SENS%d:TYPE?'%(NRP))
      SCPI = self.queryFloat(':READ%d:POW?'%(NRP))
      return SCPI


   #####################################################################
   ### Verizon 5G
   #####################################################################
   def Set_V5GState(self,sState):
      self.write('SOUR1:BB:V5G:STAT %s;*OPC?'%sState)

   def Set_V5G_Wave(self,sWaveform):
      ### sWaveform = Uplink_Config_1
      self.query('SOUR1:BB:V5G:SETT:PCON "%s";*OPC?'%sWaveform)
      #self.write('SOUR1:BB:V5G:SETT:PCON "%s"'%sWaveform)


#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   # this won't be run when imported
   SMW = VSG()
#   SMW.jav_Open("192.168.1.114","Test.csv")
   SMW.jav_Open("127.0.0.1")
#   SMW.Set_Freq(6e9)
