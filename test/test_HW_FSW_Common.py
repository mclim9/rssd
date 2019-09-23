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
        self.FSW = VSA()
        try:
            self.FSW.jav_Open(host,prnt=0)
            #self.FSW.jav_Reset()
            self.FSW.jav_ClrErr()
            self.FSW.dLastErr = ""
        except:
            self.assertTrue(1)                  #FAIL

    def tearDown(self):                         #Run after each test
        self.FSW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_FSW_Connect(self):
        self.FSW.jav_IDN(prnt=0)
        self.assertEqual(self.FSW.Make,"Rohde&Schwarz")

    def test_FSW_CommonSettings(self):
        self.FSW.Init_ACLR()
        self.FSW.Set_Freq(1e6)
        self.FSW.Set_RefLevel(10)
        self.FSW.Set_ResBW(1e6)
        self.FSW.Set_VidBW(1e6)
        self.FSW.Set_Span(100e6)
        self.FSW.Get_AttnMech()
        self.FSW.Get_RefLevel()
        self.assertEqual(self.FSW.jav_Error()[0],'0')

    def test_FSW_Marker(self):
        self.FSW.Set_Mkr_Peak()
        asdf = self.FSW.Get_Mkr_Freq()
        self.assertEqual(self.FSW.jav_Error()[0],'0')

    def test_FSW_ACLR(self):
        self.FSW.Get_ACLR()
        #var = input("Please enter something: ")
        self.assertEqual(self.FSW.jav_Error()[0],'0')

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    if 0:                   #Run w/o test names
        unittest.main()
    else:                   #Verbose run
        suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
        unittest.TextTestRunner(verbosity=2).run(suite)
