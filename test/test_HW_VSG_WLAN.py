###############################################################################
### Rohde & Schwarz Driver Test
### Purpose: SMW.WLAN_K54 test
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
host = '10.0.0.7'                                       #Get local machine name
host = '192.168.1.114'

###############################################################################
### Code Start
###############################################################################
import os
import unittest
from rssd.VSG.WLAN_K54  import VSG
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
    def test_SMW_WLAN_Get(self):
        nullVal = self.SMW.Get_WLAN_Standard()
        nullVal = self.SMW.Get_WLAN_ChBW()
        nullVal = self.SMW.Get_WLAN_PPDU()
        nullVal = self.SMW.Get_WLAN_MCS()
        nullVal = self.SMW.Get_WLAN_Modulation()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_WLAN_Set(self):
        # self.SMW.Set_Freq(self.Freq)
        self.SMW.Set_WLAN_BBState('OFF')
        self.SMW.Set_WLAN_ChBW(160)
        self.SMW.Set_WLAN_Standard('AC')
        self.SMW.Set_WLAN_MCS(1)
        self.SMW.Set_WLAN_Modulation('QPSK')
        # self.SMW.Set_WLAN_BBState('ON')
        # self.SMW.Set_RFState('ON')                      #Turn RF Output on
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_WLAN_Set_A(self):
        setVal = 'A'
        self.SMW.Set_WLAN_BBState('OFF')
        self.SMW.Set_WLAN_Standard(setVal)
        getVal = self.SMW.Get_WLAN_Standard()
        if self.connected: self.assertEqual(setVal,getVal)

    def test_SMW_WLAN_Set_B(self):
        setVal = 'B'
        self.SMW.Set_WLAN_BBState('OFF')
        self.SMW.Set_WLAN_Standard(setVal)
        getVal = self.SMW.Get_WLAN_Standard()
        if self.connected: self.assertEqual(setVal,getVal)

    # def test_SMW_WLAN_Set_G(self):
    #     setVal = 'G'
    #     self.SMW.Set_WLAN_BBState('OFF')
    #     self.SMW.Set_WLAN_Standard(setVal)
    #     getVal = self.SMW.Get_WLAN_Standard()
    #     self.assertEqual(setVal,getVal)

    def test_SMW_WLAN_Set_N(self):
        setVal = 'N'
        self.SMW.Set_WLAN_BBState('OFF')
        self.SMW.Set_WLAN_Standard(setVal)
        getVal = self.SMW.Get_WLAN_Standard()
        if self.connected: self.assertEqual(setVal,getVal)

    def test_SMW_WLAN_Set_AC(self):
        setVal = 'AC'
        self.SMW.Set_WLAN_BBState('OFF')
        self.SMW.Set_WLAN_Standard(setVal)
        getVal = self.SMW.Get_WLAN_Standard()
        if self.connected: self.assertEqual(setVal,getVal)

    def test_SMW_WLAN_Set_AX(self):
        setVal = 'AX'
        self.SMW.Set_WLAN_BBState('OFF')
        self.SMW.Set_WLAN_Standard(setVal)
        getVal = self.SMW.Get_WLAN_Standard()
        if self.connected: self.assertEqual(setVal,getVal)

    def test_SMW_WLAN_Set_Bad(self):
        """Test exception"""
        setVal = 'BAD'
        self.SMW.Set_WLAN_BBState('OFF')
        self.SMW.Set_WLAN_Standard(setVal)

    def test_SMW_WLAN_Set_BBON(self):
        self.SMW.Set_WLAN_ChBW(20)
        self.SMW.Set_WLAN_BBState('ON')

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
