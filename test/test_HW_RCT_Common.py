###############################################################################
### Purpose: rssd.RCT.Common test
###              _   ___        __  _____         _
###             | | | \ \      / / |_   _|__  ___| |_
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '192.168.1.160'              #Get local machine name

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.RCT.Common    import RCT

class TestGeneral(unittest.TestCase):
    def setUp(self):                      #run before each test
        self.CMP = RCT().jav_OpenTest(host)

    def tearDown(self):                         #Run after each test
        self.assertEqual(self.CMP.jav_Error()[0],'0')
        self.CMP.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_RCT_Ex_GenArb(self):
        self.CMP.Init_Gen()
        self.CMP.Set_Gen_Port('P1.IFOut')
        self.CMP.Set_Gen_Port_State('ON')
        self.CMP.Set_Gen_Freq(6e9)
        self.CMP.Set_Gen_Mode('ARB')
        self.CMP.Set_Gen_ArbWv('Test.wv')
        self.CMP.Set_Gen_ArbExec()
        self.CMP.Set_Gen_RFPwr(-50)
        self.CMP.Set_Gen_RFState('ON')

    def test_RCT_Ex_GenGet(self):
        self.CMP.Get_Gen_ArbWv()
        self.CMP.Get_Gen_Freq()
        self.CMP.Get_Gen_Mode()
        self.CMP.Get_Gen_Port()

    def test_RCT_Ex_GenCW(self):
        self.CMP.Init_Gen()
        self.CMP.Set_Gen_Port('P1.IFOut')
        self.CMP.Set_Gen_Port_State('ON')
        self.CMP.Set_Gen_Freq(6e9)
        self.CMP.Set_Gen_Mode('CW')
        self.CMP.Set_Gen_RFPwr(-50)
        self.CMP.Set_Gen_RFState('ON')

    def test_RCT_Ex_MeasFFT(self):
        self.CMP.Init_Meas_FFT()
        self.CMP.Set_Meas_Freq(6e9)
        self.CMP.Set_Meas_Port('P1.IFIn')
        self.CMP.Set_Meas_Autolevel()
        # self.CMP.Set_Meas_RefLevl(-10)
        # self.CMP.Set_Meas_UserMargin(0)
        self.CMP.Set_Meas_RFBW(10e6)
        self.CMP.Set_Meas_Span(100e6)

    def test_RCT_Ex_MeasPwr(self):
        self.CMP.Init_Meas_Power()
        self.CMP.Set_Meas_Freq(6e9)
        self.CMP.Set_Meas_UserMargin(0)
        self.CMP.Set_Meas_Expected_Nom_Power(0)
        self.CMP.Set_Meas_TriggerSource('IF Power')
        self.CMP.Set_Meas_TriggerThreshold(-10)
        self.CMP.Set_Meas_TriggerThreshold(-40)
        self.CMP.Set_Meas_Pwr_MLength(100e-6)
        self.CMP.Set_Meas_RFBW(100e6)
        self.CMP.Get_Meas_Power()

    def test_RCT_System(self):
        self.CMP.Get_Options()
        self.CMP.Init_Syst()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
