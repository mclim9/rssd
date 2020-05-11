# # -*- coding: future_fstrings -*-
# ###############################################################################
### Rohde & Schwarz driver Test
### Purpose: VSA.ADemod_K7 test
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
host = '192.168.1.109'                              #Get local machine name

###############################################################################
### Code Start
###############################################################################
from rssd.VSA.ADemod_K7 import VSA                  # pylint: disable=E0611,E0401
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #Run before each test
        print("",end="")
        self.FSW = VSA()
        self.FSW.debug = 0
        self.FSW.jav_Open(host,prnt=0)
        self.FSW.jav_ClrErr()
        self.FSW.dLastErr = ""
        self.FSW.Init_ADemod()

    def tearDown(self):                             #Run after each test
        self.FSW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_FSW_ADemod(self):
        self.FSW.Set_Adem_dbw(1e6)
        self.FSW.Set_Adem_LPassStat('OFF')
        self.FSW.Set_Adem_LPassStat('ON')
        self.FSW.Set_Adem_LPassAbsolute('3kHz')
        self.FSW.Set_Adem_LPassManual(1e6)
        self.FSW.Set_Adem_LPassRelative('5PCT')
        getVal = self.FSW.Set_Adem_dbw()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
