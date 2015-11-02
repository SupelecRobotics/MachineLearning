import sys
import socket
import time
import signal
import RPi.GPIO as GPIO
import serial
import numpy as np
import cv2
import pickle
import thread
from functions import *
import RobotFinder
import PerspectiveTransformer
import StatProcesser
from RaspiBluetooth import *

TCP_PORT_STREAM = 5004
TCP_PORT_PARAM = 5005

NB_ROBOTS = 4

BLINK_TIME_WAITING_CONNECT = 0.1
BLINK_TIME_RUNNING = 0.5

pinLED = 11

def quitCallback(signal,frame):
    logFile.write('Exiting cleanly\n')
    logFile.close()
    ledParams[0] = 3
    sys.exit(0)
    


def ledControl(threadName, ledStatus):

    while(True):
        if(ledStatus[0] == 0):
            GPIO.output(pinLED, True)
            time.sleep(BLINK_TIME_WAITING_CONNECT)
            GPIO.output(pinLED, False)
            time.sleep(BLINK_TIME_WAITING_CONNECT)
        elif(ledStatus[0] == 1):
            GPIO.output(pinLED, True)
        elif(ledStatus[0] == 2):
            GPIO.output(pinLED, True)
            time.sleep(BLINK_TIME_RUNNING)
            GPIO.output(pinLED, False)
            time.sleep(BLINK_TIME_RUNNING)
        else:
            GPIO.output(pinLED, False)
        

def stream(threadName, params):

    print 'Waiting for stream connection'
    connStream = waitForConnection(TCP_PORT_STREAM)

    print 'Stream connection accepted'

    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

    cap = params[2]

    while(cap.isOpened() and not params[0]):
        ret,frame = cap.read()
        if(ret):
            result, imgencode = cv2.imencode('.jpg', frame, encode_param)
            data = np.array(imgencode)
            stringData = data.tostring()
            try:
                connStream.send( str(len(stringData)).ljust(16))
                connStream.send( stringData )
            except:
                pass

    print 'Releasing stream objects'
    connStream.close()
    params[1] = True

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinLED, GPIO.OUT)

ledParams = [3]
thread.start_new_thread(ledControl, ('LED Control', ledParams))


cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 600)

params = [False, False, cap]

ledParams[0] = 0

print 'Waiting for params connection'
connParam = waitForConnection(TCP_PORT_PARAM)

print 'Params connection accepted'

thread.start_new_thread(stream, ('Stream', params))

end = False
matchBegin = False

blueTSer = None
color = 'y'

ledParams[0] = 1

try:
    while(not end):        
        length = recvall(connParam,16)
        if(length != 0):
            inData = recvall(connParam, int(length))
            end,matchBegin,color = processData(connParam, inData,color)
            
except (KeyboardInterrupt, SystemExit):
    end = True

params[0] = True
connParam.close()

while(not params[1]):
    pass

if(matchBegin):
    print 'Beginning match !'
    
    blueTSer = serial.Serial( "/dev/ttyAMA0", baudrate=38400,timeout = 5 )

    robFinder = []

    for i in range(0,NB_ROBOTS):
        robFinder.append(RobotFinder.RobotFinder(i))

    perspTrans = PerspectiveTransformer.PerspectiveTransformer(color)
    statProc = StatProcesser.StatProcesser()


    lastMsg = ''
    lostTracking = True

    logFile = open('camLog.txt','w')

    ledParams[0] = 2

    signal.signal(signal.SIGTERM, quitCallback)
    signal.signal(signal.SIGINT, quitCallback)

    while(cap.isOpened()):
        ret,frame = cap.read()
        statProc.update()
        if(ret):
            coords = robFinder[0].process(frame)
            tableCoords = perspTrans.transform(coords)
            statProc.addPoints(tableCoords)
            statProc.printPointDistribution()
            logFile.write(str(statProc.getCurrentPoint()) + '\n')
            lastMsg,lostTracking = sendCoordsOfRobot(blueTSer, 0, statProc.getCurrentPoint(), lastMsg, lostTracking)
                

cap.release()





