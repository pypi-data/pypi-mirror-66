import numpy as np

try:
    from numba import jit
except:
    from takagiabm.toolbox.numbaUtils import fakeJit
    print('jit')
    jit = fakeJit

digit=list('0123456789abcdef')


def convert(c):
    v=ord(c)
    if(48<=v<=57):
        return v-48
    else:
        return v-87# 返回a的值。

def ifColorArrEqual(color1,color2):

    if (-0.00390625<color1[0]-color2[0]<=0.00390625)&(-0.00390625<color1[1]-color2[1]<=0.00390625)&\
        (-0.00390625<color1[2]-color2[2]<=0.00390625):
        return True
    else:
        return False

@jit
def ifColorEqual2(color1,color2):
    c=color1-color2
    for i in c:
        if(i<-0.00390625)|(i>0.00390625):
            return False
    return True
# )
#     if (<c[0]<=0.00390625)&(-0.00390625<color1[1]-color2[1]<=0.00390625)&\
#         (-0.00390625<color1[2]-color2[2]<=0.00390625):
#         return True
#     else:
#         return False

def ifstrequal(s1,s2):
    if(s1==s2):
        return True
    else:
        return False
def getColorArr(value='#ffffff') -> np.ndarray:  # pos或者wh的输入都是tuple
    value = value.lower()
    c0=convert(value[1])
    c1=convert(value[2])
    c2=convert(value[3])
    c3=convert(value[4])
    c4=convert(value[5])
    c5=convert(value[6])
    a1 = (c0 * 16 + c1) / 256.0
    a2 = (c2* 16 + c3) / 256.0
    a3 = (c4 * 16 + c5) / 256.0

    return np.array([a1, a2, a3])

def getColorList(value='#ffffff') -> np.ndarray:  # pos或者wh的输入都是tuple
    value = value.lower()
    c0=convert(value[1])
    c1=convert(value[2])
    c2=convert(value[3])
    c3=convert(value[4])
    c4=convert(value[5])
    c5=convert(value[6])
    a1 = (c0 * 16 + c1) / 256.0
    a2 = (c2* 16 + c3) / 256.0
    a3 = (c4 * 16 + c5) / 256.0

    return [a1, a2, a3]

if __name__=='__main__':
    import time

    m1=[0,0,0]
    m2=[0.00001,0.000,0.1]
    ifColorArrEqual(m1, m2)
    t0 = time.time()
    for i in range(100000):
        a=ifColorArrEqual(m1,m2)
    t1=time.time()
    s1='#ffffff'
    s2='#aaaaaa'
    for i in range(100000):
        a=ifstrequal(s1,s2)
    t2=time.time()
    print(t1-t0,t2-t1)