import requests

import numpy as np
from scipy.spatial import distance

def de(x,y):
    return distance.euclidean(x,y)

class Filali_KNN_Classifier():

    def fit(self,x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

    def predict(self, x_test):
        predictions=[]
        for x in x_test :
            l=self.plusProche(x)
            predictions.append(l)
        return predictions

    def plusProche(self,x):
        distMin = de(x, self.x_train[0])
        mi=0
        for i in range(1,len(self.x_train)):
            dist=de(x, self.x_train[i])
            if dist < distMin :
                distMin = dist
                mi = i
        return self.y_train[mi]

def ethique(N):
    if N in ["maimouni","El maimouni","elmaimouni","El Maimouni"]:
        return 0
    else:
        return np.random.random_sample()*100