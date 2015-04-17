import pickle
import cv2
import numpy as np
import RobotsFinder
import sys
#import CameraUndistorter

def nothing(x):
    pass

def mouseCallback(event,x,y,flags,cbParam):
    param,mode = cbParam

    if(mode == 0):
        if(event == cv2.EVENT_LBUTTONDOWN):
            param["roi"].append((x,y))
        elif(event == cv2.EVENT_RBUTTONDOWN):
            if(len(param["roi"]) > 0):
                param["roi"].pop()

def saveParam(param):
    with open('RobotsFinder_' + sys.argv[1] + '.dat', 'w') as file:
        pickler = pickle.Pickler(file)
        pickler.dump(param)

def loadParam():
    with open('RobotsFinder_' + sys.argv[1] + '.dat', 'r') as file:
        depickler = pickle.Unpickler(file)
        param = depickler.load()
        return param

def createTrackbars():
    cv2.namedWindow('Colors', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Match max', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Hmin', 'Colors', 0, 179, nothing)
    cv2.createTrackbar('Hmax', 'Colors', 0, 179, nothing)
    cv2.createTrackbar('Smin', 'Colors', 0, 255, nothing)
    cv2.createTrackbar('Smax', 'Colors', 0, 255, nothing)
    cv2.createTrackbar('Vmin', 'Colors', 0, 255, nothing)
    cv2.createTrackbar('Vmax', 'Colors', 0, 255, nothing)
    cv2.createTrackbar('MatchMax', 'Match max', 0, 1000, nothing)

    cv2.setTrackbarPos('Hmax', 'Colors', 179)
    cv2.setTrackbarPos('Smax', 'Colors', 255)
    cv2.setTrackbarPos('Vmax', 'Colors', 255)

def updateTrackbars(param):
    cv2.setTrackbarPos('Hmin', 'Colors', param["colorMin"][0])
    cv2.setTrackbarPos('Smin', 'Colors', param["colorMin"][1])
    cv2.setTrackbarPos('Vmin', 'Colors', param["colorMin"][2])
    cv2.setTrackbarPos('Hmax', 'Colors', param["colorMax"][0])
    cv2.setTrackbarPos('Smax', 'Colors', param["colorMax"][1])
    cv2.setTrackbarPos('Vmax', 'Colors', param["colorMax"][2])
    cv2.setTrackbarPos('MatchMax', 'Match max', param["matchMax"])

def readParamsFromTrackbars(param):
    colorMin = np.array([cv2.getTrackbarPos('Hmin', 'Colors'),
                         cv2.getTrackbarPos('Smin', 'Colors'),
                         cv2.getTrackbarPos('Vmin', 'Colors')])
    colorMax = np.array([cv2.getTrackbarPos('Hmax', 'Colors'),
                         cv2.getTrackbarPos('Smax', 'Colors'),
                         cv2.getTrackbarPos('Vmax', 'Colors')])
    matchMax = cv2.getTrackbarPos('MatchMax', 'Match max')
    
    param["colorMin"] = colorMin
    param["colorMax"] = colorMax
    param["matchMax"] = matchMax

def cropFrameAddContours(frame, mask, contours, roiPts):
    cropped = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.drawContours(cropped, contours, -1, (255, 0, 0),3)
    if(len(roiPts) >= 2):
        cv2.polylines(cropped, np.array([roiPts]), False, (255,255,255), 4)
    return cropped

cap = cv2.VideoCapture('http://169.254.22.56:8554/')
#cap = cv2.VideoCapture(0)
end = False

robotsFinder = RobotsFinder.RobotsFinder(sys.argv[1])

#undistorter = CameraUndistorter.CameraUndistorter()
#undistorter.loadParam()

createTrackbars()

cv2.namedWindow('Result')
mode = 0
param = {"roi":[], "upstairs":[]}
cbParam = (param, mode)
cv2.setMouseCallback('Result', mouseCallback, cbParam)

#TEMPORAIRE
testPic = cv2.imread('Tableframe.jpg')
#FIN

while(cap.isOpened() and not end):
    ret,frame = cap.read()
    #TEMPORAIRE
    frame = testPic
    #FIN
    readParamsFromTrackbars(param)
    robotsFinder.setParam(param)

    if(ret):
        #frame = undistorter.undistort(frame)
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        _,mask,validContours = robotsFinder.process(hsvFrame)
        finalFrame = cropFrameAddContours(frame, mask, validContours, param["roi"])
        cv2.imshow('Result', finalFrame)
        
        
    key = cv2.waitKey(1) & 0xFF
    if(key == ord('q')):
        end = True
    elif(key == ord('s')):
        saveParam(param)
    elif(key == ord('l')):
        param = loadParam()
        updateTrackbars(param)
        cbParam = (param, mode)
        cv2.setMouseCallback('Result', mouseCallback, cbParam)

cap.release()        
cv2.destroyAllWindows()
