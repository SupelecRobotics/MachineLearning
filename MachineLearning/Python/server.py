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

TCP_IP = ''
TCP_PORT = 5003

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)
conn, addr = s.accept()

end  = False

cv2.namedWindow('SERVER')

while(not end):

    length = recvall(conn,16)
    stringData = recvall(conn, int(length))
    data = numpy.fromstring(stringData, dtype='uint8')

    decimg=cv2.imdecode(data,1)
    cv2.imshow('SERVER',decimg)

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        end = True

s.close()
cv2.destroyAllWindows() 
