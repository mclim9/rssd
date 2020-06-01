from __future__ import print_function
#coding: future_fstrings
###############################################################################
### Rohde & Schwarz SCPI Driver Software Test
### Purpose: rssd.test.examples
###############################################################################
### Code Start
###############################################################################
import unittest
import rssd.test.yaVISA
import rssd.test.FileIO

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #Run before each test
        from importlib import reload
        reload(rssd.test.yaVISA)
        reload(rssd.test.FileIO)
        print("",end="")

    def tearDown(self):                             #Run after each test
        pass

###############################################################################
### <Test>
###############################################################################
    def test_EX_helloworld(self):
        import rssd.examples.AAA_CommandTime as example

    # def test_EX_CMW_GPRF_Loopback(self):
    #     import rssd.examples.CMW_GPRF_Loopback as example
    #     self.assertTrue(1)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    # unittest.main()     #Run w/o test names
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
    