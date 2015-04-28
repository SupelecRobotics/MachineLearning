import pickle
import numpy as np
import cv2

class PerspectiveTransformer:

    def __init__(self):

        self.TABLE_W = 2000
        self.TABLE_H = 3000
        
        with open('RefPoints.dat','r') as file:
            depickler = pickle.Unpickler(file)
            refPoints = depickler.load()

        with open('PerspectivePoints.dat','r') as file:
            depickler = pickle.Unpickler(file)
            points = depickler.load()

        self.M = cv2.findHomography(np.float32(points), np.float32(refPoints), cv2.RANSAC, 5.0)[0]

    def transform(self, srcPoints):
        if(srcPoints.size > 0):
            tab = cv2.perspectiveTransform(srcPoints.reshape(-1,1,2),self.M)[0].tolist()
            for i in range(0,len(tab)):
                if(tab[i][0] < 0 or tab[i][0] >= self.TABLE_W or tab[i][1] < 0 or tab[i][1] >= self.TABLE_H):
                    del tab[i]
            return tab
        else:
            return None
