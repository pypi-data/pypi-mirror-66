# 教程

注意：

1、以下示例若有脱离代码的独立语句，请默认已经执行过了import takagiabm as tak这一语句。

2、示例基于普通的python解释器，使用PyPy的朋友们可以酌情更改。

## 基础例子：
### 用不到四十行（含空行和注释行）代码写一个兰顿蚂蚁。
注：去除注释和空行，实际代码量大约30行。

兰顿蚂蚁是由克里斯托夫·兰顿提出的[细胞自动机](https://baike.baidu.com/item/%E7%BB%86%E8%83%9E%E8%87%AA%E5%8A%A8%E6%9C%BA/2765689)的例子。它由克里斯托夫·兰顿在1986年提出，它由黑白格子和一只“蚂蚁”构成，是一个二维[图灵机](https://baike.baidu.com/item/%E5%9B%BE%E7%81%B5%E6%9C%BA)。兰顿蚂蚁拥有非常简单的逻辑和复杂的表现。在2000年兰顿蚂蚁的[图灵完备性](https://baike.baidu.com/item/%E5%9B%BE%E7%81%B5%E5%AE%8C%E5%A4%87%E6%80%A7)被证明。兰顿蚂蚁的想法后来被推广，比如使用多种颜色。

在平面上的正方形格被填上黑色或白色。在其中一格正方形有一只“蚂蚁”。它的头部朝向上下左右其中一方。

若蚂蚁在黑格，右转90度，将该格改为白格，向前移一步；

若蚂蚁在白格，左转90度，将该格改为黑格，向前移一步。

很多时，蚂蚁刚刚开始时留下的路线都会有接近对称、像是会重复。但不论起始状态如何，蚂蚁的路线必然是无限长的。

—— 百度百科“兰顿蚂蚁”



#### 分析需求。

这个例子包含以下两个含义：

1、实现一只蚂蚁，每次会爬行一格，遇到白色方格就向右转，遇到黑色方格就向左转。

2、遇到白色方格就把格子变成黑的，遇到黑色方格就把格子变成白的。

因此我们需要这样定义：

1、首先定义一个可以旋转、前进的，且有方向性的Agent。前面的简介中已经提到过，可以让Agent旋转的网格被称为自由网格，相应的模型被称为GridModel，上面的Agent被称为GridAgent,网格的每一个小格子也是一个Agent，只不过不能移动，被称为Cell。

2、Agent需要将自己目前所在的格子换个颜色。

首先，我们要先导入相应的模块：

#### 导入包

```python
import numpy as np
import takagiabm as tak
```
接下来就是编写主要内容了。

#### 创建模型初始化函数

为了初始化我们的蚂蚁Agent，我们需要编写一个函数，创建一个蚂蚁，并且将蚂蚁添加到当前的模型网格中去。代码如下：

```python
def agentSetup(model):
    for i in range(1):
        a = tak.GridAgent(np.array([int(model.width / 2), int(model.height / 2)]))
        triangle2 = tak.scale(tak.takTriangle, 3)  # 设置形状为takagi库的三角形，缩放比例为3.
        a.setShape(triangle2)  # 设置形状为三角形。
        a.setSpeed(np.array([1, 0]))  # 设置速度。
        a.setColor(tak.red)  # 设置颜色
        model.addAgent(a)
```
以上代码的含义是：

a = tak.GridAgent(np.array([int(model.width / 2), int(model.height / 2)]))：创建一个代理人Agent代表蚂蚁，并将它放在网格中心。

triangle2 = tak.scale(tak.takTriangle, 3)  ： 设置形状为takagi库的三角形，缩放比例为3.

a.setShape(triangle2)  # 设置形状为triangle2

a.setSpeed(np.array([1, 0]))  # 设置a的初始速度，方向为向x轴正方向。

a.setColor(tak.red)设置颜色为红色

model.addAgent(a):将刚刚创建的小蚂蚁添加到模型中。

注意这个函数传进去了一个参数model，这个model代表的就是仿真模型，它负责管理所有的Agent和Cell，以及收集仿真数据，计算仿真结果等。

#### 创建Agent连续执行的函数

```python

def agentLoop(agent):  # 代理人(也就是蚂蚁)执行的函数
    global stat
    color = agent.getCellColor()

    if (color == tak.white):
        agent.setCellColor(tak.black)
        agent.turn('RIGHT')
    else:
        agent.setCellColor(tak.white)
        agent.turn('LEFT')
    agent.move()
```

这一步应该很清楚了，就是Agent一次一次的获取单元格的颜色，然后如果颜色是白色就将颜色设置为黑色并向右转，黑色相反。

最后调用了一步agent.move(),意思是让agent移动。当没有任何参数传入时，这个函数的意思是保持已经设置好的速度移动一次。

比如刚开始时蚂蚁的速度是[1,0]，且它在白色的格子上，所以下一时刻就要向右转，上面的语句”agent.turn('RIGHT')“得到执行，所以其速度就被设为了[0,-1]，调用agent.move()之后,便往下移动了一格。

#### Agent和Model的初始化：

```python
tak.GridAgent = tak.prepareAgent(tak.GridAgent, agentLoop)
tak.GridModel = tak.prepareModel(tak.GridModel, modelInitFunc=agentSetup, width=100, height=100,
                                 agentActivationPolicy='casual')
```



这两句的意思就是，初始设定模型的参数。参数的含义如下：

```python
tak.prepareAgent(agentClass=None, agentStepFunc=None, agentOnClicked=None)->agentClass
```

意思是设置Agent的属性。

在这里我们用到了:

agentClass,也就是传入这个函数的tak.GridAgent;

另外agentStepFunc的意思就是Agent在仿真的每一步都会执行的动作函数，对应的就是我们刚刚定义好的agentLoop函数。

另一个函数是设置Model属性的。

```python
tak.prepareModel(modelClass=None,
                 varList=[],
				 dataCounterList=[], 
				 width=34, height=34,
                 agentActivationPolicy='casual', 
                 cellActivationPolicy='casual',
                 bgcolor='#000000',
                 modelInitFunc=None, wrapPolicy=None)->modelClass:
```
目前我们只用到了设置模型网格的宽度、高度（都是100），还有模型初始化时、只执行一次的函数modelInitFunc,也就是我们定义的agentSetup这个函数；以及agent的激活策略agentActivationPolicy，选择‘casual’.

激活策略一共有三种选项：”none“,'casual'和'random'，分别代表不激活、随意激活（按照乱序，不分先后，但是也不是随机）和随机激活。默认为'casual'。在此示例中只有一个Agent,无所谓先后顺序，因此选用‘casual’就可以了。

#### 启动仿真

```python
if __name__ == "__main__":
    tak.simStart(__file__, tak.GridModel)  
```

这个方法同时启动了图形界面。输入参数就是tak.GridModel,还有一个系统保留的变量\__file__，意思是代表当前文件的路径。在自动重新加载的时候会用得到这个变量。

点击运行，我们就能看到以下界面：

![1587569066226](src/兰顿蚂蚁教程)



中间位置就是我们的蚂蚁了。点击左上角，就可以开始仿真了。

完整代码如下：



```
'''
简明版兰顿蚂蚁示例。
作者：侯展意
协议：木兰2.0
'''

import numpy as np
import takagiabm as tak


def agentSetup(model):
    for i in range(1):
        a = tak.GridAgent(np.array([int(model.width / 2), int(model.height / 2)]))
        triangle2 = tak.scale(tak.takTriangle, 3)  # 设置形状为takagi库的三角形，缩放比例为3.
        a.setShape(triangle2)  # 设置形状为三角形。
        a.setSpeed(np.array([1, 0]))  # 设置速度。 
        a.setColor(tak.red)  # 设置颜色
        model.addAgent(a)


def agentLoop(agent):  # 代理人(也就是蚂蚁)执行的函数
    global stat
    color = agent.getCellColor()

    if (color == tak.white):
        agent.setCellColor(tak.black)
        agent.turn('RIGHT')
    else:
        agent.setCellColor(tak.white)
        agent.turn('LEFT')
    agent.move()


tak.GridAgent = tak.prepareAgent(tak.GridAgent, agentLoop)
tak.GridModel = tak.prepareModel(tak.GridModel, modelInitFunc=agentSetup, width=100, height=100,
                                 agentActivationPolicy='casual')
if __name__ == "__main__":
    tak.simStart(__file__, tak.GridModel)  # 这个方法同时启动了图形界面。

```



## 设置颜色、形状、大小

### 调用自带颜色
takagi自带一些常用颜色。使用方法如下表：
```python
agent=GridAgent()
agent.setColor(tak.red)
```
可以调用的颜色列在下面：
red,green,blue,black,white,yellow,magenta(紫色),pink,orange。
### 自定义颜色
实际上，上文中的内置颜色，只是字符串类型的全局变量而已。若对这些颜色效果不满意，也可以这样做：
```python
agent=GridAgent()
agent.setColor("#456fac")
```
就可以设置心仪的颜色了。

### 设置形状及其缩放
takagi自带了一些常用形状，目前有三角形、正方形、箭头三种，名字分别为takTriangle、takRectangle和takArrow。  

与颜色相比，多了一个前缀“tak”。 

takTriangle的优点是形状清晰、节省计算资源。盖因takTriangle是三个顶点，另两个形状都是四个顶点。

至于缩放可以调用tak.scale(shape,ratio)。第一个数是形状，第二个数是比例。如果比例大于1就是放大，小于1就是缩小。   


使用方法如下：    

```python
agent=GridAgent()
triangle=tak.takTriangle
enlargedTriangle=tak.scale(tak.takTriangle,2.0)
agent.setShape(enlargedTriangle)
```

### 自定义形状
tak的各种形状实际上都是np.ndarray类型的数组——n行，2列。   

可以自定义形状的每个基点，保存在一个np.ndarray矩阵中。这是一个n行2列的矩阵，每行的两个元素分别是某个顶点的横纵坐标。   

形状的轮廓从矩阵第一行代表的点开始，向下顺次连接每一行代表的点，直到最后一行代表的点，再连接到第一行代表的点，一笔画完即可。  

形状的中心是（0.5,0.5），范围是一个从（0,0）到（1,1）的正方形，允许稍微超出。       

旋转和缩放都以（0.5,0.5）这个点为中心进行操作。形状的正方向指向y轴正方向，也就是沿着(0,1)的方向。  
例如绘制三角形的轮廓，就是这样的：   

takTriangle=np.array([[0.2,0],[0.5,1.2],[0.8,0]])   

箭头：

takArrow=np.array([[0.5,1],[0.1,0],[0.5,0.3],[0.9,0]])

## 目前还不能插入图片。

