import socket
import pickle
from RaspiBluetooth import *

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def waitForConnection(TCP_PORT):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', TCP_PORT))
    s.listen(True)
    conn, addr = s.accept()
    s.close()

    return conn

def dumpInto(fileName, param):
    with open(fileName,'w') as file:
        pickler = pickle.Pickler(file)
        pickler.dump(param)

def loadFromFileAndSend(fileName, sock):
    with open(fileName,'r') as file:
        depickler = pickle.Unpickler(file)
        param = depickler.load()
        outData = str(param)
        sock.send( str(len(outData)).ljust(16))
        sock.send( outData )

def processData(sock, inData, color):

    end = False
    matchBegin = False

    c = inData[0]

    if(c == 'o'):
        colorParams = eval(inData[1:])
        dumpInto('ColorParams.dat', colorParams)
    elif(c == 'l'):
        loadFromFileAndSend('ColorParams.dat', sock)
    elif(c == 'p'):
        perspPoints = eval(inData[1:])
        dumpInto('PerspectivePoints.dat', perspPoints)
    elif(c == 'm'):
        loadFromFileAndSend('PerspectivePoints.dat', sock)
    elif(c == 'i'):
        ratioParams = eval(inData[1:])
        dumpInto('Ratios.dat', ratioParams)
    elif(c == 'k'):
        loadFromFileAndSend('Ratios.dat', sock)
    elif(c == 'b'):
        bluetoothInit()
    elif(c == 'x'):
        end = True
    elif(c == 'X'):
        end = True
        matchBegin = True
    elif(c == 'r'):
        loadFromFileAndSend('RefPoints_'+ color + '.dat', sock)
    elif(c == 'g' or c == 'y'):
        color = c
        
    return end,matchBegin,color
        
