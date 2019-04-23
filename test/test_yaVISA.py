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
    def test_yaVISA(self):
        from rssd.yaVISA import jaVisa              #pylint:disable=E0611,E0401
        self.K2 = jaVisa()

    def test_yaVISASocket(self):
        from rssd.yaVISA_socket import jaVisa       #pylint:disable=E0611,E0401
        self.K2 = jaVisa()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
