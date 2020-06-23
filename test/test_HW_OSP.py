###############################################################################
### Purpose: rssd.self.OSP.common.py driver test
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
from rssd.OSP.Common import OSP

class TestGeneral(unittest.TestCase):
    def setUp(self):                      #run before each test
        self.OSPxx0 = OSP().jav_OpenTest(host)

    def tearDown(self):                         #Run after each test
        self.assertEqual(self.OSPxx0.jav_Error()[0],'0')
        self.OSPxx0.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_OSP_Get(self):
        self.OSPxx0.Get_OSP_Info()
        self.OSPxx0.Get_OSP_Modules()

    def test_OSP_CompatibilityMode(self):
        self.OSPxx0.Set_CompatabilityMode(1)
        self.OSPxx0.Set_CompatabilityMode(0)

    def test_OSP_SP6T(self):
        setVal = 1
        self.OSPxx0.Set_SW(11, 1, setVal)
        getVal = self.OSPxx0.Get_SW_SP6T(11, 1)
        if self.OSPxx0.connected: self.assertEqual(setVal, getVal)
        setVal = 3
        self.OSPxx0.Set_SW(11, 1, setVal)
        getVal = self.OSPxx0.Get_SW_SP6T(11, 1)
        if self.OSPxx0.connected: self.assertEqual(setVal, getVal)

    def test_OSP_SPDT(self):
        setVal = 1
        self.OSPxx0.Set_SW(11, 1, setVal)
        getVal = self.OSPxx0.Get_SW_SPDT(11, 1)
        if self.OSPxx0.connected: self.assertEqual(setVal, getVal)
        setVal = 0
        self.OSPxx0.Set_SW(11, 1, setVal)
        getVal = self.OSPxx0.Get_SW_SPDT(11, 1)
        if self.OSPxx0.connected: self.assertEqual(setVal, getVal)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
#coverage run -a -m unittest -b -v test_HW_OSP_Common
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=4).run(suite)
