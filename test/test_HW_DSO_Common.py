"""rssd.DSO.common.py driver test"""
###############################################################################
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
from rssd.DSO.Common import DSO

class TestGeneral(unittest.TestCase):
    def setUp(self):                            # run before each test
        self.DSO = DSO().jav_OpenTest(host)

    def tearDown(self):                         # Run after each test
        self.assertEqual(self.DSO.jav_Error()[0],'0')
        self.DSO.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_RTx_Gets(self):
        self.DSO.Get_AcqTime()
        self.DSO.Get_ChState()
        self.DSO.Get_SamplingRate()
        self.DSO.Get_TimeRes()
        self.DSO.Get_TimeScale()
        self.DSO.Get_Trace(1, 1)

    def test_RTx_Cursor_Get(self):
        self.DSO.Get_Cursor_X_Delta()
        self.DSO.Get_Cursor_X_Delta_Inverse()
        self.DSO.Get_Cursor_Y_Delta()
        self.DSO.Get_Cursor_Y_Delta_Slope()

    def test_RTx_Cursor_Set(self):
        self.DSO.Set_Cursor_All_Off()
        self.DSO.Set_Cursor_Function('HOR')
        self.DSO.Set_Cursor_Max_Peak()
        self.DSO.Set_Cursor_Source(1)
        self.DSO.Set_Cursor_State('ON')
        self.DSO.Set_Cursor_Style('LIN')
        self.DSO.Set_Cursor_Tracking('ON')

    def test_RTx_Meas_Res(self):
        self.DSO.Get_Meas_Res_Actual(1)
        self.DSO.Get_Meas_Res_Average(1)
        self.DSO.Get_Meas_Res_Event_Count(1)
        self.DSO.Get_Meas_Res_Negetive_Peak(1)
        self.DSO.Get_Meas_Res_Positive_Peak(1)
        self.DSO.Get_Meas_Res_Reliability(1)
        self.DSO.Get_Meas_Res_RMS(1)
        self.DSO.Get_Meas_Res_Std_Dev(1)
        self.DSO.Get_Meas_Res_Wave_Count(1)
    
    def test_RTx_Meas_Set(self):
        self.DSO.Set_Meas_Additional('HIGH', 'ON')
        self.DSO.Set_Meas_All_Off()
        self.DSO.Set_Meas_All_On()
        self.DSO.Set_Meas_Clear_Statistics()
        self.DSO.Set_Meas_Main('HIGH')
        self.DSO.Set_Meas_Enable('ON')
        self.DSO.Set_Meas_Source('C1W2')
        self.DSO.Set_Meas_Statistics('ON')

    def test_RTx_Set(self):
        self.DSO.Init_Measurement()
        self.DSO.Set_Autoset()
        self.DSO.Set_ChCoupling('AC')
        self.DSO.Set_ChStatus('ON')
        self.DSO.Set_ChState('ON')
        self.DSO.Set_DisplayUpdate('ON')
        self.DSO.Set_SweepCont('ON')
        self.DSO.Set_SweepCont('OFF')
        self.DSO.Set_System_Preset()

    def test_RTx_Set_Time(self):
        sec = 0.001
        self.DSO.Set_AcqTime(5)
        self.DSO.Set_TimeRef(sec)
        self.DSO.Set_TimeScale(sec)
        self.DSO.Set_TimeRes(sec)

    def test_RTx_Set_Volt(self):
        volt = 0.01
        self.DSO.Set_VoltOffset(volt)
        self.DSO.Set_VoltRange(volt)
        self.DSO.Set_VoltScale(volt)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
#coverage run -a -m unittest -b -v test_HW_NRP_Common
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=4).run(suite)
