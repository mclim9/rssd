# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose : Vector Signal Analyzer Common Functions
###############################################################################
from rssd.VSA.Common import VSA

class VSA(VSA):
    """ Rohde & Schwarz Vector Signal Analyzer Noise Figure Object """
    def __init__(self):
        super(VSA, self).__init__()
        self.Model = "FSW"

    ###########################################################################
    ### FSW V5G
    ###########################################################################
    def Init_Noise(self):
        self.Set_Channel('NOISE')

    ###########################################################################
    ### FSW ENR & Noise (With Option Installed)
    ###########################################################################
    def Set_NF_ENR_Cal_Type(self, sENRtype):
        """ DIOD | RES (Noise Diode or Resistor)"""
        self.write(':SENS:CORR:ENR:COMM OFF')
        self.write(':SENS:CORR:ENR:CAL:TYPE %s'%sENRtype)

    def Set_NF_ENR_Meas_Type(self, sENRtype):
        """ DIOD | RES (Noise Diode or Resistor)"""
        self.write('SENS:CORR:ENR:MEAS:TYPE %s'%sENRtype)

    def Set_NF_ENR_Meas_Mode(self, sENRmode):
        """TABL """
        self.write('SENS:CORR:ENR:MEAS:MODE %s'%sENRmode)

    def Set_NF_ENR_Temp(self, fnoiseTemp):
        """Temp in Kelvin = C + 273.15"""
        self.write(':SENS:CORR:TEMP:CONT MAN')
        self.write(':SENS:CORR:TEMP %f'%fnoiseTemp)

    def Set_NF_ENR_Table(self, sENRtable):
        """Table Name"""
        self.write(":SENS:CORR:ENR:MEAS:TABL:SEL '%s'"%sENRtable)     #'346B.1321'

    def Set_NF_Cal_Type(self, snoiseCalType):
        """AUTO | MAN Measurement Mode"""
        self.write('CONF:CONT %s'%snoiseCalType)

    def Config_NF_Cal(self, snoiseCalTemp):
        """HOT|COLD"""
        self.write('CONF:MEAS %s'%snoiseCalTemp)

    def Set_NF_2ndCorr_State(self, sState):
        """ON|OFF|1|0"""
        if sState in (1, '1', 'ON'):
            self.write('SENS:CORR:STAT ON')
        if sState in (0, '0', 'OFF'):
            self.write('SENS:CORR:STAT OFF')

    def Set_NF_Cal_State(self, sState):
        """ON|OFF|1|0"""
        if sState in (1, '1', 'ON'):
            self.write('SENS:CORR:STAT ON;*WAI')
        if sState in (0, '0', 'OFF'):
            self.write('SENS:CORR:STAT OFF;*WAI')

    def Set_NF_Sweep(self, sNoiseSweep):
        """SING|CONT"""
        self.write('SENS:CONF:LIST %s'%sNoiseSweep)
        self.Set_InitImm()

    def Set_NF_Single_Meas(self):
        """perform a single frequency measurement"""
        self.write(f'CONF:FREQ:SING')

    def Set_NF_Single_Coupled_To_List(self, sState):
        """ON|OFF|1|0"""
        if sState in (1, '1', 'ON'):
            self.write('FREQ:SING:COUP ON')
        if sState in (0, '0', 'OFF'):
            self.write('FREQ:SING:COUP OFF')

    def Set_NF_Single_Freq(self, fFreq):
        """Frequency in Single Sweep Mode"""
        self.write(f'FREQ:SING {fFreq:.0f}')

    def Set_NF_DUT_InLoss_Mode(self, sinputMode):
        """SPOT | TABL"""
        self.write('CORR:LOSS:INP:MODE %s'%sinputMode)

    def Set_NF_DUT_InLoss_TableName(self, sinTableName):
        self.write("CORR:LOSS:INP:TABL:SEL '%s'"%sinTableName)

    def Set_NF_DUT_InLoss_Table(self, sinputTable):
        """Enter loss table as csv: '1MHz,10,2MHz,12'"""
        self.write('CORR:LOSS:INP:TABL %s'%sinputTable)

    def Set_NF_DUT_OutLoss_Mode(self, soutputMode):
        """SPOT | TABL"""
        self.write('CORR:LOSS:OUTP:MODE %s'%soutputMode)

    def Set_NF_DUT_OutLoss_TableName(self, soutTableName):
        self.write("CORR:LOSS:OUTP:TABL:SEL '%s'"%soutTableName)

    def Set_NF_DUT_OutLoss_Table(self, soutputTable):
        """Enter loss table as csv: '1MHz,10,2MHz,12'"""
        self.write('CORR:LOSS:OUTP:TABL %s'%soutputTable)

    ###########################################################################
    ### Retrieve Measurements
    ###########################################################################
    def Get_NF_Gain(self):
        Gain = self.queryFloat('TRAC? TRACE1, GAIN')
        return Gain

    def Get_NoiseFigure(self):
        NF = self.queryFloat('TRAC? TRACE1, NOIS')
        return NF

    def Get_YFactor(self):
        YFac = self.queryFloat('TRAC? TRACE1, YFAC')
        return YFac

    def Get_NoiseTemp(self):
        NTemp = self.queryFloat('TRAC? TRACE1, TEMP')
        return NTemp

    def Get_NF_CalCold(self):
        NCalCold = self.queryFloat('TRAC? TRACE1, CPC')
        return NCalCold

    def Get_NF_CalHot(self):
        NCalHot = self.queryFloat('TRAC? TRACE1, CPH')
        return NCalHot

    def Get_NF_PHot(self):
        NPHot = self.queryFloat('TRAC? TRACE1, PHOT')
        return NPHot

    def Get_NF_PCold(self):
        NPCold = self.queryFloat('TRAC? TRACE1, PCOL')
        return NPCold

    def System_Preset(self):
        self.write('SYST:PRES:CHAN')

###############################################################################
### Run if Main
###############################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    FSW = VSA()
    FSW.jav_Open("192.168.1.109")
    FSW.Init_Noise()
    FSW.jav_ClrErr()
    del FSW
