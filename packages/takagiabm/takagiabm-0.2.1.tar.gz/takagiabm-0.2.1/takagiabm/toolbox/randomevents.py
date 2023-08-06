'''

命名规则：
rand代表随机的，一般是均匀分布。
possion代表泊松分布

Int代表整数，bool代表布尔型

Succ....Generator代表一连串的随机变量，含有这个的都是类，不是函数。

'''
import numpy as np

try:
    from numba import jit
except:
    from takagiabm.toolbox.numbaUtils import fakeJit

    jit = fakeJit


@jit
def randBool(trueProb):
    '''
    返回一个boolean(也就是True或者False)。当trueProb=0.8的时候，有80%的概率返回True。适合判断概率事件。
    '''
    if (0 <= trueProb <= 1):
        if (np.random.rand() < trueProb):
            return True
        else:
            return False
    else:
        raise Exception('randomBoolean（trueProb）只支持0<=trueProb<=1的数，而你输入的数是%f' % trueProb)


@jit
def possionInt(lamda):
    '''
    返回一个服从泊松分布的整数，常用于排队论等场合下。
    '''
    x1 = np.random.poisson(lam=lamda)
    # print(x1)
    return x1


class SuccPossionBoolGenerator():
    '''
    连续生成bool型的变量，其中的True服从泊松分布。常用于排队论相关的问题。
    '''

    def __init__(self, lamda):
        self.lamda = lamda
        self.timeToNext = 0

    def genBoolean(self):
        '''
        生成当前的boolean量
        '''
        if (self.timeToNext <= 0):
            self.timeToNext = possionInt(self.lamda)
            return True
        else:
            self.timeToNext -= 1
            return False


randomChoice = randBool
if __name__ == '__main__':
    s=SuccPossionBoolGenerator(lamda=5)
    for i in range(100):
        print(s.genBoolean())

    print(s)
