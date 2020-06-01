###############################################################################
### Purpose: rssd.VSG.Common test
###              _   ___        __  _____         _
###             | | | \ \      / / |_   _|__  ___| |_
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '10.0.0.7'                                       #Get local machine name
host = '192.168.1.114'

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.VSG.Common    import VSG
from rssd.test.yaVISA   import jaVISA_mock              #pylint: disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                    #run before each test
        print("",end="")
        self.SMW = VSG()
        self.SMW.debug      = 0
        self.SMW.jav_Open(host)
        self.connected      = 1
        if self.SMW.K2 == 'NoVISA':
            mock = jaVISA_mock()
            self.SMW.jav_Open   = mock.jav_Open
            self.SMW.write      = mock.write
            self.SMW.query      = mock.query
            self.SMW.jav_Error  = mock.jav_Error
            self.connected      = 0
        self.SMW.jav_ClrErr()
        self.SMW.dLastErr = ""

    def tearDown(self):                                 #Run after each test
        self.assertEqual(self.SMW.jav_Error()[0],'0')
        self.SMW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_SMW_ALC(self):
        setVal = 'ON'
        self.SMW.Set_ALC_RFDriveAmp(setVal)

    def test_SMW_Arb_Freq(self):
        setVal = 10e6
        self.SMW.Set_ArbClockFreq(setVal)
        getVal = self.SMW.Get_ArbClockFreq()
        if self.connected: self.assertEqual(setVal,getVal)

    # def test_SMW_Arb_State(self):
    #     setVal = '/var/user/UCS2010/GSM.wv'
    #     self.SMW.Set_ArbWv(setVal)
    #     self.SMW.Set_ArbState(1)
    #     self.SMW.Set_ArbState(0)
    #     getVal = self.SMW.Get_ArbName()
    #     nulVal = self.SMW.Get_ArbInfo()
    #     nulVal = self.SMW.Get_PowerInfo()
    #     if self.connected: self.assertTrue(getVal.find(setVal) > -1)

    def test_SMW_BB_State(self):
        self.SMW.Set_BBState(1)
        self.SMW.Set_BBState(0)

    def test_SMW_Connect(self):
        if self.connected: self.assertEqual(self.SMW.Make,"Rohde&Schwarz")

    def test_SMW_CrestFactor(self):
        getVal = self.SMW.Get_CrestFactor()

    def test_SMW_OS(self):
        self.SMW.Set_OS_Dir('UCS2010')
        getVal = self.SMW.Get_OS_Dir()
        getVal = self.SMW.Get_OS_FileList()

    def test_SMW_Init_Wideband(self):
        self.SMW.Init_Wideband()

    def test_SMW_IQMod(self):
        self.SMW.Set_IQMod(1)
        self.SMW.Set_IQMod(0)
        self.SMW.Set_IQMod('OFF')
        self.SMW.Set_IQMod('ON')

    def test_SMW_Freq(self):
        setVal = 2e6
        self.SMW.Set_Freq(setVal)
        getVal = self.SMW.Get_Freq()
        if self.connected: self.assertEqual(setVal,getVal)

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

    def test_SMW_ListMode_TrigSource(self):
        self.SMW.Set_ListMode_TrigSource('SING')
        self.SMW.Set_ListMode_TrigSource('AUTO')
        self.SMW.Set_ListMode_TrigSource('STEP')
        self.SMW.Set_ListMode_TrigSource('ESTEP')
        self.SMW.Set_ListMode_TrigSource('ESING')

    def test_SMW_PhaseDelta(self):
        setVal = -10
        self.SMW.Set_PhaseDelta(setVal)

    def test_SMW_Pwr(self):
        setVal = -10
        self.SMW.Set_RFPwr(setVal)
        getVal = self.SMW.Get_PowerRMS()
        self.assertEqual(self.SMW.jav_Error()[0],'0')
        if self.connected: self.assertEqual(setVal,getVal)

    def test_SMW_SysConfigAll(self):
        getVal = self.SMW.Get_SysC_All()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
