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
from rssd.VSA.VSA_K70      import VSA

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #run before each test
        self.FSW = VSA().jav_OpenTest(host)
        self.FSW.Init_VSA()

    def tearDown(self):                             #Run after each test
        self.assertEqual(self.FSW.jav_Error()[0],'0')
        self.FSW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_FSW_VSA_Auto(self):
        self.FSW.Set_VSA_Capture_Length(0)
        self.FSW.Set_VSA_Capture_Time(0)

    def test_FSW_VSA_EQ(self):
        self.FSW.Set_VSA_EqualizerState(0)
        getVal = self.FSW.Get_VSA_EqualizerState()
        if self.FSW.connected: self.assertEqual(getVal, '0')
        self.FSW.Set_VSA_EqualizerState('OFF')
        getVal = self.FSW.Get_VSA_EqualizerState()
        if self.FSW.connected: self.assertEqual(getVal, '0')
        self.FSW.Set_VSA_EqualizerState(1)
        getVal = self.FSW.Get_VSA_EqualizerState()
        if self.FSW.connected: self.assertEqual(getVal, '1')
        self.FSW.Set_VSA_EqualizerState('ON')
        getVal = self.FSW.Get_VSA_EqualizerState()
        if self.FSW.connected: self.assertEqual(getVal, '1')

    def test_FSW_VSA_Get(self):
        self.FSW.Get_VSA_IQImbalance()
        self.FSW.Get_VSA_GainImbalance()
        # self.FSW.Get_VSA_IQSkew()
        self.FSW.Get_VSA_MER()
        self.FSW.Get_VSA_Rho()
        self.FSW.Get_VSA_ResultSumamry()
        self.FSW.Get_VSA_symbol_rate()
        # self.FSW.Get_VSA_SymbolRateError()

    def test_FSW_VSA_Meas(self): #error
        self.FSW.Set_VSA_Symbol_Rate(1e6)
        self.FSW.Set_VSA_Filter_Type('RRC')
        self.FSW.Set_VSA_Filter_Alpha(0.2)
        self.FSW.Set_VSA_Capture_Time(1e-3)
        self.FSW.Set_VSA_Capture_Length(500)
        self.FSW.Set_VSA_EqualizerState(1)
        self.FSW.Set_VSA_Result_Length(200)
        self.FSW.Set_VSA_Result_Length('MAX')
        self.FSW.Get_VSA_Meas_Params()

    def test_FSW_VSA_Mod(self):
        self.FSW.Set_VSA_Mod('QPSK')
        self.FSW.Set_VSA_Mod('OQPSK')
        self.FSW.Set_VSA_Mod('8PSK')
        self.FSW.Set_VSA_Mod('16APSK')
        self.FSW.Set_VSA_Mod('32APSK')
        self.FSW.Set_VSA_Mod('64APSK')
        self.FSW.Set_VSA_Mod('256APSK')

    def test_FSW_VSA_Mod_QAM(self):
        self.FSW.Set_VSA_Mod_Type('QAM')
        self.FSW.Set_VSA_Mod_QAM(16)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
#coverage run -a -m unittest -b -v test_HW_VSA_VSA
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
