##########################################################
### Rohde & Schwarz Software Test
###
### Purpose: FSW_driver software test
### Author:  mclim
### Date:    2018.05.07
##########################################################
### User Entry
##########################################################
host = '192.168.1.109'           #Get local machine name
port = 5025                      #Reserve a port for your service.

##########################################################
### Code Start
##########################################################
#from RS_ATE_Python2.driver.FSW_Common import VSA
from driver.FSW_Common import VSA
#import .driver.FSW_Common
import unittest

class TestGeneral(unittest.Testcase):
   def setUp(self):                 #run before each test
      print("Setup")

   def test_FSW_Connect(self):
      FSW = VSA()
      FSW.VISA_Open(host)
      FSW.Set_DisplayUpdate("ON")
      

if __name__ == '__main__':
	unittest.main()
