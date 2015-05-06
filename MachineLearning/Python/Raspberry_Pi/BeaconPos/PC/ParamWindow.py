import numpy as np
import cv2


class ParamWindow:

    def __init__(self):
        
        cv2.namedWindow('Params', cv2.WINDOW_NORMAL)
        cv2.createTrackbar('Hmin', 'Params', 0, 179, self.nothing)
        cv2.createTrackbar('Hmax', 'Params', 0, 179, self.nothing)
        cv2.createTrackbar('Smin', 'Params', 0, 255, self.nothing)
        cv2.createTrackbar('Smax', 'Params', 0, 255, self.nothing)
        cv2.createTrackbar('Vmin', 'Params', 0, 255, self.nothing)
        cv2.createTrackbar('Vmax', 'Params', 0, 255, self.nothing)

        cv2.createTrackbar('Rmin', 'Params', 0, 100, self.nothing)
        cv2.createTrackbar('Rmax', 'Params', 100, 200, self.nothing)

        cv2.setTrackbarPos('Hmax', 'Params', 179)
        cv2.setTrackbarPos('Smax', 'Params', 255)
        cv2.setTrackbarPos('Vmax', 'Params', 255)

        cv2.setTrackbarPos('Rmin', 'Params', 0)
        cv2.setTrackbarPos('Rmax', 'Params', 200)

    def nothing(self, x):
        pass

    def getHSV(self):
        
        lowHSV = [cv2.getTrackbarPos('Hmin', 'Params'),
                  cv2.getTrackbarPos('Smin', 'Params'),
                  cv2.getTrackbarPos('Vmin', 'Params')]
        
        highHSV = [cv2.getTrackbarPos('Hmax', 'Params'),
                   cv2.getTrackbarPos('Smax', 'Params'),
                   cv2.getTrackbarPos('Vmax', 'Params')]

        return lowHSV, highHSV

    def setHSV(self, lowHSV, highHSV):

        cv2.setTrackbarPos('Hmin', 'Params', lowHSV[0])
        cv2.setTrackbarPos('Smin', 'Params', lowHSV[1])
        cv2.setTrackbarPos('Vmin', 'Params', lowHSV[2])
        
        cv2.setTrackbarPos('Hmax', 'Params', highHSV[0])
        cv2.setTrackbarPos('Smax', 'Params', highHSV[1])
        cv2.setTrackbarPos('Vmax', 'Params', highHSV[2])

    def getRatioTol(self):

        tolMin = cv2.getTrackbarPos('Rmin', 'Params')
        tolMax = cv2.getTrackbarPos('Rmax', 'Params')

        return tolMin,tolMax

    def setRatioTol(self, tolMin, tolMax):

        cv2.setTrackbarPos('Rmin', 'Params', tolMin)
        cv2.setTrackbarPos('Rmax', 'Params', tolMax)
