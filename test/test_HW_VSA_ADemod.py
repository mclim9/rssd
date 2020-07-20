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
from rssd.VSA.ADemod_K7     import VSA              #pylint: disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #run before each test
        self.FSW = VSA().jav_OpenTest(host)
        self.FSW.Init_ADemod()

    def tearDown(self):                             #Run after each test
        self.assertEqual(self.FSW.jav_Error()[0],'0')
        self.FSW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_FSW_ADemod(self):
        self.FSW.Set_Adem_dbw(3e6)
        self.FSW.Set_Adem_LPassStat('OFF')
        self.FSW.Set_Adem_LPassStat('ON')
        self.FSW.Set_Adem_LPassAbsolute('3kHz')
        self.FSW.Set_Adem_LPassManual(1e6)
        self.FSW.Set_Adem_LPassRelative('5PCT')
        getVal = self.FSW.Get_Adem_dbw()
        if self.FSW.connected: self.assertEqual(getVal, 3e6)

    def test_FSW_ADemod_PM(self):
        self.FSW.Set_Freq(28e9)                          # RF Freq
        self.FSW.Set_Adem_dbw(200e3)                # Demod BW
        self.FSW.Set_Adem_Coupling('AC')            # Coupling
        self.FSW.Set_Adem_PM_Unit('DEG')            # Units
        self.FSW.Set_Adem_PM_Scale(4)               # Y Scaling
        self.FSW.Set_Adem_PM_RefPos(50)             # Phase Reference Position
        self.FSW.Set_Adem_PM_RefVal(1)              # Phase Reference Value
        self.FSW.Set_In_YIG('ON')                        # YIG ON

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    #coverage run -a -m unittest -b -v test_HW_VSA_ADemod
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
