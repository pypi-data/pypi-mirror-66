# Python的基于主体建模的仿真库——TakagiABM ！

Talented  ABM Kit for Python
## 简介：
### 一些闲话
在正式开始文档之前，我想分享一个我本人的故事。

相信很多熟悉Python等高级语言却又想做网络仿真的朋友们一定对NetLogo这种语言有不小的“腹诽“吧。正如知乎上一位记不住名字的大神说得好，NetLogo语法简单，但是怕就怕在你学过C, Java, Python之类的这些语言 (oVo)...巧了，我刚好只会这三种。

又有一位大佬说：你要学会NetLogo，首先要把其他高级语言都忘掉……但是我为什么要把他们忘掉，尽管现在我是机械专业，但是以后指不定要靠他们吃饭啊。

于是我就试着不忘记亲爱的Python，想着用NetLogo的方式来解决问题。可是自己看不懂教程。好不容易会了一点，写Python的时候,又觉得什么ask啊，turtle啊之类的语句在脑海里挥之不去。实在是爱不起来啊。

Python有一个专用的仿真库名曰MESA，这个库似乎很火爆，在github上有七八十位贡献者，也有数百上千个星标。大家可以搜索一下。
这个库使用的是Python+tornado的后端，使用基于HTML的技术进行显示。技术框架先进，但是显示的刷新速率并不高。

由于Netlogo的语法本人有点不太喜欢，所以为完成网络仿真的作业，本人便重新编写了一个ABD仿真的代码，参考了Netlogo的架构以及一些类似Python 仿真库的API写法。

### 命名原因
此库的名称本来准备叫做Talented ABM Kit,但是tak这三个字母已经被占用了。于是我就想能不能像PIL加三个字母加成pillow一样，加几个字母区分一下，顺便也让这个框架的名字更好读。所以，就成了TakagiABM。  

**注意：此库名称较长，故以下将此库简称为tak.**

### 性能
与MESA不同，tak深度依赖于numpy，对于一般的Python解释器程序（基于cPython），在以50×50单元格的生命游戏为例，在我自己的电脑上，tak用最简单粗暴的写法实现时，每步仿真运算大约0.05秒，而在调用了tak的库函数之后速度可以提升到后者每一步大约0.04秒，速度上略强于MESA，MESA每一步大约0.06～0.07秒；

但是当使用PyPy解释器的时候，由于PyPy不支持PyOpenGL以及PyQt5,所以只能以无界面的方式进行仿真。同样运行生命游戏，MESA只需0.01秒。但是此库需要0.9秒。

以上问题的原因MESA中的网格以Python原生形式储存，以Web作为可视化，所以PyPy跑起来就得心应手；而tak中的位置信息深度依赖于numpy的存储与矩阵运算（为的是进行快速的矩阵运算），且而PyPy对numpy的支持非常差，因此造成了这个速度差距。    


不过，如果你不清楚PyPy是什么的话，只要记住tak多数情况下会比MESA快就好了。   

p.s. 什么?连MESA是什么都不知道吗？这……请参阅这里：  
https://mesa.readthedocs.io/en/master/tutorials/intro_tutorial.html   
这个库在github上非常火爆，有七八十人在贡献这个项目，并且在不断更新。甚至一些刊物上的论文也是用它发的仿真结果。所以如果Python水平高的话，还是推荐用这个库。只是中文资料比较少，或者说……几乎没有?

## 优势

### 语法简单
与MESA相反，每个模型都要把代理对象再继承一下。tak无需面向对象编程的过程，其代码基本都是面向过程的。API的命名和结构参考了Arduino和Scratch，做到尽可能的简单。

### 动态加载
tak的图形界面可以动态加载代码，图形界面启动后，每次重启仿真时都会重新加载一遍仿真代码，无需关闭图形界面再重启，省时省力。MESA也有这样的特性，但是它每次都会自动打开一个新的标签页，改代码还是比较麻烦。

### 中文文档
我目前就读与安全性专业，有一些网络仿真的内容，虽然代码能力一般，但还算比较乐意写文档的。当然对于复杂应用，还是推荐读MESA的文档。
### 交互支持
MESA对鼠标操作图形元素的支持比较一般，但是tak基于PyQt，所以比较擅长交互，对于鼠标和键盘的交互支持更好。尽管这个特征仍在开发中。
### 绘制更快
一方面，tak基于PyOpenGL和PyQtGraph，元素数量较多时运行也比较快；另一方面即使元素较多，可视化界面发生严重卡顿，也不易崩溃。

相反，MESA中，由于浏览器可视化和Python程序之间是异步的，所以浏览器端可视化部分不能绘制过多的元素，否则可能会导致崩溃。




### 安装方式：
```bash
 pip install takagiabm
```
如果有类似报错：
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
ERROR: Could not find a version that satisfies the requirement takagiabm (from versions: none)
ERROR: No matching distribution found for takagiabm

说明国内源可能还没有完成同步。不过，这个库只有几十kb大小，暂时换用官方源也无妨。不过，它依赖的numpy,pyqt5之类的几十MB的大包（numpy ，pyopengl，pyqt5，pyqtgraph  ），还是先用国内源安装好吧。
尝试：

