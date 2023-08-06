'''
生命游戏。使用分立网格，速度比连续网格有很大的提升。在本人的计算机上，速度提升的幅度可达70%.
可以尝试用pypy运行这个例子。DiscreteGrid相比Grid，针对pypy特殊优化过，因此pypy的速度比使用cpython要快6~8倍。可惜的就是界面需要借助
cpython的pyqt 和pyqtgraph来实现，没有办法显示这种流畅的视觉效果，也算是一个遗憾吧。
'''
import random
import numpy as np
import takagiabm as tak# 这是第一种导入的方式。其他示例中还有另一种导入风格，可以按照喜好选用。
def modelSetup(model):
    global density
    for x in range(model.width):
        for y in range(model.height):

            a=(x,y)
            if(random.random()>1-density.value/100.0):# 将50%的单元格设置为生.其余可自行定义.
                model.grid.getCellByPos(a).setProperty('alive', True)
                model.grid.getCellByPos(a).setProperty('color', tak.red)# 导入颜色.
            else:
                model.grid.getCellByPos(a).setProperty('alive', False)
                model.grid.getCellByPos(a).setProperty('color', tak.black)# 设置为黑色.

def countAliveNeighbors(neighbors=[]):# 在外部定义函数也是可以的！
    count=0
    for n in neighbors:
        if(n.getTrait('alive')==True):
            count+=1
        else:
            continue
    return count

def cellStep(cell):
    global usegreen
    
    cell.model.startTiming('getNeighbors')

    neighbors=cell.getNeighbors()# 获取八个邻居
    cell.model.endTiming('getNeighbors')
    count=countAliveNeighbors(neighbors)
    if(count==3):
        
        cell.setTraitLater('alive',True)# 属性不会立即改变,会等到所有的cell都step完了之后再改变.
    elif(count==8):
        pass
    elif(count==2):
        pass
    else:  
        cell.setTraitLater('alive',False)


    if(cell.getTrait('alive')==True):
        cell.setColor(tak.red)
    else:
        cell.setColor(tak.black)

density=tak.Var('density',20,range=(0,1,100))#min,max,step，最小，最大和步长。
varList=[density]
tak.DiscreteGridModel.varList=varList
tak.DiscreteGridModel.agentActivationPolicy='none'# 没有Agent,就不用激活。
tak.DiscreteGridModel.cellActivationPolicy='casual'
#每轮每个agent都要被访问到。
tak.DiscreteGridModel.initAgents=modelSetup
tak.DiscreteGridCell.step=cellStep

if __name__=="__main__":
    tak.DiscreteGridModel.width=100
    tak.DiscreteGridModel.height=100
    tak.simStart(__file__, tak.DiscreteGridModel, varList, noGUI=True, maxSteps=100)





