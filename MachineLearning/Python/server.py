import socket
import cv2
import numpy

TCP_IP = ''
TCP_PORT = 5001

cap = cv2.VideoCapture(0)
cap.set(CV_CAP_PROP_FRAME_WIDTH, 800)
cap.set(CV_CAP_PROP_FRAME_HEIGTH, 600)

encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)
conn, addr = s.accept()

end  = False

while(cap.isOpened() and not end):

    ret,frame = cap.read()
    if(ret):
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()
        conn.send( str(len(stringData)).ljust(16))
        conn.send( stringData )

s.close()
