import numpy as np
import cv2

WMIN = 10
HMIN = 10

MH = 71
MW = 80

class StreamWindow:

    def mouseCallback(self,event,x,y,flags,param):
        if(self.beaconPos.isConnected()):
            if(event == cv2.EVENT_LBUTTONDOWN):
                selectedRefPoint = self.statusWindow.getSelectedRefPoint()

                if(selectedRefPoint >= len(self.points)):

                    for i in range(len(self.points),selectedRefPoint):
                        self.points.append(None)

                    self.points.append((x,y))
                    self.statusWindow.selectNextRefPoint()
                    
                else:
                    self.points[selectedRefPoint] = (x,y)
                    self.statusWindow.selectNextRefPoint()

                
            elif(event == cv2.EVENT_RBUTTONDOWN):
                selectedRefPoint = self.statusWindow.getSelectedRefPoint()
                if(selectedRefPoint < len(self.points)):
                    self.points[selectedRefPoint] = None
                    self.statusWindow.selectPrevRefPoint()

    def __init__(self):

        self.points = []

        self.frozen = False

        self.cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))

        self.selectColor = True
        
        cv2.namedWindow('Stream')
        cv2.setMouseCallback('Stream', self.mouseCallback, None)
        

    def setBeaconPos(self, beaconPos):

        self.beaconPos = beaconPos

    def setParamWindow(self, paramWindow):

        self.paramWindow = paramWindow

    def setStatusWindow(self, statusWindow):

        self.statusWindow = statusWindow

    def update(self):

        if(self.beaconPos.isConnected()):

            if(self.frozen):
                frame = self.prevFrame.copy()
            else:
                frame = self.beaconPos.getFrame()
                self.prevFrame = frame.copy()

            if(self.selectColor):
                colorParam = self.paramWindow.getHSV()
                ratioTolMin, ratioTolMax = self.paramWindow.getRatioTol()

                ratioMin = (float(ratioTolMin) / float(100)) * float(MW) / float(MH)
                ratioMax = (float(ratioTolMax) / float(100)) * float(MW) / float(MH)
                
                mask = cv2.inRange(frame, np.array(colorParam[0]), np.array(colorParam[1]))

                frame = cv2.bitwise_and(frame, frame, mask = mask)

                # ---------------

                mask = cv2.erode(mask, self.cross)
                contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

                validContours = []

                for cnt in contours:
                    x,y,w,h = cv2.boundingRect(cnt)
                    ratio = float(w) / float(h)
                    if(w > WMIN and h > HMIN and ratio > ratioMin and ratio < ratioMax):
                        validContours.append(cnt)

                # ---------------

                cv2.drawContours(frame, validContours, -1, (0, 255, 0),2)
            

            selectedRefPoint = self.statusWindow.getSelectedRefPoint()

            for i in range(0, len(self.points)):
                if(self.points[i] is not None):
                    if(i == selectedRefPoint):
                        cv2.circle(frame,self.points[i],5,(255,255,255),2)
                    else:
                        cv2.circle(frame,self.points[i],5,(255,0,0),2)
                

        else:
            frame = np.zeros((600,800))
            cv2.putText(frame, 'LAN Disconnected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

        cv2.imshow('Stream', frame)

    def toggleFreeze(self):
        self.frozen = not self.frozen
        

    def getPoints(self):
        return self.points

    def setPoints(self, points):
        self.points = points

    def clearPoints(self):

        self.points = []

    def toggleColorSelect(self):

        self.selectColor = not self.selectColor
