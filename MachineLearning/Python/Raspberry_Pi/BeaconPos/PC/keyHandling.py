import numpy as np
import cv2

def handleKey(key, calibController):

    if(key == 27):
        calibController.disconnectLAN(0)
        return True
    else:
        if(key == ord('c')):
            calibController.connectLAN()
        elif(key == ord('o')):
            calibController.sendColorParams()
            calibController.sendRatioParams()
        elif(key == ord('p')):
            calibController.sendPerspectiveParams()
        elif(key == ord('l')):
            calibController.loadColorParams()
            calibController.loadRatioParams()
        elif(key == ord('m')):
            calibController.loadPerspectiveParams()
        elif(key == ord('z')):
            calibController.selectNextRobType()
        elif(key == ord('s')):
            calibController.selectPrevRobType()
        elif(key == ord('d')):
            calibController.selectNextRefPoint()
        elif(key == ord('q')):
            calibController.selectPrevRefPoint()
        elif(key == ord(' ')):
            calibController.toggleFreezeImg()
        elif(key == ord('b')):
            calibController.connectBluetooth()
        elif(key == ord('x')):
            calibController.disconnectLAN(1)
        return False
        
