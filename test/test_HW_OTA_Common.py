"""rssd.self.OTA.common.py driver test"""
import unittest
from rssd.OTA.Common import OTA

host = '192.168.1.40'              #Get local machine name

class TestGeneral(unittest.TestCase):
    def setUp(self):                      #run before each test
        self.ATSxxxx = OTA().open(host, type='test')

    def tearDown(self):                         #Run after each test
        self.assertEqual(self.ATSxxxx.SCPI_error(self)[0],'0')
        self.ATSxxxx.close()

    def test_OTA_Query(self):
        self.ATSxxxx.query('*IDN?')

if __name__ == '__main__':
#coverage run -a -m unittest -b -v test_HW_OTA_Common
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=4).run(suite)
