###############################################################################
### Rohde & Schwarz Driver Test
### Purpose: SMW.Fading test
### Author:  mclim
### Date:    2020.05.08
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
# host = '169.254.2.20'

###############################################################################
### Code Start
###############################################################################
from rssd.VSG.Fading import VSG
import os
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                                        #run before each test
        self.SMW = VSG()
        self.SMW.debug = 0
        self.SMW.jav_Open(host)
        self.SMW.K2.timeout = 5000
        self.SMW.jav_ClrErr()
        self.SMW.dLastErr = ""

    def tearDown(self):                                     #Run after each test
        self.SMW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_SMW_Fading(self):
        getVal = self.SMW.Get_Fade_Standard()
        getVal = self.SMW.Get_Fade_State()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_Fading_State(self):
        # self.SMW.Set_Fade_State('ON')
        # getVal = self.SMW.Get_Fade_State()
        # self.assertEqual(getVal,1)
        # self.SMW.Set_Fade_State('OFF')
        # getVal = self.SMW.Get_Fade_State()
        self.assertEqual(getVal,0)
        self.assertEqual(self.SMW.jav_Error()[0],'0')



###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
