# # -*- coding: future_fstrings -*-
###############################################################################
### Purpose: rssd.VSA.Common_IQ test
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
from rssd.VSA.Common        import VSA              #pylint: disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #run before each test
        self.FSW = VSA().jav_OpenTest(host)
        self.FSW.Init_IQ()

    def tearDown(self):                                 #Run after each test
        self.assertEqual(self.FSW.jav_Error()[0],'0')
        self.FSW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_FSW_IQ_Common(self):
        self.FSW.Set_IQ_BW(100e6)
        self.FSW.Set_IQ_SamplingRate(100e6)
        self.FSW.Set_IQ_RecLength(100)
        self.FSW.Set_IQ_Samples(100)
        self.FSW.Set_IQ_Time(1e-3)
        getVal = self.FSW.Get_IQ_RecLength()
        getVal = self.FSW.Get_IQ_SamplingRate()

    def test_FSW_Get_IQData(self):
        self.FSW.Set_IQ_RecLength(10)
        self.FSW.Set_SweepCont(0)
        getVal = self.FSW.Get_IQ_Data()
        if self.FSW.connected == 0: getVal = self.FSW.Get_IQ_Data_Ascii(2)
        # if self.FSW.connected == 1: getVal = self.FSW.Get_IQ_Data_Ascii(5)
        getVal = self.FSW.Get_IQ_Data_Ascii2()
        if self.FSW.connected == 1: getVal = self.FSW.Get_IQ_Data_Bin()

    def test_FSW_Set_IQ_ALCR(self):
        self.FSW.Set_IQ_ACLR(9e6,10e6)
        self.FSW.Get_Mkr_BandACLR()

    def test_FSW_Set_IQ_Adv(self):
        self.FSW.Set_IQ_Adv_Mode(0)
        self.FSW.Set_IQ_Adv_Mode(1)
        self.FSW.Set_IQ_Adv_TransAlgo("AVER")
        self.FSW.Set_IQ_Adv_WindowLenth(101)
        self.FSW.Set_IQ_Adv_FFTLenth(4096+1)
        self.FSW.Set_IQ_Adv_Window('P5')

    def test_FSW_Set_IQSpectrum(self):
        self.FSW.Set_IQ_SpectrumWindow()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
