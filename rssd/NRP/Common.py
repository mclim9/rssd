"""
### Purpose : NRP Power Sensor
###
### VISAFmt : RSNRP::0x0138::100961::INSTR
###           RSNRP::<Modl>::<SerN>::INSTR
###           USB::0x0AAD::<Modl>::<SerN>::INSTR
###
### Product  |USB ID      Product  |USB ID
### ---------|------      ---------|------
### NRP8S     0x00E2      NRP33SN-V 0x0168
### NRP8SN    0x0137      NRP40S    0x015F
### NRP18S    0x0138      NRP40SN   0x0160
### NRP18SN   0x0139      NRP50S    0x0161
### NRP33S    0x0145      NRP50SN   0x0162
### NRP33SN   0x0146      NRPM      0x0195
###
### Product  |USB ID      Product  |USB ID      Product  |USB ID
### ---------|------      ---------|------      ---------|------
### NRP-Z11  0x00C        NRP-Z31    0x02C      NRP-Z81    0x023
### NRP-21   0x003        NRP-Z37    0x02D      NRP-Z85    0x083
### NRP-Z22  0x013        NRP-Z51    0x016      NRP-Z86    0x095
### NRP-Z23  0x014        NRP-Z52    0x017      NRP-Z91    0x021
### NRP-Z24  0x015        NRP-Z55    0x018      NRP-Z92    0x062
### NRP-Z27  0x02F        NRP-Z56    0x019      NRP-Z98    0x052
### NRP-Z28  0x051        NRP-Z57    0x070"""
import numpy as np
from rssd.yaVISA import jaVisa

class PMr(jaVisa):
    """ Rohde & Schwarz Power Meter Object """
    def __init__(self):
        super(PMr,self).__init__()     # Python2/3
        self.Model = "NRP"

    #####################################################################
    ### NRP Get Methods
    #####################################################################
    def Get_AvailableNRP(self):
        resList = self.jav_reslist()
        asdf = [s for s in resList if "USB0::0x0AAD::0x" in s]
        print(asdf)

    def Get_Average(self):
        outp = self.queryInt('SENS:AVER:COUN?')
        return outp

    def Get_Freq(self):
        outp = self.query(':SENS:FREQ?\n')
        return outp

    def Get_BufferedMeas(self,bState):
        if (bState == 1) or (bState == 'ON'):
            self.write('SENS:POW:AVG:BUFF:STAT ON')                #Configure a buffered measurement
        else:
            self.write('SENS:POW:AVG:BUFF:STAT ON')                #Configure a buffered measurement

    def Get_EventStatus(self):
        outp = self.query('STAT:OPER:MEAS:EVEN?')
        return outp

    def Get_Offset(self):
        ### Offset = Loss
        ### +Num => +Reading
        ### -Num ==> -Reading
        outp = self.queryFloat('SENS:CORR:OFFS?')
        return outp

    def Get_Power(self):
        # self.write('UNIT:POW DBM')  # Not a function for NRP-Zxx
        # self.write('SENS:FUNC "POW:AVG"')
        self.write(':INIT:IMM')
        outp = self.query('FETCH?\n')
        self.write(':INIT:CONT OFF')
        print('Done')
        x = np.fromstring(outp,dtype=np.float, sep=',')             # Convert String to Float
        y = np.multiply(10,(np.log10(abs(np.multiply(x,1000)))))    # Convert Watts to dBm
        return outp

    def Get_NRPM_PowerAll(self):
        ### NRP3M
        self.write('UNIT:POW DBM')
        # self.write('SENS:FUNC "POW:AVG"')
        self.write('SENS:CHAN1:ENAB ON')
        self.write('SENS:CHAN2:ENAB ON')
        self.write('SENS:CHAN3:ENAB ON')
        self.query('INIT:IMM;*OPC?')
        outp = self.queryFloat('FETCH:ALL?')
        return outp

#####################################################################
### NRP Set Methods
#####################################################################
    def Set_Aperture(self,fAPR):
        self.write('SENS:POW:AVG:APER %f'%fAPR)

    def Set_Average(self,iAvg):
        self.write('SENS:AVER:COUN %d'%iAvg)

    def Set_AverageMode(self,sState):
        """ON | OFF"""
        if sState in (1,'1','ON'):
            self.write('SENS:AVER:COUN:AUTO OFF')
        elif sState in (0,'0','OFF'):
            self.write('SENS:AVER:COUN:AUTO ON')

    def Set_BufferSize(self,iSize):
        self.write('SENS:POW:AVG:BUFF:SIZE %d'%iSize)                #Buffer size is randomly selected to 17

    def Set_Freq(self,fFreq):
        self.write('SENS:FREQ %f'%fFreq)

    def Set_Function(self,sFunc):
        """ POW:AVG """
        self.write('SENS:FUNC "%s"'%sFunc)

    def Set_InitImm(self):
        self.write('INIT:IMM')

    def Set_InitCont(self,sState):
        """ ON; OFF """
        self.write('INIT:CONT %s'%sState)

    #####################################################################
    ### NRPM
    ###    - NRP-ZKU    USB cable (3.0m) to R&S®NRPxxS(N)
    ###    - NRPM3      OTA power sensor
    ###    - NRPM-ZKD3 Interface cable; R&S®NRPM3 to R&S®NRPM-ZD3
    ###    - NRPM-ZD3  Cable feedthrough for anechoic chamber
    ###    - NRPM-Axx  OTA Antenna module: A66(27-75)
    #####################################################################
    def Set_NRPM_LED(self,sState,iSensor=1):
        """ON | OFF"""
        if sState in (1,'1','ON'):
            self.write('SYST:LED:CHAN%d:COL 255'%iSensor)
        elif sState in (0,'0','OFF'):
            self.write('SYST:LED:CHAN%d:COL 0'%iSensor)

    def Set_PowerOffset(self,fOffset):
        self.write('SENS:CORR:OFFS:STAT ON')
        self.write('SENS:CORR:OFFS %f'%fOffset)

    def Set_PowerOffsetState(self,sState):
        """ON | OFF"""
        if sState in (1,'1','ON'):
            self.write('SENS:CORR:OFFS:STAT ON')
        elif sState in (0,'0','OFF'):
            self.write('SENS:CORR:OFFS:STAT OFF')

    def Set_TriggerSource(self,sSource):
        """BUS; EXT2; INT; IMM """
        self.write('TRIG:SOUR %s'%sSource)

    def Set_TriggerAuto(self,sState):
        """ON | OFF"""
        if sState in (1,'1','ON'):
            self.write('TRIG:ATR:STAT ON')          #Auto-Trigger ON
        elif sState in (0,'0','OFF'):
            self.write('TRIG:ATR:STAT OFF')         #Auto-Trigger OFF

    def Set_TriggerCount(self,iNum):
        self.write('TRIG:COUN %d'%iNum)


#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    # this won't be run when imported
    NRP = PMr()
    NRP.Get_AvailableNRP()
    NRP.jav_openvisa("USB0::0x0AAD::0x0196::900105::INSTR")
    NRP.jav_logscpi()
    NRP.Set_Freq(24e9)
    NRP.Get_Power()
    NRP.jav_ClrErr()
