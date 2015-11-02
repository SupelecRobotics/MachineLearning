import socket
import cv2
import numpy

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

TCP_IP = '192.168.0.1'
TCP_PORT = 5001

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

cv2.namedWindow('Client')

end = False

while(not end):
    
    length = recvall(sock,16)
    if(length):
        stringData = recvall(sock, int(length))
        data = numpy.fromstring(stringData, dtype='uint8')
        
        decimg=cv2.imdecode(data,1)
        
    cv2.imshow('Client',decimg)

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        end = True

sock.close()
cv2.destroyAllWindows() 
