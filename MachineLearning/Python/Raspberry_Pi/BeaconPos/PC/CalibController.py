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
        self.ratioParams = []

    def connectLAN(self):
        self.beaconPos.connectLAN('192.168.2.2')
        if(self.beaconPos.isConnected()):
            self.ratioParams = self.beaconPos.getRatioParams()
            tolMin, tolMax = self.ratioParams[self.statusWindow.getSelectedRobType()]
            self.paramWindow.setRatioTol(tolMin, tolMax)
            
            self.colorParams = self.beaconPos.getColorParams()
            HSV = self.colorParams[self.statusWindow.getSelectedRobType()]
            self.paramWindow.setHSV(HSV[0], HSV[1])
            self.statusWindow.setRefPoints(self.beaconPos.getRefPoints())

    def sendColorParams(self):

        self.colorParams[self.statusWindow.getSelectedRobType()] = self.paramWindow.getHSV()

        self.beaconPos.setColorParams(self.colorParams)

    def sendRatioParams(self):

        self.ratioParams[self.statusWindow.getSelectedRobType()] = self.paramWindow.getRatioTol()

        self.beaconPos.setRatioParams(self.ratioParams)
                       

    def sendPerspectiveParams(self):

        points = self.streamWindow.getPoints()

        if(len(points) >= 4):
            self.beaconPos.setPoints(points)

    def loadColorParams(self):

        self.colorParams = self.beaconPos.getColorParams()
        selectedRobType = self.statusWindow.getSelectedRobType()
        self.paramWindow.setHSV(self.colorParams[selectedRobType][0],self.colorParams[selectedRobType][1])

    def loadRatioParams(self):

        self.ratioParams = self.beaconPos.getRatioParams()
        selectedRobType = self.statusWindow.getSelectedRobType()
        self.paramWindow.setRatioTol(self.ratioParams[selectedRobType][0],self.ratioParams[selectedRobType][1])

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
        self.ratioParams[selectedRobType] = self.paramWindow.getRatioTol()

        self.statusWindow.selectNextRobType()

        selectedRobType = self.statusWindow.getSelectedRobType()

        self.paramWindow.setHSV(self.colorParams[selectedRobType][0],self.colorParams[selectedRobType][1])
        self.paramWindow.setRatioTol(self.ratioParams[selectedRobType][0],self.ratioParams[selectedRobType][1])


    def selectPrevRobType(self):

        selectedRobType = self.statusWindow.getSelectedRobType()

        self.colorParams[selectedRobType] = self.paramWindow.getHSV()
        self.ratioParams[selectedRobType] = self.paramWindow.getRatioTol()

        self.statusWindow.selectPrevRobType()

        selectedRobType = self.statusWindow.getSelectedRobType()

        self.paramWindow.setHSV(self.colorParams[selectedRobType][0],self.colorParams[selectedRobType][1])
        self.paramWindow.setRatioTol(self.ratioParams[selectedRobType][0],self.ratioParams[selectedRobType][1])

    def toggleFreezeImg(self):
        self.streamWindow.toggleFreeze()

    def connectBluetooth(self):

        self.beaconPos.connectBluetooth()

    def disconnectLAN(self,mode):

        self.beaconPos.disconnectLAN(mode)

