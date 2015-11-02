import time
import numpy as np
import cv2

TABLE_W = 2000
TABLE_H = 3000

table = cv2.imread('schema_table2.png')
cv2.imshow('Table',table)
h,w = table.shape[:2]
file = open('camLog.txt','r')

for line in file:
    frame = table.copy()
    line = line.strip()
    if("Exiting" not in line):
        point = eval(line)
        if(point is not None):
            x = int(point[0] * w / TABLE_W)
            y = int(point[1] * h / TABLE_H)
            cv2.circle(frame,(x,y),5,(255,255,255),2)
    cv2.imshow('Table',frame)
    cv2.waitKey(1)


cv2.destroyAllWindows()
file.close()
