###############################################################################
### Rohde & Schwarz Driver Test
### Purpose: RCT.NR5G_KM601 test
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
host = '192.168.1.160'              #Get local machine name

###############################################################################
### Code Start
###############################################################################
from rssd.RCT.NR5G_KM601 import RCT
import os
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                      #run before each test
        self.CMP = RCT()
        self.CMP.debug = 0
        self.CMP.jav_Open(host)
        self.CMP.jav_ClrErr()
        self.CMP.Init_5GNR()
        self.CMP.dLastErr = ""

    def tearDown(self):                         #Run after each test
        self.CMP.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_CMP_5GNR_ChBW(self):
        self.CMP.Set_5GNR_ChannelBW(200)
        getVal = self.CMP.Get_5GNR_ChannelBW()
        self.assertEqual(self.CMP.jav_Error()[0],'0')

    def test_CMP_5GNR_Direction(self):
        self.CMP.Set_5GNR_Direction('UL')
        getVal = self.CMP.Get_5GNR_Direction()
        self.assertEqual(getVal,'UL')
        self.assertEqual(self.CMP.jav_Error()[0],'0')

    def test_CMP_5GNR_FreqRange(self):
        self.CMP.Set_5GNR_Direction('UL')
        self.CMP.Set_5GNR_FreqRange('HIGH')
        getVal = self.CMP.Get_5GNR_FreqRange()
        self.assertEqual(getVal,'HIGH')

    def test_CMP_5GNR_PhaseComp(self):
        self.CMP.Set_5GNR_PhaseCompensate('ON')
        getVal = self.CMP.Get_5GNR_PhaseCompensate()
        self.CMP.Set_5GNR_PhaseCompensate_Freq(39e9)
        getVal = self.CMP.Get_5GNR_PhaseCompensate()
        getVal = self.CMP.Get_5GNR_PhaseCompensate_Freq()
        self.assertEqual(self.CMP.jav_Error()[0],'0')

    def test_CMP_5GNR_TransPrecoding(self):
        self.CMP.Set_5GNR_TransPrecoding('ON')
        getVal = self.CMP.Get_5GNR_TransPrecoding()
        self.CMP.Set_5GNR_TransPrecoding('OFF')
        getVal = self.CMP.Get_5GNR_TransPrecoding()
        self.assertEqual(self.CMP.jav_Error()[0],'0')

    def test_CMP_5GNR_Get_UL(self):
        self.CMP.Set_5GNR_Direction('UL')
        # nullVal = self.CMP.Get_5GNR_CC_Freq()
        nullVal = self.CMP.Get_5GNR_Direction()
        nullVal = self.CMP.Get_5GNR_FreqRange()
        nullVal = self.CMP.Get_5GNR_RefA()
        nullVal = self.CMP.Get_5GNR_ChannelBW()
        nullVal = self.CMP.Get_5GNR_TransPrecoding()
        nullVal = self.CMP.Get_5GNR_PhaseCompensate()
        nullVal = self.CMP.Get_5GNR_CellID()
        ### "=User="
        nullVal = self.CMP.Get_5GNR_BWP_SubSpace()
        nullVal = self.CMP.Get_5GNR_BWP_Count()
        nullVal = self.CMP.Get_5GNR_BWP_ResBlock()
        nullVal = self.CMP.Get_5GNR_BWP_ResBlockOffset()
        ### "==Ch=="
        nullVal = self.CMP.Get_5GNR_BWP_Ch_Modulation()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_ResBlock()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_ResBlockOffset()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_SymbNum()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_SymbOff()
        nullVal = self.CMP.Get_5GNR_BWP_Center()
        ### "=DMRS="
        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_Mapping()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_1stDMRSSym()

        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_Config()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_AddPosition()

        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_MSymbLen()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_CDMGroup()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_Antenna()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_RelPwr()
        
        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_SeqGenMeth()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_SeqGenSeed()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_SeqGen_n_SCID()
        ### "=PTRS="
        nullVal = self.CMP.Get_5GNR_BWP_Ch_PTRS_State()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_PTRS_L()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_PTRS_K()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_PTRS_Pow()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_PTRS_RE_Offset()
        self.assertEqual(self.CMP.jav_Error()[0],'0')

    # def test_CMP_5GNR_Set_UL(self):
    #     self.CMP.Set_5GNR_Direction('UL')
    #     self.CMP.Set_5GNR_CC_Num(1)
    #     self.CMP.Set_5GNR_TransPrecoding('OFF')
    #     self.CMP.Set_5GNR_PhaseCompensate('OFF')
    #     self.CMP.Set_5GNR_FreqRange('HIGH')
    #     self.CMP.Set_5GNR_ChannelBW(100)
    #     self.CMP.Set_5GNR_BWP_SubSpace(120)
    #     self.CMP.Set_5GNR_BWP_ResBlock(66)
    #     self.CMP.Set_5GNR_BWP_ResBlockOffset(0)
    #     self.CMP.Set_5GNR_BWP_Ch_ResBlock(66)
    #     self.CMP.Set_5GNR_BWP_Corset_ResBlock(66)
    #     #self.CMP.Set_5GNR_BWP_Ch_ResBlockOffset(NR_RBO)
    #     self.CMP.Set_5GNR_BWP_Ch_Modulation('QPSK')
    #     # self.CMP.Set_5GNR_SSB()
    #     self.assertEqual(self.CMP.jav_Error()[0],'0')

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
