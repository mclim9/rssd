# -*- coding: future_fstrings -*-
#pylint: disable=R0201,W0613
'''RSSD test bus class'''

from rssd.bus.bus import bus

class jaTest(bus):                          #pylint: disable=R0205
    """Instrument Common functions"""
    def __init__(self):
        self.EOL        = '\n'

    def open(self, resourceID, param=None):
        self.connected          = 0
        return self

    def query(self, SCPIstr):
        return "<notRead>"

    def read_raw(self):
        return b'1234567890'

    def write_raw(self, SCPIstr):
        pass

    def write(self, SCPIstr):
        pass
