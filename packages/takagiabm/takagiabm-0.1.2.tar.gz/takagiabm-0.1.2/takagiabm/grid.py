import numpy as np
import time
from takagiabm.agent import GridAgent,BaseAgent

from itertools import chain
from takagiabm.toolbox.typeutils import getColorArr
try:

    from numba import jit
except:
    print('检测到未安装numba.如果装有numba,可以让仿真速度更快。')
    from takagiabm.toolbox.numbaUtils import fakeJit
    jit=fakeJit


@jit
def xLoop(width,pos):
    if( pos[0]<0):
        pos[0]=width-1
    elif(pos[0]>=width):
        pos[0]=0
@jit
def yLoop(height,pos):
    if(pos[1]<0):
        pos[1]=height-1
    elif(pos[1]>=height):
        pos[1]=0
@jit
def xBlock(grid,pos):

    if( pos[0]<0):
        pos[0]=0
    elif(pos[0]>=grid.width):
        pos[0]=grid.width-1

@jit
def yBlock(grid,pos):
    if(pos[1]<0):
        pos[1]=0
    elif(pos[1]>=grid.height):
        pos[1]=grid.height-1
@jit
def xyWrap(height,width,pos):
    if( pos[0]<0):
        pos[0]=width-1
    else:
        pos[0]=0
    if(pos[1]<0):
        pos[1]=height-1
    else:
        pos[1]=0
@jit
def inBody(width,height,pos):
    return (0<pos[0]<width-1)&(0<pos[1]<height-1)
neighborDic={'':np.array([[1,0],[1,1],[0,1],[-1,1],\
                      [-1,0],[-1,-1],[0,-1],[1,-1]]),\
            '+':np.array([[1,0],[0,1],[-1,0],[0,-1]]),\
            'x':np.array([[1,1],[-1,1],[-1,-1],[1,-1]])
                      }


class Cell(BaseAgent):
    __slots__ = ('model','grid','properties')
    def __init__(self,pos,grid=None,model=None,color='#ffffff'):
        super().__init__(model=model,pos=pos)
        self.model=model
        self.grid=grid
        self.properties['color']=color# self.properties这个词典继承自Agent基类.

    def step(self):
        pass

    def getNeighbors(self,shape=''):
        return self.grid.getNeighbors(self.pos,shape)

    def getNeighborProperties(self,propertyName,shape=''):
        return self.grid.getNeighborProperties(self.pos,propertyName,shape)

    def __repr__(self):
        return 'cell at grid ,pos:'+str(self.pos)
    def setProperty(self,propertyName:str,property):
        if(type(propertyName)!=type('')):
            raise Exception(\
                '警告:agent或者cell的属性只能以字符串命名.你输入的是%s'%(repr(property)))
        self.properties[propertyName]=property
    def onClicked(self):
        pass

