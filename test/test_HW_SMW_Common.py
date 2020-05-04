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
host = '10.0.0.7'              #Get local machine name

###############################################################################
### Code Start
###############################################################################
from rssd.VSG.Common import VSG
import os
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                      #run before each test
        self.SMW = VSG()
        try:
            self.SMW.debug = 0
            self.SMW.jav_Open(host)
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
    def test_SMW_Arb_Freq(self):
        setVal = 10e6
        self.SMW.Set_ArbClockFreq(setVal)
        getVal = self.SMW.Get_ArbClockFreq()
        self.assertEqual(setVal,getVal)

    def test_SMW_CrestFactor(self):
        getVal = self.SMW.Get_CrestFactor()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_SysConfigAll(self):
        getVal = self.SMW.Get_SysC_All()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_Connect(self):
        self.assertEqual(self.SMW.Make,"Rohde&Schwarz")

    def test_SMW_Freq(self):
        setVal = 2e6
        self.SMW.Set_Freq(setVal)
        getVal = self.SMW.Get_Freq()
        self.assertEqual(self.SMW.jav_Error()[0],'0')
        self.assertEqual(setVal,getVal)

    def test_SMW_Pwr(self):
        setVal = -10
        self.SMW.Set_RFPwr(setVal)
        getVal = self.SMW.Get_PowerRMS()
        self.assertEqual(self.SMW.jav_Error()[0],'0')
        self.assertEqual(setVal,getVal)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    if 0:                   #Run w/o test names
        unittest.main()
    else:                   #Verbose run
        suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
        unittest.TextTestRunner(verbosity=2).run(suite)
        # os.system('coverage run -m unittest -v test.test_HW_SMW_Common')
