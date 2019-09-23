# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Vector Signal Analyzer Common Functions
### Author:  Martin C Lim
### Date:    2018.02.01
#####################################################################
from rssd.yaVISA import jaVisa              # pylint: disable=E0611,E0401
try:
    import rssd.VSA_Leveling as VSAL        # pylint: disable=E0611,E0401
except:
    pass

class VSA(jaVisa):
    """ Rohde & Schwarz Vector Signal Analyzer Object """
    def __init__(self):
        super(VSA, self).__init__()
        self.Model = "FSW"
        print('hello world')