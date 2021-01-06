"""Test rssd.bus.jaVISA"""
ipaddress = '192.168.58.115'

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.bus.jaVISA import jaVisa                  #pylint:disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #Run before each test
        print("",end="")
        self.instr = jaVisa()
        # self.instr.jav_Open(IPAddr)

    def tearDown(self):                             #Run after each test
        self.instr.close()

###############################################################################
### <Test>
###############################################################################
    def func_open(self):
        self.instr.open(f'TCPIP::{ipaddress}::5025::SOCKET')       # socket

    def test_open_hislip(self):
        self.instr.open(f'TCPIP::{ipaddress}::hislip0::INSTR')     # hislip

    def test_open_socket(self):
        self.instr.open(f'TCPIP::{ipaddress}::5025::SOCKET')       # socket

    def test_open_vxi11(self):
        self.instr.open(f'TCPIP::{ipaddress}::instr0::INSTR')      # vxi11

    def test_query(self):
        self.func_open()
        self.instr.query('*IDN?')

    def test_read_raw(self):
        self.func_open()
        self.instr.write('*IDN?')
        self.instr.read_raw()

    def test_reslist(self):
        self.func_open()
        self.instr.reslist()

    def test_write(self):
        self.func_open()
        self.instr.write('kdf')

    def test_write_raw(self):
        self.func_open()
        self.instr.write_raw('kdf')

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':                                  # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
