"""
Terms:  Azimuth:    Θθ; Theta; Turntable
        Elevation:  Φφ; Phi; Cradle
OTA:    ATS000      Az over El
        ATS1500     Az over El
        ATS1800     Az over El
"""
from rssd.OTA.Common     import OTA           #pylint: disable=E0611,E0401

class OTA(OTA):
    """ Rohde & Schwarz ATS1800 Object """
    def __init__(self):
        super(OTA, self).__init__()
        self.Model = "ATS1800"
        self.EOL   = '\x00'

    #####################################################################
    ### OTA Get Functions
    #####################################################################
    def Get_AzimuthAngle(self):
        rdStr = self.query(f'SENS:AZIM:POS?')
        return rdStr

    def Get_AzimuthRunning(self):
        rdStr = self.query(f'SENS:AZIM:BUSY?')
        return rdStr

    def Get_AzimuthSpeed(self):
        rdStr = self.query(f'CONT:AZIM:SPE?')
        return rdStr

    def Get_ElevateAngle(self):
        rdStr = self.query(f'SENS:ELEV:POS?')
        return rdStr

    def Get_ElevateRunning(self):
        rdStr = self.query(f'SENS:ELEV:BUSY?')
        return rdStr

    def Get_ElevateSpeed(self):
        rdStr = self.query(f'CONT:ELEV:SPE?')
        return rdStr

    def Get_SysStat(self):
        rdStr = self.query('SYST:STAT?')
        return rdStr

    #####################################################################
    ### OTA Init Functions
    #####################################################################
    def Init_Measurement(self):
        #Configure instrument measurment
        pass

    #####################################################################
    ### OTA Set Functions
    #####################################################################
    def Set_AzimuthAngle(self,angle):
        self.query(f'CONT:AZIM:POS:TARG {angle}')
        self.query(f'CONT:AZIM:STAR')

    def Set_AzimuthSpeed(self,speed):
        """Speed: 1 to 150 degree/sec"""
        self.query(f'CONT:AZIM:SPE {speed}')

    def Set_AzimuthStop(self):
        self.query(f'CONT:AZIM:STOP')

    def Set_ElevateAngle(self,angle):
        self.query(f'CONT:ELEV:POS:TARG {angle}')
        self.query(f'CONT:ELEV:STAR')

    def Set_ElevateSpeed(self,speed):
        """Speed: 1 to 150 degree/sec"""
        self.query(f'CONT:ELEV:SPE {speed}')

    def Set_ElevateStop(self):
        self.query(f'CONT:ELEV:STOP')

###############################################################################
### Debug Main.  Won't run when imported
###############################################################################
if __name__ == "__main__":
    # http://169.254.2.10/Tc3PlcHmiWeb/Port_851/Visu/webvisu.htm
    ATS1800 = OTA().open('169.254.2.10', type = 'socket', param = 200)
    ATS1800.Set_ElevateAngle(40)
    print(ATS1800.Get_ElevateRunning())
    print(ATS1800.Get_ElevateAngle())
