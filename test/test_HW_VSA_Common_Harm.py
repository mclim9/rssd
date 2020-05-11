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
        self.FSW.Init_Harm()

    def tearDown(self):                         #Run after each test
        self.FSW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_FSW_Harm_Common(self):
        self.FSW.Set_Harm_num(3)
        self.FSW.Set_Harm_adjust()
        getVal = self.FSW.Get_Harm()
        self.assertEqual(self.FSW.jav_Error()[0],'0')

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
