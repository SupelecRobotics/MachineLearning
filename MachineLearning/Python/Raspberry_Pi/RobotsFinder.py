import pickle
import numpy as np
import cv2

H0 = 350
H2 = 430

MH = 71
MW = 80

class RobotsFinder:

    # Classe qui s'occupe de donner la position sur l'image de la base des robots vus par la caméra
    # Doit être calibrée avant utilisation.

    def __init__(self, robotID):

        self.robotID = robotID
        
        if(robotID == 0 or robotID == 1):
            self.ROBOTS_HEIGHT = H0
        else:
            self.ROBOTS_HEIGHT = H2
            
        self.MARK_HEIGHT = MH
        
        self.wMin = 20 #Temporaire
        self.hMin = 20 #Temporaire
        
        self.cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))

        refImg = cv2.imread('baliseEmbarqueeReference.png')
        refImg = cv2.cvtColor(refImg, cv2.COLOR_BGR2GRAY)
        self.refContours = cv2.findContours(refImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]

        self.param = {}

        self.ratioMin = 0.8*float(MW/MH)
        self.ratioMax = 1.2*float(MW/MH)
        
        self.param["colorMin"] = np.array([0, 0, 0])
        self.param["colorMax"] = np.array([179, 255, 255])
        self.param["matchMax"] = 0

    def setParam(self, param):
        self.param = param
        
    def loadParamFromFile(self):
        path = 'RobotsFinder_' + str(self.robotID) + '.dat'
        with open(path, 'r') as file:
            depickler = pickle.Unpickler(file)
            self.param = depickler.load()

    def getBasePos(self, x, y, w, h):
        xBase = x + w/2
        yBase = y + h + (float(self.ROBOTS_HEIGHT)/float(self.MARK_HEIGHT)) * h
        return (int(xBase), int(yBase))
        

    def process(self,frame):

        if(len(self.param["roi"]) >= 3):
            roiMask = np.empty((frame.shape[0], frame.shape[1]), np.uint8)         
            cv2.fillPoly(roiMask, np.array([self.param["roi"]]), (255,255,255))
            frame = cv2.bitwise_and(frame, frame, mask = roiMask)
        
        cropped = cv2.inRange(frame, self.param["colorMin"], self.param["colorMax"])
        eroded = cv2.erode(cropped, self.cross)
        contours,_ = cv2.findContours(eroded.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        validContours = []
        basesPos = np.empty([0,2],float)

        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            ratio = float(w) / float(h)
            if(cv2.matchShapes(cnt, self.refContours[0], 3, 1) < self.param["matchMax"]/float(1000) and w > self.wMin and h > self.hMin and ratio > self.ratioMin and ratio < self.ratioMax):
                validContours.append(cnt)
                currBasePos = self.getBasePos(x,y,w,h)
                if(len(self.param["upstairs"]) >= 3 and cv2.pointPolygonTest(self.param["upstairs"], currBasePos)):
                    basesPos = np.vstack((basesPos, (currBasePos[0], currBasePos[1] + STAIRWAY_HEIGHT)))
                else:
                    basesPos = np.vstack((basesPos, currBasePos))

        return basesPos, eroded, validContours
