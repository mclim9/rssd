# -*- coding: future_fstrings -*-
###############################################################################
### Purpose: OTA ATS1000 Functions
###  _____  _____   ____ _______ ____ _________     _______  ______
### |  __ \|  __ \ / __ \__   __/ __ \__   __\ \   / /  __ \|  ____|
### | |__) | |__) | |  | | | | | |  | | | |   \ \_/ /| |__) | |__
### |  ___/|  _  /| |  | | | | | |  | | | |    \   / |  ___/|  __|
### | |    | | \ \| |__| | | | | |__| | | |     | |  | |    | |____
### |_|    |_|  \_\\____/  |_|  \____/  |_|     |_|  |_|    |______|
###                         _            _           _
###                        | |          | |         | |
###             _   _ _ __ | |_ ___  ___| |_ ___  __| |
###            | | | | '_ \| __/ _ \/ __| __/ _ \/ _` |
###            | |_| | | | | ||  __/\__ \ ||  __/ (_| |
###             \__,_|_| |_|\__\___||___/\__\___|\__,_|
###
### Terms:  Azimuth:    Θθ; Theta; Turntable;
###         Elevation:  Φφ; Phi; Arm;
### OTA:    ATS1000     Great Circle Cut; Turntable & Elevation Arm
###############################################################################
# import time
from rssd.OTA.Common     import OTA           #pylint: disable=E0611,E0401

class OTA(OTA):
    """ Rohde & Schwarz ATS1000 Object """
    def __init__(self):
        super(OTA, self).__init__()
        self.Model = "ATS1000"
        self.EOL   = '\x00'

    #####################################################################
    ### OTA Get Functions
    #####################################################################
    def Get_AzimuthAngle(self):
        rdStr = self.query(f'CX').split(',')[2]
        return rdStr

    def Get_AzimuthRunning(self):
        return 'TBD'

    def Get_AzimuthSpeed(self):
        return 'TBD'

    def Get_CxAngle(self):
        rdStr = self.query(f'CX')
        return rdStr

    def Get_ElevateAngle(self):
        rdStr = self.query(f'CX').split(',')[0]
        return rdStr

    def Get_ElevateRunning(self):
        return 'TBD'

    def Get_ElevateSpeed(self):
        return 'TBD'

    def Get_IDN(self):
        rdStr = self.query(f'*IDN?')
        return rdStr

    def Get_SysStat(self):
        return 'TBD'

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
        self.write(f'LD 1 DV')                  #Set Azimuth
        self.write(f'LD 72 SF')                 #Set Speed
        self.write(f'LD {angle:.2f} DG NP GO')

    def Set_AzimuthSpeed(self,speed):
        #Speed: 1-72 degree/sec
        self.write(f'LD 1 DV')                  #Set Azimuth
        self.write(f'LD {speed} SF')

    def Set_AzimuthStop(self):
        self.write(f'LD 1 DV')                  #Set Azimuth
        self.write(f'ST')

    def Set_AzimuthTrigger(self,angle):
        self.write(f'LD 1 DV')                  #Set Azimuth
        self.write(f'TR 1 GO')                  #Trigger enable
        self.write(f'LD {angle} DG TR')

    def Set_ElevateAngle(self,angle):
        self.write(f'LD 3 DV')                  #Set Arm
        self.write(f'LD 10 AF')                 #Set Speed
        self.write(f'LD {angle:.2f} DG NP GO')

    def Set_ElevateSpeed(self,speed):
        #Speed: 1-20 degree/sec
        self.write(f'LD 3 DV')                  #Set Arm
        self.write(f'LD {speed} AF')

    def Set_ElevateStop(self):
        self.write(f'LD 3 DV')                  #Set Arm
        self.write(f'ST')

###############################################################################
### Debug Main.  Won't run when imported
###############################################################################
if __name__ == "__main__":
    ATS1000 = OTA()
    ATS1000.jav_Open('192.168.1.50',port=200)
    # print(ATS1000.Get_ElevateAngle())
    # print(ATS1000.Get_AzimuthAngle())
    print(ATS1000.Get_IDN())
