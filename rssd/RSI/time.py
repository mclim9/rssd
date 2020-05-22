###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Timer Object
### Author : Martin C Lim
###############################################################################
import timeit
import time

class timr():                                                       #pylint: disable=E0102
    """ Rohde & Schwarz Vector Signal Analyzer 5GNR Object """
    def __init__(self):
        self.ticks  = []
        self.n      = 0

    def clear(self):
        self.ticks = []

    def tick(self):
        self.ticks.append(timeit.default_timer())

    def getTimes(self):
        deltaTimes = []
        for i,tick in enumerate(self.ticks):
            deltaTimes = self.ticks[i+1] - self.ticks[i]
        return deltaTimes


#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    asdf = timr()
    asdf.tick()
    time.sleep(1.2)
    asdf.tick()
    asdf.getTimes()
    pass
    