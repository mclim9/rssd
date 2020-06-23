###############################################################################
### Purpose: rssd.self.VSE.common.py driver test
###              _   ___        __  _____         _   
###             | | | \ \      / / |_   _|__  ___| |_ 
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_ 
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '127.0.0.1'                              #Get local machine name

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.VSE.K96 import VSE

class TestGeneral(unittest.TestCase):
    def setUp(self):                            #run before each test
        self.VSE = VSE().jav_OpenTest(host)

    def tearDown(self):                         #Run after each test
        self.assertEqual(self.VSE.jav_Error()[0],'0')
        self.VSE.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_VSE_Example(self):
        Fs = 122.88e6
        IQFile = 'IQFile.iqw'
        OFDMCfg = "\\misc\\OFDM.xml"
        self.VSE.jav_Reset()
        self.VSE.Init_K96()                          #Change Channel
        self.VSE.Set_DisplayUpdate("ON")             #Display On
        self.VSE.Set_SweepCont(0)                    #Continuous Sweep Off
        self.VSE.Set_IQ_SamplingRate(Fs)             #Sampling Rate
        self.VSE.Set_File_InputIQW(Fs,IQFile)        #VSE Input File
        self.VSE.Set_K96_File_Config(OFDMCfg)        #K96 Demod File
        self.VSE.Set_K96_BurstSearch("OFF")          #Burst Search off
        self.VSE.Set_K96_OFDMSymbols(14)
        self.VSE.K96_EVM_AutoCal()
        getVal = self.VSE.Get_EVM()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
#coverage run -a -m unittest -b -v test_HW_VSE_Common
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=4).run(suite)
