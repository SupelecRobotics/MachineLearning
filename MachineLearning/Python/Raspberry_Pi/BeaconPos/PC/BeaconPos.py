import socket
import numpy as np
import cv2

class BeaconPos:

    def __init__(self):

        self.connected = False
        
        self.STREAM_PORT = 5004
        self.PARAMS_PORT = 5005

    def connectLAN(self, adress):


        self.paramsSock = socket.socket()
        self.paramsSock.connect((adress, self.PARAMS_PORT))
        
        self.streamSock = socket.socket()
        self.streamSock.connect((adress, self.STREAM_PORT))
        self.connected = True
        print 'Connection OK'

    def disconnectLAN(self, mode):

        if(self.connected):
            if(mode == 0): # 0 : quitte sans match, 1 : quitte et démarre le match
                self.send('x')
            else:
                self.send('X')
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

    def setRatioParams(self, params):

        self.send('i' + str(params))

    def setPoints(self, points):

        self.send('p' + str(points))

    def setRefPoints(self, refPoints):

        pass

    def getColorParams(self):

        if(self.isConnected):
            self.send('l')
            length = self.recvall(self.paramsSock,16)
            stringData = self.recvall(self.paramsSock, int(length))

            return eval(stringData)

    def getPoints(self):

        if(self.isConnected):
            self.send('m')
            length = self.recvall(self.paramsSock,16)
            stringData = self.recvall(self.paramsSock, int(length))
            return eval(stringData)

    def getRefPoints(self):

        if(self.isConnected):
            self.send('r')
            length = self.recvall(self.paramsSock,16)
            stringData = self.recvall(self.paramsSock, int(length))
            return eval(stringData)

    def getRatioParams(self):

        if(self.isConnected):
            self.send('k')
            length = self.recvall(self.paramsSock,16)
            stringData = self.recvall(self.paramsSock, int(length))

        return eval(stringData)

    def connectBluetooth(self):

        self.send('b')

    def setStartColor(self,c):

        if(self.isConnected and (c =='y' or c == 'g')):
            self.send(c)
        
