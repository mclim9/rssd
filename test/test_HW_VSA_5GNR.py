###############################################################################
### Rohde & Schwarz Driver Test
### Purpose: self.VSA.NR5G_K144 test
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
host = '192.168.1.109'              #Get local machine name

###############################################################################
### Code Start
###############################################################################
from rssd.VSA.NR5G_K144 import VSA
import os
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                      #run before each test
        self.FSW = VSA()
        self.FSW.debug = 0
        self.FSW.jav_Open(host)
        self.FSW.K2.timeout = 5000
        # self.FSW.jav_Reset()
        self.FSW.jav_ClrErr()
        self.FSW.Init_5GNR()
        self.FSW.dLastErr = ""

    def tearDown(self):                         #Run after each test
        self.FSW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_FSW_5GNR_Direction(self):
        self.FSW.Set_5GNR_Direction('UL')
        getVal = self.FSW.Get_5GNR_Direction()
        self.assertEqual(getVal,'UL')
        self.FSW.Set_5GNR_Direction('DL')
        getVal = self.FSW.Get_5GNR_Direction()
        self.assertEqual(getVal,'DL')

    def test_FSW_5GNR_FreqRange(self):
        self.FSW.Set_5GNR_Direction('UL')
        self.FSW.Set_5GNR_FreqRange('LOW')
        getVal = self.FSW.Get_5GNR_FreqRange()
        self.assertEqual(getVal,'LOW')
        self.FSW.Set_5GNR_FreqRange('MIDD')
        getVal = self.FSW.Get_5GNR_FreqRange()
        self.assertEqual(getVal,'MIDD')
        self.FSW.Set_5GNR_FreqRange('HIGH')
        getVal = self.FSW.Get_5GNR_FreqRange()
        self.assertEqual(getVal,'HIGH')

    def test_FSW_5GNR_Get_DL(self):
        self.FSW.Set_5GNR_Direction('DL')
        nullVal = self.FSW.Get_5GNR_CC_Freq()
        nullVal = self.FSW.Get_5GNR_Direction()
        nullVal = self.FSW.Get_5GNR_FreqRange()
        nullVal = self.FSW.Get_5GNR_RefA()
        nullVal = self.FSW.Get_5GNR_ChannelBW()
        nullVal = self.FSW.Get_5GNR_TransPrecoding()
        nullVal = self.FSW.Get_5GNR_PhaseCompensate()
        nullVal = self.FSW.Get_5GNR_SSB_SubSpace()
        nullVal = self.FSW.Get_5GNR_BWP_SubSpace()
        nullVal = self.FSW.Get_5GNR_BWP_Count()
        nullVal = self.FSW.Get_5GNR_BWP_ResBlock()
        nullVal = self.FSW.Get_5GNR_BWP_ResBlockOffset()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_Modulation()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_ResBlock()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_ResBlockOffset()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_SymbNum()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_SymbOff()
        nullVal = self.FSW.Get_5GNR_BWP_Center()
        ### "=DMRS="
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_Config()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_Mapping()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_1stDMRSSym()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_AddPosition()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_MSymbLen()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_SeqGenMeth()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_SeqGenSeed()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_RelPwr()
        ### "=PTRS=")
        nullVal = self.FSW.Get_5GNR_BWP_Ch_PTRS_State()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_PTRS_L()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_PTRS_K()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_PTRS_Pow()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_PTRS_RE_Offset()
        self.assertEqual(self.FSW.jav_Error()[0],'0')

    def test_FSW_5GNR_Get_UL(self):
        self.FSW.Set_5GNR_Direction('UL')
        nullVal = self.FSW.Get_5GNR_CC_Freq()
        nullVal = self.FSW.Get_5GNR_Direction()
        nullVal = self.FSW.Get_5GNR_FreqRange()
        nullVal = self.FSW.Get_5GNR_RefA()
        nullVal = self.FSW.Get_5GNR_ChannelBW()
        nullVal = self.FSW.Get_5GNR_TransPrecoding()
        nullVal = self.FSW.Get_5GNR_PhaseCompensate()
        nullVal = self.FSW.Get_5GNR_SSB_SubSpace()
        ### "=User="
        nullVal = self.FSW.Get_5GNR_BWP_SubSpace()
        nullVal = self.FSW.Get_5GNR_BWP_Count()
        nullVal = self.FSW.Get_5GNR_BWP_ResBlock()
        nullVal = self.FSW.Get_5GNR_BWP_ResBlockOffset()
        ### "==Ch=="
        nullVal = self.FSW.Get_5GNR_BWP_Ch_Modulation()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_ResBlock()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_ResBlockOffset()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_SymbNum()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_SymbOff()
        nullVal = self.FSW.Get_5GNR_BWP_Center()
        ### "=DMRS="
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_Config()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_Mapping()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_1stDMRSSym()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_AddPosition()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_MSymbLen()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_SeqGenMeth()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_SeqGenSeed()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_DMRS_RelPwr()
        ### "=PTRS=")
        nullVal = self.FSW.Get_5GNR_BWP_Ch_PTRS_State()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_PTRS_L()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_PTRS_K()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_PTRS_Pow()
        nullVal = self.FSW.Get_5GNR_BWP_Ch_PTRS_RE_Offset()
        self.assertEqual(self.FSW.jav_Error()[0],'0')

    def test_FSW_5GNR_Set_DL(self):
        self.FSW.Set_5GNR_Direction('DL')
        self.FSW.Set_5GNR_CC_Num(1)
        self.FSW.Set_5GNR_TransPrecoding('OFF')
        self.FSW.Set_5GNR_PhaseCompensate('ON')
        self.FSW.Set_5GNR_PhaseCompensate_Freq(1e6)
        self.FSW.Set_5GNR_FreqRange('HIGH')
        self.FSW.Set_5GNR_ChannelBW(100)
        self.FSW.Set_5GNR_BWP_SubSpace(120)
        self.FSW.Set_5GNR_BWP_ResBlock(66)
        self.FSW.Set_5GNR_BWP_ResBlockOffset(0)
        self.FSW.Set_5GNR_BWP_Ch_ResBlock(66)
        self.FSW.Set_5GNR_BWP_Corset_ResBlock(66)
        #self.FSW.Set_5GNR_BWP_Ch_ResBlockOffset(NR_RBO)
        self.FSW.Set_5GNR_BWP_Ch_Modulation('QPSK')
        # self.FSW.Set_5GNR_SSB()
        self.assertEqual(self.FSW.jav_Error()[0],'0')

    def test_FSW_5GNR_Set_UL(self):
        self.FSW.Set_5GNR_Direction('UL')
        self.FSW.Set_5GNR_CC_Num(1)
        self.FSW.Set_5GNR_TransPrecoding('OFF')
        self.FSW.Set_5GNR_PhaseCompensate('OFF')
        self.FSW.Set_5GNR_FreqRange('HIGH')
        self.FSW.Set_5GNR_ChannelBW(100)
        self.FSW.Set_5GNR_BWP_SubSpace(120)
        self.FSW.Set_5GNR_BWP_ResBlock(66)
        self.FSW.Set_5GNR_BWP_ResBlockOffset(0)
        self.FSW.Set_5GNR_BWP_Ch_ResBlock(66)
        self.FSW.Set_5GNR_BWP_Corset_ResBlock(66)
        #self.FSW.Set_5GNR_BWP_Ch_ResBlockOffset(NR_RBO)
        self.FSW.Set_5GNR_BWP_Ch_Modulation('QPSK')
        # self.FSW.Set_5GNR_SSB()
        self.assertEqual(self.FSW.jav_Error()[0],'0')

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
