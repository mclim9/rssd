#####################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose : Vector Signal Demod Functions
### Author  : Martin C Lim
### Date    : 2019.10.23
from rssd.VSA.Common import VSA

class VSA(VSA):
    """ Rohde & Schwarz Vector Signal Analyzer Analog Demod Object """
    def __init__(self):
        super(VSA,self).__init__()     #Python2

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
        EVM     = self.Get_VSA_EVM()
        PhaseEr = self.Get_VSA_PhaseError()
        MagEr   = self.Get_VSA_MagnitudeError()
        FreqEr  = self.Get_VSA_CarrierFreqError()
        IQOff   = self.Get_VSA_IQOffset()
        return f"{EVM},{PhaseEr},{MagEr},{FreqEr},{IQOff}"

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

    def Set_VSA_Filter_Alpha(self,alpha):
        """  """
        self.write(f':SENS:DDEM:TFIL:ALPH {alpha}')

    def Set_VSA_Filter_Type(self,sName):
        """RC | RRC | Gauss | GMSK | None """
        self.write(f':SENS:DDEM:TFIL:NAME "{sName}"')

    def Set_VSA_Mod(self,sMod):
        """ QPSK | 8PSK | 16APSK | 32APSK """
        if sMod == 'QPSK':
            self.Set_VSA_Mod_Type('QPSK')
            self.write(':SENS:DDEM:QPSK:FORM NORM')
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