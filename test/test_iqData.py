# -*- coding: future_fstrings -*-
###############################################################################
### Purpose:Test rssd.iqdata.py
###############################################################################
import os
import unittest
from rssd.iqdata      import IQ             # pylint: disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                            #Run before each test
        self.IQ = IQ()
        
    def tearDown(self):                         #Run after each test
        pass

###############################################################################
### </Test>
###############################################################################
    def test_readIqTar(self):
        self.IQ.readIqTar('test/fixture/Sine-1MHZ.iq.tar')
        self.assertAlmostEqual(self.IQ.iqData[241].real,0.978118896)

    def test_readIqw(self):
        self.IQ.readIqw('test/fixture/Sine-1MHZ.iqw')
        self.assertAlmostEqual(self.IQ.iqData[241].real,0.40673828)

    def test_readWv(self):
        self.IQ.readWv('test/fixture/Sine-1MHZ.wv')
        self.assertAlmostEqual(self.IQ.iqData[241].real,0.97814874)

    def test_writeIqTar(self):
        self.IQ.iqData = [(.0+.1j),(.2+.3j),(.4+.5j),(.6+.7j),(.8+.9j),(.10+.11j),(.12+.13j),(.14+.15j),(.16+.17j),(.18+.19j)]
        self.IQ.writeIqTar('Test.iq.tar')

    def test_writeIqW(self):
        self.IQ.iqData = [(.0+.1j),(.2+.3j),(.4+.5j),(.6+.7j),(.8+.9j),(.10+.11j),(.12+.13j),(.14+.15j),(.16+.17j),(.18+.19j)]
        self.IQ.writeIqw('Test.iqw')

    def test_writeWv(self):
        self.IQ.iqData = [(.0+.1j),(.2+.3j),(.4+.5j),(.6+.7j),(.8+.9j),(.10+.11j),(.12+.13j),(.14+.15j),(.16+.17j),(.18+.19j)]
        self.IQ.fSamplingRate = 1e6
        self.IQ.writeWv('Test.wv')

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':                              # pragma: no cover
    #coverage run -a -m unittest discover -b -v -p test_iqData.py
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
