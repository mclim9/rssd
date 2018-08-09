#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: OSP Open Switch Platform Common Functions
### Author:  Martin C Lim
### Date:    2018.06.15
### Strctr : pyvisa-->yavisa-->OSP_Common.py
#####################################################################
from rssd.yaVISA import jaVisa

class OSP(jaVisa):
   def __init__(self):
      super(OSP, self).__init__()
      self.Model = "OSP1x0"
             
   #####################################################################
   ### OSP Switching Functions
   #####################################################################
   def Get_SW_SPDT(self,slot=11,sw=1):
      # ROUT:CLOS? (@F01A11(0161))
      outstr = 'ROUT:CLOS? (@F01A%02d(01%02d))'%(slot,sw)
      print(outstr)
      state = self.queryInt(outstr)[0]
      print("A%02d SW%d @Pos%d"%(slot,sw,state))
      return int(state)

   def Get_SW_SP6T(self,slot=11,sw=1):
      # ROUT:CLOS? (@F01A11(0161))
      for pos in range(0,7):
         outstr = 'ROUT:CLOS? (@F01A%02d(%02d%02d))'%(slot,pos,sw)
         state = self.queryInt(outstr)[0]
         if state == 1:
            CurrState = pos
            print("A%02d SW%02d @Pos%02d"%(slot,sw,pos))
      return CurrState
         
   def Set_SW(self,slot=11,sw=1,pos=1):
      # ROUT:CLOS (@F01A11(0161))
      outstr = 'ROUT:CLOS (@F01A%02d(%02d%02d))'%(slot,pos,sw)
      print(outstr)
      self.write(outstr)

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   RFU3 = OSP()
   RFU3.jav_openvisa('TCPIP0::192.168.1.150::INSTR')
   RFU3.Set_SW(11,43,0)    #K52
   RFU3.Set_SW(11,56,0)    #K51
   RFU3.Set_SW(11,55,0)    #K50
   RFU3.Set_SW(11,67,6)    #K71
   RFU3.Set_SW(11,49,1)    #K70
   RFU3.jav_ClrErr()
