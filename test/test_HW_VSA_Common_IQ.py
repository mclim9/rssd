# # -*- coding: future_fstrings -*-
# ###############################################################################
### Rohde & Schwarz driver Test
### Purpose: self.FSW_common test
### Author:  mclim
### Date:    2018.05.07
###              _   ___        __  _____         _   
###             | | | \ \      / / |_   _|__  ___| |_ 
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_ 
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '192.168.1.109'                          #Get local machine name

###############################################################################
### Code Start
###############################################################################
from rssd.VSA.Common import VSA                 # pylint: disable=E0611,E0401
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                            #Run before each test
        print("",end="")
        self.FSW = VSA()
        self.FSW.debug = 0
        self.FSW.jav_Open(host,prnt=0)
        #self.FSW.jav_Reset()
        self.FSW.jav_ClrErr()
        self.FSW.dLastErr = ""
        self.FSW.Init_IQ()

    def tearDown(self):                         #Run after each test
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
        self.assertEqual(self.FSW.jav_Error()[0],'0')

    def test_FSW_Get_IQData(self):
        self.FSW.Set_IQ_RecLength(10)
        self.FSW.Set_SweepCont(0)
        getVal = self.FSW.Get_IQ_Data()
        # getVal = self.FSW.Get_IQ_Data_Ascii()
        getVal = self.FSW.Get_IQ_Data_Ascii2()
        getVal = self.FSW.Get_IQ_Data_Bin()
        self.assertEqual(self.FSW.jav_Error()[0],'0')

    def test_FSW_Set_IQ_ALCR(self):
        self.FSW.Set_IQ_ACLR(9e6,10e6)
        self.FSW.Get_Mkr_BandACLR()
        self.assertEqual(self.FSW.jav_Error()[0],'0')

    def test_FSW_Set_IQ_Adv(self):
        self.FSW.Set_IQ_Adv_Mode()
        self.FSW.Set_IQ_Adv_TransAlgo("AVER")
        self.FSW.Set_IQ_Adv_WindowLenth(101)
        self.FSW.Set_IQ_Adv_FFTLenth(4096+1)
        self.FSW.Set_IQ_Adv_Window('P5')
        self.assertEqual(self.FSW.jav_Error()[0],'0')

    def test_FSW_Set_IQSpectrum(self):
        self.FSW.Set_IQ_SpectrumWindow()
        self.assertEqual(self.FSW.jav_Error()[0],'0')


###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
