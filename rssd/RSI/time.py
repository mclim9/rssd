###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Timer Object
### Author : Martin C Lim
###############################################################################
import timeit
import time

class timer():                                                       #pylint: disable=E0102
    def __init__(self):
        self.ticks  = []
        self.n      = 0

    def start(self):
        self.ticks = []
        self.tick()

    def tick(self):
        self.ticks.append(timeit.default_timer())

    def deltaTimes(self):
        deltaTimes  = []
        maxIndx     = len(self.ticks)-1
        for i,tick in enumerate(self.ticks):
            if (i < maxIndx):
                deltaTimes.append(self.ticks[i+1] - self.ticks[i])
        deltaTimes.append(self.ticks[maxIndx] - self.ticks[0])
        return deltaTimes

    def deltaTimeTxt(self):
        outStr = ""
        for each in self.deltaTimes():
            outStr += f'{each:2,.3f},'
        return outStr

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    asdf = timer()
    asdf.tick()
    time.sleep(0.6)
    asdf.start()
    time.sleep(1.2)
    asdf.tick()
    adf =asdf.deltaTimeTxt()
    pass
    