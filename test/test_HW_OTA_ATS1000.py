"""rssd.self.OTA.common.py driver test"""
import unittest
from rssd.OTA.ATS1000 import OTA

host = '192.168.1.50'                           #Get local machine name

class TestGeneral(unittest.TestCase):
    def setUp(self):                            #run before each test
        self.ATS1000 = OTA().open(host, type='test')

    def tearDown(self):                         #Run after each test
        self.assertEqual(self.ATS1000.SCPI_error(self)[0],'0')
        self.ATS1000.close()

    def test_OTA_Init(self):
        self.ATS1000.Init_Measurement()

    def test_OTA_Azimuth(self):
        setVal = 10
        self.ATS1000.Set_AzimuthSpeed(setVal)
        getVal = self.ATS1000.Get_AzimuthSpeed()
        if self.ATS1000.connected : self.assertEqual(setVal, getVal)
        setVal = 10
        self.ATS1000.Set_AzimuthAngle(setVal)
        getVal = self.ATS1000.Get_AzimuthAngle()
        getVal = self.ATS1000.Get_AzimuthRunning()
        if self.ATS1000.connected : self.assertEqual(setVal, getVal)
        self.ATS1000.Set_AzimuthTrigger(5)

    def test_OTA_Elevation(self):
        setVal = 10
        self.ATS1000.Set_ElevateSpeed(setVal)
        getVal = self.ATS1000.Get_ElevateSpeed()
        if self.ATS1000.connected : self.assertEqual(setVal, getVal)
        setVal = 10
        self.ATS1000.Set_ElevateAngle(setVal)
        getVal = self.ATS1000.Get_ElevateAngle()
        getVal = self.ATS1000.Get_ElevateRunning()
        if self.ATS1000.connected : self.assertEqual(setVal, getVal)

    def test_OTA_Stop(self):
        self.ATS1000.Set_AzimuthStop()
        self.ATS1000.Set_ElevateStop()

    def test_OTA_SystemStat(self):
        self.ATS1000.Get_SysStat()
        self.ATS1000.Get_CxAngle()

if __name__ == '__main__':
#coverage run -a -m unittest -b -v test_HW_OTA_Common
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=4).run(suite)
