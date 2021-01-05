"""FSW/SMW 5G NR Demo
"""
#pylint: disable=E0611,E0401
from rssd.VSG.Common import VSG
from rssd.VSA.Common import VSA

class VST(object):
    """ Rohde & Schwarz Vector Signal Transceiver Object """
    def __init__(self):
        self.Freq       = 19e9
        self.SMW        = ''
        self.FSW        = ''

    def jav_Open(self,SMW_IP,FSW_IP,OFile=''):
        self.SMW = VSG().jav_Open(SMW_IP,OFile)  #Create SMW Object
        self.FSW = VSA().jav_Open(FSW_IP,OFile)  #Create FSW Object
        return self

    def jav_OpenTest(self,SMW_IP,FSW_IP):
        self.SMW = VSG().jav_OpenTest(SMW_IP)  #Create SMW Object
        self.FSW = VSA().jav_OpenTest(FSW_IP)  #Create FSW Object
        return self

    def jav_Close(self):
        self.SMW.jav_Close()
        self.FSW.jav_Close()

    def jav_ClrErr(self):
        self.SMW.jav_ClrErr()
        self.FSW.jav_ClrErr()

    def Set_Freq(self,freq):
        self.SMW.Set_Freq(freq)
        self.FSW.Set_Freq(freq)

##########################################################
### Instrument Settings
##########################################################
if __name__ == "__main__":
    VST = VST().jav_Open('192.168.1.114','192.168.1.109')
    VST.Set_Freq(9e9)
    VST.jav_Close()
