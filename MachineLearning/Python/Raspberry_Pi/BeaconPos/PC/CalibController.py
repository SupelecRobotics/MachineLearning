import numpy as np
import cv2

NB_ROB_TYPES = 4

class CalibController:

    def __init__(self, streamWindow, beaconPos, paramWindow, statusWindow):

        self.refPoints = []

        self.streamWindow = streamWindow
        self.beaconPos = beaconPos
        self.paramWindow = paramWindow
        self.statusWindow = statusWindow

        self.colorParams = []

        self.selectedRobType = 0

    def connectLAN(self):
        self.beaconPos.connectLAN('192.168.2.2')
        if(self.beaconPos.isConnected()):
            self.colorParams = self.beaconPos.getColorParams()
            HSV = self.colorParams[self.selectedRobType]
            self.paramWindow.setHSV(HSV[0], HSV[1])
            self.statusWindow.setRefPoints(self.beaconPos.getRefPoints())

    def sendColorParams(self):

        self.colorParams[self.selectedRobType] = self.paramWindow.getHSV()

        self.beaconPos.setColorParams(self.colorParams)
                       

    def sendPerspectiveParams(self):

        points = self.streamWindow.getPoints()

        if(len(points) >= 4):
            self.beaconPos.setPoints(points)

    def loadColorParams(self):

        colorParams = self.beaconPos.getColorParams()
        self.paramWindow.setHSV(colorParams[self.selectedRobType][0],colorParams[self.selectedRobType][1])

    def loadPerspectiveParams(self):
        self.statusWindow.setRefPoints(self.beaconPos.getRefPoints())
        self.streamWindow.setPoints(self.beaconPos.getPoints())

    def selectNextRefPoint(self):

        self.statusWindow.selectNextRefPoint()

    def selectPrevRefPoint(self):

        self.statusWindow.selectPrevRefPoint()

    def selectNextRobType(self):

        selectedRobType = self.statusWindow.getSelectedRobType()

        self.colorParams[selectedRobType] = self.paramWindow.getHSV()

        self.statusWindow.selectNextRobType()

        self.paramWindow.setHSV(self.colorParams[self.selectedRobType][0],self.colorParams[self.selectedRobType][1])


    def selectPrevRobType(self):

        selectedRobType = self.statusWindow.getSelectedRobType()

        self.colorParams[selectedRobType] = self.paramWindow.getHSV()

        self.statusWindow.selectPrevRobType()

        self.paramWindow.setHSV(self.colorParams[self.selectedRobType][0],self.colorParams[self.selectedRobType][1])

    def toggleFreezeImg(self):
        self.streamWindow.toggleFreeze()

