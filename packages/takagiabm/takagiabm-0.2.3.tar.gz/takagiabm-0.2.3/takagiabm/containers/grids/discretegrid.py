'''
这是容纳只能上下左右平移运动的代理人的网格，不允许代理人旋转运动。

'''

from takagiabm.agents.gridagents.freegrid.freegridcell import Cell
from itertools import chain
from takagiabm.agents.gridagents.discretegrid.discretegridcell import DiscreteGridCell
from takagiabm.containers.grids.basegrid import BaseGrid
def xLoop(width, pos):
    if (pos[0] < 0):
        pos[0] = width - 1
    elif (pos[0] >= width):
        pos[0] = 0


def yLoop(height, pos):
    if (pos[1] < 0):
        pos[1] = height - 1
    elif (pos[1] >= height):
        pos[1] = 0


def xBlock(width, pos):
    if (pos[0] < 0):
        pos[0] = 0
    elif (pos[0] >= width):
        pos[0] = width - 1


def yBlock(height, pos):
    if (pos[1] < 0):
        pos[1] = 0
    elif (pos[1] >= height):
        pos[1] = height - 1


def xyWrap(height, width, pos):
    if (pos[0] < 0):
        pos[0] = width - 1
    else:
        pos[0] = 0
    if (pos[1] < 0):
        pos[1] = height - 1
    else:
        pos[1] = 0


def inBody(width, height, pos):
    return (0 < pos[0] < width - 1) & (0 < pos[1] < height - 1)


neighborDic = {'': [[1, 0], [1, 1], [0, 1], [-1, 1], \
                    [-1, 0], [-1, -1], [0, -1], [1, -1]], \
               '+': [[1, 0], [0, 1], [-1, 0], [0, -1]], \
               'x': [[1, 1], [-1, 1], [-1, -1], [1, -1]]
               }


class DiscreteGrid(BaseGrid):
    neighborList = [None] * 8

    def __init__(self, model=None, width=0, height=0):  # 分别是表格的宽度和高度.
        super().__init__(model=model,width=width,height=height)

        # 使用tuple来进行存储或许可以提升寻址速度？maybe.如果出现错误就改过来吧。
        self.cells = tuple(
            [tuple([DiscreteGridCell(pos=[i, j], grid=self, model=self.model) for i in range(width)]) for j in
             range(height)])

        global neighborDic
        self.neighborDic = neighborDic

    def setWrapAction(self, policyName: str):
        d = {'torus': (xLoop, yLoop), 'box': (xBlock, yBlock), 'vcylinder': (xBlock, yLoop),
             'hcylender': (xLoop, yBlock)}
        if policyName.lower() in d.keys():
            self.xWrapAction, self.yWrapAction = d[policyName]
        else:
            raise Exception('未能识别的绕转类型：%s' % policyName + '允许的绕转类型为：%s' % (repr(d.keys())))

    def getCellByPos(self, pos):

        pos = self.getCellPos(pos)  # 只能保证它在范围内。小心，这一步是内部的方法，它不会修改矩阵
        # if (pos.dtype != np.int):
        #     pos = pos.astype(np.int)  # 若不是整数，就转换为整数
        return self.cells[pos[1]][pos[0]]

    def getCellByPosInt(self, pos:list):

        self.xWrapAction(self.width, pos)  # 这俩是这个Grid类的属性,不是其方法.因此不用传入self.
        self.yWrapAction(self.height, pos)
        c = self.cells[pos[1]][pos[0]]
        return c

    def getNeighbors(self, pos:list, shape='') -> list:

        nbd = self.neighborDic[shape]
        if (inBody(self.width, self.height, pos)):  # 若位于中腹

            for i in range(len(nbd)):
                a = pos[0] + nbd[i][0]
                b = pos[1] + nbd[i][1]
                self.neighborList[i] = self.cells[b][a]
            return self.neighborList
        else:
            p = [0, 0]
            for i in range(len(nbd)):  # 若位于角或边
                p[0] = pos[0] + nbd[i][0]
                p[1] = pos[1] + nbd[i][1]
                self.xWrapAction(self.width, p)  # 这俩是这个Grid类的属性,不是其方法.因此不用传入self.
                self.yWrapAction(self.height, p)
                self.neighborList[i] = self.cells[p[1]][p[0]]
            l = list(set(self.neighborList))
           # print('getneoghbor!!!!!')
            return l  # 去重

    def getNeighborProperties(self, pos, propertyName: str, shape='') -> list:
        nbd = self.neighborDic[shape]
        l = [None] * len(nbd)
        if (propertyName in self.mat.keys()):
            if inBody(self.width, self.height, pos):  # 若位于中腹
                a = self.mat['alive'][(pos[0] - 1):(pos[0] + 2), (pos[1] - 1):(pos[1] + 2)]  # 直接从矩阵上获取值。
                l = a.tolist()
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

    def getCellPos(self, pos: list):  # 这个函数的目的是检测pos是否在网格内部，如果不是，就依据边界策略
        # 将网格的位置调整一下。允许的入口参数类型为numpy的浮点数。
        # 单元的位置是一个numpy.ndarray数组.因此直接在内存中修改即可.
        # s1 = np.floor(pos)  # .astype(np.int)
        # vari = pos - s1

        self.xWrapAction(self.width, pos)  # 这俩是这个Grid类的属性,不是其方法.因此不用传入self.
        self.yWrapAction(self.height, pos)
        return pos  # pos.astype(np.int)

    def getCellPosInt(self, pos: list):  # 在这个函数中功能同上，但是numpy内部的数据类型不同。单元的位置是一个numpy.ndarray数组.其值为整数，速度比上一个
        # 大概可以快好多倍。如果需要频繁寻址，且确定输入位置参数是整数类型，请选择此函数。因此直接在内存中修改即可.

        self.xWrapAction(self.width, pos)  # 这俩是这个Grid类的属性,不是其方法.因此不用传入self.
        self.yWrapAction(self.height, pos)

        return pos

    def getAllCellsIter(self):  # iterator:
        iterChain = chain.from_iterable(self.cells)  # (*self.cells),返回一个迭代器.

        return iterChain

    def getAllCells(self) -> list:
        return list(self.getAllCellsIter())

    def getCellColor(self, pos) -> str:

        return self.cells[pos[1]][pos[0]].getColor()


    def setCellColor(self, pos, color: str) -> None:

        cell = self.cells[pos[1]][pos[0]]  # 先行后列,逐个定位.
        cell.setColor(color)

    def placeAgent(self, agent) -> None:
        pos = agent.getPosOnGrid()
        agent.grid = self
        self.cellList[pos[1]][pos[0]].add(agent)

    def moveAgent(self, agent, deltaPos):
        super().moveAgent(agent,deltaPos)

    def moveAgentTo(self, agent, targetPos):
        super().moveAgentTo(agent,targetPos)


    # def isCellEmpty(self, pos):
    #     return self.getAgentNumInCell(pos) == 0
    #
    # def getAgentNumInCell(self, pos):  # 输入位置,返回单元格内对象的数目.
    #     return len(self.cellList[pos[0]][pos[1]])
    #
    # def getAgentsByPos(self, pos):
    #     return list(self.cellList[pos[1]][pos[0]])

    def removeAgent(self, agent):
        super().removeAgent(agent)


if __name__ == '__main__':
    g = FreeGrid(width=70, height=70)
    g.setWrapAction('torus')
    s = g.getCellPos(np.array([69.52483393, 19.15510416]))
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
