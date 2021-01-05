""" rssd.yaVISA.py driver test
"""
from __future__ import print_function
import unittest
from rssd.yaVISA import jaVisa

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #Run before each test
        self.instr = jaVisa().jav_OpenTest('192.168.1.108')
        self.instr.jav_ClrErr()
        print("",end="")
        self.instr.debug = 0

    def tearDown(self):                             #Run after each test
        try:
            self.instr.jav_Close()
        except:
            pass

###############################################################################
### <Test>
###############################################################################
    def test_yaVISA_Basic(self):
        # self.instr.write('')
        # self.instr.jav_write_raw('')
        self.instr.query('')
        # self.instr.jav_read_raw()

    def test_yaVISA_Clear(self):
        self.instr.jav_Clear()
        self.instr.jav_Error()

    def test_yaVISA_Delay(self):
        self.instr.delay(0.1)

    def test_yaVISA_IDN(self):
        self.instr.jav_IDN()
        self.instr.jav_Error()

    def test_yaVISA_LogSCPI(self):
        self.instr.jav_logscpi()
        # self.instr.f.close()

    def test_yaVISA_OPCWait(self):
        self.instr.jav_OPC_Wait('')

    def test_yaVISA_Query(self):
        self.instr.queryFloat('')
        self.instr.queryFloatArry('')
        self.instr.queryInt('')
        self.instr.queryIntArry('')

    def test_yaVISA_Raw(self):
        self.instr.jav_write_raw(b'1234')
        self.instr.jav_read_raw()

    def test_yaVISA_Reset(self):
        self.instr.jav_Reset()

    def test_yaVISA_Resources(self):
        self.instr.jav_reslist()

    def test_yaVISA_SCPIList(self):
        self.instr.jav_scpilist(['*IDN','*OPC?'])

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    # coverage run -a -m unittest -b -v test_SW_yaVISA_socket
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
