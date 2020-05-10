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
# host = '169.254.2.20'

###############################################################################
### Code Start
###############################################################################
from rssd.VSG.LTE_K55 import VSG
import os
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                      #run before each test
        self.SMW = VSG()
        self.SMW.debug = 0
        self.SMW.jav_Open(host)
        self.SMW.K2.timeout = 5000
        # self.SMW.jav_Reset()
        self.SMW.jav_ClrErr()
        self.SMW.dLastErr = ""

    def tearDown(self):                         #Run after each test
        self.SMW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_SMW_LTE_Get_DL(self):
        setVal = 'ON'
        self.SMW.Set_LTE_BBState(0)
        self.SMW.Set_LTE_Direction('DL')
        nullVal = self.SMW.Get_LTE_Direction()
        nullVal = self.SMW.Get_LTE_Duplex()
        nullVal = self.SMW.Get_LTE_ChBW()
        nullVal = self.SMW.Get_LTE_ResBlock()           # Need to test DL
        nullVal = self.SMW.Get_LTE_ResBlockOffset()     # Need to test DL
        nullVal = self.SMW.Get_LTE_Modulation()         # Need to test DL
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_LTE_Get_UL(self):
        setVal = 'ON'
        self.SMW.Set_LTE_BBState(0)
        self.SMW.Set_LTE_Direction('UL')
        nullVal = self.SMW.Get_LTE_Direction()
        nullVal = self.SMW.Get_LTE_Duplex()
        nullVal = self.SMW.Get_LTE_ChBW()
        nullVal = self.SMW.Get_LTE_ResBlock()           # Need to test DL
        nullVal = self.SMW.Get_LTE_ResBlockOffset()     # Need to test DL
        nullVal = self.SMW.Get_LTE_Modulation()         # Need to test DL
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_LTE_CC(self):
        self.SMW.Set_LTE_CC(1)
        self.SMW.Get_LTE_CC()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_LTE_Direction(self):
        self.SMW.Set_LTE_Direction('BAD')
        self.SMW.Set_LTE_Direction('UL')
        getVal = self.SMW.Get_LTE_Direction()
        self.assertEqual(getVal,'UL')
        self.SMW.Set_LTE_Direction('DL')
        getVal = self.SMW.Get_LTE_Direction()
        self.assertEqual(getVal,'DL')

    def test_SMW_LTE_Direction(self):
        self.SMW.Set_LTE_Duplex('TDD')
        self.SMW.Set_LTE_Duplex('TDD')
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_LTE_Set_UL(self):
        self.SMW.Set_Freq(2e9)
        self.SMW.Set_LTE_BBState('OFF')                     # Baseband OFF
        self.SMW.Set_LTE_Direction('UL')
        self.SMW.Set_LTE_ChBW(20)
        self.SMW.Set_LTE_ResBlock(66)
        self.SMW.Set_LTE_ResBlockOffset(0)
        self.SMW.Set_LTE_Modulation('QPSK')
        # self.SMW.Set_LTE_BBState('ON')
        # self.SMW.Set_RFState('ON')                          # Turn RF Output on
        self.SMW.Set_RFPwr(-50)                             # Output Power
        # self.SMW.delay(0.5)
        self.assertEqual(self.SMW.jav_Error()[0],'0')

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
