###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Timer Object
### Author : Martin C Lim
###############################################################################
import timeit
import time

class timer():                                                       #pylint: disable=E0102
    def __init__(self):
        self.timeStart  = 0
        self.numTest    = 100
        self.curTest    = 1
        self.ticks      = []
        self.n          = 0

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

        ### Calculate time left
        remTest = self.numTest - self.curTest
        deltaTime = (timeit.default_timer() - self.timeStart) / self.curTest
        timeLeft = deltaTime * (remTest) / (60 * 60)
        deltaTimes.append(timeLeft)     # in hours
        self.curTest += 1
        return deltaTimes

    def deltaTimeTxt(self):
        outStr = ""
        for each in self.deltaTimes():
            outStr += f'{each:2,.3f},'
        return outStr

    def suite_start(self):
        self.timeStart = timeit.default_timer()


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
    