# Programme qui tournera sur chacun des 3 RasPi/balises autour de la map
# Il lit le flux vidéo, reconnaît les objets importants et envoie leurs coordonnées (plus éventuellement d'autres infos) au robot
import numpy as np
import cv2
import CylinderFinder
import TennisBallFinder
import RobotsFinder
import PerspectiveTransformer
import serial
import RPi.GPIO as GPIO
import time
import RaspiBluetooth
import functions

blueTSer = RaspiBluetooth.bluetoothInit()

#undistorter = CameraUndistorter.CameraUndistorter()
#undistorter.loadParam()

#Ouverture de la caméra
#cap = cv2.VideoCapture("/dev/video0")
cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720)

end = False

frameProcessors,perspectiveTransformer = functions.initProcessors()


while(cap.isOpened() and not end):
    ret,frame = cap.read()
    
    if(ret):
        #frame = undistorter.undistort(frame)
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frameCoords = findObjects(hsvFrame, frameProcessors)
        tableCoords = getTableCoords(frameCoords, perspectiveTransformer)
        sendCoords(blueTSer, tableCoords)

cap.release()
cv2.destroyAllWindows()
