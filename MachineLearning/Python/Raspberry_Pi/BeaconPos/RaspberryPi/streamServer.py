import socket
import numpy as np
import cv2

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

TCP_IP = ''
TCP_PORT1 = 5003

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s1.bind((TCP_IP, TCP_PORT1))
s1.listen(True)
conn1, addr1 = s1.accept()

cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 600)

encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

try:
    while(cap.isOpened()):
        ret,frame = cap.read()
        if(ret):
            result, imgencode = cv2.imencode('.jpg', frame, encode_param)
            data = np.array(imgencode)
            stringData = data.tostring()
            conn1.send( str(len(stringData)).ljust(16))
            conn1.send( stringData )
        
except (KeyboardInterrupt, SystemExit):
    cap.release()
    s1.close()
    conn1.close()
