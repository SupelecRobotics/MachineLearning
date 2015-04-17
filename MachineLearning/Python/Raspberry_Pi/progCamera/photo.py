import cv2
import numpy as np

cap = cv2.VideoCapture(0)

ret = False

while(not ret):
    ret,frame = cap.read()

cv2.imwrite('photo.jpg',frame)
        
cap.release()
