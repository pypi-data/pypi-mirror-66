
# TakagiABM  API与接口参考文档。
[TOC]


###  简介
TakagiABM库参考了NetLogo，主体一共有agent（代理人）、cell（网格单元）、model(控制者)三类，分别对应于NetLogo的turtle、patch和observer。

# Agent
## BaseAgent()
基类.所有的Agent和Cell都继承自这一类。
### 属性：
### self.pos:np.ndarray
为当前的x,y坐标。目前要求为两个整数。
### self.properties：dict
用于保存自身属性的变量,这是一个词典。但是不推荐直接使用索引的方式取得其中的元素，因为这样就会绕过代码中的类型检查，容易出现越界等情况。

BaseAgent有一个'color'键是默认初始化的，初始化时默认为白色，类型为字符串。形如"#ffffff"。     
例如“#ff0000”代表正红色，“#00ff00”代表正绿色，“#0000ff”代表正蓝色

### def setColor(self,color:str)->None:
将自身的颜色设置为此字符串类型。
###     def getColor(self)->str:
返回一个十六进制颜色字符串形如“#aaaaaa”
### setProperty(self,propertyName:str,property:object)->None:
设置自身的属性，立即生效。用法在self.getProperty中一并示出。
### setPropertyLater(self,propertyName,property:object)->None:
也是设置自身的属性，入口参数同self.setProperty。在仿真过程中调用这个函数时，在整个仿真程序的当前步中，当所有代理人各自刷新时，若调用此函数设置属性，此BaseAgent的属性将暂时不变，等到模型此步调用完所有的代理人以后，再更新属性。

这个方法的用处不妨举例说明：对于生命游戏等等场合的仿真，如果每个代理人在被调用时都立即更新自己是否存活，那么其周围尚未更新的代理人，相邻的生命数量都会被改变，造成仿真结果完全错误。如果在模型该步调用好所有代理人之后再更新属性，就能避免这个错误的发生。

不妨在生命游戏例程GameOfLife中尝试一下将这个函数(或者是setTraitLater)换成setProperty/setTrait，以体会其差别。

### getProperty(self,propertyName:str)->object:
获取自身的属性。
：(略去了BaseAgent初始化时的输入参数)：
```python
baseAgent=BaseAgent()
baseAgent.setProperty('alive',123)
print(baseAgent.getProperty('alive'))
# 运行结果：123
```
### setTrait(self,traitName:str,trait:object)->None:
与setProperty的用法相同。之所以封装一下，是因为trait差不多是有“属性”这个意思的单词中最简短易拼写的，能少打一半字母（尽管从英语角度来看不太严谨。）
### getTrait(self,traitName:str)->object:
同getProperty。

### setTraitLater(self,traitName:str,trait:object)
同setPropertyLater.


##  GridAgent(BaseAgent)

这是用于网格上的Agent类。目前只有这一类可以使用（当然了，NetLogo最多的用途也是在网格上）。
### 属性：

### self.speed:numpy.ndarray([x:int,y:int])
是此Agent的速度。分别是x方向和y方向的分量。由于需要旋转操作，需要计算矩阵乘法，所以使用numpy.ndarray来加快运算速度。
注：numpy.ndarray这个叫法可能比较陌生，但它就是大名鼎鼎的np.array()、np.zeros()之类的函数所返回的numpy矩阵类型。
### self.pos:np.ndarray([x：int,y:int])
是此Agent当前的位置。
### def  __init__(self,pos=np.ndarray([x,y]))
初始化一个Agent，设定其位于x,y。必须输入整数，否则报错。
###  def  getCellHatchColor（self）->str:
获取当前所在单元格的颜色。返回一个十六进制颜色字符串
###  def  setCellHatchColor（self,color:str）->None
设置当前所在单元格的颜色。

