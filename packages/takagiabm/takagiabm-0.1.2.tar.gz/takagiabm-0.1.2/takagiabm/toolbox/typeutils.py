import numpy as np
def getColorArr(value='#ffffff') -> np.ndarray:  # pos或者wh的输入都是tuple
    #print('pos',pos)
    # if (type(pos) != np.ndarray):
    #     #self.cells[pos[1]][pos[0]].getColor()
    #     raise Exception("必须选定以位置pos=np.ndarray(x:int,y:int)之一作为索引,类别为np.ndarray。")

    digit = list(map(str, range(10))) + list("abcdef")
    value = value.lower()
    a1 = (digit.index(value[1]) * 16 + digit.index(value[2])) / 256.0
    a2 = (digit.index(value[3]) * 16 + digit.index(value[4])) / 256.0
    a3 = (digit.index(value[5]) * 16 + digit.index(value[6])) / 256.0
    return np.array([a1, a2, a3])