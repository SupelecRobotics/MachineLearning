import numpy as np
import cv2
import StreamWindow
import ParamWindow
import StatusWindow
import CalibController
import BeaconPos
from keyHandling import handleKey
import time

print "Start"

streamWindow = StreamWindow.StreamWindow()
paramWindow = ParamWindow.ParamWindow()
beaconPos = BeaconPos.BeaconPos()
statusWindow = StatusWindow.StatusWindow(beaconPos)
calibController = CalibController.CalibController(streamWindow, beaconPos, paramWindow, statusWindow)

streamWindow.setBeaconPos(beaconPos)
streamWindow.setParamWindow(paramWindow)
streamWindow.setStatusWindow(statusWindow)

end = False

while(not end):

    streamWindow.update()
    statusWindow.update()

    end = handleKey(cv2.waitKey(1) & 0xFF, calibController)

cv2.destroyAllWindows()
