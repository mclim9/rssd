###############################################################################
### Rohde & Schwarz Driver Test
### Purpose: rssd.nrq_common.py driver test
### Author:  mclim
### Date:    2018.08.23
###              _   ___        __  _____         _   
###             | | | \ \      / / |_   _|__  ___| |_ 
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_ 
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '192.168.1.40'              #Get local machine name
#host = 'NRQ6-101507.local'                #Get local machine name

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.NRQ.Common import NRQ

class TestGeneral(unittest.TestCase):
    def setUp(self):                      #run before each test
        self.NRQ6 = NRQ()
        try:
            self.NRQ6.jav_Open(host)
            self.NRQ6.jav_Reset()
            self.NRQ6.jav_ClrErr()
            self.NRQ6.dLastErr = ""
        except:
            pass

    def tearDown(self):                         #Run after each test
        self.NRQ6.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_NRQ_Connect(self):
        self.assertEqual(self.NRQ6.Make,"ROHDE&SCHWARZ")

    def test_NRQ_Freq(self):
        SetVal = 1e9
        self.NRQ6.Set_Freq(SetVal)
        GetVal = self.NRQ6.Get_Freq()
        self.assertEqual(SetVal,int(GetVal))

    def test_NRQ_IQ_RecLength(self):
        SetVal = 2468
        self.NRQ6.Set_IQ_RecLength(SetVal)
        GetVal = self.NRQ6.Get_IQ_RecLength()
        self.assertEqual(SetVal,int(GetVal))

    def test_NRQ_IQ_SamplingRate(self):
        SetVal = 12345678
        self.NRQ6.Set_IQ_SamplingRate(SetVal)
        GetVal = self.NRQ6.Get_IQ_SamplingRate()
        self.assertTrue(SetVal<int(GetVal))

    def test_NRQ_Power(self):
        GetVal = self.NRQ6.Get_Power()
        #print(GetVal)
        self.assertTrue(GetVal > -9999)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=4).run(suite)
