"""Test rssd.instrument"""
ipaddress = '192.168.58.115'

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.instrument import instr                   #pylint:disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #Run before each test
        print("",end="")
        self.instr = instr()

    def tearDown(self):                             #Run after each test
        print(self.instr.Model)
        self.instr.close()

###############################################################################
### <Test>
###############################################################################
    def test_open_default(self):
        self.instr.open(ipaddress)

    def test_open_hislip(self):
        self.instr.open(ipaddress, type='hislip')

    def test_open_socket(self):
        self.instr.open(ipaddress, type='socket')

    def test_open_test(self):
        self.instr.open(ipaddress, type='test')

    def test_open_visa_socket(self):
        self.instr.open(ipaddress, type='visa-socket')

    def test_open_vxi11(self):
        self.instr.open(ipaddress, type='vxi11')

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':                                  # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
