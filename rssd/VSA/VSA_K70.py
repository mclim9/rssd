# -*- coding: future_fstrings -*-
# #####################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose : Vector Signal Demod Functions
### Author  : Martin C Lim
### Date    : 2019.10.23
#####################################################################
from rssd.VSA.Common import VSA                 #pylint: disable=E0611,E0401

class VSA(VSA):                                 #pylint: disable=E0102
    """ Rohde & Schwarz Vector Signal Analyzer Object """
    def __init__(self):
        super(VSA, self).__init__()             #Python 2/3

    ###########################################################################
    ### VSA Get Functions
    ###########################################################################
    def Get_VSA_EVM(self):
        rdStr = self.query(':CALC2:MARK:FUNC:DDEM:STAT:EVM?')
        return rdStr

    def Get_VSA_CarrierFreqError(self):
        rdStr = self.query(':CALC2:MARK:FUNC:DDEM:STAT:CFER?')
        return rdStr

    def Get_VSA_IQImbalance(self):
        rdStr = self.query(':CALC2:MARK:FUNC:DDEM:STAT:IQIM?')
        return rdStr

    def Get_VSA_GainImbalance(self):
        rdStr = self.query(':CALC2:MARK:FUNC:DDEM:STAT:GIMB?')
        return rdStr

    def Get_VSA_IQOffset(self):
        rdStr = self.query(':CALC2:MARK:FUNC:DDEM:STAT:OOFF?')
        return rdStr

    def Get_VSA_IQSkew(self):
        rdStr = self.query(':CALC2:MARK:FUNC:DDEM:STAT:IQSK?')
        return rdStr

    def Get_VSA_MagnitudeError(self):
        rdStr = self.query(':CALC2:MARK:FUNC:DDEM:STAT:MERR?')
        return rdStr

    def Get_VSA_Meas_Params(self):
        EVM     = float(self.Get_VSA_EVM())
        PhaseEr = float(self.Get_VSA_PhaseError())
        MagEr   = float(self.Get_VSA_MagnitudeError())
        FreqEr  = float(self.Get_VSA_CarrierFreqError())
        IQOff   = float(self.Get_VSA_IQOffset())
        return f'{EVM:.4f},{PhaseEr:.4f},{MagEr:.4f},{FreqEr:.4f},{IQOff:.4f}'

    def Get_VSA_MER(self):
        rdStr = self.query(':CALC2:MARK:FUNC:DDEM:STAT:SNR?')
        return rdStr

    def Get_VSA_PhaseError(self):
        rdStr = self.query(':CALC2:MARK:FUNC:DDEM:STAT:PERR?')
        return rdStr

    def Get_VSA_ResultSumamry(self):
        rdStr = self.query(':TRACE2:DATA? TRACE1')
        return rdStr

    def Get_VSA_Rho(self):
        rdStr = self.query(':CALC2:MARK:FUNC:DDEM:STAT:RHO?')
        return rdStr

    def Get_VSA_symbol_rate(self):
        rdStr = self.query(':SENS:DDEM:SRAT?')
        return rdStr

    def Get_VSA_SymbolRateError(self):
        rdStr = self.query(':CALC2:MARK:FUNC:DDEM:STAT:SRER?')
        return rdStr

    ###########################################################################
    ### VSA Init Functions
    ###########################################################################
    def Init_VSA(self,sName=""):
        self.Set_Channel("DDEM",sName)

    ###########################################################################
    ### VSA Set Functions
    ###########################################################################
    def Set_VSA_Capture_Length(self,length):
        """Number of symbols"""
        if length == 0:
            self.write(f':SENS:DDEM:RLEN:AUTO ON')
        else:
            self.write(f':SENS:DDEM:RLEN:AUTO OFF')
            self.write(f':SENS:DDEM:RLEN:VAL {length} SYM')

    def Set_VSA_Capture_Time(self,time):
        """secs"""
        if time == 0:
            self.write(f':SENS:DDEM:RLEN:AUTO ON')
        else:
            self.write(f':SENS:DDEM:RLEN:AUTO OFF')
            self.write(f':SENS:DDEM:RLEN:VAL {time} S')

    def Set_VSA_EqualizerState(self,sState):
        """ ON; OFF"""
        if (sState == 'ON') or (sState == 1):
            self.write(f':SENS:DDEM:EQU:STAT ON')
        else:
            self.write(f':SENS:DDEM:EQU:STAT ON')

    def Set_VSA_Filter_Alpha(self,alpha):
        """ Alpha Value """
        self.write(f':SENS:DDEM:TFIL:ALPH {alpha}')

    def Set_VSA_Filter_Type(self,sName):
        """RC | RRC | Gauss | GMSK | None """
        self.write(f':SENS:DDEM:TFIL:NAME "{sName}"')

    def Set_VSA_Mod(self,sMod):
        """ QPSK | OQPSK | 8PSK | 16APSK | 32APSK """
        if sMod == 'QPSK':
            self.Set_VSA_Mod_Type('QPSK')
            self.write(':SENS:DDEM:QPSK:FORM NORM')
        elif sMod == 'OQPSK':
            self.Set_VSA_Mod_Type('QPSK')
            self.write(':SENS:DDEM:QPSK:FORM OFFS')
        elif sMod == '8PSK':
            self.Set_VSA_Mod_Type('PSK')
            self.write(':SENS:DDEM:PSK:FORM NORM')
            self.write(':SENS:DDEM:PSK:NST 8')
        elif sMod == '16APSK':
            self.Set_VSA_Mod_Type('APSK')
            self.write(':SENS:DDEM:APSK:NST 16')
        elif sMod == '32APSK':
            self.Set_VSA_Mod_Type('APSK')
            self.write(':SENS:DDEM:APSK:NST 32')
        elif sMod == '64APSK':
            self.Set_VSA_Mod_Type('UQAM')
            self.query(':INIT:IMM;*OPC?')
            self.write(':SENS:DDEM:USER:NAME "C:\\R_S\\instr\\user\\VSA\\Constellation\\DVB-S2X\\64APSK_8_16_20_20_4_5.vam"')
        elif sMod == '256APSK':
            self.Set_VSA_Mod_Type('UQAM')
            self.query(':INIT:IMM;*OPC?')
            self.write(':SENS:DDEM:USER:NAME "C:\\R_S\\instr\\user\\VSA\\Constellation\\DVB-S2X\\256APSK_135_180.vam"')

    def Set_VSA_Mod_PSK(self,iState):
        """2 | 8"""
        self.write(f':SENS:DDEM:PSK:NST {iState}')

    def Set_VSA_Mod_QAM(self,iState):
        """16 | 32 | 64 | 128 | 256 | 512 | 1024"""
        self.write(f':SENS:DDEM:QAM:NST {iState}')

    def Set_VSA_Mod_Type(self,sMod):
        """PSK|MSK|QAM|QPSK|FSK|ASK|APSK"""
        self.write(f':SENS:DDEM:FORM {sMod}')

    def Set_VSA_Symbol_Rate(self,rate):
        """Symbol Rate, Hz"""
        self.write(f':SENS:DDEM:SRAT {rate}')
    
    def Set_VSA_Result_Length(self,dLength):
        """integer length or 'MAX' """
        if dLength == 'MAX':
            self.write(':SENS:DDEM:TIME 64000')                     # Result Length
            self.write(':CALC:ELIN:STAT ON')                        # Full Evaluation Range
        else:
            self.write(f':SENS:DDEM:TIME {int(dLength)}')           # Result Length

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    VSA = VSA()
    VSA.jav_Open("192.168.1.109")
    VSA.Init_VSA()
    VSA.Set_InitImm()
    VSA.jav_Close()