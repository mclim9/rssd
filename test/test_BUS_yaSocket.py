"""Test rssd.bus.jaVISA"""
ipaddress = '192.168.58.114'

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.bus.jaSocket import jaSocket              #pylint:disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #Run before each test
        print("",end="")
        self.instr = jaSocket()
        self.instr.open(ipaddress, 5025)

    def tearDown(self):                             #Run after each test
        self.instr.close()

###############################################################################
### <Test>
###############################################################################
    def test_query(self):
        rdStr = self.instr.query('*IDN?')

    # def test_read_raw(self):
    #     self.instr.write('*IDN?')
    #     rdStr = self.instr.read_raw()

    def test_write(self):
        self.instr.write('kdf')

    def test_write_raw(self):
        self.instr.write_raw('kdf')

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':                                  # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
