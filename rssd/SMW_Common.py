#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Generator Common Functions
### Author : Martin C Lim
### Date   : 2018.02.01
### Requird: python -m pip install pyvisa
#####################################################################
from yaVISA 

<<<<<<< HEAD
class VSG(yaVISA.jaVisa,object):
=======
class VSG(jaVisa):
>>>>>>> remotes/origin/object-inheritance-proposal
   def __init__(self):
      try:
         super().__init__()            #Python3
      except:
         super(VSG,self).__init__()    #Python2
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
      SCPI = self.query('SOUR:BB:ARB:CLOC?')
      return float(SCPI)

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

   def Set_RFPwr(self,fPow):   #fPow
      self.write('SOUR:POW %f'%fPow);          #RF Pwr
      
   def Set_RFState(self,sState):
      self.query('OUTP %s;*OPC?'%sState)

   def Set_DriveAmp(self,sState):
      ### ON, OFF, AUTO, FIX, 
      self.query('SOUR:POW:ALC:DAMP %s;*OPC?'%sState)
      
   def Set_IQMod(self,sState):
      ### ON, OFF 
      self.query('SOUR:POW:ALC:DAMP %s;*OPC?'%sState)
      
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
   SMW.jav_Open("192.168.1.114","Test.csv")
   SMW.Set_Freq(6e9)
