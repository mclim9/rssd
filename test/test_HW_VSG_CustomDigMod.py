###############################################################################
### Rohde & Schwarz Driver Test
### Purpose: VSG.CustomDigMod test
### Author:  mclim
### Date:    2018.06.13
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
from rssd.VSG.CustomDigMod import VSG
import os
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                                    #run before each test
        self.SMW = VSG()
        self.SMW.debug = 0
        self.SMW.jav_Open(host)
        self.SMW.K2.timeout = 5000
        self.SMW.jav_ClrErr()
        self.SMW.dLastErr = ""

    def tearDown(self):                                 #Run after each test
        self.SMW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_SMW_CDM(self):
        self.SMW.Set_CDM_State('ON')
        getVal = self.SMW.Get_CDM_State()
        self.assertEqual(getVal,1)                      #Value
        self.SMW.Set_CDM_State('OFF')
        getVal = self.SMW.Get_CDM_State()
        self.assertEqual(getVal,0)                      #Value
        self.assertEqual(self.SMW.jav_Error()[0],'0')

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
