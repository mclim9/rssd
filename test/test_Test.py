from __future__ import print_function
##########################################################
### Rohde & Schwarz Software Test
###
### Purpose: Test test
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
import unittest

class TestGeneral(unittest.TestCase):
   def setUp(self):              #run before each test
      print('MMM', end='')
      pass
      
   def test_Test1(self):
      self.assertEqual("as"+"df","asdf")
      
   def test_Test2(self):
      self.assertEqual(12+23,35)
   
   def test_Test3(self):
      self.assertTrue('FOO'.isupper())
      self.assertFalse('Foo'.isupper())
   
   def tearDown(self):
      pass

if __name__ == '__main__':
   if 0:    #Run w/o test names
      unittest.main()
   else:    #Verbose run
      suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
      unittest.TextTestRunner(verbosity=2).run(suite)
