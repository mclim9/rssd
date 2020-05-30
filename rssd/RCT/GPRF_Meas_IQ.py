# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Radio Communication Tester(RCT) General Purpose RF(GPRF) Functions
### Author : Martin C Lim
### Date   : 2018.05.29
###############################################################################
import struct                                   # For IQ Manipulation
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
        rdStr = self.queryFloat('FETCh:GPRF:MEAS:IQRecorder:SRATe?')
        return rdStr

    def Get_IQR_data_ASCII(self):
        self.write('FORMAT:BASE:DATA ASCII')
        rdStr = self.query('FETC:GPRF:MEAS:IQR?')
        return rdStr

    def Get_IQR_data_Bin(self):
        self.write('FORMAT:BASE:DATA REAL,32')
        self.write('FETC:GPRF:MEAS:IQR?')
        rdStr = self.K2.read_raw()
        numBytes = int(chr(rdStr[3]))           # Number of Bytes
        numIQ    = int(rdStr[2:2+numBytes])
        IQBytes  = rdStr[(numBytes+4):-1]       # Remove Header
        IQAscii  = struct.unpack("<" + 'f' * int(numIQ/4),IQBytes)          #pylint: disable=W0612
        self.write('FORMAT:BASE:DATA ASCII')
        return IQBytes

    ###########################################################################
    ### RCT Init Functions
    ###########################################################################
    def Init_Meas_IQCapture(self,port=1):
        self.write('INIT:GPRF:MEAS:IQR')
        self.Set_Meas_Port(port)
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:FORMat IQ')

    ###########################################################################
    ### RCT Set Functions
    ###########################################################################
    def Set_Meas_Freq(self,fFreq):                                          #Val
        self.write(f'CONF:GPRF:MEAS:RFS:FREQ {fFreq}')

    def Set_IQR_Bandwidth(self,iBW):
        """1000:1250 | 500:625 | 250:312.5 160/40/10:Unsupported"""
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:FILTer:BANDpass:BWIDth {iBW} MHz')

    def Set_IQR_filename(self,sFile):
        """IQ Output Filename"""
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:IQFile "@USERDATA/iqrecorder/{sFile}.iqw"')
        self.Set_IQR_filename_state('ON')

    def Set_IQR_filename_state(self,sState):
        """OFF | ON | ONLY"""
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:WTFile {sState}')

    def Set_IQR_InitImm(self):
        self.query('STOP:GPRF:MEAS:IQR;*OPC?')
        self.query('INIT:GPRF:MEAS:IQR;*OPC?')
        self.Set_IQR_filename_state('OFF')
        # self.query('ABOR:GPRF:MEAS:IQR;*OPC?')

    def Set_IQR_Length(self,iLength):
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:CAPTure 1, {iLength}')
        # self.write(f'CONFigure:GPRF:MEAS:IQRecorder:FILTer:TYPe GAUSs')

    def Set_IQR_SamplingRate(self,fFreq):
        """Sampling Rate, MHz"""
        # 10/40/160 BW ->  Unsupported
        fFreq = float(fFreq)
        if fFreq < 156.25:
            print('Set_IQR_SamplingRate Frequency below 156.25 not supported')
        elif fFreq < 312.5:             #  250 MHz BW -->  312.5 MHz
            self.Set_IQR_Bandwidth(250)
            ratio = fFreq/312.5
            self.Set_IQR_SamplingRate_Ratio(ratio)
        elif fFreq < 625:               #  500 MHz BW -->  625 MHz
            self.Set_IQR_Bandwidth(500)
            ratio = fFreq/625
            self.Set_IQR_SamplingRate_Ratio(ratio)
        elif fFreq < 1250:              # 1000 MHz BW --> 1250 MHz
            self.Set_IQR_Bandwidth(1000)
            ratio = fFreq/1250
            self.Set_IQR_SamplingRate_Ratio(ratio)
        else:
            print('Frequency too high')

    def Set_IQR_SamplingRate_Ratio(self,fRatio):
        """Fs = BP Filt BW * Ratio"""
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:RATio {fRatio}')

    def Set_IQR_timeout(self,fTime):
        """Timeout, sec"""
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:TOUT {fTime}')

    def Set_IQR_Time(self,fTime):
        """Capture Time, sec"""
        Fs     = self.Get_IQR_srate()
        numIQ  = int(Fs * fTime)
        self.Set_IQR_Length(numIQ)

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

    def Set_IQR_Units(self,sUnit):
        """VOLT (Float32) | RAW"""
        self.write(f'CONFigure:GPRF:MEAS:IQRecorder:MUNit {sUnit}')

###############################################################################
### Run if Main
###############################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    CMP = RCT()
    CMP.jav_Open("192.168.1.160")
    # CMP.Set_IQR_timeout(1)
    # CMP.Init_Meas_IQCapture()
    # CMP.Set_IQR_Time(0.0125)
    # CMP.Set_IQR_SamplingRate(245.76)
    print(CMP.Get_IQR_data_ASCII()[0:50])
    rd = (CMP.Get_IQR_data_Bin())
    print(rd)
    CMP.jav_ClrErr()
    CMP.jav_Close()
