import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)

ret = False

while(not ret):
    ret,frame = cap.read()

cv2.imshow("Test", frame)
frame = frame[:,:,::-1]
plt.imshow(frame)
plt.show()
cv2.waitKey(0)

cap.release()
