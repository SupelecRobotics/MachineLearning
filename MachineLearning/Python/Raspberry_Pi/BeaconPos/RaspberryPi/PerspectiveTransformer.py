import pickle
import numpy as np
import cv2

MR = 40

class PerspectiveTransformer:

    def __init__(self,color):

        self.TABLE_W = 2000
        self.TABLE_H = 3000
        
        with open('RefPoints_' + color + '.dat','r') as file:
            depickler = pickle.Unpickler(file)
            refPoints = depickler.load()

        with open('PerspectivePoints.dat','r') as file:
            depickler = pickle.Unpickler(file)
            points = depickler.load()

        for i in range(0, len(refPoints)):

            if(i >= len(points)):
                del refPoints[i]
            elif(points[i] is None):
                del points[i]
                del refPoints[i]

        if(len(refPoints) < 4):
            raise Exception('Not enough ref points !')
        self.M = cv2.findHomography(np.float32(points), np.float32(refPoints), cv2.RANSAC, 5.0)[0]

    def transform(self, srcPoints):
        if(srcPoints.size > 0):
            tab = cv2.perspectiveTransform(srcPoints.reshape(-1,1,2),self.M)[0].tolist()
            for i in range(0,len(tab)):
                tab[i][1] -= MR
                if(tab[i][0] < 0 or tab[i][0] >= self.TABLE_W or tab[i][1] < 0 or tab[i][1] >= self.TABLE_H):
                    del tab[i]
            return tab
        else:
            return None
