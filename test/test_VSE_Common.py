###############################################################################
### Rohde & Schwarz Software Test
###
### Purpose: self.VSE_driver software test
### Author:  mclim
### Date:    2018.05.07
###############################################################################
### User Entry
###############################################################################
host = '127.0.0.1'                              #Get local machine name
port = 5025                                     #Reserve a port for your service.

###############################################################################
### Code Start
###############################################################################
from rssd.VSE_Common import VSE
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                      #run before each test
        self.VSE = VSE()
        try:
            self.VSE.VISA_Open(host)
            self.VSE.VISA_Reset()
            self.VSE.VISA_ClrErr()
            self.VSE.dLastErr = ""
        except:
            self.assertTrue(1)

    def test_VSE_Connect(self):
        self.assertEqual(self.VSE.Make,"Rohde&Schwarz")
        self.assertEqual(self.VSE.Model,"VSE")

    def test_VSE_IQ_Settings(self): 
        self.VSE.Set_Freq(1e6)
        self.VSE.Set_RefLevel(10)
        self.VSE.Set_SamplingRate(123e6)
        self.VSE.Set_SweepTime(1.234e-6)
        rlen = self.VSE.Get_IQ_RecLength()
        self.assertEqual(rlen,123)

    def test_VSE_IQ_Data2File(self):
        self.VSE.Get_IQ_Data()
        self.assertEqual(self.VSE.VISA_Error()[0],"0")
        
        
        
'''
    def test_VSE_Marker(self):        
        self.VSE.Set_Mkr_Peak()
        self.VSE.Get_Mkr_Freq()
        self.assertEqual(self.VSE.dLastErr,"")
'''

if __name__ == '__main__':
    if 0:     #Run w/o test names
        unittest.main(buffer=1)
    else:     #Verbose run
        suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
        unittest.TextTestRunner(verbosity=2,buffer=1).run(suite)
