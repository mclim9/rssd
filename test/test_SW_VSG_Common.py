###############################################################################
### Rohde & Schwarz Driver Test
### Purpose: self.SMW_Common test
### Author:  mclim
### Date:    2020.05.08
###              _   ___        __  _____         _   
###             | | | \ \      / / |_   _|__  ___| |_ 
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_ 
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '10.0.0.7'              #Get local machine name
# host = '169.254.2.20'

###############################################################################
### Code Start
###############################################################################
from rssd.VSG.Common    import VSG
from rssd.test.yaVISA   import jaVISA_mock
import os
import unittest

class TestGeneral(unittest.TestCase):
    # def __init__(self, *args, **kwargs):
    #     super(TestingClass, self).__init__(*args, **kwargs)

    def setUp(self):                      #run before each test
        self.SMW = VSG()
        mock = jaVISA_mock()
        self.SMW.jav_Open   = mock.jav_Open
        self.SMW.write      = mock.write
        self.SMW.query      = mock.query
        self.SMW.jav_Error  = mock.jav_Error
        self.SMW.debug = 0
        self.SMW.jav_Open(host)
        # self.SMW.K2.timeout = 5000
        # self.SMW.jav_Reset()
        self.SMW.jav_ClrErr()
        self.SMW.dLastErr = ""

    def tearDown(self):                         #Run after each test
        self.SMW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_SMW_ALC(self):
        setVal = 'ON'
        self.SMW.Set_ALC_RFDriveAmp(setVal)
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_Arb_Freq(self):
        setVal = 10e6
        self.SMW.Set_ArbClockFreq(setVal)
        getVal = self.SMW.Get_ArbClockFreq()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_Arb_State(self):
        setVal = 'test.wv'
        self.SMW.Set_ArbWv(setVal)
        self.SMW.Set_ArbState(1)
        self.SMW.Set_ArbState(0)
        getVal = self.SMW.Get_ArbName()
        nulVal = self.SMW.Get_ArbInfo()
        nulVal = self.SMW.Get_PowerInfo()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_BB_State(self):
        self.SMW.Set_BBState(1)
        self.SMW.Set_BBState(0)
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_Connect(self):
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_CrestFactor(self):
        getVal = self.SMW.Get_CrestFactor()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_Init_Wideband(self):
        self.SMW.Init_Wideband()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_IQMod(self):
        self.SMW.Set_IQMod(1)
        self.SMW.Set_IQMod(0)
        self.SMW.Set_IQMod('OFF')
        self.SMW.Set_IQMod('ON')
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_Freq(self):
        setVal = 2e6
        self.SMW.Set_Freq(setVal)
        getVal = self.SMW.Get_Freq()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_ListMode(self):
        self.SMW.Set_RFState(1)
        self.SMW.Set_ListMode_File('testListMode.lsw')
        self.SMW.Set_ListMode_File('testListMode')
        self.SMW.Set_ListMode('LIST')
        self.SMW.Set_ListMode_TrigSource('SING')
        self.SMW.Set_ListMode_Dwell(0.01)
        self.SMW.Set_ListMode_RMode('LIVE')
        # self.SMW.Set_ListMode_TrigExecute()
        # self.SMW.Set_ListMode_TrigWait()
        getVal = self.SMW.Get_ListMode_IndexCurr()
        getVal = self.SMW.Get_ListMode_IndexStop()
        self.SMW.Set_ListMode('CW')
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_ListMode_TrigSource(self):
        self.SMW.Set_ListMode_TrigSource('SING')
        self.SMW.Set_ListMode_TrigSource('AUTO')
        self.SMW.Set_ListMode_TrigSource('STEP')
        self.SMW.Set_ListMode_TrigSource('ESTEP')
        self.SMW.Set_ListMode_TrigSource('ESING')
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_PhaseDelta(self):
        setVal = -10
        self.SMW.Set_PhaseDelta(setVal)
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_Pwr(self):
        setVal = -10
        self.SMW.Set_RFPwr(setVal)
        getVal = self.SMW.Get_PowerRMS()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_SysConfigAll(self):
        getVal = self.SMW.Get_SysC_All()
        self.assertEqual(self.SMW.jav_Error()[0],'0')


###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
    # os.system('coverage run -m unittest -v test.test_HW_SMW_Common')
