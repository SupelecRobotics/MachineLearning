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

camPos = 'm'

#blueTSer = RaspiBluetooth.bluetoothInit()

#undistorter = CameraUndistorter.CameraUndistorter()
#undistorter.loadParam()

#Ouverture de la caméra
cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720)

end = False

frameProcessors,perspectiveTransformer = functions.initProcessors(camPos)

#TEMPORAIRE
#testPic = cv2.imread('Tableframe.jpg')
#FIN

print "Debut lecture frames"


while(cap.isOpened() and not end):
    ret,frame = cap.read()

    #TEMPORAIRE
    #frame = testPic
    #FIN
    
    if(ret):
        #frame = undistorter.undistort(frame)
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frameCoords = functions.findObjects(hsvFrame, frameProcessors)
        tableCoords = functions.getTableCoords(frameCoords, perspectiveTransformer)
        print tableCoords["robot0"]
        with open('log.txt','a') as logfile:
            logfile.write(str(tableCoords["robot0"])+'\n')
        #RaspiBluetooth.sendCoords(blueTSer, tableCoords)

cap.release()
cv2.destroyAllWindows()
