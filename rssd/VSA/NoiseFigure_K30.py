# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose : Vector Signal Analyzer Common Functions
### Author  : Kevin Kishimoto
### Date    : 2018.10.01
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
    def Set_FSW_Option(self, sfswOption):
        self.write('INST:SEL %s'%sfswOption)

    def Set_ENR_Cal_Type(self, sENRtype):
        self.write('SENS:CORR:ENR:CAL:TYPE %s'%sENRtype)        #DIODe|RES (Noise Diode or Resistor)

    def Set_NF_Meas_Type(self, sENRtype):
        self.write('SENS:CORR:ENR:MEAS:TYPE %s'%sENRtype)       #DIODe|RES  (Noise Diode or Resistor)

    def Set_NF_Meas_Mode(self, sENRmode):
        self.write('SENS:CORR:ENR:MEAS:MODE %s'%sENRmode)       #|TABL

    def Get_Noise_Temp(self, fnoiseTemp):
        self.write('SENS:CORR:TEMP %f'%fnoiseTemp)

    def Set_Noise_LossIn(self, fnoiseLossIn):
        self.write('SENS:CORR:LOSS:INP:TABL:SEL %f'%fnoiseLossIn)

    def Set_ENR_Table(self, sENRtable):
        self.write("CORR:ENR:MEAS:TABL:SEL '%s'"%sENRtable)     #'346B.1321'

    def Set_Noise_Cal_Type(self, snoiseCalType):
        self.write('CONF:CONT %s'%snoiseCalType)

    def Config_Noise_Cal(self, snoiseCalTemp):
        self.write('CONF:MEAS %s'%snoiseCalTemp)                #HOT|COLD

    def Set_2nd_Stage_Correction(self):
        self.write('SENS:CONF:CORR')

    def Set_Noise_Cal_State(self, sState):
        self.write('SENS:CORR:STAT %s*WAI'%sState)              #ON|OFF|1|0

    def Get_Noise_Sweep(self, sNoiseSweep):
        self.write('SENS:CONF:LIST %s'%sNoiseSweep)             #SINGL|CONT
        self.Set_InitImm()

    def Set_Noise_Meas_Single(self):
        self.write('CONF:FREQ:SING')

    def Set_Single_Coupled_To_List(self):
        self.write('FREQ:SING:COUP ON')                         #ON|OFF|1|0

    def Set_Single_Freq(self, sFreq):
        self.write('FREQ:SING %s'%sFreq)

    def Set_DUT_InLoss_Mode(self, sinputMode):
        self.write('CORR:LOSS:INP:MODE %s'%sinputMode)          #SPOT|TABL

    def Set_DUT_InLoss_TableName(self, sinTableName):
        self.write("CORR:LOSS:INP:TABL:SEL '%s'"%sinTableName)

    def Set_DUT_InLoss_Table(self, sinputTable):
        #Enter loss table as csv: '1MHz,10,2MHz,12'
        self.write('CORR:LOSS:INP:TABL %s'%sinputTable)

    def Set_DUT_OutLoss_Mode(self, soutputMode):
        self.write('CORR:LOSS:OUTP:MODE %s'%soutputMode)

    def Set_DUT_OutLoss_TableName(self, soutTableName):
        self.write("CORR:LOSS:OUTP:TABL:SEL '%s'"%soutTableName)

    def Set_DUT_OutLoss_Table(self, soutputTable):
        #Enter loss table as csv: '1MHz,10,2MHz,12'
        self.write('CORR:LOSS:OUTP:TABL %s'%soutputTable)

    ###########################################################################
    ### Retrieve Measurements
    ###########################################################################
    def Get_Noise_Gain(self):
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

    def Get_Noise_CalCold(self):
        NCalCold = self.queryFloat('TRAC? TRACE1, CPC')
        return NCalCold

    def Get_Noise_CalHot(self):
        NCalHot = self.queryFloat('TRAC? TRACE1, CPH')
        return NCalHot

    def Get_Noise_PHot(self):
        NPHot = self.queryFloat('TRAC? TRACE1, PHOT')
        return NPHot

    def Get_Noise_PCold(self):
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
