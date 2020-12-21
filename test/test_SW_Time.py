# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Software Test
###
### Purpose:Test FileIO.py
### Author: mclim
### Date:   2018.06.04
###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.RSI.time          import timer

class TestGeneral(unittest.TestCase):
    def setUp(self):                            #Run before each test
        self.TMR = timer()

    def tearDown(self):                         #Run after each test
        pass

###############################################################################
### </Test>
###############################################################################
    def test_loops(self):
        loop1 = 3
        loop2 = 7
        self.TMR.numTest = loop1 * loop2
        self.TMR.suite_start()
        for i in range(loop1):
            for j in range(loop2):
                self.TMR.start()
                self.TMR.tick()
                self.TMR.tick()
                print(self.TMR.Get_Params_Time())

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':                              # pragma: no cover
    # coverage run -a -m unittest -b -v test_SW_Time
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