```bash
pip install takagiabm -i https://pypi.org/simple
```
安装好之后运行以下命令：
```bash
python
>>> import takagiabm
>>> takagiabm.help()

您好,欢迎使用TakagiABM仿真库！
请移步https://gitee.com/hzy15610046011/TakagiABM,转到demos文件夹中复制相应的示例文件.
谢谢你的使用！有问题请反馈到邮箱1295752786@qq.com中,欢迎您不吝赐教！
```


说明安装成功！
## 版本及依赖包：
python3及以上版本，且确保支持以下库：
### 仅仿真逻辑：
numpy

最好也安装numba，可以显著提速。

### 需要界面可视化时：
numpy  
pyopengl  
pyqt5  
pyqtgraph    
numba(不是必须，但有比没有强。)



注意，当启动图形界面时，不支持PyPy，盖因PyPy不支持PyQt、PyOpenGL。

可以直接将全项目以zip下载下来，或是克隆下来之后直接运行根目录下的simu.py文件。

## 示例及使用方式介绍

在地址 https://gitee.com/hzy15610046011/TakagiABM/tree/master/demos 中复制代码LantonAnt到你的IDE中，然后直接运行：
```bash
python LantonAnt.py
```

界面启动以后，就可以看到一个兰顿蚂蚁模型。黑白色就是方格，如图所示：
其中红蚂蚁是按照兰顿蚂蚁规律运行的，绿色和蓝色的蚂蚁初始速度向着斜右上方，不是上下左右运动，所以轨迹有所不同。

![ant](src/兰顿蚂蚁.png)
界面左侧显示的是当前所有在界面上移动的代理人的各种信息，比如位置等。对于这个实验，只有一个代理人，就是这只小蚂蚁；和下方的文本栏目暂时无效果。
#### 开始仿真
点击左上角“开始”，拖动滑块即可调整仿真速度。点击以后此按钮文字变为”暂停“. 
点击“重启”，重置仿真。此时仿真文件中的设置项将被重新加载。如果在重启之前修改代码，那么下一次仿真就可以按照此次的设置执行。也就是说，**代码文件支持动态修改**，对于小修小改，无需重新启动图形界面。但是推荐将仿真的相关内容都写在同一个文件里面。
点击“暂停“，可以暂停仿真。此时”暂停“的文字变为”继续“。点击”继续“的时候，仿真继续执行。  
点击”单步“，可以进行单步仿真。  

同样可以进行其他仿真，比如下面的生命游戏（GameOfLife.py中）

![src](src/生命游戏.png)

#### 各项指标的含义
当前步代表当前仿真进行的步数；  

设定步速是滑动条控制的步速；  

实际帧率是显示刷新的实际频率；  

实际步速是模型仿真每秒走过的步数。   

由于模型可以仿真多步刷新一次，所以当设定步速高于最大刷新率（根据网格的大小而定，对于34*34的网格，最大刷新速率大约为55fps）时，模型步速将高于实际帧率。


## 简易教程：
打开兰顿蚂蚁的代码，发现以下内容：
```python
'''
增强版兰顿蚂蚁教程：当速度不是水平竖直的时候，效果如何？
'''
from takagiabm.agent import GridAgent
from takagiabm.model import GridModel
from takagiabm.control import simStart
import numpy as np
import takagiabm.toolbox.looks as shapes
import random


def agentSetup(model):
    colorList = ['#ff0000', '#00ff00', '#0000ff']
    for i in range(3):
        a = GridAgent()
        a.setPos(np.array([int(model.width * random.random()),int(model.height * random.random())]))# 设置其位置。
        triangle2 = shapes.scale(shapes.takTriangle, 3)  # 设置形状为takagi库的三角形，缩放比例为3.
        a.setShape(triangle2)  # 设置形状为三角形。
        a.setSpeed(np.array([1, i]))  # 设置速度。只有第一只蚂蚁速度是水平数值的，因此会有不同的运动规律。
        a.setColor(colorList[i])  # 设置颜色
        model.addAgent(a)


def agentLoop(agent):  # 代理人(也就是蚂蚁)执行的函数
    global stat
    color = agent.getCellColor()

    if (color == '#ffffff'):
        agent.setCellColor('#000000')
        agent.turn('RIGHT')
    else:
        agent.setCellColor('#ffffff')
        agent.turn('LEFT')
    agent.move()


stat = 0
GridAgent.step = agentLoop
GridModel.initAgents = agentSetup
if __name__ == "__main__":
    GridModel.width = 70  # 设置网格宽度
    GridModel.height = 70  # 设置网格高度
    simStart(__file__, GridModel)  # 这个方法同时启动了图形界面。
```
仿真的控制是由仿真模型对象GridModel来完成的。它每走一步，称为仿真前进一步。仿真每前进一步，所有的agent都会被激活一次，也就是调用一下step。

## API&接口教程
对于API,请参阅 [API](https://gitee.com/hzy15610046011/TakagiABM/blob/master/API.md) ，也就是与此readme.md同一目录下的API.md文件。




