# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: OTA Common Functions
### Author : Martin C Lim
### Date   : 20xx.xx.xx
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
### Terms:  Azimuth:    Theta; Turntable;
###         Elevation:  Phi; ATS1000 Arm; 
### OTA:    ATS1000     Great Circle Cut; Turntable & Elevation Arm
###         ATS1500     Az over El;
###         ATS1800     Az over El;
###############################################################################
from rssd.yaVISA     import jaVisa           #pylint: disable=E0611,E0401
import time

class OTA(jaVisa):
    """ Rohde & Schwarz Over The Air Chamber Object """
    def __init__(self):
        super(OTA, self).__init__()
        self.Model = "OTA"
        self.EOL   = '\x00'
        self.cmdWait = 0.05     #Seconds

    def query(self,cmd):
        cmd = cmd + self.EOL
        self.K2.read_termination = '\x00'
        self.K2.sendall(cmd.encode())               #Write if connected
        sOut = self.K2.recv(2048).strip()           #read socket
        read = sOut.decode()
        return read

        # self.write(cmd)
        # time.sleep(self.cmdWait)
        # rdStr = self.K2.recv(2048).strip().decode()
        # return rdStr

    #####################################################################
    ### OTA Get Functions
    #####################################################################

    #####################################################################
    ### OTA Init Functions
    #####################################################################
    def Init_Measurement(self):
        #Configure instrument measurment
        pass

    #####################################################################
    ### OTA Set Functions
    #####################################################################

###############################################################################
### Debug Main.  Won't run when imported
###############################################################################
if __name__ == "__main__":
    ATS1000 = OTA()
    ATS1000.jav_Open('192.168.1.50',port=200)
    print(ATS1000.Get_IDN())
