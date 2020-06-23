###############################################################################
### Rohde & Schwarz driver Test
### Purpose: self.VSE_Common test
### Author:  mclim
### Date:    2018.05.07
###              _   ___        __  _____         _   
###             | | | \ \      / / |_   _|__  ___| |_ 
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_ 
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###                 Please start VSE prior to test
###############################################################################
### User Entry
###############################################################################
host = '127.0.0.1'                              #Get local machine name
port = 5025                                     #Reserve a port for your service.

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.VSE.Common import VSE

class TestGeneral(unittest.TestCase):
    def setUp(self):                            #Run before each test
        self.VSE = VSE().jav_OpenTest(host)

    def tearDown(self):                         #Run after each test
        self.assertEqual(self.VSE.jav_Error()[0],'0')
        self.VSE.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_VSE_Connect(self):
        if self.VSE.connected == 1: self.assertEqual(self.VSE.Make,"Rohde&Schwarz")
        self.assertEqual(self.VSE.Model,"VSE")

    def test_VSE_IQ_Settings(self): 
        self.VSE.Set_Freq(1e6)
        self.VSE.Set_RefLevel(10)
        self.VSE.Set_SamplingRate(123e6)
        self.VSE.Set_SweepTime(1.234e-6)
        rlen = self.VSE.Get_IQ_RecLength()
        if self.VSE.connected == 1: self.assertEqual(rlen,123)

    def test_VSE_IQ_Data2File(self):
        if self.VSE.connected == 1: self.VSE.Get_IQ_Data()

    # def test_VSE_Marker(self):        
    #     self.VSE.Set_Mkr_Peak()
    #     self.VSE.Get_Mkr_Freq()
    #     self.assertEqual(self.VSE.dLastErr,"")

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=1).run(suite)
