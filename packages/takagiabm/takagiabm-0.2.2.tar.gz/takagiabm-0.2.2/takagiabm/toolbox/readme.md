这个文件夹的内容是一些处理相关的算法。
####taktimecounter.py
计时器类
#### typeutils.py
是一些涉及类型的转换算法，比如说颜色的字符串与元组之间的互化。
#### looks.py
一些agent的形状和颜色。
#### kinematics.py
运动学的内容，比如矩阵的旋转、加减法等。使用了numba进行速度优化。
#### numbaUtils.py
关于numba的一些调用，比如定义了一个叫jit的假函数，用来在没装numba的时候也不报错。
#### randomevents.py
这个是一些随机的事件，可以按照某种随机规律返回布尔数值，从而决定agent是否干某件事情。