"""Test rssd.instrument"""
ipaddress = '192.168.58.115'

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.instrument import instr

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #Run before each test
        print("",end="")
        self.instr = instr()
        self.instr.open(ipaddress)

    def tearDown(self):                             #Run after each test
        self.instr.close()

###############################################################################
### <Test>
###############################################################################
    def test_query(self):
        rdStr = self.instr.query('*IDN?')


###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':                                  # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
