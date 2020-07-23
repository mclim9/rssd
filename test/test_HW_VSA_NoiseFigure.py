# # -*- coding: future_fstrings -*-
###############################################################################
### Purpose: rssd.VSA.NoiseFigure_K30 test
###              _   ___        __  _____         _
###             | | | \ \      / / |_   _|__  ___| |_
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '192.168.1.1'                              #Get local machine name

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.VSA.NoiseFigure_K30     import VSA        #pylint: disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #run before each test
        self.FSW = VSA().jav_OpenTest(host)
        self.FSW.Init_Noise()

    def tearDown(self):                             #Run after each test
        self.assertEqual(self.FSW.jav_Error()[0],'0')
        self.FSW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_FSW_NoiseFigure_SingleFreq(self):
        ### Must be in FreqConfig-->Tuning Mode-->Single Freq prior to test
        # self.FSW.Set_NF_FreqSweepMOde('Single')
        self.FSW.Set_NF_Single_Freq(20e9)
        self.FSW.Set_NF_Single_Meas()
        self.FSW.Set_NF_Single_Coupled_To_List('ON')
        self.FSW.Set_NF_ENR_Cal_Type('RES')

    def test_FSW_NoiseFigure_Sweep(self):
        ### Must be in FreqConfig-->Tuning Mode-->Sweep prior to test
        ### ENR Settings
        # self.FSW.Set_NF_ENR_Cal_Type('DIOD')
        self.FSW.Set_NF_ENR_Meas_Type('DIOD')
        self.FSW.Set_NF_ENR_Meas_Mode('TABL')
        self.FSW.Set_NF_ENR_Temp(0)
        self.FSW.Set_NF_ENR_Table('DEFAULT')
        self.FSW.Set_NF_Cal_Type("AUTO")
        self.FSW.Config_NF_Cal('HOT')
        self.FSW.Set_NF_2ndCorr_State('OFF')
        # self.FSW.Set_NF_Cal_State('ON')
        # self.FSW.Set_NF_Sweep('SING')
        self.FSW.Set_NF_DUT_InLoss_Mode("SPOT")
        self.FSW.Set_NF_DUT_InLoss_TableName('DEFAULT')
        self.FSW.Set_NF_DUT_InLoss_Table('1MHz,10,2MHz,12')
        self.FSW.Set_NF_DUT_OutLoss_Mode('SPOT')
        self.FSW.Set_NF_DUT_OutLoss_TableName('DEFAULT')
        self.FSW.Set_NF_DUT_OutLoss_Table('1MHz,10,2MHz,12')

    def test_FSW_NF_Get_Default(self):
        nullVal = self.FSW.Get_NF_Gain()
        nullVal = self.FSW.Get_NoiseFigure()
        nullVal = self.FSW.Get_NoiseTemp()
        nullVal = self.FSW.Get_NF_PHot()
        nullVal = self.FSW.Get_NF_PCold()

    def test_FSW_NF_Get_Extra(self):
        nullVal = self.FSW.Get_NF_CalCold()
        nullVal = self.FSW.Get_NF_CalHot()
        self.FSW.Get_YFactor()

    def test_FSW_NF_States(self):
        self.FSW.Set_NF_2ndCorr_State(1)
        self.FSW.Set_NF_2ndCorr_State(0)
        self.FSW.Set_NF_Cal_State(1)
        self.FSW.Set_NF_Cal_State(0)
        self.FSW.Set_NF_Single_Coupled_To_List(1)
        self.FSW.Set_NF_Single_Coupled_To_List(0)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
