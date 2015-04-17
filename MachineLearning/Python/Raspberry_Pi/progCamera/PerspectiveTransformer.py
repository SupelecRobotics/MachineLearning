import pickle
import numpy as np
import cv2

class PerspectiveTransformer:

    # Classe qui gère la transformation entre les coordonnées d'un point sur une frame
    # et ses coordonnées réelles sur la table.
    # Charge ses paramètres depuis le fichier PerspectiveTransformer.dat, lui-même créé par le programme perspectiveCalibration.py
    

    def loadParamFromFile(self):
        with open('PerspectiveTransformer.dat', 'r') as file:
            depickler = pickle.Unpickler(file)
            data = depickler.load()
            frameRefPoints = np.float32(data[0])
            tableRefPoints = np.float32(data[1])
            self.M,_ = cv2.findHomography(frameRefPoints, tableRefPoints, cv2.RANSAC,5.0)

    def transform(self, srcPoints):
        if(srcPoints.size > 0):
            tab = cv2.perspectiveTransform(srcPoints.reshape(-1,1,2),self.M)[0].tolist()
            for i in range(0,len(tab)):
                if(tab[i][0] < 0 or tab[i][0] >= 2000 or tab[i][1] < 0 or tab[i][1] >= 3000):
                    del tab[i]
            return tab
        else:
            return None
