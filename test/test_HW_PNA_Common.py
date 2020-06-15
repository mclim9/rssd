# # -*- coding: future_fstrings -*-
################################################################################
### Purpose: rssd.PNA.common test
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
from rssd.PNA.Common        import PNA              #pylint: disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #run before each test
        self.FSWP = PNA().jav_OpenTest(host)

    def tearDown(self):                             #Run after each test
        self.assertEqual(self.FSWP.jav_Error()[0],'0')
        self.FSWP.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_FSWP_Freq(self):
        self.FSWP.Init_Spectral()
        self.FSWP.Set_FreqStart(10e6)
        self.FSWP.Set_FreqStop(100e6)
        self.FSWP.Set_Freq(100e6)
        rdStr = self.FSWP.Get_Freq()
        #var = input("Please enter something: ")
        if self.FSWP.connected: self.assertEqual(100e6,rdStr)                    # Valuecompare

    def test_FSWP_Get(self):
        self.FSWP.Init_PhaseNoise()
        self.FSWP.Get_AttnMech()
        self.FSWP.Get_Channels()
        self.FSWP.Get_RefLevel()
        self.FSWP.Get_SweepPoints()
        self.FSWP.Get_SweepTime()
        self.FSWP.Get_SweepType()

    def test_FSWP_GetScreenshot(self):
        getVal = self.FSWP.Get_Screenshot()

    def test_FSWP_GetTrace(self):
        getVal = self.FSWP.Get_Trace_Data()

    def test_FSWP_Harmonics(self):
        self.FSWP.Init_Harm()
        self.FSWP.Set_Harm_num(3)
        self.FSWP.Set_Harm_adjust()
        getVal = self.FSWP.Get_Harm_Values()

    def test_FSWP_Input(self):
        self.FSWP.Set_Freq(1e9)
        self.FSWP.Set_Input('RF')
        # self.FSWP.Set_In_YIG('ON')
        # self.FSWP.Set_In_HPFilter('ON')

    def test_FSWP_Marker(self):
        self.FSWP.Init_Spectral()
        self.FSWP.Set_Mkr_AllOff()
        self.FSWP.Set_Mkr_Peak()
        self.FSWP.Set_Mkr_On(2)
        self.FSWP.Set_Mkr_Next()
        getVal = self.FSWP.Get_Mkr_Freq()
        getVal = self.FSWP.Get_Mkr_XY()
        getVal = self.FSWP.Get_Mkr_Y()

    def test_FSWP_PhaseNoise(self):
        self.FSWP.Init_PhaseNoise()
        self.FSWP.Set_SweepCont(0)          # Single Sweep
        self.FSWP.Set_PwrThreshold(-10)
        self.FSWP.Set_Xcorr(100)
        self.FSWP.Set_XcorrOpt(1)
        getVal = self.FSWP.Get_FreqLock()
        getVal = self.FSWP.Get_Freq()
        getVal = self.FSWP.Get_Power()
        getVal = self.FSWP.Get_PN_Decade()
        getVal = self.FSWP.Get_PN_Int()

    def test_FSWP_Spectral_Settings(self):
        self.FSWP.Init_Spectral()
        self.FSWP.Set_SweepCont(1)          # Contiuous Sweep
        self.FSWP.Set_Freq(1e6)
        self.FSWP.Set_RefLevel(10)
        self.FSWP.Set_ResBW(1e6)
        self.FSWP.Set_ResBW(0)              # Auto
        self.FSWP.Set_VidBW(1e6)
        self.FSWP.Set_Span(100e6)
        self.FSWP.Set_AttnMech(10)
        self.FSWP.Set_AttnAuto()
        self.FSWP.Set_Autolevel()
        self.FSWP.Get_IFOvld()
        self.FSWP.Set_DisplayUpdate('ON')

    def test_FSWP_Sys_Overload(self):
        getVal = self.FSWP.Get_Ovld_Stat()

    def test_FSWP_Trace(self):
        self.FSWP.Init_PhaseNoise()
        self.FSWP.Set_Trace_Avg('POW')
        self.FSWP.Set_Trace_Detector('RMS')
        self.FSWP.Set_Trace_AvgCount(20)
        self.FSWP.Set_Trace_AvgOff()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    #coverage run -a -m unittest discover -b -v -p test_HW_PNA_Common.py
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