### move(self，deltaPos:np.ndarray([x,y]))->None:
移动相对位置横向x格，纵向y格。如果出界，则会从网格对侧再次进入。
### moveTo(self，pos:np.ndarray([x,y])->None:
移动到网格上的绝对位置：横向第x-1格，索引为x，纵向第y-1格，索引为y（因为索引是从0开始的！）。如果出界，则会从网格对侧再次进入。

### step(self)->None:
此Agent的动作函数。每一个周期内，所有的Agent都会被激活一次。
### getAgents(self)->[Agent(),Agent(),...]
获取此Agent当前单元格的其他Agent（），返回Agent的列表，<u>注意：此列表包括当前的Agent.</u>
### getAgentsByPos(self,pos:np.ndarray([x,y]))->[Agent(),Agent(),...]
返回pos位置的单元格中全部Agent的列表。<u>注意：此列表与getAgents的返回值类似，也包括当前的Agent</u>。
## Cell
### class Cell（BaseAgent):
### 属性：
与其继承的BaseAgent相比，暂时无新的属性。请参阅BaseAgent。
### def getNeighbors(self,shape=""):
获取此单元格邻近的所有cell。shape可以输入不同参数，列举如下：
1、shape='+' ,返回上下左右四个单元格。
2、shape='x' (是一个小写的第24个英文字母x，不是乘号)，返回对角的四个单元格，亦即左上、左下、右上、右下。
3、什么参数都不输入，或者输入其他字符串：获取邻接的八个单元格。在生命游戏中用到的就是这个。

##  Model

Model是观察者和控制者的角色，主要有以下功能：

1、管理Agent的加入、清除以及激活。

2、收集Agent的数据。当有图形界面的时候还负责向可视化的图表传递数据。

3、管理交互变量，比如羊吃草模型中可以通过滑块修改的草的生长率、羊的出生率。

所有的Model都具有这三种功能，所以其基类BaseModel也是按照这种方式组织的。

### BaseModel

#### 属性：
##### dataCounters=[]
储存计数器变量，见DataCounter对象。
##### self.agentSet = set()
存储agent的集合。不过不推荐对这个属性进行操作，如果造成agent异常删除，可能导致仿真程序崩溃。
##### self.currentStep = 0
记录模型当前的仿真进行到了多少步。
##### self.agentUpdateList = []  
这是用来在执行结束之后再刷新的列表.当调用agent.setTraitLater（trait,value）的时候，就会在这个列表后面append一个元素。每一步执行完毕之后，这个列表中的内容会被更新。
##### self.activator = Activator(self)
定义激活器，它管理着模型中的激活策略。
##### self.timeCounter = TakTimeCounter(self)
定义计时器。当怀疑某些代码性能存在问题时可以使用这个计时器。
#### def __init__(self):
初始化。
#### def countAgentData(self):
收集代理人数据的函数。在这个函数中将调用数据收集器进行数据收集。
#### def startTiming(self, timerName):
开始计时。
#### def endTiming(self, timerName):
结束计时。
#### def addAgent(self, agent):
添加代理人agent.
#### def removeAgent(self, agent):
移除Agent
#### def stepRoutine(func):# 装饰器。
这是一个装饰器，主要功能功能有计算当前仿真已经进行的步数等。
#### @stepRoutine
#### def step(self):
这个就是仿真进行的变量。调用之后，它使得仿真前进一步。

### GridModel(BaseModel)
为了管理Agent,不同的Model都有不同的容器。比如说这个GridModel，使用Grid作为容器，Grid可以容纳GridAgent和Cell两种Agent,相当于netlogo的turtle 和patch.
#### 属性
    stepRoutine = BaseModel.stepRoutine  # 先把step的时候的数据记录下来再说.
    width = 0
    height = 0
    lastStep = 0  # 用于测速的变量，记录上一次的速度。
    wrapPolicy = None
    agentActivationPolicy = 'random'# agent激活的函数。
    cellActivationPolicy = 'random'# cell激活方式
    agentActivationAction = None  # agent激活的函数.
    cellActivationAction = None  # cell激活的函数.
#### initAgents(self)
初始化代理人Agents。这个函数很常用。


#### 







