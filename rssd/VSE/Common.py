""" Vector Signal Explorer Common Functions"""
from rssd.VSA.Common import VSA

class VSE(VSA):
    """ Rohde & Schwarz Vector Signal Explorer Object """
    def __init__(self):
        super(VSE,self).__init__()     #Python2/3
        self.Model = "VSE"

    #####################################################################
    ### VSE Display
    #####################################################################
    def Set_Group(self,sGroup):
        GroupList = self.query('INST:BLOC:LIST?').split(',')
        print("Grup:%s"%GroupList)
        if ("'" + sGroup + "'") in GroupList:
            pass
        else:
            self.write(":INST:BLOC:CRE '%s'"%(sGroup))
        self.write("INST:BLOC:USE 1, '%s'"%sGroup)

    #####################################################################
    ### VSE Input
    #####################################################################
    def Set_Input(self,sType):
        """RF|FILE"""
        self.write(f'INP:SEL {sType}')

    def Set_File_InputIQT(self,sFilename):
        ABW = '10MHz'
        IQCh = '2'
        self.write("INST:BLOC:CHAN:FILE:IQT '%s',%s,%s"%(sFilename,ABW,IQCh))

    def Set_File_InputIQW(self,Fs,sFileName='\\file.iqw'):
        abw = 0.8*float(Fs)
        val = "'%s',%d,%d,IQIQ"%(sFileName,abw,Fs)
        print("VSE_Common  :" + val)
        self.write("INST:BLOC:CHAN:FILE:IQW " + val)

    #####################################################################
    ### VSE Attenuation
    #####################################################################

    #####################################################################
    ### VSE Frequency
    #####################################################################

    #####################################################################
    ### VSE Time/Sweep
    #####################################################################
    def Set_SweepCont(self, sState):
        """0 | 1 """
        if sState in (1, '1', 'ON'):
            self.write('INIT:SEQ:MODE CONT')            #Continuous Sweep
        elif sState in (0, '0', 'OFF'):
            self.write('INIT:SEQ:MODE SING')            #Single Sweep
        else:
            print('Set_SweepCont error')

    #####################################################################
    ### VSE IQ Analyzer
    #####################################################################

    #####################################################################
    ### VSE Common Query
    #####################################################################

    #####################################################################
    ### VSE marker
    #####################################################################

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    VSE = VSE()
    VSE.jav_Open("127.0.0.1")         #Prints IDN String
    #VSE.Set_File_InputIQW(115.3e6,'C:\\Users\\LIM_M\\ownCloud\\ATE\\00_Code\\RS_ATE_Python2\\file.iqw')
    VSE.Set_SweepCont(0)
    VSE.jav_ClrErr()
