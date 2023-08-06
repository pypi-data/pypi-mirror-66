import numpy as np
# from numba import jit

import time
try:

    from numba import njit
except:
    print('检测到未安装numba.如果装有numba,可以让仿真速度更快。')
    from takagiabm.toolbox.numbaUtils import fakeJit
    jit = fakeJit

rotMat = np.array([[0, -1], [1, 0]])
centralPoint=np.array([0.5,0.5])

def getPosOnGrid(pos:np.ndarray):
    return np.floor(pos).astype(int)

def calcTurnMat(dir,arr,speed):
    global rotMat,centralPoint

    speed = dir*np.dot(rotMat, speed.T).T
    vertArray =dir* np.dot(rotMat, arr.T).T + centralPoint
    return speed,vertArray
def calcTurnFloatMat(angle,arr,speed):
    rotMat = np.array([[-np.cos(angle), np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    speed = np.dot(rotMat, speed.T).T
    vertArray = np.dot(rotMat, arr.T).T + centralPoint
    return speed,vertArray
def turnWithVert(dir: int,speed:np.ndarray,vertArray:np.ndarray):
    global rotMat,centralPoint
    arr = vertArray - centralPoint
    if (dir == 'LEFT'):
        return calcTurnMat(1,arr,speed)
    elif (dir == 'RIGHT'):
        return calcTurnMat(-1, arr, speed)
    else:
        return calcTurnFloatMat(dir,arr,speed)
def turnNoVert(self, dir: str):
    global rotMat
    a = centralPoint
    if (dir == 'LEFT'):
        self.speed = np.dot(rotMat, self.speed.T).T
    elif (dir == 'RIGHT'):
        self.speed = -np.dot(rotMat, self.speed.T).T

if __name__ =='__main__':
    n=np.array([1.0, 1], dtype=np.float32)
    m=np.array([[1, 1.0], [2, 2], [3, 3]], dtype=np.float32)
    t0=time.time()
    for i in range(1000):
        a=turnWithVert('LEFT',n,m)
    t1=time.time()

    print(t1-t0)