###############################################################################
### Purpose: rssd.RCT.NR5G_KM601 test
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
import unittest
from rssd.RCT.NR5G_KM601    import RCT

class TestGeneral(unittest.TestCase):
    def setUp(self):                      #run before each test
        self.CMP = RCT().jav_OpenTest(host)
        self.CMP.Init_5GNR()
    def tearDown(self):                         #Run after each test
        self.assertEqual(self.CMP.jav_Error()[0],'0')
        self.CMP.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_CMP_5GNR_ChBW(self):
        self.CMP.Set_5GNR_ChannelBW(200)
        getVal = self.CMP.Get_5GNR_ChannelBW()

    def test_CMP_5GNR_Direction(self):
        self.CMP.Set_5GNR_Direction('UL')
        getVal = self.CMP.Get_5GNR_Direction()
        if self.CMP.connected: self.assertEqual(getVal,'UL')

    def test_CMP_5GNR_FreqRange(self):
        self.CMP.Set_5GNR_Direction('UL')
        self.CMP.Set_5GNR_FreqRange('HIGH')
        getVal = self.CMP.Get_5GNR_FreqRange()
        if self.CMP.connected: self.assertEqual(getVal,'HIGH')

    def test_CMP_5GNR_Get(self):
        self.CMP.Get_AmpSettings()
        self.CMP.Get_5GNR_CC_Offset()
        self.CMP.Get_5GNR_Params(1,1,0)

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
        self.CMP.Get_5GNR_BWP_ResBlock()
        self.CMP.Get_5GNR_BWP_ResBlockOffset()
        ### "==Ch=="
        self.CMP.Get_5GNR_BWP_Ch_Modulation()
        self.CMP.Get_5GNR_BWP_Ch_ResBlock()
        self.CMP.Get_5GNR_BWP_Ch_ResBlockOffset()
        self.CMP.Get_5GNR_BWP_Ch_SymbNum()
        self.CMP.Get_5GNR_BWP_Ch_SymbOff()
        nullVal = self.CMP.Get_5GNR_BWP_Center()
        ### "=DMRS="
        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_Mapping()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_1stDMRSSym()

        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_Config()
        self.CMP.Get_5GNR_BWP_Ch_DMRS_AddPosition()

        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_MSymbLen()
        self.CMP.Get_5GNR_BWP_Ch_DMRS_CDMGroup()
        self.CMP.Get_5GNR_BWP_Ch_DMRS_Antenna()
        self.CMP.Get_5GNR_BWP_Ch_DMRS_RelPwr()
        
        nullVal = self.CMP.Get_5GNR_BWP_Ch_DMRS_SeqGenMeth()
        self.CMP.Get_5GNR_BWP_Ch_DMRS_SeqGenSeed()
        self.CMP.Get_5GNR_BWP_Ch_DMRS_SeqGen_n_SCID()

        ### "=PTRS="
        nullVal = self.CMP.Get_5GNR_BWP_Ch_PTRS_State()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_PTRS_L()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_PTRS_K()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_PTRS_Pow()
        nullVal = self.CMP.Get_5GNR_BWP_Ch_PTRS_RE_Offset()

    def test_CMP_5GNR_Set_DL(self):
        self.CMP.Set_5GNR_Direction('DL')
        self.CMP.Get_5GNR_Direction()
        self.CMP.Get_5GNR_SSB_SubSpace()
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

    def test_CMP_5GNR_PhaseComp(self):
        self.CMP.Set_5GNR_PhaseCompensate('ON')
        getVal = self.CMP.Get_5GNR_PhaseCompensate()
        self.CMP.Set_5GNR_PhaseCompensate_Freq(39e9)
        getVal = self.CMP.Get_5GNR_PhaseCompensate()
        getVal = self.CMP.Get_5GNR_PhaseCompensate_Freq()

    def test_CMP_5GNR_TransPrecoding(self):
        self.CMP.Set_5GNR_TransPrecoding('ON')
        getVal = self.CMP.Get_5GNR_TransPrecoding()
        self.CMP.Set_5GNR_TransPrecoding('OFF')
        getVal = self.CMP.Get_5GNR_TransPrecoding()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
