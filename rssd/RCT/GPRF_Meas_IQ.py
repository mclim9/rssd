# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Radio Communication Tester(RCT) General Purpose RF(GPRF) Functions
### Author : Martin C Lim
### Date   : 2018.05.29
###############################################################################
from rssd.RCT.Common import RCT                 #pylint: disable=E0611,E0401

class RCT(RCT):                                 #pylint: disable=E0102
    """ Rohde & Schwarz Radio Comm Tester Object """
    def __init__(self):
        super(RCT, self).__init__()
        self.Model = "CMW-GPRF"

    ###########################################################################
    ### RCT Get Functions
    ###########################################################################
    def Get_IQR_srate(self):
        rdStr = self.query('FETCh:GPRF:MEAS:IQRecorder:SRATe?')
        return rdStr

    def Get_IQR_data(self):
        self.write('FORMAT:BASE:DATA REAL, 32')
        rdStr = self.query('FETCh:GPRF:MEAS:IQRecorder?')
        self.write('FORMAT:BASE:DATA ASCII')
        return rdStr

    ###########################################################################
    ### RCT Init Functions
    ###########################################################################
    def Init_Meas_IQCapture(self,port=1):
        self.write('INIT:GPRF:MEAS:IQR')
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:FORMat IQ')

    ###########################################################################
    ### RCT Set Functions
    ###########################################################################
    def Set_Meas_Freq(self,fFreq):                                          #Val
        self.write(f'CONF:GPRF:MEAS:RFS:FREQ {fFreq}')

    def Set_IQR_InitImm(self):
        self.query('STOP:GPRF:MEAS:IQRecorder;*OPC?')
        self.query('INIT:GPRF:MEAS:IQRecorder;*OPC?')

    def Set_Meas_SweepTime(self,fTime):
        if fTime > 0:
            self.write('CONF:GPRF:MEAS:SPEC:FSW:SWT %f'%fTime)
        else:
            self.write('CONF:GPRF:MEAS:SPEC:FSW:SWT:AUTO ON')

    def Set_IQR_timeout(self,fTime):
        """Timeout, sec"""
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:TOUT {fTime}')

    def Set_IQR_filename(self,sFile):
        """IQ Output Filename"""
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:IQFile "@USERDATA/iqrecorder/{sFile}.iqw"')
        self.Set_IQR_filename_state('ON')

    def Set_IQR_filename_state(self,sState):
        """OFF | ON | ONLY"""
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:WTFile {sState}')

    def Set_IQR_Length(self,iLength):
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:CAPTure 1, {iLength}')
        # self.write(f'CONFigure:GPRF:MEAS:IQRecorder:FILTer:TYPe GAUSs')

    def Set_IQR_Bandwidth(self,iBW):
        """1000:1250 | 500:625 | 250/160/40/10:312.5 """
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:FILTer:GAUSs:BWIDth iBW')

    def Set_IQR_SamplingRate_Ratio(self,fRatio):
        """Fs = BP Filt BW * Ratio"""
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:RATio {fRatio}')

    def Set_IQR_Units(self,sUnit):
        """VOLT | RAW"""
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:MUNit {sUnit}')

    def Set_IQR_Trig_Slope(self,sSlope):
        """Trigger Slope: REDG | FEDGe"""
        self.write(f'TRIGger:GPRF:MEAS:IQRecorder:SLOPe {sSlope}')

    def Set_IQR_Trig_Source(self,sSource):
        """Trigger Source 'IF Power'; 'Free Run' """
        self.write(f'TRIGger:GPRF:MEAS<i>:IQRecorder:SOURce {sSource}')

    def Set_IQR_Trig_Threshold(self,sdBm):
        """Trigger Threshold, dBm"""
        self.write(f'TRIGger:GPRF:MEAS:IQRecorder:THReshold {sdBm}')

    def Set_IQR_Trig_Timeout(self,iTime):
        """Trigger Timeout, sec"""
        self.write(f'TRIGger:GPRF:MEAS:IQRecorder:TOUT {iTime}')

    def Set_IQR_Trig_MinGap(self,iTime):
        """Trigger Timeout, sec"""
        self.write(f'TRIGger:GPRF:MEAS:IQRecorder:MGAP {iTime}')

###############################################################################
### Run if Main
###############################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    CMP = RCT()
    CMP.jav_Open("192.168.1.160")
    CMP.Set_IQR_timeout(1)
    CMP.Init_Meas_IQCapture()
    CMP.Set_IQR_Bandwidth(160)
    CMP.Set_IQR_SamplingRate_Ratio(0.786432)
    # CMP.Set_IQR_Length(3686400)       #15.00 msec  29 MB
    CMP.Set_IQR_Length(30720)           #0.125 uSec 246 kB
    print(CMP.Get_IQR_srate())
    CMP.Set_IQR_filename('tesasdft')
    CMP.Set_IQR_filename_state('ON')
    CMP.Set_IQR_InitImm()
    CMP.jav_ClrErr()
    CMP.jav_Close()