class Grid():
    neighborList=[None]*8
    def __init__(self,model=None,width=0,height=0):# 分别是表格的宽度和高度.
        self.model=model
        self.width=width   # 网格的宽度(列数)
        self.height=height # 网格的高度(行数)
        self.cellList=[[set() for i in range(width)] for j in range(height)]


        # 使用tuple来进行存储或许可以提升寻址速度？maybe.如果出现错误就改过来吧。
        self.cells=tuple([tuple([Cell(pos=np.array([i,j]),grid=self,model=self.model) for i in range(width)]) for j in range(height)])
        # self.cellMat=np.zeros((70,70))
        global neighborDic
        self.neighborDic=neighborDic
        s = np.zeros((70, 70), dtype=np.bool)

        self.mat={'alive':s}


    def setWrapAction(self, policyName:str):
        d={'torus':(xLoop,yLoop),'box':(xBlock,yBlock),'vcylinder':(xBlock,yLoop),'hcylender':(xLoop,yBlock)}
        if policyName.lower() in d.keys():
            self.xWrapAction, self.yWrapAction=d[policyName]
        else:
            raise Exception('未能识别的绕转类型：%s'%policyName+'允许的绕转类型为：%s'%(repr(d.keys())))



    def getCellByPos(self, pos:np.ndarray):

        pos=self.getCellPos(pos)# 只能保证它在范围内。小心，这一步是内部的方法，它不会修改矩阵
        if (pos.dtype!=np.int):
            pos=pos.astype(np.int)# 若不是整数，就转换为整数
        return self.cells[pos[1]][pos[0]]
    def getCellByPosInt(self,pos:np.ndarray):

        self.xWrapAction(self.width, pos)  # 这俩是这个Grid类的属性,不是其方法.因此不用传入self.
        self.yWrapAction(self.height, pos)
        c=self.cells[pos[1]][pos[0]]
        # self.model.endTiming('test')
        return c
    def getNeighbors(self,pos:np.ndarray,shape='')->list:

        nbd=self.neighborDic[shape]
        if(0<pos[0]<self.width-1)&(0<pos[1]<self.height-1):# 若位于中腹
            for i in range(len(nbd)):
                p = pos + nbd[i]
                self.neighborList[i]= self.cells[p[1]][p[0]]
            return self.neighborList
        else:
            for i in range(len(nbd)):# 若位于角或边
                p = pos + nbd[i]
                self.xWrapAction(self.width, p)  # 这俩是这个Grid类的属性,不是其方法.因此不用传入self.
                self.yWrapAction(self.height, p)
                self.neighborList[i] = self.cells[p[1]][p[0]]
            l=list(set(self.neighborList))
            return l# 去重

    def getNeighborProperties(self,pos,propertyName:str,shape='')->list:
        nbd=self.neighborDic[shape]
        l = [None] * len(nbd)
        if(propertyName in self.mat.keys()):
            if(0<pos[0]<self.width-1)&(0<pos[1]<self.height-1):# 若位于中腹
                a=self.mat['alive'][(pos[0]-1):(pos[0]+2),(pos[1]-1):(pos[1]+2)]# 直接从矩阵上获取值。
                l = a.tolist()
                #print('l::',l)
                l[1].pop(1)
                p = sum(l, [])
                # print(p)
                return p

            else:
                for i in range(len(nbd)):
                    arrayVar = pos + nbd[i]
                    arrayVar = self.getCellPos(arrayVar)
                    l[i] = self.cells[arrayVar[1]][arrayVar[0]].properties[propertyName]
                return l



    def getCellPos(self,pos:np.ndarray):# 这个函数的目的是检测pos是否在网格内部，如果不是，就依据边界策略
        #将网格的位置调整一下。允许的入口参数类型为numpy的浮点数。
        # 单元的位置是一个numpy.ndarray数组.因此直接在内存中修改即可.
        s1=np.floor(pos)#.astype(np.int)
        vari=pos-s1
        pos=s1
        self.xWrapAction(self.width, pos)# 这俩是这个Grid类的属性,不是其方法.因此不用传入self.
        self.yWrapAction(self.height, pos)
        vari+=pos#.astype(np.float)
        return vari#pos.astype(np.int)
    def getCellPosInt(self,pos:np.ndarray):# 在这个函数中功能同上，但是numpy内部的数据类型不同。单元的位置是一个numpy.ndarray数组.其值为整数，速度比上一个
        # 大概可以快好多倍。如果需要频繁寻址，且确定输入位置参数是整数类型，请选择此函数。因此直接在内存中修改即可.

        self.xWrapAction(self.width, pos)# 这俩是这个Grid类的属性,不是其方法.因此不用传入self.
        self.yWrapAction(self.height, pos)

        return pos

    def getAllCellsIter(self):#iterator:
        iterChain=chain.from_iterable(self.cells)#(*self.cells),返回一个迭代器.

        return iterChain
    def getAllCells(self)->list:
        return list(self.getAllCellsIter())
    def getCellColor(self,pos:np.ndarray)->str:
        pos=np.floor(pos).astype(np.int)

        return self.cells[pos[1]][pos[0]].getColor()

    def getCellColorArray(self,pos=None)->np.array:# pos或者wh的输入都是tuple

        s = self.cells[pos[1]][pos[0]].properties['color']
        if(s=='#000000'):
            return None
        digit = list(map(str, range(10))) + list("abcdef")
        value = s.lower()
        a1 = (digit.index(value[1]) * 16 + digit.index(value[2])) / 256.0
        a2 = (digit.index(value[3]) * 16 + digit.index(value[4])) / 256.0
        a3 = (digit.index(value[5]) * 16 + digit.index(value[6])) / 256.0
        return (a1,a2,a3)

    def setCellColor(self,pos:np.ndarray,color:str)->None:

        cell=self.cells[pos[1]][pos[0]]# 先行后列,逐个定位.
        cell.setColor(color)

    def placeAgent(self,agent)->None:
        pos=agent.getPosOnGrid()
        agent.grid=self
        self.cellList[pos[1]][pos[0]].add(agent)


    def moveAgent(self,agent,deltaPos=np.array([0,0])):
        # if(type(deltaPos)==type((1,2))):
        #    # print(type(pos))
        #     raise Exception('sdsds')

        lastPos=agent.pos
        pos=deltaPos+lastPos
       #
        #print(self.model.currentStep,pos)
        self.moveAgentTo(agent,pos)


    def moveAgentTo(self,agent,targetPos0=np.array([0,0])):
        # targetPos=np.floor(targetPos0).astype(np.int)
        targetPos=self.getCellPos(targetPos0)


        targetPosInt=np.floor(targetPos).astype(np.int)
        lastPos=np.floor(agent.pos).astype(np.int)
        agent.pos = targetPos
        # print('ap,tp',agent.pos,targetPos0,targetPos)
       # print(self.model.currentStep,agent,targetPosInt,targetPos,lastPos,self.cellList[lastPos[1]][lastPos[0]])
       #  for l in self.cellList:
       #      print(l)
        if agent in self.cellList[lastPos[1]][lastPos[0]]:
            self.cellList[lastPos[1]][lastPos[0]].remove(agent)# 索引是先行后列，但是位置是先列（x）后行(y)
        else:
            raise Exception('未找到此Agent,可能已经"死亡"或被从网格中移除。')
        self.cellList[targetPosInt[1]][targetPosInt[0]].add(agent)

    def isCellEmpty(self,pos):
        return self.getAgentNumInCell(pos)==0

    def getAgentNumInCell(self,pos):# 输入位置,返回单元格内对象的数目.
        return len(self.cellList[pos[0]][pos[1]])

    def getAgentsByPos(self,pos):
        # print(list(self.cellList[pos[1]][pos[0]]),pos)
        return list(self.cellList[pos[1]][pos[0]])

    def removeAgent(self,agent):
        pos=self.getCellPos(agent.pos)
        pos = np.floor(agent.pos).astype(np.int)
        self.cellList[pos[1]][pos[0]].remove(agent)


if __name__=='__main__':
    g=Grid(width=70,height=70)
    g.setWrapAction('torus')
    s=g.getCellPos(np.array([69.52483393,19.15510416]))
    print(s)
    # s=g.getCellByPos(np.array((1, 2)))
    # t0=time.time()
    # for j in range(10000):
    #     l=[]
    #     for i in range(8):
    #         l+=[g.cells[56][56]]
    #
    # t1=time.time()
    # for i in range(10000):
    #     s=g.mat['alive'][56:59,56:59]
    #     l=s.tolist()
    #     # print(s)
    #     l[1].pop(1)
    #     p=sum(l, [])
    #     # for j in range(8):
    #     #     l+=[g.mat['a'][56][56]]
    # print(p)
    # t2=time.time()

    # print(t1-t0,t2-t1)
    # print('posfffff',s.pos)
    # print(s.getNeighbors())
    #
    # print(g.getCellPos(np.array((1,2))))

