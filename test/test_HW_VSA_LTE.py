###############################################################################
### Rohde & Schwarz Driver Test
### Purpose: self.VSA.LTE_K100 test
### Author:  mclim
### Date:    2020.05.08
###              _   ___        __  _____         _   
###             | | | \ \      / / |_   _|__  ___| |_ 
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_ 
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '192.168.1.109'                      #Get local machine name

###############################################################################
### Code Start
###############################################################################
from rssd.VSA.LTE_K100 import VSA
import os
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                      #run before each test
        self.FSW = VSA()
        self.FSW.debug = 0
        self.FSW.jav_Open(host)
        self.FSW.K2.timeout = 5000
        self.FSW.jav_ClrErr()
        self.FSW.dLastErr = ""
        self.FSW.Init_LTE()

    def tearDown(self):                         #Run after each test
        self.FSW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_FSW_LTE_Get_DL(self):
        self.FSW.Set_LTE_Direction('DL')
        nullVal = self.FSW.Get_LTE_Direction()
        nullVal = self.FSW.Get_LTE_Duplex()
        nullVal = self.FSW.Get_LTE_ChBW()
        nullVal = self.FSW.Get_LTE_ResBlock()           # Need to test DL
        nullVal = self.FSW.Get_LTE_ResBlockOffset()     # Need to test DL
        nullVal = self.FSW.Get_LTE_Modulation()         # Need to test DL
        self.assertEqual(self.FSW.jav_Error()[0],'0')

    def test_FSW_LTE_Get_UL(self):
        self.FSW.Set_LTE_Direction('UL')
        nullVal = self.FSW.Get_LTE_Direction()
        nullVal = self.FSW.Get_LTE_Duplex()
        nullVal = self.FSW.Get_LTE_ChBW()
        nullVal = self.FSW.Get_LTE_ResBlock()           # Need to test DL
        nullVal = self.FSW.Get_LTE_ResBlockOffset()     # Need to test DL
        nullVal = self.FSW.Get_LTE_Modulation()         # Need to test DL
        self.assertEqual(self.FSW.jav_Error()[0],'0')

    def test_FSW_LTE_CC(self):
        self.FSW.Get_LTE_CC()

    def test_FSW_LTE_Direction(self):
        self.FSW.Set_LTE_Direction('UL')
        getVal = self.FSW.Get_LTE_Direction()
        self.assertEqual(getVal,'UL')
        self.FSW.Set_LTE_Direction('DL')
        getVal = self.FSW.Get_LTE_Direction()
        self.assertEqual(getVal,'DL')

    def test_FSW_LTE_Set_UL(self):
        self.FSW.Set_Freq(2e9)
        self.FSW.Set_LTE_Direction('UL')
        self.FSW.Set_LTE_ChBW(20)
        self.FSW.Set_LTE_ResBlock(66)
        self.FSW.Set_LTE_ResBlockOffset(0)
        self.FSW.Set_LTE_Modulation('QPSK')
        # self.FSW.delay(0.5)
        self.assertEqual(self.FSW.jav_Error()[0],'0')

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)