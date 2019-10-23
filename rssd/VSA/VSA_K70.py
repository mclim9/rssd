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
        self.Set_Channel("VSA")

    ###########################################################################
    ### VSA Set Functions
    ###########################################################################
    def Set_VSA_capture_length(self,length):
        """Number of symbols"""
        if length == 0:
            self.write(f':SENS:DDEM:RLEN:AUTO ON')
        else:
            self.write(f':SENS:DDEM:RLEN:AUTO OFF')
            self.write(f':SENS:DDEM:RLEN:VAL {length} SYM')

    def Set_VSA_symbol_rate(self,rate):
        """Symbol Rate"""
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
