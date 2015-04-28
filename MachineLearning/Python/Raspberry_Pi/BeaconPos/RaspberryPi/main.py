import socket
import numpy as np
import cv2
import pickle
import thread
from functions import *
import RobotFinder
import PerspectiveTransformer

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
            connStream.send( str(len(stringData)).ljust(16))
            connStream.send( stringData )

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

try:
    while(not end):        
        length = recvall(connParam,16)
        if(length != 0):
            inData = recvall(connParam, int(length))
            end,blueTSer = processData(connParam, inData)
            
except (KeyboardInterrupt, SystemExit):
    end = True

param[0] = True
connParam.close()

while(not param[1]):
    pass


print 'Beginning match !'

for i in range(0,NB_ROBOTS):
    robFinder[i] = RobotFinder.RobotFinder(i)


end = False

try:
    while(cap.isOpened() and not end):
        ret,frame = cap.read()
        if(ret):
            # TODO !
        
            
except (KeyboardInterrupt, SystemExit):
    end = True

cap.release()





