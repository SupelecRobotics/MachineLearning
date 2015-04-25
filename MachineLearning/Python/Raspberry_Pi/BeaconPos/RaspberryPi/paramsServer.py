import socket
import numpy as np
import cv2
import pickle

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

TCP_IP = ''
TCP_PORT2 = 5004

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s2.bind((TCP_IP, TCP_PORT2))
s2.listen(True)
conn2, addr2 = s2.accept()

try:
    while(True):        
        length = recvall(conn2,16)
        if(length != 0):
            inData = recvall(conn2, int(length))
            print inData
            
except (KeyboardInterrupt, SystemExit):
    s2.close()
    conn2.close()
