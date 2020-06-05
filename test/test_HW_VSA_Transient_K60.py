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
host = '192.168.1.109'                              #Get local machine name

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.VSA.Transient_K60     import VSA              #pylint: disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #run before each test
        self.FSW = VSA().jav_OpenTest(host)
        self.FSW.Init_TranAna()

    def tearDown(self):                             #Run after each test
        self.assertEqual(self.FSW.jav_Error()[0],'0')
        self.FSW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_FSW_TransientAnalysis_Chirp_Get(self):
        self.FSW.Set_TA_Mode('CHIRP')
        self.FSW.Set_SweepCont(0)
        self.FSW.jav_Wait('INIT:IMM')
        self.FSW.Get_TA_ChirpTable()
        self.FSW.Get_TA_ChirpStat()
        self.FSW.Get_TA_ChirpStats_TimeBegin()
        self.FSW.Get_TA_ChirpStats_TimeLength()
        self.FSW.Get_TA_ChirpStats_Rate()
        self.FSW.Get_TA_ChirpStats_StateDev()
        self.FSW.Get_TA_ChirpStats_AvgFreq()
        self.FSW.Get_TA_ChirpStats_Bandwidth()
        self.FSW.Get_TA_ChirpStats_FreqDevAvg()

    def test_FSW_TransientAnalysis_Hop_Get(self):
        self.FSW.Set_TA_Mode('HOP')
        self.FSW.Set_SweepCont(0)
        self.FSW.jav_Wait('INIT:IMM')
        self.FSW.Get_TA_HopTable()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
