from __future__ import print_function
#coding: future_fstrings
###############################################################################
### Rohde & Schwarz SCPI Driver Software Test
### Purpose: Import Library-->Create Object-->Catch obvious typos.
###          Tests do not require instrument.
### Author:  mclim
### Date:    2018.06.13
###############################################################################
### Code Start
###############################################################################
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #Run before each test
        print("",end="")
        pass

    def tearDown(self):                             #Run after each test
        pass

###############################################################################
### <Test>
###############################################################################
    def test_yaVISASocket(self):
        setting = 1.23
        from rssd.yaVISA_socket import jaVisa       #pylint:disable=E0611,E0401
        self.Instr = jaVisa()
        self.Instr.debug = 0
        self.Instr.jav_Open('www.google.com',port=80)
        self.Instr.K2.settimeout(setting)
        rdStr = self.Instr.K2.gettimeout()
        self.Instr.K2.close()
        self.assertEqual(setting,rdStr)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)