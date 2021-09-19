""" OTA Common Functions

Terms:  Azimuth:    Theta; Turntable;
        Elevation:  Phi; ATS1000 Arm;
OTA:    ATS1000     Great Circle Cut; Turntable & Elevation Arm
        ATS1500     Az over El;
        ATS1800     Az over El;
"""
from rssd.instrument import instr

class OTA(instr):
    """ Rohde & Schwarz Over The Air Chamber Object """
    def __init__(self):
        super(OTA, self).__init__()
        self.Model      = "OTA"
        self.EOL        = '\x00'
        self.cmdWait    = 0.05     #Seconds

    def query(self,cmd):                            #pragma: no cover
        self.bus.EOL = self.EOL
        read = self.bus.query(cmd + self.EOL).strip()
        return read[:-1]

###############################################################################
### Debug Main.  Won't run when imported
###############################################################################
if __name__ == "__main__":
    ATS1000 = OTA()
    ATS1000.open('169.254.2.10', type = 'socket', param = 200)
    print(ATS1000.Get_IDN())
