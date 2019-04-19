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
###############################################################################
from rssd.yaVISA_socket     import jaVisa           #pylint: disable=E0611,E0401
import time

class OTA(jaVisa):
    def __init__(self):
        super(OTA, self).__init__()
        self.Model = "OTA"
        self.EOL   = '\x00'

    def query(self,cmd):
        self.write(cmd)
        time.sleep(0.05)
        rdStr = self.K2.recv(2048).strip().decode()
        return rdStr

    #####################################################################
    ### OTA Get Functions
    #####################################################################
    def Get_CxAngle(self):
        rdStr = self.query(f'CX')
        return rdStr 

    def Get_IDN(self):
        rdStr = self.query(f'*IDN?')
        return rdStr 

    def Get_PhiAngle(self):
        # Phi; Elevation; Azimuth; 
        rdStr = self.query(f'CX').split(',')[2]
        return rdStr

    def Get_ThetaAngle(self):
        # Theta; Turntable
        rdStr = self.query(f'CX').split(',')[0]
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
    def Set_PhiAngle(self,angle):
        # Phi; Elevation; Azimuth; 
        self.write(f'LD 3 DV')
        self.write(f'LD 10 AF')
        self.write(f'LD {angle:.2f} DG NP GO')

    def Set_PhiStop(self):
        self.write(f'LD 3 DV')
        self.write(f'ST')

    def Set_ThetaAngle(self,angle):
        # Theta; Turntable
        self.write(f'LD 1 DV')
        self.write(f'LD 72 SF')
        self.write(f'LD {angle:.2f} DG NP GO')

    def Set_ThetaStop(self):
        self.write(f'LD 1 DV')
        self.write(f'ST')

###############################################################################
### Debug Main.  Won't run when imported
###############################################################################
if __name__ == "__main__":
    if 1:
        ATS1000 = OTA()
        ATS1000.EOL = '\x00'
        ATS1000.jav_Open('192.168.1.50',port=200)
    else:
        ATS1000 = OTA()
        ATS1000.EOL = '\n'
        ATS1000.jav_logscpi()
        ATS1000.jav_Open('192.168.1.109',port=5025)
    # print(ATS1000.Get_PhiAngle())
    # print(ATS1000.Get_ThetaAngle())
    print(ATS1000.Get_IDN())
