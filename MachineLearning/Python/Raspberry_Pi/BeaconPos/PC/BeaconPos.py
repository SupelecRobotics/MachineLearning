import socket
import numpy as np
import cv2

class BeaconPos:

    def __init__(self):

        self.connected = False
        
        self.STREAM_PORT = 5005
        self.PARAMS_PORT = 5004

        self.TEST_colorParams = [ [ (0,0,0),(179,255,255) ], [ (0,0,0),(179,255,255) ], [ (0,0,0),(179,255,255) ], [ (0,0,0),(179,255,255) ]]
        self.TEST_points = [(0, 0), (34, 23), (23, 234), (123, 98)]
        self.TEST_refPoints = [(0, 0), (45, 65), (12, 17), (5, 35)]

    def connectLAN(self, adress):
        
        self.streamSock = socket.socket()
        self.streamSock.connect((adress, self.STREAM_PORT))

        self.paramsSock = socket.socket()
        self.paramsSock.connect((adress, self.PARAMS_PORT))

        #if(err1 == 0 and err2 == 0):
        self.connected = True

        print 'Connection OK'

    def disconnectLAN(self):

        if(self.connected):
            self.streamSock.close()
            self.paramsSock.close()
            self.connected = False

    def isConnected(self):
        return self.connected

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def send(self, stringData):

        self.paramsSock.send( str(len(stringData)).ljust(16))
        self.paramsSock.send( stringData )

    def getFrame(self):
        if(self.isConnected):
            length = self.recvall(self.streamSock,16)
            stringData = self.recvall(self.streamSock, int(length))
            data = np.fromstring(stringData, dtype='uint8')
            decimg=cv2.imdecode(data,1)
            return decimg
        else:
            return None
    
    def setColorParams(self, params):

        self.send('o' + str(params))

        self.TEST_colorParams = list(params) # Temporaire

    def setPoints(self, points):

        self.TEST_points = list(points) # Temporaire

    def setRefPoints(self, refPoints):

        self.TEST_refPoints = list(refPoints) # Temporaire

    def getColorParams(self):

        return list(self.TEST_colorParams) # Temporaire

    def getPoints(self):

        return list(self.TEST_points) # Temporaire

    def getRefPoints(self):

        return list(self.TEST_refPoints) # Temporaire

    def connectBluetooth(self):

        return True # Temporaire

    def beginMatch(self):
        
        pass # Temporaire

    
        
