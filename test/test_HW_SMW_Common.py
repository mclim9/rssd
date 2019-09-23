###############################################################################
### Rohde & Schwarz Driver Test
### Purpose: self.SMW_Common test
### Author:  mclim
### Date:    2018.06.13
###              _   ___        __  _____         _   
###             | | | \ \      / / |_   _|__  ___| |_ 
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_ 
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '192.168.1.114'              #Get local machine name

###############################################################################
### Code Start
###############################################################################
from rssd.VSG.Common import VSG
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                      #run before each test
        self.SMW = VSG()
        try:
            self.SMW.jav_Open(host,prnt=0)
            self.SMW.jav_Reset()
            self.SMW.jav_ClrErr()
            self.SMW.dLastErr = ""
        except:
            self.assertTrue(1)

    def tearDown(self):                         #Run after each test
        self.SMW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_SMW_Connect(self):
        self.SMW.jav_IDN(prnt=0)
        self.assertEqual(self.SMW.Make,"Rohde&Schwarz")

    def test_SMW_Freq(self):
        frq = 1e6
        self.SMW.Set_Freq(frq)
        rdFrq = self.SMW.Get_Freq()
        self.assertEqual(self.SMW.jav_Error()[0],'0')
        self.assertEqual(frq,rdFrq)

    def test_SMW_Pwr(self):
        pwr = -10
        self.SMW.Set_RFPwr(pwr)
        rdPwr = self.SMW.Get_PowerRMS()
        self.assertEqual(self.SMW.jav_Error()[0],'0')
        self.assertEqual(pwr,rdPwr)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    if 0:                   #Run w/o test names
        unittest.main()
    else:                   #Verbose run
        suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
        unittest.TextTestRunner(verbosity=2).run(suite)
