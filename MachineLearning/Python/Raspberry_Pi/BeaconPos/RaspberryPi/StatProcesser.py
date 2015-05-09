import os
import time

MAX_DIST = 40
TIME_KEEP = 2


def distance2(pos1, pos2):
    return (pos1[0] - pos2[0])*(pos1[0] - pos2[0]) + (pos1[1] - pos2[1])*(pos1[1] - pos2[1])

class StatProcesser:

    def __init__(self):
        self.points = {}
        self.lastTime = time.time()

    def printPointDistribution(self):

        os.system('clear')
        for p in self.points :

            msg = str((int(p[0]),int(p[1]))) + ' |'
            for i in range(0,self.points[p][0]):
                msg += '#'
                
            print msg

        p = self.getMostLikely()
        if(p is not None):
            print '\n' + str((int(p[0]),int(p[1])))

    def getMostUnlikely(self):

        pMin = None
        minNbPoints = float('inf')

        for p in self.points:

            if(self.points[p][0] < minNbPoints):
                pMin = p
                minNbPoints = self.points[p][0]

        return pMin

    def addToList(self, point):
            

        put = False

        for p in self.points:

            if (distance2(p, point) < MAX_DIST):
                self.points[p][0] += 1
                self.points[p][1] = time.time()
                put = True
                break

        if(not put):
            self.points[point] = [1,time.time()]

    def getLessRecent(self):

        pOld = None
        t = float('inf')

        for p in self.points:

            if(self.points[p][1] < t):
                pOld = p
                t = self.points[p][1]

        return pOld

    def update(self):

        if(time.time() - self.lastTime > TIME_KEEP):
            self.points = {}
##            pOld = self.getLessRecent()
##            if(pOld is not None):
##                del self.points[pOld]
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

            if(self.points[p][0] > maxNbPoints):
                pMax = p
                maxNbPoints = self.points[p][0]

        return pMax

        
            
