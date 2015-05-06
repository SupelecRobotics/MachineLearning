import time

TIME_KEEP = 2
MAX_DELTA = 100


def distance2(pos1, pos2):
    return (pos1[0] - pos2[0])*(pos1[0] - pos2[0]) + (pos1[1] - pos2[1])*(pos1[1] - pos2[1])


class StatProcesser:

    def __init__(self):

        self.lastPos = None
        self.timeWithoutNewPts = 0
        self.lastTime = 0

    def addPos(self,positions):

        print self.timeWithoutNewPts

        if(positions is None or len(positions) == 0):
            self.timeWithoutNewPts = time.time() - self.lastTime
            self.lastTime = time.time()
            if(self.timeWithoutNewPts > TIME_KEEP):
                self.lastPos = None
            return

        self.timeWithoutNewPts = 0

        if(self.lastPos is None):
            self.lastPos = positions[0]
            return

        iMax = 0
        minD2 = 0

        for i in range(0,len(positions)):

            d2 = distance2(self.lastPos, positions[i])
            if(d2 > MAX_DELTA):
                del positions[i]
            else:
                if(d2 < minD2):
                    iMax = i
                    mniD2 = d2
        if(len(positions) > 0):
            self.lastPos = positions[iMax]

    def getCurrPos(self):

        return self.lastPos
