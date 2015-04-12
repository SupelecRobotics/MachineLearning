import pickle
import cv2
import numpy as np
import CameraUndistorter

end = False

class PointsList:

    def __init__(self):
        self.tablePoints = {"Coin gauche":(0,0), "Coin droit":(0,2000), "Coin zone gauche":(400,400), "Coin zone droit":(1600,400), "Milieu depart":(1000,650)}
        self.indexes = self.tablePoints.keys()
        self.i = 0
        
        self.camPoints = {}
        self.end = False

    def addCamPoint(self, x, y):
        print self.indexes[self.i] + "= " + str(x) + "," + str(y)
        self.camPoints[self.indexes[self.i]] = (x,y)
        self.i = self.i + 1
        if(self.i >= len(self.indexes)):
            self.end = True

    def draw(self, frame):
        modifFrame = frame.copy()
        for p in self.camPoints.values():
            cv2.circle(modifFrame,p,5,(255,0,0),2)
            
        if(self.i < len(self.indexes)):
            cv2.putText(modifFrame, self.indexes[self.i] + " " + str(self.i+1) + "/" + str(len(self.indexes)), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255))

        return modifFrame

    def skip(self):
        self.i = self.i + 1
        if(self.i >= len(self.indexes)):
            self.end = True

    def back(self):
        if(self.i > 0):
            self.i = self.i - 1
            if(self.indexes[self.i] in self.camPoints):
                del self.camPoints[self.indexes[self.i]]

def camCallback(event,x,y,flags,param):
    if(event == cv2.EVENT_LBUTTONDOWN):
        param.addCamPoint(x,y)
    elif(event == cv2.EVENT_RBUTTONDOWN):
        param.back()

def saveParam(ptsList):
    with open('PerspectiveTransformer.dat', 'w') as file:
        pickler = pickle.Pickler(file)

        tableList = []
        camList = []
        for k in ptsList.camPoints.keys():
            tableList.append(ptsList.tablePoints[k])
            camList.append(ptsList.camPoints[k])
        
        pickler.dump((tableList,camList))
        print tableList
        print camList


cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('http://10.13.152.226:8554/')

cv2.namedWindow('Cam')

ptsList = PointsList()
cv2.setMouseCallback('Cam', camCallback, ptsList)

while(cap.isOpened() and not end):

    if(ptsList.end):
        end = True
        saveParam(ptsList)
        
    ret,frame = cap.read()

    if(ret):
        modifFrame = ptsList.draw(frame)
        cv2.imshow('Cam',modifFrame)

    key = cv2.waitKey(1) & 0xFF
    if(key == ord('q')):
        end = True
    elif(key == ord('s')):
        saveParam(ptsList)
    elif(key == ord(' ')):
        ptsList.skip()

cap.release()        
cv2.destroyAllWindows()
