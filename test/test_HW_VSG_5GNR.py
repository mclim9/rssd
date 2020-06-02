###############################################################################
### Rohde & Schwarz Driver Test
### Purpose: VSG.NR5G_K144 test
###              _   ___        __  _____
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
from rssd.VSG.NR5G_K144 import VSG                      #pylint: disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                    #run before each test
        self.SMW = VSG().jav_OpenTest(host)

    def tearDown(self):                                 #Run after each test
        self.assertEqual(self.SMW.jav_Error()[0],'0')
        self.SMW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_SMW_5GNR_BWP_Sub(self):
        self.SMW.Get_5GNR_BWP_SubSpaceTotal()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_5GNR_Direction(self):
        self.SMW.Set_5GNR_Direction('UL')
        getVal = self.SMW.Get_5GNR_Direction()
        if self.SMW.connected: self.assertEqual(getVal,'UL')
        self.SMW.Set_5GNR_Direction('DL')
        getVal = self.SMW.Get_5GNR_Direction()
        if self.SMW.connected: self.assertEqual(getVal,'DL')

    def test_SMW_5GNR_FreqRange(self):
        self.SMW.Set_5GNR_FreqRange('LOW')
        getVal = self.SMW.Get_5GNR_FreqRange()
        if self.SMW.connected: self.assertEqual(getVal,'LOW')
        self.SMW.Set_5GNR_FreqRange('MIDD')
        getVal = self.SMW.Get_5GNR_FreqRange()
        if self.SMW.connected: self.assertEqual(getVal,'MIDD')
        self.SMW.Set_5GNR_FreqRange('HIGH')
        getVal = self.SMW.Get_5GNR_FreqRange()
        if self.SMW.connected: self.assertEqual(getVal,'HIGH')

    def test_SMW_5GNR_Get_DL(self):
        self.SMW.Set_5GNR_Direction('DL')
        self.SMW.Set_5GNR_BBState(0)
        nullVal = self.SMW.Get_5GNR_CC_Freq()
        nullVal = self.SMW.Get_5GNR_Direction()
        nullVal = self.SMW.Get_5GNR_FreqRange()
        nullVal = self.SMW.Get_5GNR_RefA()
        nullVal = self.SMW.Get_5GNR_ChannelBW()
        nullVal = self.SMW.Get_5GNR_TransPrecoding()
        nullVal = self.SMW.Get_5GNR_PhaseCompensate()
        nullVal = self.SMW.Get_5GNR_SSB_SubSpace()
        nullVal = self.SMW.Get_5GNR_BWP_SubSpace()
        nullVal = self.SMW.Get_5GNR_BWP_Count()
        nullVal = self.SMW.Get_5GNR_BWP_ResBlock()
        nullVal = self.SMW.Get_5GNR_BWP_ResBlockOffset()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_Modulation()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_ResBlock()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_ResBlockOffset()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_SymbNum()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_SymbOff()
        nullVal = self.SMW.Get_5GNR_BWP_Center()
        ### "=DMRS="
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_Config()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_Mapping()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_1stDMRSSym()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_AddPosition()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_MSymbLen()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_SeqGenMeth()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_SeqGenSeed()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_RelPwr()
        ### "=PTRS=")
        nullVal = self.SMW.Get_5GNR_BWP_Ch_PTRS_State()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_PTRS_L()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_PTRS_K()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_PTRS_Pow()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_PTRS_RE_Offset()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    # def test_SMW_5GNR_Get_RBMax(self):
    #     nullVal = self.SMW.Get_5GNR_RBMax()
    #     self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_5GNR_Get_TMCat(self):
        nullVal = self.SMW.Get_5GNR_TM_Cat()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_5GNR_Get_UL(self):
        self.SMW.Set_5GNR_Direction('UL')
        self.SMW.Set_5GNR_BBState(0)
        nullVal = self.SMW.Get_5GNR_CC_Freq()
        nullVal = self.SMW.Get_5GNR_Direction()
        nullVal = self.SMW.Get_5GNR_FreqRange()
        nullVal = self.SMW.Get_5GNR_RefA()
        nullVal = self.SMW.Get_5GNR_ChannelBW()
        nullVal = self.SMW.Get_5GNR_TransPrecoding()
        nullVal = self.SMW.Get_5GNR_PhaseCompensate()
        nullVal = self.SMW.Get_5GNR_SSB_SubSpace()
        ### "=User="
        nullVal = self.SMW.Get_5GNR_BWP_SubSpace()
        nullVal = self.SMW.Get_5GNR_BWP_Count()
        nullVal = self.SMW.Get_5GNR_BWP_ResBlock()
        nullVal = self.SMW.Get_5GNR_BWP_ResBlockOffset()
        ### "==Ch=="
        nullVal = self.SMW.Get_5GNR_BWP_Ch_Modulation()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_ResBlock()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_ResBlockOffset()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_SymbNum()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_SymbOff()
        nullVal = self.SMW.Get_5GNR_BWP_Center()
        ### "=DMRS="
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_Config()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_Mapping()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_1stDMRSSym()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_AddPosition()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_MSymbLen()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_SeqGenMeth()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_SeqGenSeed()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_DMRS_RelPwr()
        ### "=PTRS=")
        nullVal = self.SMW.Get_5GNR_BWP_Ch_PTRS_State()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_PTRS_L()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_PTRS_K()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_PTRS_Pow()
        nullVal = self.SMW.Get_5GNR_BWP_Ch_PTRS_RE_Offset()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_5GNR_Set_CC(self):
        self.SMW.Set_5GNR_CC_Num(2)
        self.SMW.Set_5GNR_CC_Offset(100e6)
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_5GNR_Set_DL(self):
        self.SMW.Set_5GNR_BBState('OFF')                     # Baseband OFF
        self.SMW.Set_5GNR_Direction('DL')
        self.SMW.Set_5GNR_CC_Num(1)
        self.SMW.Set_5GNR_TransPrecoding('OFF')
        self.SMW.Set_5GNR_PhaseCompensate('ON')
        self.SMW.Set_5GNR_PhaseCompensate_Freq(1e6)
        self.SMW.Set_5GNR_FreqRange('HIGH')
        self.SMW.Set_5GNR_ChannelBW(100)
        self.SMW.Set_5GNR_BWP_SubSpace(120)
        self.SMW.Set_5GNR_BWP_ResBlock(66)
        self.SMW.Set_5GNR_BWP_ResBlockOffset(0)
        self.SMW.Set_5GNR_BWP_Ch_ResBlock(66)
        self.SMW.Set_5GNR_BWP_Corset_ResBlock(66)
        #self.SMW.Set_5GNR_BWP_Ch_ResBlockOffset(NR_RBO)
        self.SMW.Set_5GNR_BWP_Ch_Modulation('QPSK')
        self.SMW.Set_5GNR_SSB()
        # self.SMW.Set_5GNR_BBState('ON')
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_5GNR_Set_SubSpace(self):
        self.SMW.Set_5GNR_FreqRange('LOW')
        self.SMW.Set_5GNR_ChannelBW(20)
        self.SMW.Set_5GNR_BWP_SubSpace(15)
        self.SMW.Set_5GNR_ChannelBW(100)
        self.SMW.Set_5GNR_FreqRange('MIDD')
        self.SMW.Set_5GNR_BWP_SubSpace(30)
        self.SMW.Set_5GNR_FreqRange('HIGH')
        self.SMW.Set_5GNR_BWP_SubSpace(60)
        self.SMW.Set_5GNR_BWP_SubSpace(120)
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_5GNR_Set_FRC_State(self):
        self.SMW.Set_5GNR_FRC_State('ON')
        self.SMW.Set_5GNR_FRC_State('OFF')
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_5GNR_Set_UL(self):
        self.SMW.Set_5GNR_BBState('OFF')                     # Baseband OFF
        self.SMW.Set_5GNR_Direction('UL')
        self.SMW.Set_5GNR_CC_Num(1)
        self.SMW.Set_5GNR_TransPrecoding('OFF')
        self.SMW.Set_5GNR_PhaseCompensate('OFF')
        self.SMW.Set_5GNR_FreqRange('HIGH')
        self.SMW.Set_5GNR_ChannelBW(100)
        self.SMW.Set_5GNR_BWP_SubSpace(120)
        self.SMW.Set_5GNR_BWP_ResBlock(66)
        self.SMW.Set_5GNR_BWP_ResBlockOffset(0)
        self.SMW.Set_5GNR_BWP_Ch_ResBlock(66)
        self.SMW.Set_5GNR_BWP_Corset_ResBlock(66)
        #self.SMW.Set_5GNR_BWP_Ch_ResBlockOffset(NR_RBO)
        self.SMW.Set_5GNR_BWP_Ch_Modulation('QPSK')
        self.SMW.Set_5GNR_SSB()
        # self.SMW.Set_5GNR_BBState('ON')
        self.assertEqual(self.SMW.jav_Error()[0],'0')

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
