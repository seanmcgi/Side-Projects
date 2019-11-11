import random
import pandas as pd
import numpy as np

class NeuralNetwork(object):
    def __init__(self,cont,gens):
        #parameters:
        self.input_size = 7
        self.output_size = 1
        self.hidden_size = 4
        #weights:
        self.W1,self.W2 = init(cont,gens)
        
    def forward(self,X):
        self.z = np.dot(X,self.W1)
        self.z2 = self.sigmoid(self.z)
        self.z3 = np.dot(self.z2,self.W2)
        o = self.sigmoid(self.z3)
        return o

    def sigmoid(self,X):
        return 1/(1+np.exp(-X))

    def Print(self):
        print(self.W1,self.W2)    
        
    def weights(self):
        return self.W1,self.W2

filename = 'weights.csv'


def init(cont,gens):
    df = pd.read_csv(filename)

    arr = np.rot90(df.values)

    W2 = np.array([arr[0]])
    W2 = np.rot90(np.flip(W2))

    W1 = np.array([arr[7],arr[6],arr[5],arr[4],arr[3],arr[2],arr[1]])
    if cont is False:
        rand(W1,W2,gens)
    if df.iat[0,1] <100 and gens > 30 and cont is True:
        print('randomizing', df.iat[0,1],df.iat[1,0])
        gens = 0
        W1 = np.random.randn(7,4)
        W2 = np.random.randn(4,1)
    return W1,W2
    

def rand(W1,W2,gens):
    if gens <20:
        limit = 30
    else:
        limit = 10
    changes = random.randint(0,limit)
    for i in range(0,changes):    
        mat = random.randint(0,1)
        mult = random.randint(0,1)
        val = random.uniform(0,1)
        
        if mat is 1:
            col = random.randint(0,3)
            row = random.randint(0,6)
            if mult is 1:
                W1[row][col] *= val
            else:
                W1[row][col] /= val
        else:
            row = random.randint(0,3)
            if mult is 1:
                W2[row] *= val
            else:
                W2[row] /= val
        


def test(player,rect,vel,time,y,NN):
    dist_right = abs(player[0]-25-rect[0])/600
    dist_top = abs(player[1]-25-rect[3])/500
    dist_left = abs(player[0]+25-rect[1])/600
    dist_bottom = abs(player[1]+25-rect[2])/500
    dist_roof = abs(player[1]+25-y)/500
    dist_floor = abs(player[1]-25)/500
    signal_in = np.array([dist_right,dist_left,dist_top,dist_bottom,dist_roof,dist_floor,vel])
    o = NN.forward(signal_in)
    if o > .5:
        return True
    return False
    


def jump(player,rect1,rect2,vel,time,y,NN):
    if abs(player[0]-rect1[0])<abs(player[0]-rect2[0]):
        return test(player,rect1,vel,time,y,NN)
    return test(player,rect2,vel,time,y,NN)
    

def end(time,NN):
    W1,W2 = NN.weights()

    df = pd.DataFrame({'time':time,
                       'W1a':W1[0],
                       'W1b':W1[1],
                       'W1c':W1[2], 
                       'W1d':W1[3],
                       'W1e':W1[4],
                       'W1f':W1[5],
                       'W1g':W1[6],
                       'W2':np.rot90(W2)[0]
                       })
    df.to_csv(filename)
        
        
    return

def reset():
    W1 = np.random.randn(7,4)
    W2 = np.random.randn(4,1)


    df = pd.DataFrame({'time':0,
                       'W1a':W1[0],
                       'W1b':W1[1],
                       'W1c':W1[2], 
                       'W1d':W1[3],
                       'W1e':W1[4],
                       'W1f':W1[5],
                       'W1g':W1[6],
                       'W2':np.rot90(W2)[0]
                       })
    df.to_csv('weights.csv')
    