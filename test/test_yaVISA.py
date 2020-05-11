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
        try:
            self.instr.jav_Close()
        except:
            pass


###############################################################################
### <Test>
###############################################################################
    def test_yaVISA_delay(self):
        from rssd.yaVISA import jaVisa
        self.instr = jaVisa()
        self.instr.delay(0.1)

    # def test_yaVISA_noVISA(self):
    #     # Test will not make a VISA connection.  Testing exception paths
    #     from rssd.yaVISA import jaVisa
    #     self.instr = jaVisa()
    #     # self.instr.K2.settimeout(0.01)
    #     self.instr.jav_Open('1.1.1.1')
    #     self.instr.jav_ClrErr                       # except
    #     self.assertTrue(1)

    def test_yaVISAs_delay(self):
        from rssd.yaVISA_socket import jaVisa
        self.instr = jaVisa()
        self.instr.delay(0.1)

    def test_yaVISAs_Open(self):
        setting = 1.23
        from rssd.yaVISA_socket import jaVisa       #pylint:disable=E0611,E0401
        self.Instr = jaVisa()
        self.Instr.debug = 0
        # self.Instr.jav_Open('www.yahoo.com',port=80)
        # self.Instr.K2.settimeout(setting)
        # rdStr = self.Instr.K2.gettimeout()
        # self.Instr.jav_Close()
        # self.assertEqual(setting,rdStr)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    # unittest.main()     #Run w/o test names
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
