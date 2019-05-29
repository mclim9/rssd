# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: NRQ Common Functions
### Author : Martin C Lim
### Date   : 2018.02.01
#####################################################################
from rssd.yaVISA import jaVisa

class NRQ(jaVisa):
    """ Rohde & Schwarz NRQ6 Object """
    def __init__(self):
        super(NRQ, self).__init__()
        self.Model = "NRQ"
        
    #####################################################################
    ### NRQ Display
    #####################################################################
    def Get_Channels(self):
        ChList = self.query('INST:LIST?').split(',')
        return(ChList)
        
    def Set_DisplayUpdate(self,state):
        # Param: ON|OFF
        self.write('SYST:DISP:UPD %s'%state);                  #Display Update State
         
    #####################################################################
    ### NRQ Common Settings
    #####################################################################
    def Set_Freq(self,fFreq):
        self.write('SENS:FREQ %.0f'%fFreq)

    def Get_Freq(self):
        SRead = self.queryFloat(':SENS:FREQ?')
        return SRead

    def Set_Attn(self,fAttn):
        if fFreq == 0:
            self.write(':SENS:INP:ATT:AUTO ON')
        else:
            self.write(':SENS:INP:ATT:AUTO OFF')
            self.write(':SENS:INP:ATT %f'%fAttn)
            
    def Get_Power(self):
        self.write('UNIT:POW DBM')
        self.write('SENS:FUNC "POW:AVG"')
        self.write('INIT:CONT ON')
        fRead = self.queryFloat('FETCH?')
        return fRead
        
    #####################################################################
    ### NRQ IQ Commands
    #####################################################################
    def Get_IQ_SamplingRate(self):
        # SamplingRate = IQ_BW / 0.8
        iRead = self.queryFloat(':SENS:BAND:SRAT?')                     #Sampling Rate
        return iRead
        
    def Set_IQ_SamplingRate(self,fFreq):
        # SamplingRate = IQ_BW / 0.8
        self.write('SENS:BAND:TYPE SRAT')
        self.write('SENS:BAND:VAR ON')
        self.write('SENS:BAND:SRAT %d'%fFreq);                     #Sampling Rate
        
    def Get_IQ_RecLength(self):
        iRead = self.queryInt('SENS:TRAC:IQ:RLEN?')
        return iRead

    def Set_IQ_RecLength(self,iLen):
        self.write('SENS:TRAC:IQ:RLEN %d'%iLen)
 
    def Get_IQ_Data(self):
        self.write('SENS:FUNC “XTIM:VOLT:IQ”')
        self.write('SENS:BAND:TYPE SRAT')
        self.write('TRIG:SOUR IMM')
        self.write('SENS:TRAC:IQ:DATA:FORM IQPAIR')
        self.write('FORM:DATA REAL,32')
        self.write('INIT:IMM')
        self.write('FETCH?')
        
    def Get_IQtoIQW(self):
        ####################################################################
         """ Get the IQ data and store to IQW file to process in VSE """
         ####################################################################
         self.write("SENS:FUNC 'XTIM:VOLT:IQ'")
         self.write("SENS:TRAC:IQ:DATA:FORM IQPAIR")
         self.write("FORM:DATA REAL,32")
         #self.write("FORM:DATA ASCII")

         self.write("INIT:IMM")
         self.write("FETCH?")
         data = self.jav_read_raw()
         
         # Read num of digits to get for No of floats
         if self.Get_IQ_RecLength() < 125000000:
              digits = data[1]
              print(digits)
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
              
         iqfile = open ('nrq.iqw', "wb")
         iqfile.write(data[2 + int(digits):])
         iqfile.close()
            
#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    NRQ6 = NRQ()
#    NRQ6.jav_Open("NRQ6-101507.local")
    NRQ6.jav_Open("192.168.1.40")
    NRQ6.Get_IQtoIQW()
    NRQ6.jav_ClrErr()
