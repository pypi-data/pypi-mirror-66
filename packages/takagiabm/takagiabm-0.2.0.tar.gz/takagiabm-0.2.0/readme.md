# Python的基于主体建模的仿真库——TakagiABM ！

Talented  ABM Kit for Python

## 教程参考

教程请参阅：[教程](https://gitee.com/hzy15610046011/TakagiABM/blob/master/tutorial.md)

## 安装方式：

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
教程请参阅[教程](https://gitee.com/hzy15610046011/TakagiABM/blob/master/tutorial.md)
## 简介：
### 一些闲话
在正式开始文档之前，我想分享一个我本人的故事。

相信很多熟悉Python等高级语言却又想做网络仿真的朋友们一定对NetLogo这种语言有不小的“腹诽“吧。正如知乎上一位记不住名字的大神说得好，NetLogo语法简单，但是怕就怕在你学过C, Java, Python之类的这些语言 (oVo)...巧了，我刚好只会这三种。

Python有一个专用的仿真库名曰MESA，这个库似乎很火爆，在github上有七八十位贡献者，也有数百上千个星标。相比我写的这个库，MESA还是更强大一些，但是上手难度也更大，需要有熟练的面向对象知识，完成相同或相似模型所需的代码量也要大很多，感兴趣的大家可以搜索一下。    

MESA这个库，可视化部分使用的是Python Tornado的后端，使用基于Web进行显示。相比之下技术框架着实先进，可是显示的刷新速率却一般，当绘制元素多的时候，浏览器界面甚至会完全卡住，不受控制。

由于Netlogo的语法本人有点不太喜欢，所以为完成网络仿真的作业，本人便重新编写了一个ABM仿真的代码，参考了Netlogo的架构以及一些类似Python 仿真库的API写法。

### 命名及相关含义
#### 命名
此库的名称本来准备叫做Talented ABM Kit,简称TAK，但是在PyPI上tak这三个字母已经被占用了。于是我就想能不能像PIL加三个字母加成pillow一样，加几个字母区分一下，顺便也让这个框架的名字更好读。      

如果你熟悉日本动漫的话应该知道几个姓Takagi的角色（e.g.,《柯南》里面），不过在这里我指的是山本崇一朗先生画的那位（请看到这里的老哥/老姐多多包涵，若审美观/感情观不同，可以发邮件友好交流或者留言，切勿人身攻击，手动抱拳。）。    

可是，作为中国人，总不能直接整个日本名字当库名吧。所以，我又在后面缀上了一个“ABM”，以明用途，以示区别。

 至于命名的版权问题……应该没问题，毕竟我又不拿这个库赚钱。当然，如果给我发律师函，我改就是了，可是非法所得根本没有，我也没法退啊。

再说了，Python自身的名字也是取自文艺作品——*Monty Python's Flying Circus*这个英国喜剧，也没见版权方找Guido大神的麻烦嘛。虽然水平差的很远很远，但我和这位大神的起名逻辑一样，都是选择了文艺作品名称中的人名。

p.s. 《擅长捉弄的高木同学》的英文译名是*Karakai Jozu no Takagi-san*(罗马音),或者是*Skilled Teaser Tagaki-san*又或者*Teasing Master Takagi-san*。


#### 标识
TakagiABM的标识是一个带有红丝带的草帽。
#### 官方简称
官方建议简称TakagiABM为“tak”，因为这也是这个名字的本义。

```python
import takagiabm as tak
```
在这里皮一下，如果你（像我一样）觉得西片太太天下第一，那么可以采用这些非官方的称谓：

```python
import takagiabm as Takagi
import takagiabm as Mrs_Nishikata
```

但是我个人还是推荐官方的建议简称“tak”，因为简易、省事，不易出错。

**注意：以下的所有文字叙述和代码示例中，都将此库简称为tak.**



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
numba(不是必须，提速优化用。)



注意，当启动图形界面时，不支持PyPy，盖因PyPy不支持PyQt、PyOpenGL。

可以直接将全项目以zip下载下来，或是克隆下来之后直接运行根目录下的simu.py文件。



## 优势

### 语法简单
与MESA相反，每个模型都要把代理对象再继承一下。tak无需面向对象编程的过程，其代码基本都是面向过程的。API的命名和结构参考了MESA（但是项目基础和内部的源码实现机理不同）、Arduino和Scratch，力求尽可能的简单明了。

### 动态加载
tak的图形界面可以动态加载代码，图形界面启动后，每次点击界面上的“重启”按钮时，仿真代码都会在界面不关闭的情况下重新加载，因此支持动态修改自己的仿真参数，无需关闭图形界面再重启，省时省力。

MESA也有这样的特性，但是它每次都会自动打开一个新的标签页，所以说，更改代码还是比较麻烦。

### 中文文档
我目前就读与安全性专业，有一些网络仿真的内容，虽然代码能力一般，但还算比较乐意写文档的。当然对于复杂应用，还是推荐读MESA的文档。
### 交互支持
MESA对鼠标操作图形元素的支持比较一般，但是tak基于PyQt，所以比较擅长交互，对于鼠标和键盘的交互支持更好。尽管这个特征仍在开发中。
### 绘制更快
一方面，tak基于PyOpenGL和PyQtGraph，元素数量较多时运行也比较快；另一方面即使元素较多，可视化界面发生严重卡顿，也不易崩溃。

相反，MESA中，由于浏览器可视化和Python程序之间是异步的，所以浏览器端可视化部分不能绘制过多的元素。若元素过多，卡顿现象会比tak更加严重，而且很可能发生图形界面崩溃。

## 性能
tak的技术框架按照网格分成两类。一类是自由网格，另一类是分立网格。前者允许Agent在网格中自由地前后左右平移、旋转，后者只允许Agent在网格中进行以整数网格为单位的运动，不允许旋转。   

自由网格需要对每个Agent的顶点都进行旋转矩阵叉乘的坐标变换，所以性能调校更偏重快速矩阵相乘一些，也就是普通Python解释器+numba+numpy的方向，对于pypy支持不够友好；   

分立网格不需要进行坐标变换，不需要矩阵相乘计算；自由网格则是需要坐标变换的。因此，分立网格的设计思想是尽量全部采用纯Python实现，减少C链接库的使用，这样有利于PyPy解释器进行提速。

当然，倘若用普通解释器跑起来的话，由于少了矩阵运算，所以分立网格的运行速度还是比前者自由网格快的。（详见 [生命游戏](https://gitee.com/hzy15610046011/TakagiABM/tree/master/demos/GameOfLife%E7%94%9F%E5%91%BD%E6%B8%B8%E6%88%8F)中的例子，运用了分立网格的GameOfLife_DiscreteGrid.py的帧率在我的电脑上可达18帧，而运用了自由网格的GameOfLife.py帧率一直在9~10帧附近徘徊。二者渲染时间相差无几，时间主要差在遍历网格上了。）    

但是值得注意的是，为了提升tak的渲染速度，整套图形化界面都挂在与C++有关的库上，所以目前pypy无法运行图形界面系统。当使用pypy时，需要指定模式为无图形界面启动。

作为对比，MESA使用的是纯Python的方案，以Web作为可视化，PyPy只承担后端运算功能。因此它使用pypy的时候，跑起可视化来也得心应手。所以对pypy解释器的可视化支持方面，也是tak的一个劣势。    

p.s.不过，如果你不清楚PyPy是什么的话，只要记住tak多数情况下会比MESA快就好了。   

p.p.s. 什么?连MESA是什么都不知道吗？这……请参阅这里：  
https://mesa.readthedocs.io/en/master/tutorials/intro_tutorial.html   
这个库在github上非常火爆，有七八十人在贡献这个项目，并且在不断更新。甚至一些刊物上的论文也是用它发的仿真结果。所以如果Python水平高的话，还是推荐用这个库。只是中文资料比较少，或者说……几乎没有?



## 示例及使用方式介绍

在地址 https://gitee.com/hzy15610046011/TakagiABM/tree/master/demos 中复制代码LantonAnt到你的IDE中，然后直接运行：
```bash
python LangtonAnt.py
```

界面启动以后，就可以看到一个兰顿蚂蚁模型。黑白色就是方格，如图所示：


![ant](src/兰顿蚂蚁.png)
界面左侧显示的是当前所有在界面上移动的代理人的各种信息，比如位置等。对于这个实验，只有一个代理人，就是这只小蚂蚁。由于没有添加滑动条、可视化图窗等小部件，所以界面看起来空空的。
#### 开始仿真
点击左上角“开始”，拖动滑块即可调整仿真速度。

点击“重启”，重置仿真，此时你所写的仿真文件将被重新加载。如果在重启之前修改代码，那么下一次仿真就可以按照此次的设置执行。也就是说，**代码文件支持动态修改**，对于小修小改，无需重新启动图形界面。但是推荐将仿真的相关内容都写在同一个文件里面。

点击“暂停“，可以暂停仿真。此时”暂停“的文字变为”继续“。点击”继续“的时候，仿真继续执行。  

点击”单步“，可以进行单步仿真。  

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
        a.setSpeed(np.array([1, 0]))  # 设置速度。只有第一只蚂蚁速度是水平数值的，因此会有不同的运动规律。
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


stat = 0
tak.GridAgent = tak.prepareAgent(tak.GridAgent, agentLoop)
tak.GridModel = tak.prepareModel(tak.GridModel, modelInitFunc=agentSetup, width=100, height=100,
                                 agentActivationPolicy='casual')
if __name__ == "__main__":
    tak.simStart(__file__, tak.GridModel)  # 这个方法同时启动了图形界面。

```
仿真的控制是由仿真模型对象GridModel来完成的。它每走一步，称为仿真前进一步。仿真每前进一步，所有的agent都会被激活一次，也就是调用一下step。

## API&接口教程
对于API,请参阅 [API](https://gitee.com/hzy15610046011/TakagiABM/blob/master/API.md) ，也就是与此readme.md同一目录下的API.md文件。
教程请参阅这里[教程](https://gitee.com/hzy15610046011/TakagiABM/blob/master/tutorial.md)


