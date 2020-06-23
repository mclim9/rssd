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
host = '192.168.1.50'                           #Get local machine name

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.OTA.ATS1000 import OTA

class TestGeneral(unittest.TestCase):
    def setUp(self):                            #run before each test
        self.ATS1000 = OTA().jav_OpenTest(host)

    def tearDown(self):                         #Run after each test
        self.assertEqual(self.ATS1000.jav_Error()[0],'0')
        self.ATS1000.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_OTA_Init(self):
        self.ATS1000.Init_Measurement()

    def test_OTA_Azimuth(self):
        setVal = 10
        self.ATS1000.Set_AzimuthSpeed(setVal)
        getVal = self.ATS1000.Get_AzimuthSpeed()
        if self.ATS1000.connected : self.assertEqual(setVal, getVal)
        setVal = 10
        # self.ATS1000.Set_AzimuthAngle(setVal)
        # getVal = self.ATS1000.Get_AzimuthAngle()
        if self.ATS1000.connected : self.assertEqual(setVal, getVal)

    def test_OTA_Elevation(self):
        setVal = 10
        self.ATS1000.Set_ElevateSpeed(setVal)
        getVal = self.ATS1000.Get_ElevateSpeed()
        if self.ATS1000.connected : self.assertEqual(setVal, getVal)
        setVal = 10
        self.ATS1000.Set_ElevateAngle(setVal)
        getVal = self.ATS1000.Get_ElevateAngle()
        if self.ATS1000.connected : self.assertEqual(setVal, getVal)

    def test_OTA_SystemStat(self):
        self.ATS1000.Get_SysStat()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
#coverage run -a -m unittest -b -v test_HW_OTA_Common
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=4).run(suite)
