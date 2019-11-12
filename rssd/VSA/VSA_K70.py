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
    def Get_VSA_symbol_rate(self):
        rdStr = self.query(':SENS:DDEM:SRAT?')
        return rdStr

    ###########################################################################
    ### VSA Init Functions
    ###########################################################################
    def Init_VSA(self):
        self.Set_Channel("DDEM")

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