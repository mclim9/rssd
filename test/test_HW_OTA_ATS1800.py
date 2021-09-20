"""rssd.self.OTA.common.py driver test"""

host = '192.168.1.50'                           #Get local machine name

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.OTA.ATS1800 import OTA

class TestGeneral(unittest.TestCase):
    def setUp(self):                            #run before each test
        self.ATS1800 = OTA().open(host, type='test')

    def tearDown(self):                         #Run after each test
        self.assertEqual(self.ATS1800.SCPI_error(self)[0],'0')
        self.ATS1800.close()

###############################################################################
### <Test>
###############################################################################
    def test_OTA_Init(self):
        self.ATS1800.Init_Measurement()

    def test_OTA_Azimuth(self):
        setVal = 10
        self.ATS1800.Set_AzimuthSpeed(setVal)
        getVal = self.ATS1800.Get_AzimuthSpeed()
        if self.ATS1800.connected : self.assertEqual(setVal, getVal)
        setVal = 10
        self.ATS1800.Set_AzimuthAngle(setVal)
        getVal = self.ATS1800.Get_AzimuthAngle()
        getVal = self.ATS1800.Get_AzimuthRunning()
        if self.ATS1800.connected : self.assertEqual(setVal, getVal)

    def test_OTA_Elevation(self):
        setVal = 10
        self.ATS1800.Set_ElevateSpeed(setVal)
        getVal = self.ATS1800.Get_ElevateSpeed()
        if self.ATS1800.connected : self.assertEqual(setVal, getVal)
        setVal = 10
        self.ATS1800.Set_ElevateAngle(setVal)
        getVal = self.ATS1800.Get_ElevateAngle()
        getVal = self.ATS1800.Get_ElevateRunning()
        if self.ATS1800.connected : self.assertEqual(setVal, getVal)

    def test_OTA_Stop(self):
        self.ATS1800.Set_AzimuthStop()
        self.ATS1800.Set_ElevateStop()

    def test_OTA_SystemStat(self):
        self.ATS1800.Get_SysStat()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
#coverage run -a -m unittest -b -v test_HW_OTA_Common
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=4).run(suite)
