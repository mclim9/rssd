###############################################################################
### Purpose: rssd.self.OTA.common.py driver test
###              _   ___        __  _____         _   
###             | | | \ \      / / |_   _|__  ___| |_ 
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_ 
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '192.168.1.40'              #Get local machine name

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.OTA.Common import OTA

class TestGeneral(unittest.TestCase):
    def setUp(self):                      #run before each test
        self.ATSxxxx = OTA().jav_OpenTest(host)

    def tearDown(self):                         #Run after each test
        self.assertEqual(self.ATSxxxx.jav_Error()[0],'0')
        self.ATSxxxx.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_OTA_Query(self):
        self.ATSxxxx.query('*IDN?')


###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
#coverage run -a -m unittest -b -v test_HW_OTA_Common
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=4).run(suite)
