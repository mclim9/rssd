#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: NRP Power Sensor
### Author : Martin C Lim
### Date    : 2018.05.18
### Requird: python -m pip install pyvisa
### 
### VISAFmt: USB0::0x0AAD::0x0138::100961::INSTR
###             <VS>::<Manu>::<Modl>::<SerN>::INSTR
###             TCPIP0::NRPM3-900105::inst0
### 
#####################################################################
from rssd.NRP_Common import PMr

class PMr(PMr):
    def __init__(self):
        super().__init__()
        
#####################################################################
### NRPM3M 0x0195
#####################################################################
    def Set_Sys_LED(self,bState,iSensor=1):
        if bState == 1:
            self.write('SYST:LED:CHAN%d:COL 255'%iSensor)
        else:
            self.write('SYST:LED:CHAN%d:COL 0'%iSensor)
                    
#####################################################################
### NRPM3N 0x0195
#####################################################################
    def Set_Gen_MasterPwr(self,bState,iSensor=1):
        ### This cmd sent automatically after 1min to prevent overheating.
        ### retrigger only after 5 minutes.  Damange otherwise.
        if bState == 1:
            self.write('CONT%d:APOW:STAT ON'%iSensor)
        else:
            self.write('CONT%d:APOW:STAT OFF'%iSensor)
            
    def Set_Gen_RFPwr(self,bState,iSensor=1):
        ### Suggested 1:10 duty cycle
        if bState == 1:
            self.write('OUTP%d:STAT ON'%iSensor)
            self.write('SYST:LED:CHAN%d:COL 255'%iSensor)
        else:
            self.write('OUTP%d:STAT OFF'%iSensor)
            self.write('SYST:LED:CHAN%d:COL 0'%iSensor)
            
    def Get_Gen_Freq(self):
        self.write('SOUR:FREQ?')

    def Set_Gen_Freq(self,fFreq):
        self.write('SOUR:FREQ %f'%fFreq)

    def Set_Gen_EIRP(self,bState):
        self.query('FETC?')
        
#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    # this won't be run when imported
    NRP = PMr()
    NRP.jav_openvisa("USB0::0x0AAD::0x0196::900105::INSTR")
    #  NRP.jav_logscpi()
    NRP.jav_Reset()
    NRP.Set_Freq(24e9)

    print(NRP.Get_PowerAll())          # Power Before SG on
    for i in range(1,4):
        NRP.Set_Gen_MasterPwr(1,i)
        NRP.Set_Gen_RFPwr(1,i)
        NRP.Set_Gen_Freq(24e9)
        NRP.Get_Gen_Freq()
        print(NRP.Get_PowerAll())          # Power SG on 
        NRP.Set_Gen_RFPwr(0,i)
        NRP.Set_Gen_MasterPwr(0,i)
    NRP.jav_Close()
