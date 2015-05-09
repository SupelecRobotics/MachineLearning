import pickle
import numpy as np
import cv2

##H0 = 350
##H2 = 430

H0 = 364
H2 = 430

MH = 73
MW = 80

WMIN = 20
HMIN = 20

class RobotFinder:


    def __init__(self, robType):

        self.robType = robType

        heights = [H0, H0, H2, H2]

        self.ROBOT_HEIGHT = heights[robType]
            
        self.MARK_HEIGHT = MH
        self.MARK_WIDTH = MW
        
        self.wMin = WMIN #Temporaire
        self.hMin = HMIN #Temporaire
        
        self.cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))


        # Remettre si nécessaire
        #refImg = cv2.imread('baliseEmbarqueeReference.png')
        #refImg = cv2.cvtColor(refImg, cv2.COLOR_BGR2GRAY)
        #self.refContours = cv2.findContours(refImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]

        self.param = {}

        with open('Ratios.dat', 'r') as file:
            depickler = pickle.Unpickler(file)
            param = depickler.load()
            self.ratioMin = (param[self.robType][0] / float(100)) * float(MW) / float(MH)
            self.ratioMax = (param[self.robType][1] / float(100)) * float(MW) / float(MH)

        with open('ColorParams.dat', 'r') as file:
            depickler = pickle.Unpickler(file)
            param = depickler.load()
            self.colorMin = param[self.robType][0]
            self.colorMax = param[self.robType][1]

    def getBasePos(self, x, y, w, h):
        xBase = x + w/2
        yBase = y + h + (float(self.ROBOT_HEIGHT)/float(self.MARK_WIDTH)) * w
        return (int(xBase), int(yBase))
        

    def process(self,frame):
        
        cropped = cv2.inRange(frame, np.array(self.colorMin), np.array(self.colorMax))
        eroded = cv2.erode(cropped, self.cross)
        contours,_ = cv2.findContours(eroded,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        basesPos = np.empty([0,2],float)

        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            ratio = float(w) / float(h)
            if(w > self.wMin and h > self.hMin and ratio > self.ratioMin and ratio < self.ratioMax):
                currBasePos = self.getBasePos(x,y,w,h)
                basesPos = np.vstack((basesPos, currBasePos))

        return basesPos
