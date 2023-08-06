import numpy as np
'''
这里是一个模板，可以放大、缩小。
'''
takCenterPoint=np.array([0.5,0.5])
def scale(shape:np.ndarray,factor:float):
    tmpShape=shape-takCenterPoint
    tmpShape=tmpShape*factor
    tmpShape=tmpShape+takCenterPoint
    return tmpShape
takTriangle=np.array([[0.2,0],[0.5,1.2],[0.8,0]])
takRectangle=np.array([[0,0],[1,0],[1,1],[0,1]])


red = '#ff0000'
green = '#00ff00'
blue = '#0000ff'
black='#000000'
white='#ffffff'
yellow='#ffff00'
magenta='#ff00ff'
pink='#ff69b4'
orange='#ffa500'