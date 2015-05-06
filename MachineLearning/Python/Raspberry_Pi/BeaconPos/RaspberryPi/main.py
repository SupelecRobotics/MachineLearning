import socket
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


cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 600)

params = [False, False, cap]
thread.start_new_thread(stream, ('Stream', params))
print 'Waiting for params connection'
connParam = waitForConnection(TCP_PORT_PARAM)

print 'Params connection accepted'

end = False
matchBegin = False

blueTSer = None

try:
    while(not end):        
        length = recvall(connParam,16)
        if(length != 0):
            inData = recvall(connParam, int(length))
            end,matchBegin = processData(connParam, inData)
            
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

    perspTrans = PerspectiveTransformer.PerspectiveTransformer()
    statProc = StatProcesser.StatProcesser()


    end = False
    lastMsg = ''

    try:
        while(cap.isOpened() and not end):
            ret,frame = cap.read()
            statProc.update()
            if(ret):
                coords = robFinder[2].process(frame)
                tableCoords = perspTrans.transform(coords)
                statProc.addPoints(tableCoords)
                lastMsg = sendCoordsOfRobot(blueTSer, 2, statProc.getMostLikely(), lastMsg)
                
            
                
    except (KeyboardInterrupt, SystemExit):
        end = True
        print 'User interrupt'

cap.release()





