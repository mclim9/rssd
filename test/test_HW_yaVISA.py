from __future__ import print_function
#coding: future_fstrings
###############################################################################
### Rohde & Schwarz SCPI Driver Software Test
### Purpose: Import Library-->Create Object-->Catch obvious typos.
###          Tests do not require instrument.
### Author:  mclim
### Date:    2018.06.13
###############################################################################
### User Settings
###############################################################################
IPAddr = '192.168.1.109'
IPAddr = '169.254.2.20'
IPAddr = '10.0.0.7'

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.yaVISA import jaVisa                      #pylint:disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #Run before each test
        print("",end="")
        self.instr = jaVisa()
        self.instr.debug = 0
        self.instr.jav_Open(IPAddr)
        pass

    def tearDown(self):                             #Run after each test
        self.instr.K2.close()

###############################################################################
### <Test>
###############################################################################
    def test_Clear(self):
        self.instr.jav_Clear()

    def test_OpenIDN(self):
        #Validates VISA Open; Query; jav_ClrErr
        self.assertNotEqual(self.instr.Make,"")

    def test_OPC_Wait(self):
        #Validates VISA Write; 
        self.instr.jav_OPC_Wait('*RST')

    def test_resourcelist(self):
        rl = self.instr.jav_reslist()
        self.assertNotEqual(rl,["No VISA"])

    def test_queryint(self):
        rd = self.instr.queryInt("*OPC?")
        self.assertEqual(rd,1)

    # def test_queryintarry(self):
    #     rd = self.instr.queryIntArry("*OPT?")
    #     self.assertEqual(rd,1)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':                                  # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)