import time

MAX_DIST = 10
TIME_KEEP = 3


def distance2(pos1, pos2):
    return (pos1[0] - pos2[0])*(pos1[0] - pos2[0]) + (pos1[1] - pos2[1])*(pos1[1] - pos2[1])

class StatProcesser:

    def __init__(self):
        self.points = {}
        self.lastTime = time.time()

    def getMostUnlikely(self):

        pMin = None
        minNbPoints = float('inf')

        for p in self.points:

            if(self.points[p] < minNbPoints):
                pMin = p
                minNbPoints = self.points[p]

        return pMin

    def addToList(self, point):
            

        put = False

        for p in self.points:

            if (distance2(p, point) < MAX_DIST):
                self.points[p] += 1
                put = True
                break

        if(not put):
            self.points[point] = 1

    def update(self):

        if(time.time() - self.lastTime > TIME_KEEP):
            self.points = {}
            self.lastTime = time.time()

    def addPoints(self, points):

        #print self.points

        if(points is None):
            return

        for p in points:
            
            self.addToList(tuple(p))

    def getMostLikely(self):

        pMax = None
        maxNbPoints = 0

        for p in self.points:

            if(self.points[p] > maxNbPoints):
                pMax = p
                maxNbPoints = self.points[p]

        return pMax

        
            
