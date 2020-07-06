# # -*- coding: future_fstrings -*-
# ###############################################################################
### Purpose: rssd.VSA.common test
###              _   ___        __  _____         _
###             | | | \ \      / / |_   _|__  ___| |_
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '192.168.1.108'                              #Get local machine name

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.VSA.Common        import VSA              #pylint: disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #run before each test
        self.FSW = VSA().jav_OpenTest(host)
        self.FSW.Init_Spectral()

    def tearDown(self):                             #Run after each test
        self.assertEqual(self.FSW.jav_Error()[0],'0')
        self.FSW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_FSW_Autolevel(self):
        self.FSW.Set_Autolevel()
        self.FSW.Set_Autolevel_IFOvld()

    def test_FSW_ACLR(self):
        self.FSW.Init_ACLR()
        self.FSW.Set_ACLR_AdjBW(95e6)
        self.FSW.Set_ACLR_AdjSpace(100e6)
        self.FSW.Set_ACLR_CHBW(100e6)
        self.FSW.Set_ACLR_NumAdj(2)
        self.FSW.Get_ACLR()

    def test_FSW_ChannelManagement(self):
        if self.FSW.connected: getVal = self.FSW.Get_ChannelName()
        getVal = self.FSW.Get_Channels()
        self.FSW.Init_IQ()
        if self.FSW.connected: self.FSW.Set_ChannelName('IQ','IQ_Test')
        if self.FSW.connected: self.FSW.Set_ChannelSelect('Spectrum')

    def test_FSW_Connect(self):
        self.FSW.jav_IDN()
        if self.FSW.connected: self.assertEqual(self.FSW.Make,"Rohde&Schwarz")  # Valuecompare

    def test_FSW_Ex_SpectralSettings(self):
        self.FSW.Set_Freq(1e6)
        self.FSW.Set_RefLevel(10)
        self.FSW.Set_ResBW(1e6)
        self.FSW.Set_VidBW(1e6)
        self.FSW.Set_Span(100e6)
        self.FSW.Set_AttnMech(10)
        self.FSW.Get_IFOvld()
        self.FSW.Get_ACLR()
        self.FSW.Set_DisplayUpdate('ON')

    def test_FSW_Ex_SpectralSettings_Auto(self):
        self.FSW.Set_Freq(1e6)
        self.FSW.Set_ResBW(0)
        self.FSW.Set_VidBW(0)
        self.FSW.Set_Span(100e6)
        self.FSW.Set_Autolevel()
        self.FSW.Set_AttnAuto()
        self.FSW.Get_IFOvld()
        self.FSW.Get_ACLR()
        self.FSW.Set_DisplayUpdate('ON')

    def test_FSW_Equalizer(self):
        self.FSW.Set_EQ_File('Test')
        self.FSW.Set_EQ_State('ON')
        self.FSW.Set_EQ_State('OFF')

    def test_FSW_Freq(self):
        self.FSW.Set_FreqStart(10e6)
        self.FSW.Set_FreqStop(100e6)
        # self.FSW.Set_FreqStep(1e5)
        self.FSW.Set_Freq(100e6)
        rdStr = self.FSW.Get_Freq()
        #var = input("Please enter something: ")
        if self.FSW.connected: self.assertEqual(100e6,rdStr)                    # Valuecompare

    def test_FSW_GetParams(self):
        nullVal = self.FSW.Get_Params_Amp(1)
        nullVal = self.FSW.Get_Params_Amp()
        nullVal = self.FSW.Get_Params_Sweep(1)
        nullVal = self.FSW.Get_Params_Sweep()
        nullVal = self.FSW.Get_Params_Trace(1)
        nullVal = self.FSW.Get_Params_Trace()
        nullVal = self.FSW.Get_Params_System(1)
        nullVal = self.FSW.Get_Params_System()
        nullVal = self.FSW.Get_Params_MkrBand(1)
        nullVal = self.FSW.Get_Params_MkrBand()
        nullVal = self.FSW.Get_Params(1,1,1,1,0)

    def test_FSW_GetScreenshot(self):
        getVal = self.FSW.Get_Screenshot()

    def test_FSW_GetTrace(self):
        getVal = self.FSW.Get_Trace_Data()

    def test_FSW_Input(self):
        self.FSW.Set_Freq(1e9)
        self.FSW.Set_Input('RF')
        self.FSW.Set_In_YIG('ON')
        self.FSW.Set_In_YIG('OFF')
        self.FSW.Set_In_HPFilter('ON')

    def test_FSW_Marker_dB(self):
        self.FSW.Set_Mkr_AllOff()
        self.FSW.Set_Mkr_Peak()
        self.FSW.Set_Mkr_On(2)
        self.FSW.Set_Mkr_Next(2)
        getVal = self.FSW.Get_Mkr_Freq()
        getVal = self.FSW.Get_Mkr_XY()
        getVal = self.FSW.Get_Mkr_Y()

    def test_FSW_Marker_dB(self):
        self.FSW.Set_Mkr_AllOff()
        self.FSW.Set_Mkr_BandSetRef()
        self.FSW.Set_Mkr_BandDelta(1e9)

    def test_FSW_Marker_Noise(self):
        self.FSW.Get_Mkr_Noise()

    def test_FSW_Marker_Time(self):
        self.FSW.Set_Span(0)
        self.FSW.Set_SweepTime(0.010)
        self.FSW.Set_Mkr_Time(0.001)
        rdStr = self.FSW.Get_Mkr_TimeDomain()
        if self.FSW.connected: self.assertEqual(rdStr, 0.001)
        self.FSW.Set_Span(900e6)
        self.FSW.Set_SweepTime(0)                           #Auto Sweeptime

    def test_FSW_Trigger(self):
        self.FSW.Set_Trig1_Source('IMM')
        self.FSW.Set_Trig2_Dir('OUT')
        self.FSW.Set_Trig2_OutType('DEV')

    def test_FSW_Sys_Overload(self):
        getVal = self.FSW.Get_Ovld_Stat()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    # coverage run -a -m unittest -b -v test_HW_VSA_Common
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
