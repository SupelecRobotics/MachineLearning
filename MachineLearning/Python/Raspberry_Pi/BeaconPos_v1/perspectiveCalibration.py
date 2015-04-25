import sys
import pickle
import cv2
import numpy as np
#import CameraUndistorter

TABLE_W = 2000
TABLE_H = 3000
IMG_W = 418
IMG_H = 626

if(sys.argv[1] == 'm'):
    streamIP = 'http://169.254.22.56:8554/'
elif(sys.argv[1] == 'l'):
    streamIP = 'http://169.254.22.57:8554/'
else:
    streamIP = 'http://169.254.22.57:8554/'

class PointsList:

    def __init__(self):
        self.tablePoints = []
        self.camPoints = []
        self.waitingForCamPoint = False
        self.currentTablePoint = (0,0)

    def addTablePoint(self, x, y):
        self.currentTablePoint = (int(x*float(TABLE_W)/float(IMG_W)),int(y*float(TABLE_H)/float(IMG_H)))
        self.waitingForCamPoint = True

    def addCamPoint(self, x, y):
        if(self.waitingForCamPoint):
            self.camPoints.append((x,y))
            self.tablePoints.append(self.currentTablePoint)
            self.waitingForCamPoint = False
            print self.tablePoints
            print self.camPoints

    def draw(self, table, frame):
        tableWithCircles = table.copy()
        frameWithCircles = frame.copy()
        for i in range(0, len(self.camPoints)):
            cv2.circle(tableWithCircles,(int(self.tablePoints[i][0]*float(IMG_W)/float(TABLE_W)),int(self.tablePoints[i][1]*float(IMG_H)/float(TABLE_H))),5,(255,0,0),2)
            cv2.circle(frameWithCircles,self.camPoints[i],5,(255,0,0),2)

        if(self.waitingForCamPoint):
            cv2.circle(tableWithCircles,(int(self.currentTablePoint[0]*float(IMG_W)/float(TABLE_W)),int(self.currentTablePoint[1]*float(IMG_H)/float(TABLE_H))),5,(255,0,0),2)

        return tableWithCircles,frameWithCircles


def tableCallback(event,x,y,flags,param):
    if(event == cv2.EVENT_LBUTTONDOWN):
        param.addTablePoint(x,y)

def camCallback(event,x,y,flags,param):
    if(event == cv2.EVENT_LBUTTONDOWN):
        param.addCamPoint(x,y)
        #param.addCamPoint(x,y)

def saveParam(ptsList):
    with open('PerspectiveTransformer_' + sys.argv[1] + '.dat', 'w') as file:
        pickler = pickle.Pickler(file)
        pickler.dump((ptsList.camPoints,ptsList.tablePoints))
        
def loadParam(ptsList):
    with open('PerspectiveTransformer_' + sys.argv[1] + '.dat', 'r') as file:
        depickler = pickle.Unpickler(file)
        ptsList.camPoints,ptsList.tablePoints = depickler.load()

#undistorter = CameraUndistorter.CameraUndistorter()
#undistorter.loadParam()

cap = cv2.VideoCapture(streamIP)
end = False
table = cv2.imread('schema_table2.png')

cv2.namedWindow('Table')
cv2.namedWindow('Cam')

ptsList = PointsList()
cv2.setMouseCallback('Table', tableCallback, ptsList)
cv2.setMouseCallback('Cam', camCallback, ptsList)

#TEMPORAIRE
#testPic = cv2.imread('Tableframe.jpg')
#FIN

while(cap.isOpened() and not end):

    ret,frame = cap.read()

    #TEMPORAIRE
    #frame = testPic
    #FIN

    if(ret):
        #frame = undistorter.undistort(frame)
        tableWithCircles,frameWithCircles = ptsList.draw(table,frame)
        cv2.imshow('Cam',frameWithCircles)
        cv2.imshow('Table',tableWithCircles)

    key = cv2.waitKey(1) & 0xFF
    if(key == ord('q')):
        end = True
    elif(key == ord('s')):
        saveParam(ptsList)
    elif(key == ord('l')):
        loadParam(ptsList)

cap.release()        
cv2.destroyAllWindows()
