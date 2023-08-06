import numpy as np
cimport numpy as np
digit=list('0123456789abcdef')
cdef int convert(c):
    v=ord(c)
    if(48<=v<=57):
        return v-48
    else:
        return v-87# 返回a的值。
cpdef np.ndarray getColorArr(value='#ffffff'):  # pos或者wh的输入都是tuple
    value = value.lower()
    cdef int c0,c1,c2,c3,c4,c5
    cdef float a1,a2,a3
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
