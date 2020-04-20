from __future__ import print_function
#coding: future_fstrings
###############################################################################
### Rohde & Schwarz SCPI Driver Software Test
###
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
    def test_EX_helloworld(self):
        import rssd.examples.AAA_CommandTime as example
        self.assertTrue(1)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    if 0:     #Run w/o test names
        unittest.main()
    else:     #Verbose run
        suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
        unittest.TextTestRunner(verbosity=2).run(suite)
