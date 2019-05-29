# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: NRP Power Sensor
### Author : Martin C Lim
### Date   : 2018.05.18
### Requird: python -m pip install pyvisa
### 
### VISAFmt: USB0::0x0AAD::0x0138::100961::INSTR
###             <VS>::<Manu>::<Modl>::<SerN>::INSTR
###             TCPIP0::NRPM3-900105::inst0
### 
###    Product  |USB ID          Product  |USB ID
###    ---------|------          ---------|------
###    NRP8S      0x00E2          NRP33SN-V 0x0168
###    NRP8SN     0x0137          NRP40S     0x015F
###    NRP18S     0x0138          NRP40SN    0x0160
###    NRP18SN    0x0139          NRP50S     0x0161
###    NRP33S     0x0145          NRP50SN    0x0162
###    NRP33SN    0x0146          NRPM        0x0195
#####################################################################
from rssd.yaVISA import jaVisa

class PMr(jaVisa):
    """ Rohde & Schwarz Power Meter Object """
    def __init__(self):
        super(PMr,self).__init__()     #Python2/3
        self.Model = "NRP"
        
    #####################################################################
    ### NRP Common
    #####################################################################
    def Get_AvailableNRP(self):
        resList = self.jav_reslist()
        asdf = [s for s in resList if "USB0::0x0AAD::0x" in s]
        print(asdf)
        
    def Get_Average(self):
        outp = self.queryInt('SENS:AVER:COUN?')
        return outp

    def Set_Average(self,iAvg):
        self.write('SENS:AVER:COUN %d'%iAvg)

    def Set_AverageMode(self,bAuto):
        if bAuto == 0:
            self.write('SENS:AVER:COUN:AUTO OFF')
        else:
            self.write('SENS:AVER:COUN:AUTO ON')

    def Get_Freq(self):
        outp = self.query(':SENS:FREQ?')
        return outp
        
    def Set_Freq(self,fFreq):
        self.query('SENS:FREQ %f;*OPC?'%fFreq)

    def Get_Offset(self):
        ### Offset = Loss
        ### +Num => +Reading
        ### -Num ==> -Reading
        outp = self.queryFloat('SENS:CORR:OFFS?')
        return outp
        
    def Get_Power(self):
        self.write('UNIT:POW DBM')
        self.write('SENS:FUNC "POW:AVG"')
        self.write('INIT:IMM')          
        outp = self.queryFloat('FETCH?')
        return outp

    def Get_PowerAll(self):
        ### NRP3M
        self.write('UNIT:POW DBM')
#        self.write('SENS:FUNC "POW:AVG"')
        self.write('SENS:CHAN1:ENAB ON')
        self.write('SENS:CHAN2:ENAB ON')
        self.write('SENS:CHAN3:ENAB ON')
        self.query('INIT:IMM;*OPC?')
        outp = self.queryFloat('FETCH:ALL?')
        return outp
        
    def Set_PowerOffset(self,fOffset):
        self.write('SENS:CORR:OFFS:STAT ON')
        self.write('SENS:CORR:OFFS %f'%fOffset)

    def Set_PowerOffsetState(self,bState):
        if (bState == 1) or (bState == 'ON'):
            self.write('SENS:CORR:OFFS:STAT ON')
        else:
            self.write('SENS:CORR:OFFS:STAT OFF')

    def Set_InitImm(self):
        outp = self.query('INIT:IMM;*OPC?')
        
#####################################################################
### NRP Trigger
#####################################################################
    def Set_TriggerSource(self,sSource):
        # BUS; EXT2
        self.write('TRIG:SOUR %s'%sSource)

    def Set_TriggerAuto(self,bState):
        if (bState == 1) or (bState == 'ON'):
            self.write('TRIG:ATR:STAT ON')        #Auto-Trigger ON
        else:
            self.write('TRIG:ATR:STAT OFF')      #Auto-Trigger OFF

    def Set_TriggerCount(self,iNum):
        self.write('TRIG:COUN %d'%iNum)
        
        
#####################################################################
### NRP Advanced
#####################################################################
    def Get_EventStatus(self):
        outp = self.query('STAT:OPER:MEAS:EVEN?')
        return outp
        
    def Set_BufferSize(self,iSize):
        self.write('SENS:BUFF:SIZE %d'%iSize)                #Buffer size is randomly selected to 17

    def Get_BufferedMeas(self,bState):
        if (bState == 1) or (bState == 'ON'):
            self.write('SENS:BUFF:STAT ON')                #Configure a buffered measurement
        else:
            self.write('SENS:BUFF:STAT ON')                #Configure a buffered measurement

    
#####################################################################
### NRPM
###    - NRP-ZKU    USB cable (3.0m) to R&S®NRPxxS(N)
###    - NRPM3      OTA power sensor 
###    - NRPM-ZKD3 Interface cable; R&S®NRPM3 to R&S®NRPM-ZD3
###    - NRPM-ZD3  Cable feedthrough for anechoic chamber
###    - NRPM-Axx  OTA Antenna module: A66(27-75)
#####################################################################
    def Set_Sys_LED(self,bState,iSensor=1):
        if bState == 1:
            self.write('SYST:LED:CHAN%d:COL 255'%iSensor)
        else:
            self.write('SYST:LED:CHAN%d:COL 0'%iSensor)
                            
#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    # this won't be run when imported
    NRP = PMr()
    NRP.Get_AvailableNRP()
    NRP.jav_openvisa("USB0::0x0AAD::0x0196::900105::INSTR")
#    NRP.jav_logscpi()
#    NRP.jav_Reset()
#    NRP.Set_Freq(24e9)  
#    NRP.Get_Power()
    print("asdf")
#    NRP.jav_ClrErr()
