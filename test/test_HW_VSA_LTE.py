###############################################################################
### Purpose: rssd.VSA.LTE_K100 test
###              _   ___        __  _____         _
###             | | | \ \      / / |_   _|__  ___| |_
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '192.168.1.109'                              #Get local machine name

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.VSA.LTE_K100      import VSA

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #run before each test
        self.FSW = VSA().jav_OpenTest(host)
        self.FSW.Init_LTE()

    def tearDown(self):                             #Run after each test
        self.assertEqual(self.FSW.jav_Error()[0],'0')
        self.FSW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_FSW_LTE_AutoRef(self):
        self.FSW.Set_LTE_AutoRef()

    def test_FSW_LTE_Get_DL(self):
        self.FSW.Set_LTE_Direction('DL')
        self.FSW.Set_LTE_Duplex('FDD')
        nullVal = self.FSW.Get_LTE_Direction()
        nullVal = self.FSW.Get_LTE_Duplex()
        nullVal = self.FSW.Get_LTE_ChBW()
        nullVal = self.FSW.Get_LTE_ResBlock()           # Need to test DL
        nullVal = self.FSW.Get_LTE_ResBlockOffset()     # Need to test DL
        nullVal = self.FSW.Get_LTE_Modulation()         # Need to test DL

    def test_FSW_LTE_Get_UL(self):
        self.FSW.Set_LTE_Direction('UL')
        self.FSW.Set_LTE_Duplex('FDD')
        nullVal = self.FSW.Get_LTE_Direction()
        nullVal = self.FSW.Get_LTE_Duplex()
        nullVal = self.FSW.Get_LTE_ChBW()
        nullVal = self.FSW.Get_LTE_ResBlock()           # Need to test DL
        nullVal = self.FSW.Get_LTE_ResBlockOffset()     # Need to test DL
        nullVal = self.FSW.Get_LTE_Modulation()         # Need to test DL

    def test_FSW_LTE_CC(self):
        self.FSW.Set_LTE_CC(2)
        getVal = self.FSW.Get_LTE_CC()
        if self.FSW.connected: self.assertEqual(getVal,'2')
        self.FSW.Set_LTE_CC(1)
        getVal = self.FSW.Get_LTE_CC()
        if self.FSW.connected: self.assertEqual(getVal,'1')

    def test_FSW_LTE_Direction(self):
        self.FSW.Set_LTE_Direction('UL')
        getVal = self.FSW.Get_LTE_Direction()
        if self.FSW.connected: self.assertEqual(getVal,'UL')
        self.FSW.Set_LTE_Direction('DL')
        getVal = self.FSW.Get_LTE_Direction()
        if self.FSW.connected: self.assertEqual(getVal,'DL')

    def test_FSW_LTE_Set_UL(self):
        self.FSW.Set_Freq(2e9)
        self.FSW.Set_LTE_EVMUnit('DB')
        self.FSW.Set_LTE_Duplex('TDD')
        self.FSW.Set_LTE_Duplex('FDD')
        self.FSW.Set_LTE_SubFrameCount(2)
        self.FSW.Set_LTE_Direction('UL')
        self.FSW.Set_LTE_ChBW(20)
        self.FSW.Set_LTE_ResBlock(66)
        self.FSW.Set_LTE_ResBlockOffset(0)
        self.FSW.Set_LTE_Modulation('QPSK')

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
#coverage run -a -m unittest -b -v test_HW_VSA_LTE
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
