###############################################################################
### Purpose: rssd.FSW.WLAN_K54 test
###              _   ___        __  _____         _
###             | | | \ \      / / |_   _|__  ___| |_
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '10.0.0.7'                                       #Get local machine name
host = '192.168.1.114'

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.VSA.WLAN_K91  import VSA

class TestGeneral(unittest.TestCase):
    def setUp(self):                                    #run before each test
        self.FSW = VSA().jav_OpenTest(host)
        self.FSW.Init_WLAN()

    def tearDown(self):                                 #Run after each test
        self.assertEqual(self.FSW.jav_Error()[0],'0')
        self.FSW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_FSW_WLAN_ACLR(self):
        self.FSW.Init_WLAN_ACLR()
        self.FSW.Get_ACLR()

    def test_FSW_WLAN_Get(self):
        nullVal = self.FSW.Get_WLAN_Standard()
        nullVal = self.FSW.Get_WLAN_ChBW()
        nullVal = self.FSW.Get_WLAN_PPDU()
        nullVal = self.FSW.Get_WLAN_MCS()
        nullVal = self.FSW.Get_WLAN_Modulation()
        self.assertEqual(self.FSW.jav_Error()[0],'0')

    def test_FSW_WLAN_EVM(self):
        self.FSW.Init_WLAN_EVM()
        self.FSW.Get_Params_WLAN_EVM()

    def test_FSW_WLAN_SEM(self):
        self.FSW.Init_WLAN_SEM()
        self.FSW.Get_WLAN_SEM()

    def test_FSW_WLAN_Set(self):
        # self.FSW.Set_Freq(self.Freq)
        self.FSW.Set_WLAN_ChBW(160)
        self.FSW.Set_WLAN_Standard('AC')
        self.FSW.Set_WLAN_MCS(1)
        self.FSW.Set_WLAN_Modulation('QPSK')
        self.assertEqual(self.FSW.jav_Error()[0],'0')

    def test_FSW_WLAN_Set_A(self):
        setVal = 'A'
        self.FSW.Set_WLAN_Standard(setVal)
        getVal = self.FSW.Get_WLAN_Standard()
        if self.FSW.connected: self.assertEqual(setVal,getVal)

    def test_FSW_WLAN_Set_B(self):
        setVal = 'B'
        self.FSW.Set_WLAN_Standard(setVal)
        getVal = self.FSW.Get_WLAN_Standard()
        if self.FSW.connected: self.assertEqual(setVal,getVal)

    # def test_FSW_WLAN_Set_G(self):
    #     setVal = 'G'
    #     self.FSW.Set_WLAN_Standard(setVal)
    #     getVal = self.FSW.Get_WLAN_Standard()
    #     self.assertEqual(setVal,getVal)

    def test_FSW_WLAN_Set_N(self):
        setVal = 'N'
        self.FSW.Set_WLAN_Standard(setVal)
        getVal = self.FSW.Get_WLAN_Standard()
        if self.FSW.connected: self.assertEqual(setVal,getVal)

    def test_FSW_WLAN_Set_AC(self):
        setVal = 'AC'
        self.FSW.Set_WLAN_Standard(setVal)
        getVal = self.FSW.Get_WLAN_Standard()
        if self.FSW.connected: self.assertEqual(setVal,getVal)

    def test_FSW_WLAN_Set_AX(self):
        setVal = 'AX'
        self.FSW.Set_WLAN_Standard(setVal)
        getVal = self.FSW.Get_WLAN_Standard()
        if self.FSW.connected: self.assertEqual(setVal,getVal)

    def test_FSW_WLAN_Set_Bad(self):            #Test exception
        setVal = 'BAD'
        self.FSW.Set_WLAN_Standard(setVal)

    def test_FSW_WLAN_Set_BBON(self):
        self.FSW.Set_WLAN_ChBW(20)
        if self.FSW.connected: self.FSW.Set_WLAN_BBState('ON')

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    #coverage run -a -m unittest -b -v test_HW_VSA_WLAN
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
