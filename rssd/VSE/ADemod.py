#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose : Vector Signal Explorer Analog Demod Functions
### Author  : Martin C Lim
### Date    : 2018.04.27
from rssd.VSE.Common import VSE

class VSE(VSE):
    """ Rohde & Schwarz Vector Signal Explorer Analog Demod Object """
    def __init__(self):
        super(VSE,self).__init__()     #Python2

    #####################################################################
    ### VSE ADemod Settings
    #####################################################################
    def Set_Adem_dbw(self,iBW):
        #Values is rounded up: 1;3;5;
        self.write('SENS:BWID:DEM %d'%iBW)

    #####################################################################
    ### VSE Filter Settings
    #####################################################################
    def Set_Adem_LPassStat(self,sState):
        self.write('SENSe:FILT:LPASS:STAT %s'%(sState))

    def Set_Adem_LPassAbsolute(self,sBW):
        #Low Pass Filter Absolute Values: 3kHz; 15kHz; 150kHz
        self.write('SENSe:FILT:​LPASS:​FREQ:​ABS %s'%sBW)      
        
    def Set_Adem_LPassRelative(self,sBW):
        #Low Pass Filter Relative Values:5PCT; 10PCT; 25PCT
        self.write('SENSe:FILT:LPASS:FREQ:REL %s'%sBW) 

    def Set_Adem_LPassManual(self,fBW):
        self.write('SENSe:FILT:LPASS​:FREQ:MAN %s'%fBW)      #0 to 3MHz

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    if 0:
        import sys
        print(sys.version)
    VSE = VSE()
    VSE.jav_Open("127.0.0.1")
    VSE.Set_Channel("ADEM")
    VSE.Set_DisplayUpdate('ON')
    VSE.Set_Adem_dbw(500e6)
    VSE.Set_InitImm()
 
