###############################################################################
### Purpose: rssd.self.NRP.common.py driver test
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
#host = 'NRP8-101507.local'                #Get local machine name

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.NRP.Common import PMr

class TestGeneral(unittest.TestCase):
    def setUp(self):                      #run before each test
        self.NRP8 = PMr().jav_OpenTest(host)

    def tearDown(self):                         #Run after each test
        self.assertEqual(self.NRP8.jav_Error()[0],'0')
        self.NRP8.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_NRP_Gets(self):
        self.NRP8.Get_BufferedMeas('ON')
        self.NRP8.Get_BufferedMeas('OFF')
        self.NRP8.Get_EventStatus()
        self.NRP8.Get_Offset()

    def test_NRP_List(self):
        self.NRP8.Get_AvailableNRP()

    def test_NRP_Freq(self):
        SetVal = 1e9
        self.NRP8.Set_Freq(SetVal)
        GetVal = self.NRP8.Get_Freq()
        if self.NRP8.connected: self.assertEqual(SetVal,int(GetVal))

    def test_NRP_Trigger(self):
        self.NRP8.Set_TriggerAuto(0)
        self.NRP8.Set_TriggerCount(10)
        self.NRP8.Set_TriggerSource('BUS')
        self.NRP8.Set_TriggerAuto(1)

    def test_NRP_Power(self):
        self.NRP8.Set_Freq(6e9)                              # Set Frequency
        self.NRP8.Set_AverageMode(1)                         # Auto Averaging ON
        self.NRP8.Set_Average(10)                            # Avg Count = 4
        self.NRP8.Set_PowerOffset(5)
        self.NRP8.Set_PowerOffsetState(1)
        self.NRP8.Set_InitImm()
        self.NRP8.Set_AverageMode(0)                         # Auto Averaging OFF
        self.NRP8.Set_PowerOffsetState(0)
        GetVal = self.NRP8.Get_Average()
        GetVal = self.NRP8.Get_Power()

    def test_NRPM_Power(self):
        self.NRP8.Set_Freq(6e9)                              # Set Frequency
        self.NRP8.Set_AverageMode(1)                         # Auto Averaging OFF
        self.NRP8.Set_Average(10)                            # Avg Count = 4
        self.NRP8.Set_PowerOffset(5)
        self.NRP8.Set_PowerOffsetState(1)
        self.NRP8.Set_InitImm()
        self.NRP8.Set_NRPM_LED(1)
        self.NRP8.Set_NRPM_LED(0)
        GetVal = self.NRP8.Get_NRPM_PowerAll()



###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
#coverage run -a -m unittest -b -v test_HW_NRP_Common
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=4).run(suite)
