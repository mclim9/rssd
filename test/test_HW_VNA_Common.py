# # -*- coding: future_fstrings -*-
###############################################################################
### Purpose: rssd.VSA.ADemod_K7 test
###              _   ___        __  _____         _
###             | | | \ \      / / |_   _|__  ___| |_
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '10.0.0.13'                              #Get local machine name

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.VNA.Common        import VNA              #pylint: disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #run before each test
        self.VNA = VNA().jav_OpenTest(host)

    def tearDown(self):                             #Run after each test
        self.assertEqual(self.VNA.jav_Error()[0],'0')
        self.VNA.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_VNA_Markers(self):
        self.VNA.Set_Mkr_Coupled(1)
        self.VNA.Set_Mkr_Frq(2.4e9,1)
        self.VNA.Set_Mkr_Frq(2.5e9,2)

    def test_VNA_PowerCal_Tx(self):
        self.VNA.Set_FreqStart(1e9)
        self.VNA.Set_FreqStop(6e9)
        self.VNA.Set_SweepPoints(601)
        self.VNA.Set_Pwrcal_Init()
        self.VNA.Set_Pwrcal_Tolerance(0.1)
        self.VNA.Set_Pwrcal_NumReading(10)
        # self.VNA.Set_Pwrcal_Rx(1,2)
        self.VNA.Set_Pwrcal_Measure(2)                      #Initiate Power cal
        getVal = self.VNA.Get_Pwrcal_State()                #Pwr Cal Tx State
        getVal = self.VNA.Get_Pwrcal_Rx_State()             #Pwr Cal Rx State

    def test_VNA_PowerSweep(self):
        self.VNA.Set_PowerStart(-60)
        self.VNA.Set_PowerStop(-10)

    def test_VNA_SParam(self):
        self.VNA.Set_SweepCont(0)
        self.VNA.Set_Trace_MeasAdd_SParam(1,1)              #S11 Measurement
        self.VNA.Set_Trace_MeasAdd_SParam(2,1)              #S21 Measurement
        self.VNA.Set_FreqStart(100e6)
        self.VNA.Set_FreqStop(200e6)
        self.VNA.Set_SweepPoints(1001)
        self.VNA.Set_IFBW(1000)
        self.VNA.Set_InitImm()
        self.VNA.Get_Trace_Names()

    def test_VNA_SaveData(self):
        self.VNA.Save_Cal("TestCalFile")
        self.VNA.Save_Screen('TestPicture')
        self.VNA.Save_State('TestState')
        self.VNA.Save_Trace_CSV('TestTraceCSV')
        self.VNA.Save_Trace_SxP('TestTraceSxP')

    def test_VNA_Sweep(self):
        self.VNA.Set_SweepCont(1)
        self.VNA.Set_SweepTime(1000)
        self.VNA.Set_SweepTime(0)
        self.VNA.Set_Trace_AvgCount(10)
        self.VNA.Set_Trace_Avg('ON')

    def test_VNA_TraceChanges(self):
        self.VNA.Set_Trace_MeasAdd_BWave(1,2)
        self.VNA.Set_Trace_MeasAdd_PwrMtr(1)
        self.VNA.Set_Trace_MeasAdd_SParam(2,1)
        self.VNA.Set_Trace_Select('S21')
        self.VNA.Set_Trace_MeasDel('S21')
        self.VNA.Set_Trace_DelAll()
        self.VNA.Set_Trace_MeasAdd_AWave(1,2)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
#coverage run -a -m unittest -b -v test_HW_VNA_Common
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
